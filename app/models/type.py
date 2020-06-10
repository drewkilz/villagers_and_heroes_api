from app import sql_alchemy


class Type(sql_alchemy.Model):
    __tablename__ = 'types'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    category_id = sql_alchemy.Column(sql_alchemy.SmallInteger, sql_alchemy.ForeignKey('categories.id'), index=True)
    name = sql_alchemy.Column(sql_alchemy.Unicode(255), index=True)

    category = sql_alchemy.relationship('Category')

    def __repr__(self):
        return 'Type(id={}, name={}, category={})'.format(self.id, self.name, self.category)
