
class ArgOption:

	def __init__(self, name, short_name, help_text, possible_value):
		self.Name = name
		self.Possible_Value = possible_value
		self.Help = help_text
		self.Short_name = short_name
		self.Value = None

	def __str__(self):
		return "Name: {} short-name: {} possible value: {} value: {}".format(self.Name, self.Short_name,
																																					self.Possible_Value, self.Value)

	def name(self):
		return self.Name

	def possible_value(self):
		return self.Possible_Value

	def short_name(self):
		return self.Short_name

	def help_text(self):
		temp = "{}: --{} -{}".format(self.Help, self.Name, self.Short_name)
		return temp + ("" if self.Possible_Value == [] else " possible value {}".format(self.Possible_Value))

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
