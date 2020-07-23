from datetime import datetime
from time import perf_counter
from typing import Dict, List

import cv2
import numpy as np

from app import sql_alchemy
from app.imaging import find_image, parse_and_add_data, get_data, creation_date, get_line
from app.models.character import Character
from app.models.enum import Server
from app.models.roster import Roster as RosterModel
from app.models.type import Type
from app.models.village import Village
from app.village.roster.rank import Rank
from app.village.roster.entry import Entry  # Out of order due to circular references


class Roster:
    def __init__(self, server_name):
        self._data = {}
        self._image_paths = []
        self._time = 0
        self._village_name = None
        self._server_name = server_name

    @classmethod
    def is_valid(cls, image_path):
        image = cv2.imread(image_path)

        header_village_roster_location = find_image('app/village/roster/images/Header-Village-Roster.png', image)[0]

        return True if header_village_roster_location else False

    def add_image(self, image_path):
        self._image_paths.append(image_path)

    def process(self):
        start = perf_counter()

        if not self._image_paths:
            return

        self._data = {}

        for image_path in self._image_paths:
            self._village_name, data = self._get_roster_data(image_path)

            for row in data:
                if row['name'] not in self._data:
                    self._data[row['name']] = Entry(
                        int(row['level']),
                        row['name'],
                        Rank(row['rank']['name'], row['rank']['custom_name']),
                        datetime.utcfromtimestamp(creation_date(image_path)))

        self._time = perf_counter() - start

    @property
    def count(self):
        return len(self._data)

    @property
    def entries(self):
        return self._data

    @property
    def processing_time(self):
        return self._time

    @property
    def village(self):
        return self._village_name

    @property
    def server(self):
        return self._server_name

    def _get_roster_data(self, image_path):
        data = []
        row_dimensions = []

        image = cv2.imread(image_path)

        header_village_roster_location = find_image('app/village/roster/images/Header-Village-Roster.png', image)[0]

        village_name_image = image[header_village_roster_location[1] - 72:header_village_roster_location[1] - 48,
                                   header_village_roster_location[0] - 18:header_village_roster_location[0] + 140]

        village_name = get_line(village_name_image)

        level_header_image = cv2.imread('app/village/roster/images/Header-Level.png')

        rank_location = find_image('app/village/roster/images/Header-Rank.png', image)[0]
        name_location = find_image('app/village/roster/images/Header-Name.png', image)[0]
        level_location = find_image(level_header_image, image)[0]

        data_start_y = rank_location[1] + 22
        data_end_y = rank_location[1] + 349

        # Pull a sub-image of just the rank information and parse
        parse_and_add_data(
            data, row_dimensions, 'rank', image[data_start_y:data_end_y, rank_location[0] - 8:name_location[0] - 1],
            self._get_rank_data)

        # Pull a sub-image of just the names and parse
        parse_and_add_data(
            data, row_dimensions, 'name', image[data_start_y:data_end_y, name_location[0]:level_location[0] - 1],
            get_data)

        # Pull a sub-image of just the levels and parse
        parse_and_add_data(
            data, row_dimensions, 'level',
            image[data_start_y:data_end_y, level_location[0]:level_location[0] + level_header_image.shape[:2][1]],
            get_data, whitelist='0123456789')

        return village_name, data

    @staticmethod
    def _get_rank_data(row_dimensions: List[Dict], image: np.ndarray, whitelist=None):
        # Grab the portion of the image containing the icons
        icon_image = image[0:image.shape[:2][0], 0:26]

        # Search the region for the icons
        ranks = {}
        for rank_name in (Rank.get_names()):
            rank_image_path = 'app/village/roster/images/Rank-Icon-{}.png'.format(rank_name.value)
            rank_image = cv2.imread(rank_image_path)
            rank_icon_locations = find_image(rank_image, icon_image)
            for (x, y) in rank_icon_locations:
                ranks[y] = {'x': x, 'y': y, 'name': rank_name, 'image': rank_image}

        if not row_dimensions:
            for rank_ in ranks.values():
                row_dimensions.append({'top': rank_['y'], 'bottom': rank_['y'] + rank_['image'].shape[:2][1]})

            row_dimensions.sort(key=lambda dimension: dimension['top'])

        # For each rank icon found, parse the text next to it for the customized name of the rank
        custom_ranks = get_data(row_dimensions, image[0:image.shape[:2][0], 27:image.shape[:2][1]])
        for name, key in zip(custom_ranks, sorted(ranks.keys())):
            ranks[key]['custom_name'] = name

        # Iterate to return a list, in order found, of the ranks
        ranks_found = []
        for y in sorted(ranks.keys()):
            ranks_found.append({
                'name': ranks[y]['name'],
                'custom_name': ranks[y]['custom_name']
            })

        return ranks_found

    def save(self):
        try:
            # Set up the village
            village = Village.query.filter_by(name=self._village_name).first()
            if village is None:
                village = Village(name=self._village_name, server=Type.query.filter_by(name=self._server_name).first())
                sql_alchemy.session.add(village)

            for entry_ in sorted(self.entries.values(), key=lambda entry__: entry__.rank.order):
                print(entry_)

                # Set up or fetch the character
                character = Character.query.filter_by(
                    name=entry_.name, server=Type.query.filter_by(name=Server.US2.value).first()).first()
                if character is None:
                    character = Character(name=entry_.name,
                                          server=Type.query.filter_by(name=Server.US2.value).first())
                    sql_alchemy.session.add(character)

                # Set up or fetch the roster entry
                roster = RosterModel.query.filter_by(
                    village=village, character=character, timestamp=entry_.timestamp).first()
                if not roster:
                    roster = RosterModel(village=village, character=character, level=entry_.level,
                                         rank=Type.query.filter_by(name=entry_.rank.name.value).first(),
                                         custom_rank_name=entry_.rank.custom_name, timestamp=entry_.timestamp)
                else:
                    roster.level = entry_.level
                    roster.rank = Type.query.filter_by(name=entry_.rank.name.value).first()
                    roster.custom_rank_name = entry_.rank.custom_name

                sql_alchemy.session.add(roster)

            sql_alchemy.session.commit()
        finally:
            sql_alchemy.session.remove()
