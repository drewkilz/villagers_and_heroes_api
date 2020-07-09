from app import sql_alchemy


class Village(sql_alchemy.Model):
    __tablename__ = 'villages'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    name = sql_alchemy.Column(sql_alchemy.Unicode(255), unique=True, index=True, nullable=False)
    server_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)

    server = sql_alchemy.relationship('Type', foreign_keys=[server_id])

    def __repr__(self):
        return 'Village(id={}, name={}, server={})'.format(
            self.id, self.name, self.server)
