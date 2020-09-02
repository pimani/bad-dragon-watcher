from option import Option
from discord import Embed


class OptionValues:

	def __init__(self, extract):
		self.Extract = extract
		self.ProductName = {}
		self.ProductType = {}
		self.SizeOptions = {}  # id -> object
		self.FirmnessOptions = {}
		self.ColorOptions = {}
		self.ComparatorOption = {}
		self.TypeValues = {}
		self.CumTubValues = {}
		self.SuctionCupValues = {}
		self.ToyNameString = {}
		self.FlopOption = {}
		self.load_options()

	def product_name(self):
		return self.ProductName

	def size_option(self):
		return self.SizeOptions

	def firmness_option(self):
		return self.FirmnessOptions

	def color_option(self):
		return self.ColorOptions

	def type_option(self):
		return self.TypeValues

	def comparator_option(self):
		return self.ComparatorOption

	def cum_tub_option(self):
		return self.CumTubValues

	def suction_cup_option(self):
		return self.SuctionCupValues

	def flop_option(self):
		return self.FlopOption

	def load_options(self):
		response = self.Extract.get_option_types_values()
		self.load_type()
		self.load_comparator()
		self.load_flop()
		self.load_option(response, 'size', self.SizeOptions)
		self.load_option(response, 'firmness', self.FirmnessOptions)
		self.load_option(response, 'cumtube', self.CumTubValues)
		self.load_option(response, 'suctionCup', self.SuctionCupValues)
		self.load_products()

	def load_products(self):
		response = self.Extract.get_product_list()
		type_by_name = {self.TypeValues[i].value(): self.TypeValues[i] for i in self.TypeValues}
		position = 0
		for product in response:
			self.ProductName[product['sku']] = Option(product['sku'], 'name', 'Name', product['sku'], position, product['name'])
			position += 1
			self.ProductType[product['sku']] = type_by_name[product['type']]
			if product['type'] in self.ToyNameString:
				text_list = self.ToyNameString[product['type']]
				if len(text_list[-1] + "{} : {}\n".format(product['name'], product['sku'])) > 1024:
					text_list.append("{} : {}\n".format(product['name'], product['sku']))
				else:
					text_list[-1] += "{} : {}\n".format(product['name'], product['sku'])
			else:
				self.ToyNameString[product['type']] = ["{} : {}\n".format(product['name'], product['sku'])]
		for i in self.ToyNameString.keys():
			embed_text = Embed(title="{} toy:".format(i), description="list of {} type of toy".format(i))
			part_number = 0
			for product in self.ToyNameString[i]:
				embed_text.add_field(name="List Part {}".format(part_number), value=product, inline=False)
				part_number += 1
			self.ToyNameString[i] = embed_text

	def load_comparator(self):
		self.ComparatorOption = {
			0: Option(0, "comparator", "Comparator", ">", 0, "Bigger"),
			1: Option(1, "comparator", "Comparator", "<", 1, "Smaller"),
		}

	def load_flop(self):
		self.FlopOption = {
			True: Option(True, "flop", "Flop", True, 0, "True"),
			False: Option(False, "flop", "Flop", False, 1, "False"),
		}

	def load_type(self):
		self.TypeValues = {
			0: Option(0, "type", "Type", "shooter", 0, "Shooter"),
			1: Option(1, "type", "Type", "packer", 1, "Packer"),
			2: Option(2, "type", "Type", "wearable", 2, "Wearable"),
			3: Option(3, "type", "Type", "penetrable", 3, "Penetrable"),
			4: Option(4, "type", "Type", "vibrator", 4, "Vibrator"),
			5: Option(5, "type", "Type", "insertable", 5, "Insertable"),
			6: Option(6, "type", "Type", "accessory", 6, "Merchandise"),
			7: Option(7, "type", "Type", "merchandise", 7, "Merchandise"),
		}

	def load_option(self, response, category, dic):
		if response is None:
			self.SizeOptions = {}
			return
		for i in response:
			if i['type'] == category:
				for k in i['values']:
					dic[k['id']] = Option(k['id'], i['type'], i['displayName'], k['value'], k['sortOrder'], k['displayName'])
