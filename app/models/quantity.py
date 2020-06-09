from math import trunc


class QuantityMixin:
    """
    Add a quantity value to an object, along with the ability to determine the quantity in number of stacks and
    remainder.
    """

    quantity: int = 0

    @property
    def stacks(self):
        stack_size = None

        # Imports here to avoid circular dependency during loading
        from app.models.item import Item
        from app.models.recipe import Recipe
        if isinstance(self, Recipe):
            if self.item:
                stack_size = self.item.stack_size
        elif isinstance(self, Item):
            stack_size = self.stack_size

        if stack_size is not None:
            return trunc(self.quantity / stack_size)

        return 0

    @property
    def remainder(self):
        stack_size = None

        # Imports here to avoid circular dependency during loading
        from app.models.item import Item
        from app.models.recipe import Recipe
        if isinstance(self, Recipe):
            if self.item:
                stack_size = self.item.stack_size
        elif isinstance(self, Item):
            stack_size = self.stack_size

        if stack_size is not None:
            return self.quantity - trunc(self.quantity / stack_size) * stack_size

        return self.quantity
