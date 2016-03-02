import external
import requests


"""
Use the Wikipedia API to retrieve a description for the given City
"""
def get_city_description(city_name, country_name):
    articles = external._lookup_wikipedia(city_name, country_name)

    if city_name in _known_result_indices:
        index = _known_result_indices['city_name']
    else:
        index = 0  # use first result

    return {
        'title': articles[1][index],
        'text': articles[2][index],
        'url': articles[3][index]
    }


# cities that are found in a particular search result index
_known_result_indices = {
    'New York': 1
}

