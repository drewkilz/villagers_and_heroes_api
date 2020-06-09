from dataclasses import dataclass
from decimal import Decimal
from typing import Dict, Callable, Any

from dacite import from_dict, Config


@dataclass
class Object:
    @staticmethod
    def to_int(string):
        try:
            return int(string)
        except ValueError:
            return None

    @classmethod
    def from_dict(cls, dictionary: Dict):
        return from_dict(cls, dictionary, config=Config(type_hooks={int: cls.to_int, Decimal: Decimal, bool: bool},
                                                        check_types=False))

    @staticmethod
    def convert(key: str, dictionary: Dict, lookup: Callable[[str], Any], optional=False, default=None):
        if key in dictionary:
            string_value = dictionary[key]
            if isinstance(string_value, str):
                try:
                    value = lookup(string_value)
                except ValueError:
                    if optional:
                        value = default
                    else:
                        raise ValueError('Unable to find {} with name: "{}"'.format(lookup.__name__, string_value))

                dictionary[key] = value
