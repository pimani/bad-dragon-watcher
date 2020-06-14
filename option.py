
class Option:

	def __init__(self, name, beautiful_name, short_name):
		self.Name = name
		self.Beautiful_Name = beautiful_name
		self.Short_name = short_name

	def name(self):
		return self.Name

	def beautiful_name(self):
		return self.Beautiful_Name

	def short_name(self):
		return self.Short_name

	def __eq__(self, other):
		if self.__class__ is not other.__class__:
			return False
		return self.Name == other.name()

	def __ne__(self, other):
		return not self == other

	def __hash__(self):
		return hash(self.Name)
