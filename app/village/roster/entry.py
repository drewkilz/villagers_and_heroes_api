from dataclasses import dataclass
from datetime import datetime

from app.village.roster import Rank


@dataclass
class Entry:
    level: int
    name: str
    rank: Rank
    timestamp: datetime
