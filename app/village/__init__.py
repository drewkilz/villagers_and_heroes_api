from time import perf_counter

from app.village.projects import Projects
from app.village.roster import Roster


class VillageImageParser:
    def __init__(self, server_name):
        self._original_images = []
        self._image_paths = []
        self._time = 0
        self._server_name = server_name
        self.roster = None
        self.projects = None

    def add_image(self, original_image, image_path):
        self._original_images.append(original_image)
        self._image_paths.append(image_path)

    def process(self):
        start = perf_counter()

        if not self._image_paths:
            return

        self.roster = None
        self.projects = None

        for original_image, image_path in zip(self._original_images, self._image_paths):
            if Roster.is_valid(image_path):
                if self.roster is None:
                    self.roster = Roster(self._server_name)
                self.roster.add_image(original_image, image_path)
            elif Projects.is_valid(image_path):
                if self.projects is None:
                    self.projects = Projects(self._server_name)
                self.projects.add_image(original_image, image_path)

        if self.roster:
            self.roster.process()

        if self.projects:
            self.projects.process()

        self._time = perf_counter() - start

    @property
    def processing_time(self):
        return self._time

    @property
    def village(self):
        if self.roster:
            return self.roster.village

        if self.projects:
            return self.roster.village

        return None

    @property
    def server(self):
        return self._server_name

    def save(self):
        if self.roster:
            self.roster.save()

        if self.projects:
            self.projects.save()
