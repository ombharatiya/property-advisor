from apiservices.core.RealState.driver import getTopMatches


# input1 = {
#     "minBedrooms": 1,
#     "maxBedrooms": 2,
#     "minBathrooms": 2,
#     "maxBathrooms": 4,
#     "lat": 18.3721392,
#     "lon": 121.5111211,
#     "minBudget": "8305.39",
#     "maxBudget": "8305.39"
# }


def processInputDataAndGiveMatches(input):

    try:
        lon = float(input['lon'])
        lat = float(input['lat'])
        min_budget = str(input['min_budget'])
        max_budget = str(input['max_budget'])
        min_bedrooms = int(input['min_bedrooms'])
        max_bedrooms = int(input['max_bedrooms'])
        min_bathrooms = int(input['min_bathrooms'])
        max_bathrooms = int(input['max_bathrooms'])

        if min_bathrooms > max_bathrooms:
            max_bathrooms, min_bathrooms = min_bathrooms, max_bathrooms

        if min_bedrooms > max_bedrooms:
            max_bedrooms, min_bedrooms = min_bedrooms, max_bedrooms

        if float(min_budget) > float(max_budget):
            max_budget, min_budget = min_budget, max_budget

        req_obj = {
            "minBedrooms": min_bedrooms,
            "maxBedrooms": max_bedrooms,
            "minBathrooms": min_bathrooms,
            "maxBathrooms": max_bathrooms,
            "lat": lat,
            "lon": lon,
            "minBudget": min_budget,
            "maxBudget": max_budget
        }
        # print("req_obj")
        # print(req_obj)
        list_of_properties = getTopMatches(req_obj)
        # print("list_of_properties")
        # print(list_of_properties)
        return list_of_properties, req_obj
    except Exception as e:
        print(f"Something went wrong.. :{str(e)}")
        return []
