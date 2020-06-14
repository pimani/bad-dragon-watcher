from option import Option


class Size(Option):

    def __init__(self, name, beautiful_name, short_name, order):
        super().__init__(name, beautiful_name, short_name)
        self.Order = order

    def order(self):
        return self.Order

    def __lt__(self, other):
        return self.Order > other.Order

    def __le__(self, other):
        return self.Order >= other.Order

    def __gt__(self, other):
        return self.Order < other.Order

    def __ge__(self, other):
        return self.Order <= other.Order
