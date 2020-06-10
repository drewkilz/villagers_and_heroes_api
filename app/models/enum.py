from enum import Enum


class CategoryEnum(Enum):
    CLASS = 'Class'
    CRAFTING_TYPE = 'Crafting Type'
    ITEM_TYPE = 'Item Type'
    RARITY = 'Rarity'
    SKILL = 'Skill'
    SKILL_TYPE = 'Skill Type'
    SUB_CLASS = 'Sub Class'


class Class(Enum):
    WARRIOR = 'Warrior'
    WIZARD = 'Wizard'
    HUNTER = 'Hunter'
    PRIEST = 'Priest'
    SHAMAN = 'Shaman'


class SubClass(Enum):
    LIGHTNING = 'Lightning'
    FURY = 'Fury'
    FIRE = 'Fire'
    ICE = 'Ice'
    NATURE = 'Nature'
    MARKSMAN = 'Marksman'
    HOLY = 'Holy'
    SHADOW = 'Shadow'
    EARTH = 'Earth'
    WATER = 'Water'


class CraftingType(Enum):
    SWORD = 'Warrior Swords'
    STAFF = 'Wizard Staffs'
    MACE = 'Priest Maces'
    BOW = 'Hunter Bows'
    AXE = 'Shaman Axes'

    ARMOR = 'Armor and Outfits'
    BELT = 'Belts'
    GLOVE = 'Gloves'
    BOOTS = 'Boots and Shoes'
    HATS = 'Hats and Helms'
    SHIELD = 'Priest, Shaman, and Warrior Shields'

    TRINKET = 'Carved Trinkets'

    REFINED = 'Refined Ingredients'
    TOOL = 'Crafting Tools'
    SPECIAL = 'Special Recipes'
    COMPONENTS = 'Crafting Components'
    NECKLACE = "Crafter's Necklaces"

    POWDER = 'Metal Powder and Mineral Oil'
    EMBROIDERY = 'Cloth Embroidery and Leather Stitching'
    RESIN = 'Wood Resins and Pitch'

    FOOD = 'Cooked Foods and Baked Goods'
    HEALTH = 'Health Potions'
    MANA = 'Mana Potions'
    DRAM = 'Drams'
    TRIAD = 'Triad Potions'


class ItemType(Enum):
    MINERAL = 'Mineral'
    INGREDIENT = 'Crafting Ingredient'
    COMPONENT = 'Crafting Component'
    BUG = 'Bug'
    FISH = 'Fish'
    PLANT = 'Plant'
    ITEM = 'Item'
    PREPARATION = 'Preparation'
    SWORD = 'Sword'
    STAFF = 'Staff'
    MACE = 'Mace'
    BOW = 'Bow'
    AXE = 'Axe'
    HEADWEAR = 'Headwear'
    SHIELD = 'Shield'
    NECKLACE = 'Necklace'
    BELT = 'Belt'
    RING = 'Ring'
    TRINKET = 'Trinket'
    TOTEM = 'Totem'
    BOOTS = 'Boots'
    GLOVE = 'Glove'
    ARMOR = 'Armor'
    TOOL = 'Tool'
    CONSUMABLE = 'Consumable'


class Rarity(Enum):
    COMMON = 'Common'
    UNCOMMON = 'Uncommon'
    RARE = 'Rare'
    EPIC = 'Epic'
    LEGENDARY = 'Legendary'


class SkillType(Enum):
    CRAFTING = 'Crafting'
    GATHERING = 'Gathering'
    VILLAGE = 'Village'


class Skill(Enum):
    COOKING = 'Cooking'
    SMITHING = 'Smithing'
    TAILORING = 'Tailoring'
    WOODCRAFTING = 'Woodcrafting'
    BUG_LORE = 'Bug Lore'
    FISHING = 'Fishing'
    MINING = 'Mining'
    PLANT_LORE = 'Plant Lore'
    GARDENING = 'Gardening'
    RANCHING = 'Ranching'


class CraftingSkill(Enum):
    COOKING = Skill.COOKING.value
    SMITHING = Skill.SMITHING.value
    TAILORING = Skill.TAILORING.value
    WOODCRAFTING = Skill.WOODCRAFTING.value


class GatheringSkill(Enum):
    BUG_LORE = Skill.BUG_LORE.value
    FISHING = Skill.FISHING.value
    MINING = Skill.MINING.value
    PLANT_LORE = Skill.PLANT_LORE.value


class VillageSkill(Enum):
    GARDENING = Skill.GARDENING.value
    RANCHING = Skill.RANCHING.value
