
# This algorithm return a list of dictionaries which will be transformed as a JSON object in the views.py.
# Which then will be handled by a script.
def get_gps_coordinates_and_more(coordinates):
    coordinates_info = list()
    for location in coordinates:
        one_location = dict()
        one_location.__setitem__("name_of_location", location[0])
        one_location.__setitem__("adresse", location[1])
        one_location.__setitem__("code_postal", location[2])
        one_location.__setitem__("localite", location[3])
        one_location.__setitem__("informations_supplementaires", location[4])

        str_location = "".join(location[5])
        index_start = str_location.index("!3d")  # = latitude
        index_end = str_location.index("!4d")   # = longitude
        one_location.__setitem__("lat", str_location[index_start + 3: index_end])
        one_location.__setitem__("long", str_location[index_end + 3: len(str_location)])

        coordinates_info.append(one_location)

    return coordinates_info
