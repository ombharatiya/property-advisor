from apiservices.core.RealState import MOCK_DATA
from apiservices.core.RealState.utils import distance

input1 = {
    "minBedrooms": 1,
    "maxBedrooms": 2,
    "minBathrooms": 2,
    "maxBathrooms": 4,
    "lat": 18.3721392,
    "lon": 121.5111211,
    "minBudget": "8305.39",
    "maxBudget": "8305.39"
}


output1 = [
    {'id': 1, 'match': 100.0},
    {'id': 7, 'match': 70.0},
    {'id': 2, 'match': 64.0},
    {'id': 3, 'match': 58.0},
    {'id': 10, 'match': 40.6}
]

PERCENTAGE_VALID_LOW = 40
PERCENTAGE_VALID_HIGH = 100

DISTANCE_WEIGHT = 0.3
BUDGET_WEIGHT = 0.3
BATHROOM_WEIGHT = 0.2
BEDROOM_WEIGHT = 0.2

DISTANCE_THRESHOLD_LOW = 2
DISTANCE_THRESHOLD_HIGH = 10

# considering the avg of budget max-min to find the percentage
BUDGET_THRESHOLD_LOW = 10
BUDGET_THRESHOLD_HIGH = 25

ROOMS_THRESHOLD_LOW = 0
ROOMS_THRESHOLD_HIGH = 2


def getDistanceMatch(req_data, present_data):
    lat1 = req_data['lat']
    lon1 = req_data['lon']
    lat2 = present_data['lat']
    lon2 = present_data['lon']
    old_value = distance(lat1, lon1, lat2, lon2)
    old_max = DISTANCE_THRESHOLD_HIGH
    old_min = DISTANCE_THRESHOLD_LOW
    if 0 <= old_value <= old_min:
        return 100
    if old_min < old_value < old_max:
        new_max = PERCENTAGE_VALID_HIGH
        new_min = PERCENTAGE_VALID_LOW
        old_range = (old_max - old_min)
        new_range = (new_max - new_min)
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
        return 140 - new_value
    return 0


def getBudgetMatch(req_data, present_data):
    budget_max = req_data['maxBudget']
    budget_min = req_data['minBudget']
    if (budget_max is None or budget_max is '') and (budget_min is None or budget_min is ''):
        return 0
    if budget_max is None or budget_max is '':
        budget_max = budget_min
    if budget_min is None or budget_min is '':
        budget_min = budget_max
    budget_max = float(budget_max)
    budget_min = float(budget_min)
    avg_budget = (budget_max + budget_min) / 2.0
    old_value = float(present_data['price'])
    old_low_min = budget_min - (avg_budget * BUDGET_THRESHOLD_LOW) / 100
    old_low_min = old_low_min if old_low_min > 0 else 0
    old_low_max = budget_max + (avg_budget * BUDGET_THRESHOLD_LOW) / 100
    old_low_max = old_low_max if old_low_max > 0 else 0
    if old_low_min <= old_value <= old_low_max:
        return 100

    if old_value >= old_low_max:
        old_min = old_low_max
        old_max = budget_max + (avg_budget * BUDGET_THRESHOLD_HIGH) / 100
        old_max = old_max if old_max > 0 else 0
        if old_value <= old_max:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return 140 - new_value
    else:
        old_max = old_low_min
        old_min = budget_min - (avg_budget * BUDGET_THRESHOLD_HIGH) / 100
        old_min = old_min if old_min > 0 else 0
        if old_value >= old_min:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return new_value
    return 0


def getBedroomMatch(req_data, present_data):
    bedroom_max = req_data['maxBedrooms']
    bedroom_min = req_data['minBedrooms']
    if (bedroom_max is None or bedroom_max is '') and (bedroom_min is None or bedroom_min is ''):
        return 0
    if bedroom_max is None or bedroom_max is '':
        bedroom_max = bedroom_min
    if bedroom_min is None or bedroom_min is '':
        bedroom_min = bedroom_max
    bedroom_max = int(bedroom_max)
    bedroom_min = int(bedroom_min)
    old_value = int(present_data['bedrooms'])
    old_low_min = bedroom_min - ROOMS_THRESHOLD_LOW
    old_low_min = old_low_min if old_low_min > 0 else 0
    old_low_max = bedroom_max + ROOMS_THRESHOLD_LOW
    old_low_max = old_low_max if old_low_max > 0 else 0
    if old_low_min <= old_value <= old_low_max:
        return 100

    if old_value >= old_low_max:
        old_min = old_low_max
        old_max = bedroom_max + ROOMS_THRESHOLD_HIGH
        old_max = old_max if old_max > 0 else 0
        if old_value <= old_max:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return 140 - new_value
    else:
        old_max = old_low_min
        old_min = bedroom_min - ROOMS_THRESHOLD_HIGH
        old_min = old_min if old_min > 0 else 0
        if old_value >= old_min:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return new_value
    return 0


def getBathroomMatch(req_data, present_data):
    bedroom_max = req_data['maxBathrooms']
    bedroom_min = req_data['minBathrooms']
    if (bedroom_max is None or bedroom_max is '') and (bedroom_min is None or bedroom_min is ''):
        return 0
    if bedroom_max is None or bedroom_max is '':
        bedroom_max = bedroom_min
    if bedroom_min is None or bedroom_min is '':
        bedroom_min = bedroom_max
    bedroom_max = int(bedroom_max)
    bedroom_min = int(bedroom_min)
    old_value = int(present_data['bathrooms'])
    old_low_min = bedroom_min - ROOMS_THRESHOLD_LOW
    old_low_min = old_low_min if old_low_min > 0 else 0
    old_low_max = bedroom_max + ROOMS_THRESHOLD_LOW
    old_low_max = old_low_max if old_low_max > 0 else 0
    if old_low_min <= old_value <= old_low_max:
        return 100

    if old_value >= old_low_max:
        old_min = old_low_max
        old_max = bedroom_max + ROOMS_THRESHOLD_HIGH
        old_max = old_max if old_max > 0 else 0
        if old_value <= old_max:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return 140 - new_value
    else:
        old_max = old_low_min
        old_min = bedroom_min - ROOMS_THRESHOLD_HIGH
        old_min = old_min if old_min > 0 else 0
        if old_value >= old_min:
            new_max = PERCENTAGE_VALID_HIGH
            new_min = PERCENTAGE_VALID_LOW
            old_range = (old_max - old_min)
            new_range = (new_max - new_min)
            new_value = (((old_value - old_min) * new_range) /
                         old_range) + new_min
            return new_value
    return 0


def getMatch(req_data, app_data):
    distance_match = getDistanceMatch(req_data, app_data)
    print(f"distance_match: {distance_match}")
    budget_match = getBudgetMatch(req_data, app_data)
    print(f"budget_match: {budget_match}")
    bedroom_match = getBedroomMatch(req_data, app_data)
    print(f"bedroom_match: {bedroom_match}")
    bathroom_match = getBathroomMatch(req_data, app_data)
    print(f"bathroom_match: {bathroom_match}")
    return round(
        distance_match * DISTANCE_WEIGHT
        + budget_match * BUDGET_WEIGHT
        + bedroom_match * BEDROOM_WEIGHT
        + bathroom_match * BATHROOM_WEIGHT,
        2)


app_db = MOCK_DATA.DATA


def getTopMatches(req_data):
    ans = []
    count = 10
    for data in app_db:
        if count < 0:
            break
        count = count - 1
        # obj = {'id': data['id']}
        match = getMatch(req_data, data)
        if match >= 40:
            obj = data.copy()
            obj.update({'match': match})
            ans.append(obj)
    ans.sort(key=lambda k: k['match'], reverse=True)
    return ans


# print(getTopMatches(input1))
