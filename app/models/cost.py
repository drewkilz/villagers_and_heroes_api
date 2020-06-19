from decimal import Decimal
from math import trunc


class Cost:
    total: Decimal = 0

    @property
    def gold(self):
        return trunc(self.total)

    @property
    def silver(self):
        return trunc(self.total * 100 - self.gold * 100)

    @property
    def copper(self):
        return trunc(self.total * 10000 - self.gold * 10000 - self.silver * 100)
