from enum import Enum


class CategoryEnum(Enum):
    CLASS = 'Class'
    CRAFTING_TYPE = 'Crafting Type'
    ITEM_TYPE = 'Item Type'
    RARITY = 'Rarity'
    SKILL = 'Skill'
    SKILL_TYPE = 'Skill Type'
    SUB_CLASS = 'Sub Class'
    SERVER = 'Server'
    VILLAGE_RANK = 'Village Rank'
    VILLAGE_PROJECT = 'Village Project'
    VILLAGER_CLASS = 'Villager Class'


class Class(Enum):
    ALL = 'All'
    WARRIOR = 'Warrior'
    WIZARD = 'Wizard'
    HUNTER = 'Hunter'
    PRIEST = 'Priest'
    SHAMAN = 'Shaman'


class SubClass(Enum):
    ALL = 'All'
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
    COMPONENT = 'Crafting Components'
    NECKLACE = "Crafter's Necklaces"

    POWDER = 'Metal Powder and Mineral Oil'
    EMBROIDERY = 'Cloth Embroidery and Leather Stitching'
    RESIN = 'Wood Resins and Pitch'

    FOOD = 'Cooked Food and Baked Goods'
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
    HARVEST = 'Harvest'
    QUEST = 'Quest Item'


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


class VillageRank(Enum):
    CITIZEN = 'Citizen'
    PEER = 'Peer'
    LORD = 'Lord'
    DEPUTY = 'Deputy'
    MAYOR = 'Mayor'


class Server(Enum):
    US1 = 'America 1'
    US2 = 'America 2'
    US3 = 'America 3'
    EUROPE = 'Europe'
    GERMANY = 'Germany'


class VillageProject(Enum):
    KITCHEN = 'Kitchen'
    SMITHY = 'Smithy'
    TAILORY = 'Tailory'
    WOODSHOP = 'Woodshop'
    VAULT = 'Vault'
    EMPYREAN_MACHINE = 'Empyrean Machine'
    TRAINING_GROUNDS = 'Training Grounds'
    COG_DEPO = 'COG Depo'
    YORICK = 'Statue of Yorick'
    ANABELLE = 'Statue of Anabelle'
    FREDERICH = 'Statue of Frederich'
    KINGS = 'Guardian Kings Statue'
    SOILWORKS = 'Soilworks'
    ARBORETUM = 'Arboretum'
    FISH_HATCHERY = 'Fish Hatchery'
    SUGAR_MILL = 'Sugar Mill'
    SEEDLING_NURSERY = 'Seedling Nursery'
    GEOLOGY_LAB = 'Geology Lab'
    WELLSPRING = 'Wellspring'


class VillagerClass(Enum):
    ALL = 'All'
    SMITH = 'Smith'
    CHEF = 'Chef'
    CARPENTER = 'Carpenter'
    TAILOR = 'Tailor'

    def get_crafting_skill(self):
        if self == self.SMITH:
            return CraftingSkill.SMITHING
        elif self == self.CHEF:
            return CraftingSkill.COOKING
        elif self == self.CARPENTER:
            return CraftingSkill.WOODCRAFTING
        elif self == self.TAILOR:
            return CraftingSkill.TAILORING

        return None

    def get_special_recipe(self):
        if self == self.SMITH:
            return 'Steelforged Torc'
        elif self == self.CHEF:
            return 'Whispering Secrets Ring'
        elif self == self.CARPENTER:
            return 'Ring of the Woodland Wit'
        elif self == self.TAILOR:
            return "Spellwoven Weaver's Braid"

        return None
