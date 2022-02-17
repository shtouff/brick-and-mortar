from dataclasses import dataclass, field
from datetime import datetime, date
from typing import List

from marshmallow import fields
from marshmallow_dataclass import NewType


class AirDateField(fields.Field):
    def _deserialize(self, value, attr, data, **kwargs):
        return datetime.strptime(data[attr], "%B %d, %Y").date()


AirDate = NewType("WeirdDate", date, field=AirDateField)


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
