from bam.extensions import db


association_table = db.Table(
    "association",
    db.metadata,
    db.Column("episode_id", db.ForeignKey("episode.id"), primary_key=True),
    db.Column("character_id", db.ForeignKey("character.id"), primary_key=True),
)


class Episode(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    air_date = db.Column(db.Date, nullable=False)
    episode = db.Column(db.String, nullable=False)
    characters = db.relationship(
        "Character", secondary=association_table, back_populates="episodes"
    )


class Character(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    episode = db.relationship(
        "Episode", secondary=association_table, back_populates="characters"
    )
