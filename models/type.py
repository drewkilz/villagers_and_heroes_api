"""Contains classes describing types of objects."""

from enum import Enum


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

    def is_salvageable(self):
        return self in (
            self.SWORD,
            self.STAFF,
            self.MACE,
            self.BOW,
            self.AXE,
            self.ARMOR,
            self.BELT,
            self.GLOVE,
            self.BOOTS,
            self.HATS,
            self.SHIELD
        )


class SkillType(Enum):
    CRAFTING = 'Crafting'
    GATHERING = 'Gathering'
    VILLAGE = 'Village'
