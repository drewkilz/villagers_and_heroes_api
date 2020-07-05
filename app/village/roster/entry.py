from dataclasses import dataclass

from app.village.roster import Rank


@dataclass
class Entry:
    level: int
    name: str
    rank: Rank
