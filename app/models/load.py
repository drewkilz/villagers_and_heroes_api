from dataclasses import dataclass
from enum import Enum

from app.models.category import Category
from app.models.enum import CategoryEnum
from app.models.type import Type


class LoadMixin(object):
    @classmethod
    def load(cls, data: dataclass):
        raise NotImplementedError('load() must be implemented')

    @classmethod
    def get_type(cls, type_: Enum, category: CategoryEnum):
        value = None

        if type_:
            value = Type.query.filter_by(name=type_.value, category=Category.query.filter_by(
                name=category.value).first()).first()

        return value
