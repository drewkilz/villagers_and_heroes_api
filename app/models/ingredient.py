from app import sql_alchemy


class Ingredient(sql_alchemy.Model):
    __tablename__ = 'ingredients'

    recipe_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('recipes.id'), primary_key=True,
                                   nullable=False)
    item_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('items.id'), primary_key=True,
                                 nullable=False)
    quantity = sql_alchemy.Column(sql_alchemy.SmallInteger, nullable=False)

    recipe = sql_alchemy.relationship('Recipe', foreign_keys=[recipe_id])
    item = sql_alchemy.relationship('Item', foreign_keys=[item_id])

    def __repr__(self):
        return 'Ingredient(quantity={}, item={}, recipe={})'.format(self.quantity, self.item, self.recipe)
