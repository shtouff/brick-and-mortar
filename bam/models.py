from bam.extensions import db


association_table = db.Table(
    "association",
    db.metadata,
    db.Column("episode_id", db.ForeignKey("episode.id"), primary_key=True),
    db.Column("character_id", db.ForeignKey("character.id"), primary_key=True),
)


class Episode(db.Model):
    __tablename__ = "episode"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    air_date = db.Column(db.Date, nullable=False)
    episode = db.Column(db.String, nullable=False)
    characters = db.relationship(
        "Character", secondary=association_table, back_populates="episode"
    )


class Character(db.Model):
    __tablename__ = "character"
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, nullable=False)
    status = db.Column(db.String, nullable=False)
    species = db.Column(db.String, nullable=False)
    type = db.Column(db.String, nullable=False)
    gender = db.Column(db.String, nullable=False)
    episode = db.relationship(
        "Episode", secondary=association_table, back_populates="characters"
    )


class Comment(db.Model):
    __tablename__ = "comment"
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String, nullable=False)
    comment = db.Column(db.String, nullable=False)
    episode_id = db.Column(db.Integer, db.ForeignKey("episode.id"))
    episode = db.relationship("Episode")
    character_id = db.Column(db.Integer, db.ForeignKey("character.id"))
    character = db.relationship("Character")
