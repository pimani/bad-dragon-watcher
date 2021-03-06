from argOption import ArgOption
from filter import Filter


#  TODO fuse option so that filter and argParse are being generated with the option list
#  TODO get value to init option from the api


class ArgParser:
    """
    Object to represent a bad-dragon toy.

    Correct : Tell if any error happened during the parse, boolean
    Error : Tell witch error happened, string
    Name : Name of the filter, string
    ToyName: Name of the toy, string
    Type : Category of the toy, string
    Comparator: comparator to select a variety of size ">" or "<"
    Size : Size of the toy, string
    Color : Color of the toy, string
    Firmness : Hardness of the yoy, string
    CumTube : if the toy have a cum tube, string
    SuctionCup : if the toy have a suction cup, string
    Flop : Flop of the toy, string
    """

    def __init__(self, options):
        """Init function, create the toy."""
        self.Toy_list = list(options.ProductName.keys())
        self.Options = options
        self.Option_list = []
        self.Correct = False
        self.Error = None
        self.Name = None
        self.Toy_Name = None
        self.Type = None
        self.Size = None
        self.Comparator = None
        self.Color = None
        self.Firmness = None
        self.CumTube = None
        self.SuctionCup = None
        self.Flop = None

        self.init_passer()

    def set_toy_list(self, toy_list):
        """Init the parser with a new list of toy"""
        self.Toy_list = toy_list
        self.init_passer()

    def init_passer(self):
        self.Name = ArgOption("name", "N", "Name of the filter", [])
        self.Toy_Name = ArgOption("toy-name", "n", "Name of the toy !ToyName to get the list",
                                  self.Options.product_name())
        self.Type = ArgOption("category", "ca", "Type of the toy !toyType to get the list", self.Options.type_option())
        self.Size = ArgOption("size", "s", "Size of the toy !toySize to get the list", self.Options.size_option())
        self.Comparator = ArgOption("comparator", "co", "Comparator the size of the toy !comparator to get the list",
                                    self.Options.comparator_option())
        self.Color = ArgOption("color", "c", "Color of the toy", [])
        self.Firmness = ArgOption("firmness", "f", "Firmness of the toy !toyFirmness to get the list",
                                  self.Options.firmness_option())
        self.CumTube = ArgOption("cum-tube", "ct", "Cum tube or not on the toy !cumTube to get the list",
                                 self.Options.cum_tub_option())
        self.SuctionCup = ArgOption("suction-cup", "sc", "Suction or not on the toy !suctionCup to get the list",
                                    self.Options.suction_cup_option())
        self.Flop = ArgOption("Flop", "cn", "Flop condition of the toy", self.Options.flop_option())
        self.Option_list.append(self.Name)
        self.Option_list.append(self.Toy_Name)
        self.Option_list.append(self.Type)
        self.Option_list.append(self.Size)
        self.Option_list.append(self.Comparator)
        self.Option_list.append(self.Color)
        self.Option_list.append(self.Firmness)
        self.Option_list.append(self.CumTube)
        self.Option_list.append(self.SuctionCup)
        self.Option_list.append(self.Flop)

    def passe(self, arg_list):
        """Parse the text and set value in the Option_list, if a parse error append is_correct return false"""
        self.Correct = True
        self.Error = None
        for option in self.Option_list:
            option.set_value(None)
        for arg in arg_list:
            for arg_option in self.Option_list:
                if arg.startswith("--" + arg_option.name() + "="):
                    value = arg[len("--" + arg_option.name() + "="):]
                    if len(value) > 0 and \
                       (len(arg_option.possible_value()) == 0 or value in arg_option.possible_value()):
                        if len(arg_option.possible_value()) == 0:
                            arg_option.set_value(value)
                        else:
                            arg_option.set_value(arg_option.option_values()[value])
                    else:
                        self.Error = arg_option.name() + " Bad or missing value"
                        self.Correct = False
                elif arg.startswith("-" + arg_option.short_name() + "="):
                    value = arg[len("-" + arg_option.short_name() + "="):]
                    if len(value) > 0 and \
                       (len(arg_option.possible_value()) == 0 or value in arg_option.possible_value()):
                        if len(arg_option.possible_value()) == 0:
                            arg_option.set_value(value)
                        else:
                            arg_option.set_value(arg_option.option_values()[value])
                    else:
                        self.Error = arg_option.short_name() + " Bad or missing value"
                        self.Correct = False

    def is_correct(self):
        """Tell if the parse finish without error"""
        return self.Correct

    def create_filter(self):
        return Filter(self.Name, self.get_toy_name(), self.get_type(), self.get_size(), self.get_comparator(),
                      self.get_color(), self.get_firmness(), self.get_cum_tube(), self.get_suction_cup(),
                      self.get_flop())

    def get_help(self):
        response = self.Name.help_text() + "\n"
        response += self.Toy_Name.help_text() + "\n"
        response += self.Type.help_text() + "\n"
        response += self.Size.help_text() + "\n"
        response += self.Comparator.help_text() + "\n"
        response += self.Color.help_text() + "\n"
        response += self.Firmness.help_text() + "\n"
        response += self.CumTube.help_text() + "\n"
        response += self.SuctionCup.help_text() + "\n"
        response += self.Flop.help_text()
        return response

    def get_toy_name(self):
        """Return the name of the filter."""
        return self.Toy_Name.value()

    def get_name(self):
        """Return the name of the filter."""
        return self.Name.value()

    def get_type(self):
        """Return the type of the filter."""
        return self.Type.value()

    def get_size(self):
        """Return the size of the filter."""
        return self.Size.value()

    def get_comparator(self):
        """Return the comparator of the filter."""
        return self.Comparator.value()

    def get_color(self):
        """Return the color of the filter."""
        return self.Color.value()

    def get_firmness(self):
        """Return the firmness of the filter."""
        return self.Firmness.value()

    def get_cum_tube(self):
        """Return if the toy have a cum filter."""
        return self.CumTube.value()

    def get_suction_cup(self):
        """Return if the filter have a suction cup."""
        return self.SuctionCup.value()

    def get_flop(self):
        """Return the flop condition of the filter."""
        return self.Flop.value()

    def get_correct(self):
        """Return if the last parse finish with a error."""
        return self.Correct

    def get_error(self):
        """Return the Error."""
        return self.Error

    def __str__(self):
        """Return a string to represent the filter."""
        temp = ""
        temp += str(self.get_type()) + " : "
        temp += str(self.get_name()) + " "
        temp += str(self.get_size().value()) + " "
        temp += str(self.get_color()) + " "
        temp += str(self.get_comparator()) + " "
        if self.get_firmness() is not None:
            temp += str(self.get_firmness().value()) + " "
        if self.get_cum_tube() == 'true':
            temp += "Cum tube "
        if self.get_suction_cup() == 'true':
            temp += "Suction cup "
        temp += str(self.get_flop()) + " "
        return temp

    def __eq__(self, other):
        """Test if two toy are exactly the same."""
        result = self.Name == other.Name() or self.Name is None
        result = result and (self.get_type() == other.get_type() or self.get_type() is None)
        result = result and (self.get_size() == other.get_size() or self.get_size() is None)
        result = result and (self.get_color() == other.get_color() or self.get_color() is None)
        result = result and (self.get_firmness() == other.get_firmness() or self.get_firmness() is None)
        result = result and (self.get_cum_tube() == other.get_cum_tube() or self.get_cum_tube() is None)
        result = result and (self.get_suction_cup() == other.get_suction_cup() or self.get_suction_cup() is None)
        result = result and (self.get_flop() == other.get_flop() or self.get_flop() is None)
        return result

    def __ne__(self, other):
        """Test if two toy are not exactly the same."""
        return not self.__eq__(other)
