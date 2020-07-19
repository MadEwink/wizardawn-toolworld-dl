import requests

from enum import Enum

## Constants

NAME = "Truc"
WATER = {
    'n': 0,
    'e': 0,
    's': 0,
    'w': 0
}
INFO = True
LEGEND = True


class MapGenre(Enum):
    FANTASY = 'Fantasy'


form_data = {
    'program_user': 1,
    'map_name': NAME,
    'map_genre': MapGenre.FANTASY,
    'map_climate': 1,
    'map_wide': 1,
    'map_high': 1,
    'map_equals': 5,
    'info': 1 if INFO else 0,
    'legend': 1 if LEGEND else 0,
    'water_n': WATER['n'],
    'water_s': WATER['s'],
    'water_e': WATER['e'],
    'water_w': WATER['w'],
    'Create': 'Create'
}

r = requests.post("http://bugs.python.org", data=form_data)

if r.status_code != requests.codes.ok:
    r.raise_for_status()

html = r.text
