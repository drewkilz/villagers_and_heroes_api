from dataclasses import dataclass

from marshmallow import Schema, fields

from app.models.enum import VillageRank


@dataclass
class Rank:
    name: VillageRank
    custom_name: str

    @property
    def order(self) -> int:
        if self.name == VillageRank.CITIZEN:
            return 5
        elif self.name == VillageRank.PEER:
            return 4
        elif self.name == VillageRank.LORD:
            return 3
        elif self.name == VillageRank.DEPUTY:
            return 2
        elif self.name == VillageRank.MAYOR:
            return 1

    @classmethod
    def get_names(cls):
        return [VillageRank.CITIZEN, VillageRank.PEER, VillageRank.LORD, VillageRank.DEPUTY, VillageRank.MAYOR]


class RankSchema(Schema):
    name = fields.Method('get_rank_name')
    custom_name = fields.String()
    order = fields.Integer()

    def get_rank_name(self, obj):
        return obj.name.value
