from dataclasses import dataclass, field
from datetime import datetime
from typing import Dict, List

from marshmallow import Schema, fields
from marshmallow.fields import Nested

from app.village.roster.entry import Entry, EntrySchema


@dataclass
class Snapshot:
    original_images: List[str] = field(default_factory=list)
    images: List[str] = field(default_factory=list)
    timestamps: List[datetime] = field(default_factory=list)
    entries: Dict[str, Entry] = field(default_factory=dict)


class SnapshotSchema(Schema):
    original_images = fields.List(fields.String)
    timestamps = fields.List(fields.DateTime)
    entries = fields.Dict(keys=fields.String, values=Nested(EntrySchema))
