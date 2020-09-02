
class Option:

	def __init__(self, option_id, option_type, type_display, value, sort_order, display_name):
		self.OptionId = option_id
		self.OptionType = option_type
		self.TypeDisplay = type_display
		self.Value = value
		self.SortOrder = sort_order
		self.DisplayName = display_name

	def option_id(self):
		return self.OptionId

	def option_type(self):
		return self.OptionType

	def type_display(self):
		return self.TypeDisplay

	def value(self):
		return self.Value

	def sort_order(self):
		return self.SortOrder

	def display_name(self):
		return self.DisplayName

	def __eq__(self, other):
		if self.__class__ is not other.__class__:
			return False
		return self.OptionId == other.option_id()

	def __ne__(self, other):
		return not self == other

	def __lt__(self, other):
		if self.SortOrder is None or other.SortOrder is None:
			return False
		return self.SortOrder < other.SortOrder

	def __le__(self, other):
		if self.SortOrder is None or other.SortOrder is None:
			return True
		return self.SortOrder <= other.SortOrder

	def __gt__(self, other):
		if self.SortOrder is None or other.SortOrder is None:
			return False
		return self.SortOrder > other.SortOrder

	def __ge__(self, other):
		if self.SortOrder is None or other.SortOrder is None:
			return True
		return self.SortOrder >= other.SortOrder

	def __hash__(self):
		return hash(self.OptionId)

	def __str__(self):
		return "{} {} {} {} {} {}".format(self.OptionId, self.OptionType, self.TypeDisplay, self.Value, self.SortOrder,
																			self.DisplayName)
