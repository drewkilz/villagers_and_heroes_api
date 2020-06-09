from app import sql_alchemy
from app.data import Item as DataItem
from app.models.load import LoadMixin
from app.models.quantity import QuantityMixin
from app.models.type import ItemType, CategoryEnum

SALVAGE_KIT = 'Salvage Kit'
WATER = 'Water'


class Item(sql_alchemy.Model, QuantityMixin, LoadMixin):
    __tablename__ = 'items'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True, nullable=False)
    name = sql_alchemy.Column(sql_alchemy.Unicode(255), unique=True, index=True, nullable=False)
    type_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)
    level = sql_alchemy.Column(sql_alchemy.SmallInteger, nullable=True)
    class_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=True)
    subclass_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=True)
    rarity_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)

    type = sql_alchemy.relationship('Type', foreign_keys=[type_id])
    class_ = sql_alchemy.relationship('Type', foreign_keys=[class_id])
    subclass = sql_alchemy.relationship('Type', foreign_keys=[subclass_id])
    rarity = sql_alchemy.relationship('Type', foreign_keys=[rarity_id])

    def __repr__(self):
        return 'Item(id={}, name={}, type={}, level={}, class={}, subclass={}, rarity={})'.format(
            self.id, self.name, self.type, self.level, self.class_, self.subclass, self.rarity)

    @property
    def salvageable(self):
        return self.type.name in (
            ItemType.SWORD.value,
            ItemType.STAFF.value,
            ItemType.MACE.value,
            ItemType.BOW.value,
            ItemType.AXE.value,
            ItemType.ARMOR.value,
            ItemType.BELT.value,
            ItemType.GLOVE.value,
            ItemType.BOOTS.value,
            ItemType.HEADWEAR.value,
            ItemType.SHIELD.value
        )

    @property
    def stack_size(self):
        if self.type.name in (ItemType.MINERAL.value, ItemType.BUG.value, ItemType.FISH.value, ItemType.PLANT.value,
                              ItemType.INGREDIENT.value, ):
            return 350
        elif self.type.name in (ItemType.COMPONENT.value, ):
            return 50
        elif self.name == WATER:
            return 1000
        else:
            return None

    @classmethod
    def load(cls, data: DataItem):
        item = Item(
            name=data.name,
            type=cls.get_type(data.type, CategoryEnum.ITEM_TYPE),
            level=data.level,
            class_=cls.get_type(data.class_, CategoryEnum.CLASS),
            subclass=cls.get_type(data.subclass, CategoryEnum.SUB_CLASS),
            rarity=cls.get_type(data.rarity, CategoryEnum.RARITY))

        sql_alchemy.session.add(item)
