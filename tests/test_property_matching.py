"""
Tests for the property matching algorithm.
"""
import pytest
from decimal import Decimal
from apiservices.core.RealState.driver import PropertyMatcher, MatchWeights, MatchThresholds


class TestPropertyMatcher:
    """Test cases for PropertyMatcher class."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.matcher = PropertyMatcher()
        self.sample_requirement = {
            'lat': 18.3721392,
            'lon': 121.5111211,
            'minBudget': '8000',
            'maxBudget': '10000',
            'minBedrooms': '2',
            'maxBedrooms': '3',
            'minBathrooms': '1',
            'maxBathrooms': '2'
        }
        self.sample_property = {
            'id': 1,
            'lat': 18.3721392,
            'lon': 121.5111211,
            'price': '9000',
            'bedrooms': '2',
            'bathrooms': '2'
        }
    
    def test_perfect_distance_match(self):
        """Test perfect distance match (same location)."""
        score = self.matcher.calculate_distance_match(
            self.sample_requirement, self.sample_property
        )
        assert score == 100.0
    
    def test_distance_match_within_threshold(self):
        """Test distance match within acceptable threshold."""
        far_property = self.sample_property.copy()
        far_property['lat'] = 18.4  # Slightly different location
        
        score = self.matcher.calculate_distance_match(
            self.sample_requirement, far_property
        )
        assert 40 <= score <= 100
    
    def test_distance_match_too_far(self):
        """Test distance match beyond acceptable threshold."""
        far_property = self.sample_property.copy()
        far_property['lat'] = 19.0  # Very different location
        
        score = self.matcher.calculate_distance_match(
            self.sample_requirement, far_property
        )
        assert score == 0.0
    
    def test_perfect_budget_match(self):
        """Test perfect budget match."""
        score = self.matcher.calculate_budget_match(
            self.sample_requirement, self.sample_property
        )
        assert score == 100.0
    
    def test_budget_match_within_range(self):
        """Test budget match within acceptable range."""
        expensive_property = self.sample_property.copy()
        expensive_property['price'] = '11000'  # Slightly over budget
        
        score = self.matcher.calculate_budget_match(
            self.sample_requirement, expensive_property
        )
        assert score >= 40  # Should still be acceptable
    
    def test_budget_match_too_expensive(self):
        """Test budget match for property way over budget."""
        expensive_property = self.sample_property.copy()
        expensive_property['price'] = '20000'  # Way over budget
        
        score = self.matcher.calculate_budget_match(
            self.sample_requirement, expensive_property
        )
        assert score == 0.0
    
    def test_missing_budget_requirement(self):
        """Test budget match when no budget specified."""
        no_budget_req = self.sample_requirement.copy()
        del no_budget_req['minBudget']
        del no_budget_req['maxBudget']
        
        score = self.matcher.calculate_budget_match(
            no_budget_req, self.sample_property
        )
        assert score == 0.0
    
    def test_perfect_bedroom_match(self):
        """Test perfect bedroom match."""
        score = self.matcher.calculate_bedroom_match(
            self.sample_requirement, self.sample_property
        )
        assert score == 100.0
    
    def test_bedroom_match_within_range(self):
        """Test bedroom match within acceptable range."""
        four_br_property = self.sample_property.copy()
        four_br_property['bedrooms'] = '4'  # One more than max
        
        score = self.matcher.calculate_bedroom_match(
            self.sample_requirement, four_br_property
        )
        assert score >= 40
    
    def test_bedroom_match_too_many(self):
        """Test bedroom match for property with too many bedrooms."""
        many_br_property = self.sample_property.copy()
        many_br_property['bedrooms'] = '10'  # Way more than max
        
        score = self.matcher.calculate_bedroom_match(
            self.sample_requirement, many_br_property
        )
        assert score == 0.0
    
    def test_perfect_bathroom_match(self):
        """Test perfect bathroom match."""
        score = self.matcher.calculate_bathroom_match(
            self.sample_requirement, self.sample_property
        )
        assert score == 100.0
    
    def test_overall_match_calculation(self):
        """Test overall match score calculation."""
        result = self.matcher.calculate_overall_match(
            self.sample_requirement, self.sample_property
        )
        
        assert 'overall_score' in result
        assert 'distance_score' in result
        assert 'budget_score' in result
        assert 'bedroom_score' in result
        assert 'bathroom_score' in result
        
        # Perfect match should be 100
        assert result['overall_score'] == 100.0
        assert result['distance_score'] == 100.0
        assert result['budget_score'] == 100.0
        assert result['bedroom_score'] == 100.0
        assert result['bathroom_score'] == 100.0
    
    def test_find_matches(self):
        """Test finding matches from property list."""
        test_properties = [
            self.sample_property,
            {
                'id': 2,
                'lat': 18.4,
                'lon': 121.5,
                'price': '9500',
                'bedrooms': '3',
                'bathrooms': '1'
            }
        ]
        
        matches = self.matcher.find_matches(
            self.sample_requirement, test_properties
        )
        
        assert len(matches) >= 1
        assert all('match' in match for match in matches)
        assert matches[0]['match'] >= matches[-1]['match']  # Sorted by score
    
    def test_custom_weights(self):
        """Test matcher with custom weights."""
        custom_weights = MatchWeights(distance=0.5, budget=0.3, bedrooms=0.1, bathrooms=0.1)
        custom_matcher = PropertyMatcher(weights=custom_weights)
        
        result = custom_matcher.calculate_overall_match(
            self.sample_requirement, self.sample_property
        )
        
        assert result['overall_score'] == 100.0  # Perfect match regardless of weights
    
    def test_custom_thresholds(self):
        """Test matcher with custom thresholds."""
        custom_thresholds = MatchThresholds(min_match_percentage=50.0)
        custom_matcher = PropertyMatcher(thresholds=custom_thresholds)
        
        # This should filter out more properties
        matches = custom_matcher.find_matches(self.sample_requirement)
        
        # All matches should be above the custom threshold
        assert all(match['match'] >= 50.0 for match in matches)


class TestPropertyMatcherEdgeCases:
    """Test edge cases and error conditions."""
    
    def setup_method(self):
        """Set up test fixtures."""
        self.matcher = PropertyMatcher()
    
    def test_invalid_coordinates(self):
        """Test handling of invalid coordinate data."""
        invalid_req = {
            'lat': 'invalid',
            'lon': 'invalid',
            'minBudget': '1000',
            'maxBudget': '2000'
        }
        property_data = {
            'lat': 18.3721392,
            'lon': 121.5111211,
            'price': '1500'
        }
        
        # Should handle gracefully and return 0
        score = self.matcher.calculate_distance_match(invalid_req, property_data)
        assert score >= 0
    
    def test_invalid_price_data(self):
        """Test handling of invalid price data."""
        req = {
            'minBudget': 'invalid',
            'maxBudget': 'invalid'
        }
        property_data = {
            'price': 'invalid'
        }
        
        score = self.matcher.calculate_budget_match(req, property_data)
        assert score == 0.0
    
    def test_missing_data(self):
        """Test handling of missing data."""
        empty_req = {}
        empty_property = {}
        
        result = self.matcher.calculate_overall_match(empty_req, empty_property)
        
        # Should handle gracefully
        assert isinstance(result, dict)
        assert 'overall_score' in result