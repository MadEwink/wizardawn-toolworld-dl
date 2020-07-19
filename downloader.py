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

WIDTH = 2
HEIGHT = 1

URL = "https://osricrpg.com/wizardawn/tool_world.php?run=1"


class MapGenre(Enum):
    FANTASY = 'Fantasy'
    POST_APO = 'Post-Apocalyptic',
    EXODUS_SPACESHIP = 'Exodus Spaceship'
    SCI_FI = 'Sci-Fi'
    POST_APO_FANTASY = 'Post-Apocalyptic Fantasy'
    EMPTY = 'Empty'


class MapClimate(Enum):
    COLD_NORTH_WARM_SOUTH = 1


class PageDownloader:
    def __init__(self, name=NAME, map_genre=MapGenre.FANTASY.value, map_climate=MapClimate.COLD_NORTH_WARM_SOUTH.value,
                 height=HEIGHT, width=WIDTH, hex_miles=5, info=INFO, legend=LEGEND, water=WATER):
        self.form_data = {
            'program_user': 1,  # I don't know what this is
            'map_name': name,
            'map_genre': map_genre,
            'map_climate': map_climate,
            'map_wide': height,
            'map_high': width,
            'map_equals': hex_miles,
            'info': 1 if info else 0,
            'legend': 1 if legend else 0,
            'water_n': water['n'],
            'water_s': water['s'],
            'water_e': water['e'],
            'water_w': water['w'],
            'Create': 'Create'
        }

    def get_html(self):
        r = requests.post(URL, data=self.form_data)

        if r.status_code != requests.codes.ok:
            r.raise_for_status()

        html = r.text
        return html
