
class ArgOption:

	def __init__(self, name, short_name, help_text, possible_value):
		self.Name = name
		self.Short_name = short_name
		self.Option_Value = {possible_value[i].value(): possible_value[i] for i in possible_value}
		self.Possible_Value = [self.Option_Value[i].value() for i in self.Option_Value]
		self.Help = help_text
		self.Value = None

	def __str__(self):
		return f"Name: {self.Name} short-name: {self.Short_name} possible value: {self.Possible_Value} value: {self.Value}" \
						f" option value {self.Option_Value}"

	def option_values(self):
		return self.Option_Value

	def name(self):
		return self.Name

	def possible_value(self):
		return self.Possible_Value

	def short_name(self):
		return self.Short_name

	def help_text(self):
		# + ("" if self.Possible_Value == [] else " possible value {}".format(self.Possible_Value))
		return "{}: --{} -{}".format(self.Help, self.Name, self.Short_name)

	def value(self):
		return self.Value

	def set_value(self, value):
		self.Value = value

	def __eq__(self, other):
		if self.__class__ is not other.__class__:
			return False
		return self.Name == other.name()

	def __ne__(self, other):
		return not self == other

	def __hash__(self):
		return hash(self.Name)
