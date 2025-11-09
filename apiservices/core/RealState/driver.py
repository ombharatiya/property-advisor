"""
Property matching algorithm using weighted scoring system.

This module implements the core business logic for matching properties
with search requirements based on distance, budget, bedrooms, and bathrooms.
"""
from typing import List, Dict, Optional
from dataclasses import dataclass
from apiservices.core.RealState import MOCK_DATA
from apiservices.core.RealState.utils import distance


@dataclass
class MatchWeights:
    """Configuration for match scoring weights."""
    distance: float = 0.3
    budget: float = 0.3
    bedrooms: float = 0.2
    bathrooms: float = 0.2


@dataclass
class MatchThresholds:
    """Configuration for match thresholds."""
    min_match_percentage: float = 40.0
    max_match_percentage: float = 100.0
    
    # Distance thresholds in miles
    distance_perfect: float = 2.0
    distance_max: float = 10.0
    
    # Budget thresholds in percentage
    budget_perfect: float = 10.0
    budget_max: float = 25.0
    
    # Room count thresholds
    rooms_perfect: int = 0
    rooms_max: int = 2

# Default configuration instances
WEIGHTS = MatchWeights()
THRESHOLDS = MatchThresholds()


class PropertyMatcher:
    """Property matching service with improved algorithms and caching."""
    
    def __init__(self, weights: MatchWeights = None, thresholds: MatchThresholds = None):
        self.weights = weights or WEIGHTS
        self.thresholds = thresholds or THRESHOLDS


    def calculate_distance_match(self, requirement: Dict, property_data: Dict) -> float:
        """Calculate distance match score between requirement and property."""
        lat1 = requirement['lat']
        lon1 = requirement['lon']
        lat2 = property_data['lat']
        lon2 = property_data['lon']
        
        distance_miles = distance(lat1, lon1, lat2, lon2)
        
        if distance_miles <= self.thresholds.distance_perfect:
            return 100.0
        elif distance_miles <= self.thresholds.distance_max:
            # Linear interpolation between perfect and max distance
            score_range = self.thresholds.max_match_percentage - self.thresholds.min_match_percentage
            distance_range = self.thresholds.distance_max - self.thresholds.distance_perfect
            score = self.thresholds.max_match_percentage - (
                (distance_miles - self.thresholds.distance_perfect) / distance_range * score_range
            )
            return max(score, self.thresholds.min_match_percentage)
        
        return 0.0


    def calculate_budget_match(self, requirement: Dict, property_data: Dict) -> float:
        """Calculate budget match score between requirement and property."""
        budget_max = requirement.get('maxBudget')
        budget_min = requirement.get('minBudget')
        
        if not budget_max and not budget_min:
            return 0.0
            
        # Handle cases where only one bound is provided
        if not budget_max:
            budget_max = budget_min
        if not budget_min:
            budget_min = budget_max
            
        try:
            budget_max = float(budget_max) if budget_max else 0
            budget_min = float(budget_min) if budget_min else 0
            property_price = float(property_data['price'])
        except (ValueError, TypeError):
            return 0.0
            
        avg_budget = (budget_max + budget_min) / 2.0
        
        # Perfect match range (within 10% of average)
        perfect_range_min = budget_min - (avg_budget * self.thresholds.budget_perfect) / 100
        perfect_range_max = budget_max + (avg_budget * self.thresholds.budget_perfect) / 100
        perfect_range_min = max(perfect_range_min, 0)
        
        if perfect_range_min <= property_price <= perfect_range_max:
            return 100.0
            
        # Acceptable range (within 25% of average)
        acceptable_range_min = budget_min - (avg_budget * self.thresholds.budget_max) / 100
        acceptable_range_max = budget_max + (avg_budget * self.thresholds.budget_max) / 100
        acceptable_range_min = max(acceptable_range_min, 0)
        
        if property_price > perfect_range_max and property_price <= acceptable_range_max:
            # Linear interpolation for higher prices
            price_diff = property_price - perfect_range_max
            max_diff = acceptable_range_max - perfect_range_max
            score = 100 - (price_diff / max_diff) * (100 - self.thresholds.min_match_percentage)
            return max(score, self.thresholds.min_match_percentage)
            
        elif property_price < perfect_range_min and property_price >= acceptable_range_min:
            # Linear interpolation for lower prices
            price_diff = perfect_range_min - property_price
            max_diff = perfect_range_min - acceptable_range_min
            score = 100 - (price_diff / max_diff) * (100 - self.thresholds.min_match_percentage)
            return max(score, self.thresholds.min_match_percentage)
            
        return 0.0


    def calculate_bedroom_match(self, requirement: Dict, property_data: Dict) -> float:
        """Calculate bedroom match score between requirement and property."""
        return self._calculate_room_match(
            requirement, property_data, 'Bedrooms', 'bedrooms'
        )


    def calculate_bathroom_match(self, requirement: Dict, property_data: Dict) -> float:
        """Calculate bathroom match score between requirement and property."""
        return self._calculate_room_match(
            requirement, property_data, 'Bathrooms', 'bathrooms'
        )
    
    def _calculate_room_match(self, requirement: Dict, property_data: Dict, 
                             room_type_cap: str, room_type_lower: str) -> float:
        """Generic room count matching logic for bedrooms and bathrooms."""
        max_key = f'max{room_type_cap}'
        min_key = f'min{room_type_cap}'
        
        room_max = requirement.get(max_key)
        room_min = requirement.get(min_key)
        
        if not room_max and not room_min:
            return 0.0
            
        # Handle cases where only one bound is provided
        if not room_max:
            room_max = room_min
        if not room_min:
            room_min = room_max
            
        try:
            room_max = int(room_max)
            room_min = int(room_min)
            property_rooms = int(property_data[room_type_lower])
        except (ValueError, TypeError):
            return 0.0
            
        # Perfect match range
        perfect_min = max(room_min - self.thresholds.rooms_perfect, 0)
        perfect_max = room_max + self.thresholds.rooms_perfect
        
        if perfect_min <= property_rooms <= perfect_max:
            return 100.0
            
        # Acceptable range
        acceptable_min = max(room_min - self.thresholds.rooms_max, 0)
        acceptable_max = room_max + self.thresholds.rooms_max
        
        if property_rooms > perfect_max and property_rooms <= acceptable_max:
            # Linear interpolation for higher room counts
            room_diff = property_rooms - perfect_max
            max_diff = acceptable_max - perfect_max
            if max_diff == 0:
                return 100.0
            score = 100 - (room_diff / max_diff) * (100 - self.thresholds.min_match_percentage)
            return max(score, self.thresholds.min_match_percentage)
            
        elif property_rooms < perfect_min and property_rooms >= acceptable_min:
            # Linear interpolation for lower room counts
            room_diff = perfect_min - property_rooms
            max_diff = perfect_min - acceptable_min
            if max_diff == 0:
                return 100.0
            score = 100 - (room_diff / max_diff) * (100 - self.thresholds.min_match_percentage)
            return max(score, self.thresholds.min_match_percentage)
            
        return 0.0


    def calculate_overall_match(self, requirement: Dict, property_data: Dict) -> Dict:
        """Calculate overall match score and individual component scores."""
        distance_score = self.calculate_distance_match(requirement, property_data)
        budget_score = self.calculate_budget_match(requirement, property_data)
        bedroom_score = self.calculate_bedroom_match(requirement, property_data)
        bathroom_score = self.calculate_bathroom_match(requirement, property_data)
        
        overall_score = (
            distance_score * self.weights.distance +
            budget_score * self.weights.budget +
            bedroom_score * self.weights.bedrooms +
            bathroom_score * self.weights.bathrooms
        )
        
        return {
            'overall_score': round(overall_score, 2),
            'distance_score': round(distance_score, 2),
            'budget_score': round(budget_score, 2),
            'bedroom_score': round(bedroom_score, 2),
            'bathroom_score': round(bathroom_score, 2),
        }
    
    def find_matches(self, requirement: Dict, property_list: List[Dict] = None, 
                    limit: int = 10) -> List[Dict]:
        """Find matching properties for a given requirement."""
        if property_list is None:
            property_list = MOCK_DATA.DATA
            
        matches = []
        processed_count = 0
        
        for property_data in property_list:
            if limit and processed_count >= limit:
                break
                
            match_result = self.calculate_overall_match(requirement, property_data)
            
            if match_result['overall_score'] >= self.thresholds.min_match_percentage:
                property_match = property_data.copy()
                property_match.update({
                    'match': match_result['overall_score'],
                    'distance_score': match_result['distance_score'],
                    'budget_score': match_result['budget_score'],
                    'bedroom_score': match_result['bedroom_score'],
                    'bathroom_score': match_result['bathroom_score'],
                })
                matches.append(property_match)
            
            processed_count += 1
            
        # Sort by match score (descending)
        matches.sort(key=lambda x: x['match'], reverse=True)
        return matches


# Legacy function compatibility
_default_matcher = PropertyMatcher()

def getTopMatches(req_data):
    """Legacy function for backward compatibility."""
    return _default_matcher.find_matches(req_data)
