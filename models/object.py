from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Any

from dacite import from_dict, Config


def to_int(string):
    try:
        return int(string)
    except ValueError:
        return None


@dataclass
class Object:
    @classmethod
    def from_dict(cls, dictionary: Dict, data: Any):
        return from_dict(cls, dictionary, config=Config(type_hooks={int: to_int, Decimal: Decimal, bool: bool},
                                                        check_types=False))
