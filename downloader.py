import requests

from enum import Enum


class MapGenre(Enum):
    FANTASY = 'Fantasy'
    POST_APO = 'Post-Apocalyptic',
    EXODUS_SPACESHIP = 'Exodus Spaceship'
    SCI_FI = 'Sci-Fi'
    POST_APO_FANTASY = 'Post-Apocalyptic Fantasy'
    EMPTY = 'Empty'


class MapClimate(Enum):
    COLD_NORTH_WARM_SOUTH = 1
    WARM_NORTH_COLD_SOUTH = 2
    COLD_NORTH_COLD_SOUTH = 10
    WARM_NORTH_WARM_SOUTH = 11
    SNOW = 3
    DESERT = 4
    FOREST = 5
    JUNGLE = 6
    TROPICS = 7
    LIFELESS = 8
    UNDERWORLD = 12
    RANDOM = 9


class BorderValue(Enum):
    NO = 0
    WATER = 1
    MOUNTAINS = 2


# Constants

NAME = "Truc"
WATER = {
    'n': BorderValue.MOUNTAINS.value,
    'e': BorderValue.NO.value,
    's': BorderValue.NO.value,
    'w': BorderValue.WATER.value
}
INFO = True
LEGEND = True

COLOR_MAP = True  # whether the tiles are colored
COLOR_HIGHLIGHTS = False  # whether the points of interest are colored differently

OUTER_HULL = False

WIDTH = 1  # there will be 10*WIDTH hexes on a row
HEIGHT = 1  # there will be 8*HEIGHT hexes on a column

URL = "https://osricrpg.com/wizardawn/tool_world.php?run=1"


class PageDownloader:
    def __init__(self, name=NAME, map_genre=MapGenre.FANTASY.value, map_climate=MapClimate.COLD_NORTH_WARM_SOUTH.value,
                 height=HEIGHT, width=WIDTH, hex_miles=5,
                 info=INFO, legend=LEGEND, water=WATER, color_map=COLOR_MAP, color_highlights=COLOR_HIGHLIGHTS,
                 outer_hull=OUTER_HULL):
        self.form_data = {
            'program_user': 1,  # I don't know what this is
            'map_name': name,
            'map_genre': map_genre,
            'map_climate': map_climate,
            'map_wide': width,
            'map_high': height,
            'map_equals': hex_miles,
            'info': 1 if info else 0,
            'legend': 1 if legend else 0,
            'color': 1 if color_map else 0,
            'colorl': 1 if color_highlights else 0,
            'hull': 1 if outer_hull else 0,
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
