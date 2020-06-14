"""Object to represent a bad-dragon toy."""


class Toy:
    """
    Object to represent a bad-dragon toy.

    name : name of the toy str
    type : type of the toy (penetrable, ..etc) str
    size : size of the toy str
    color : color of the toy str
    firmness : firmness of the toy str
    description : flop reason str
    toy_id : if of the toy in the clearence database str
    """

    def __init__(self, name, types, size, color, firmness, cumtube,
                 suction_cup, condition, description, toy_id):
        """Init function, create the toy."""
        self.ID = toy_id
        self.Name = name
        self.Type = types
        self.Size = size
        self.Color = color
        self.Firmness = firmness
        self.CumTube = cumtube
        self.SuctionCup = suction_cup
        self.Condition = condition
        self.Description = description

    def get_name(self):
        """Return the name of the toy."""
        return self.Name

    def get_type(self):
        """Return the type of the toy."""
        return self.Type

    def get_size(self):
        """Return the size of the toy."""
        return self.Size

    def get_color(self):
        """Return the color of the toy."""
        return self.Color

    def get_firmness(self):
        """Return the firmness of the toy."""
        return self.Firmness

    def get_cum_tube(self):
        """Return if the toy have a cum tube."""
        return self.CumTube

    def get_suction_cup(self):
        """Return if the toy have a suction cup."""
        return self.SuctionCup

    def get_condition(self):
        """Return the condition of the toy."""
        return self.Condition

    def get_description(self):
        """Return the description of the toy."""
        return self.Description

    def get_id(self):
        """Return the ID of the toy."""
        return self.ID

    def __str__(self):
        """Return a string to represent the toy."""
        temp = ""
        temp += self.Type + " : "
        temp += self.Name + " "
        temp += self.Size + " "
        temp += self.Color + " "
        for i in self.Firmness:
            temp += 'Firmness '
            temp += i + " "
        if self.get_cum_tube() == 1:
            temp += "Cum tube "
        if self.get_suction_cup() == 1:
            temp += "Suction cup "
        if self.get_condition() == "flop":
            temp += "flop : " + self.get_description()
        else:
            temp += "Ready Made"
        return temp

    def __eq__(self, other):
        """Test if two toy are exactly the same."""
        result = self.Name == other.Name() or self.Name is None
        result = result and (self.Type == other.get_type() or self.Type is None)
        result = result and (self.Size == other.get_size() or self.Size is None)
        result = result and (self.Color == other.get_color() or self.Color is None)
        result = result and (self.Firmness == other.get_firmness() or self.Firmness is None)
        result = result and (self.CumTube == other.get_cum_tube() or self.CumTube is None)
        result = result and (self.SuctionCup == other.get_suction_cup() or self.SuctionCup is None)
        result = result and (self.Condition == other.get_condition() or self.Condition is None)
        result = result and (self.Description == other.GetDescription() or self.Description is None)
        return result

    def __ne__(self, other):
        """Test if two toy are not exactly the same."""
        return not self.__eq__(other)
