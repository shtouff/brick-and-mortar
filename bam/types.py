import enum
from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List, Optional, Any

from marshmallow import fields
from marshmallow_dataclass import NewType


class AirDateField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        return datetime.strptime(data[attr], "%B %d, %Y").date()


AirDate: Any = NewType("WeirdDate", date, field=AirDateField)


@dataclass
class Episode:
    id: int
    name: str
    episode: str
    air_date: AirDate
    characters: List[int] = field(default_factory=list)


@dataclass
class Character:
    id: int
    name: str
    status: str
    species: str
    type: str
    gender: str
    episode: List[int] = field(default_factory=list)


@dataclass
class Comment:
    title: str
    comment: str
    id: Optional[int] = None
    episode: Optional[int] = None
    character: Optional[int] = None


@dataclass
class CommentForUpdate:
    title: Optional[str] = None
    comment: Optional[str] = None


class Role(enum.Enum):
    ADMIN = "ADMIN"
    USER = "USER"
    EDITOR = "EDITOR"


@dataclass
class UserAccount:
    username: str
    password: str
    role: Role
    id: Optional[int] = None
