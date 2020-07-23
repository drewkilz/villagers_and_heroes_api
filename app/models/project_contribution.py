from app import sql_alchemy


class ProjectContribution(sql_alchemy.Model):
    __tablename__ = 'project_contributions'

    id = sql_alchemy.Column(sql_alchemy.Integer, primary_key=True)
    village_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('villages.id'), index=True,
                                    nullable=False)
    character_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('characters.id'), index=True,
                                      nullable=False)
    project_id = sql_alchemy.Column(sql_alchemy.Integer, sql_alchemy.ForeignKey('types.id'), nullable=False)
    rank = sql_alchemy.Column(sql_alchemy.Integer, nullable=False)
    contribution = sql_alchemy.Column(sql_alchemy.Integer, nullable=False)
    timestamp = sql_alchemy.Column(sql_alchemy.DateTime, nullable=False)

    village = sql_alchemy.relationship('Village', foreign_keys=[village_id])
    character = sql_alchemy.relationship('Character', foreign_keys=[character_id])
    project = sql_alchemy.relationship('Type', foreign_keys=[project_id])

    def __repr__(self):
        return 'ProjectContribution(id={}, village={}, character={}, project={}, rank={}, contribution={}, ' \
               'timestamp={})'.format(
                self.id, self.village, self.character, self.project, self.rank, self.contribution, self.timestamp)
