from app import sql_alchemy


class Roster(sql_alchemy.Model):
    __tablename__ = 'roster'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    village_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('villages.id'), index=True,
                                    nullable=False)
    character_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('characters.id'), index=True,
                                      nullable=False)
    level = sql_alchemy.Column(sql_alchemy.Integer, nullable=False)
    rank_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)
    custom_rank_name = sql_alchemy.Column(sql_alchemy.Unicode(255), nullable=False)
    timestamp = sql_alchemy.Column(sql_alchemy.DateTime, nullable=False)

    village = sql_alchemy.relationship('Village', foreign_keys=[village_id])
    character = sql_alchemy.relationship('Character', foreign_keys=[character_id])
    rank = sql_alchemy.relationship('Type', foreign_keys=[rank_id])

    def __repr__(self):
        return 'Roster(id={}, village={}, character={}, level={}, rank={}, custom_rank_name={}, timestamp={})'.format(
            self.id, self.village, self.character, self.level, self.rank, self.custom_rank_name, self.timestamp)
