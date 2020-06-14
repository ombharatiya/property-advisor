from math import cos, asin, sqrt


def distance(lat1, lon1, lat2, lon2):
    p = 0.017453292519943295
    a = 0.5 - cos((lat2 - lat1) * p) / 2 + cos(lat1 * p) * \
        cos(lat2 * p) * (1 - cos((lon2 - lon1) * p)) / 2
    # return 12742 * asin(sqrt(a)) # in kms
    return 7917.512 * asin(sqrt(a))  # in miles

# "lat": 18.3721392, "lon": 121.5111279
# lat2 = 45.2625083, "lon": ,


# print(distance(18.3721392, 121.5111279, 18.3721392, 121.427272))
