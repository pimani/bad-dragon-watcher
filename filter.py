"""Filter object who work on bad-dragon toy."""
from sizeEnum import SizeSet


class Filter:
    """
    Filter object who work on bad-dragon toy.

    Name : Name of the filter, string
    ToyName: Name of the toy, string
    Type : Category of the toy, string
    Comparator: comparator to select a variety of size ">" or "<"
    Size : Size of the toy, string
    Color : Color of the toy, string
    Firmness : Hardness of the yoy, string
    CumTube : if the toy have a cum tube, string
    SuctionCup : if the toy have a suction cup, string
    Condition : Condition of the toy, string

    Every value can be None, in that case the corresponding test will always return true.
    """

    def __init__(self, name, toy_name, toy_type, size, comparator, color, firmness, cumtube, suction_cup, condition):
        """Init the object data."""
        self.Name = name
        self.ToyName = toy_name
        self.Type = toy_type
        self.Comparator = comparator
        self.Size = size
        self.Color = color
        self.Firmness = firmness
        self.CumTube = cumtube
        self.SuctionCup = suction_cup
        self.Condition = condition
        self.SizeNumber = {}
        for i in SizeSet:
            self.SizeNumber[i.short_name()] = i.order()

    def __str__(self):
        return "{}:\nToy name: {}\nCategory: {}\nSize: {}\nComparator: {}\nColor: {}\nFirmness: {}\nCumTube: {}\n" \
               "SuctionCup: {}\nCondition: {}".format(self.Name, self.ToyName, self.Type, self.Size, self.Comparator,
                                                      self.Color, self.Firmness, self.CumTube, self.SuctionCup,
                                                      self.Condition)

    def get_name(self):
        """Return the Name of the filter."""
        return self.Name

    def get_toy_name(self):
        """Return the Name of the filter."""
        return self.ToyName

    def get_type(self):
        """Return the Name of the filter."""
        return self.Type

    def get_comparator(self):
        """Return the comparator of the filter."""
        return self.Comparator

    def get_size(self):
        """Return the size of the filter."""
        return self.Size

    def get_color(self):
        """Return the color of the filter."""
        return self.Color

    def get_firmness(self):
        """Return the firmness of the filter."""
        return self.Firmness

    def get_suction_cup(self):
        """Return if there a SuctionCup on the filter."""
        return self.SuctionCup

    def get_cum_tube(self):
        """Return if there a cumtube on the filter."""
        return self.CumTube

    def get_condition(self):
        """Return the asked condition of the filter."""
        return self.Condition

    def set_toy_name(self, name):
        """Change the wanted name of the toy."""
        self.ToyName = name

    def set_type(self, toy_type):
        """Change the wanted type of the toy."""
        self.Type = toy_type

    def set_comparator(self, comparator):
        """Return the comparator of the filter."""
        self.Comparator = comparator

    def set_size(self, size):
        """Change the wanted size of the toy."""
        self.Size = size

    def set_color(self, color):
        """Change the wanted color of the toy."""
        self.Color = color

    def set_firmness(self, firmness):
        """Change the wanted firmness of the toy."""
        self.Firmness = firmness

    def set_condition(self, condition):
        """Change the wanted condition of the toy."""
        self.Condition = condition

    def test_name(self, toy):
        """Test the Name of a toy."""
        if self.get_toy_name() is None:
            return True
        return self.get_toy_name() == toy.get_name()

    def test_type(self, toy):
        """Test the type of a toy."""
        if self.get_type() is None:
            return True
        return self.get_type() == toy.get_type()

    def test_size(self, toy):
        """Test the size of a toy."""
        if self.get_size() is None:
            return True
        if self.get_comparator() == ">":
            return self.SizeNumber[toy.get_size()] >= self.SizeNumber[self.get_size()]
        if self.get_comparator() == "<":
            return self.SizeNumber[toy.get_size()] <= self.SizeNumber[self.get_size()]
        return self.SizeNumber[toy.get_size()] == self.SizeNumber[self.get_size()]

    def test_color(self, toy):
        """Test the color of a toy."""
        if self.get_color() is None:
            return True
        return self.get_color() == toy.get_color()

    def test_firmness(self, toy):
        """Test the firmness of a toy."""
        if self.get_firmness() is None:
            return True
        for i in self.get_firmness():
            if i not in toy.get_firmness():
                return False
        return True

    def test_cum_tube(self, toy):
        """Test the cum_tube of a toy."""
        if self.get_cum_tube() is None:
            return True
        return self.get_cum_tube() == toy.get_cum_tube()

    def test_suction_cup(self, toy):
        """Test the suction_cup of a toy."""
        if self.get_suction_cup() is None:
            return True
        return self.get_suction_cup() == toy.get_suction_cup()

    def test_condition(self, toy):
        """Test the condition of a toy."""
        if self.get_condition() is None:
            return True
        return self.get_condition() == toy.get_condition()

    def test_toy(self, toy):
        """Test a toy."""
        print("Test toy: {} filter : {}".format(toy, self))
        result = True and self.test_name(toy)
        result = result and self.test_type(toy)
        result = result and self.test_size(toy)
        result = result and self.test_color(toy)
        result = result and self.test_firmness(toy)
        result = result and self.test_suction_cup(toy)
        result = result and self.test_cum_tube(toy)
        result = result and self.test_condition(toy)
        return result
