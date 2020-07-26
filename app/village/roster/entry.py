from dataclasses import dataclass
from datetime import datetime

from marshmallow import Schema, fields

from app.village.roster.rank import Rank, RankSchema


@dataclass
class Entry:
    level: int
    name: str
    rank: Rank
    timestamp: datetime


class EntrySchema(Schema):
    level = fields.Integer()
    name = fields.String()
    rank = fields.Nested(RankSchema)
    timestamp = fields.DateTime()
