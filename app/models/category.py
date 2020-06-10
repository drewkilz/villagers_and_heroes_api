from app import sql_alchemy


class Category(sql_alchemy.Model):
    __tablename__ = 'categories'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    name = sql_alchemy.Column(sql_alchemy.Unicode(255), index=True, unique=True)

    types = sql_alchemy.relationship('Type', backref='types', lazy='dynamic')

    def __repr__(self):
        return 'Category(id={}, name={})'.format(self.id, self.name)
