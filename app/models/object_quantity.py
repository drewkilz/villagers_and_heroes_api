from dataclasses import dataclass
from typing import Union
from math import trunc

from .item import Item
from .recipe import Recipe


@dataclass
class ObjectQuantity:
    """
    Describes an item or recipe with an associated quantity to obtain.
    """

    object: Union[Item, Recipe]
    quantity: int

    @property
    def stacks(self):
        stack_size = None

        if isinstance(self.object, Recipe):
            if self.object.item:
                stack_size = self.object.item.stack_size
        else:
            stack_size = self.object.stack_size

        if stack_size is not None:
            return trunc(self.quantity / stack_size)

        return 0

    @property
    def remainder(self):
        stack_size = None

        if isinstance(self.object, Recipe):
            if self.object.item:
                stack_size = self.object.item.stack_size
        else:
            stack_size = self.object.stack_size

        if stack_size is not None:
            return self.quantity - trunc(self.quantity / stack_size) * stack_size

        return self.quantity
