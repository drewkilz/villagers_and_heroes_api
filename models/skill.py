"""Contains classes and constant values pertaining to villager skills."""

from dataclasses import dataclass
from enum import Enum

from models.object import Object
from models.type import SkillType


@dataclass
class Skill(Object):
    name: str
    type: SkillType


class SkillEnum(Enum):
    @classmethod
    def find(cls, name):
        if not hasattr(cls, '_member_map_by_skill_name'):
            # Create the mapping by skill name
            cls._member_map_by_skill_name = {}
            for key, skill in cls._member_map_.items():
                cls._member_map_by_skill_name[skill.value.name] = skill

        if name in cls._member_map_by_skill_name:
            return cls._member_map_by_skill_name[name]
        else:
            return None


class GatheringSkill(SkillEnum):
    BUG_LORE = Skill('Bug Lore', SkillType.GATHERING)
    FISHING = Skill('Fishing', SkillType.GATHERING)
    MINING = Skill('Mining', SkillType.GATHERING)
    PLANT_LORE = Skill('Plant Lore', SkillType.GATHERING)


class VillageSkill(SkillEnum):
    GARDENING = Skill('Gardening', SkillType.VILLAGE)
    RANCHING = Skill('Ranching', SkillType.VILLAGE)


class CraftingSkill(SkillEnum):
    COOKING = Skill('Cooking', SkillType.CRAFTING)
    SMITHING = Skill('Smithing', SkillType.CRAFTING)
    TAILORING = Skill('Tailoring', SkillType.CRAFTING)
    WOODCRAFTING = Skill('Woodcrafting', SkillType.CRAFTING)
