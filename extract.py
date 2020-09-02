"""Library to get information from the bad-dragon api."""
import json

import requests


class BadDragonApi:
    numberByPage = 60  # Number of toy to get by request on bd api, 60 is the actual max
    url_base = "https://bad-dragon.com/api/"

    def __init__(self, logger):
        self.logger = logger
        self.logger.debug("BadDragonApi : Init  : Start")
        self.total = 0
        self.products = None
        self.inventory = None
        self.init_product()
        self.init_inventory()
        self.logger.debug("BadDragonApi : Init : Finish")

    def init_product(self):
        """Get all the toy information from bad-dragon api."""
        self.logger.debug("BadDragonApi : InitProduct : Start")
        try:
            response = requests.get("{}products".format(BadDragonApi.url_base))
        except requests.ConnectionError:
            self.logger.error("BadDragonApi : InitProduct : ConnectionError")
            return
        except requests.HTTPError:
            self.logger.error("BadDragonApi : InitProduct : HTTPError")
            return
        except requests.TooManyRedirects:
            self.logger.error("BadDragonApi : InitProduct : TooManyRedirects")
            return
        except requests.URLRequired:
            self.logger.error("BadDragonApi : InitProduct : URLRequired")
            return
        except requests.RequestException:
            self.logger.error("BadDragonApi : InitProduct : RequestException")
            return
        if response.status_code == 200:
            self.products = response.json()
        else:
            # self.logger.error("BadDragonApi : InitProduct : Finish error")
            self.products = None
        self.logger.debug("BadDragonApi : InitProduct : Finish")

    def init_inventory(self):
        self.logger.debug("BadDragonApi : InitInventory : Start")
        page = 1
        self.total = 0
        self.inventory = []
        temp_inventory = None
        while page == 1 or (temp_inventory is not None
                            and temp_inventory['size'] == BadDragonApi.numberByPage):
            temp_inventory = self.get_inventory_page(page)
            page += 1
            if temp_inventory is None:
                self.inventory = None
                self.total = 0
                self.logger.error("BadDragonApi : InitInventory : Finish error")
                return
            self.total += temp_inventory['size']
            self.inventory.extend(temp_inventory['toys'])
        self.logger.debug("BadDragonApi : InitInventory : Finish {} toys"
                          .format(self.total))

    def get_inventory_page(self, page):
        try:
            response = requests.get("{}inventory-toys?price[min]=0&price[max]=300"
                                    "&sort[field]=price&&sort[direction]=asc&page="
                                    "{}&limit={}".format(BadDragonApi.url_base, page, BadDragonApi.numberByPage))
        except requests.ConnectionError:
            self.logger.error("BadDragonApi : get_inventory_page : ConnectionError")
            return
        except requests.HTTPError:
            self.logger.error("BadDragonApi : get_inventory_page : HTTPError")
            return
        except requests.TooManyRedirects:
            self.logger.error("BadDragonApi : get_inventory_page : TooManyRedirects")
            return
        except requests.URLRequired:
            self.logger.error("BadDragonApi : get_inventory_page : URLRequired")
            return
        except requests.RequestException:
            self.logger.error("BadDragonApi : get_inventory_page : RequestException")
            return
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def get_option_types_values(self):
        try:
            response = requests.get("{}option-types-values".format(BadDragonApi.url_base))
        except requests.ConnectionError:
            self.logger.error("BadDragonApi : get_option_types_values : ConnectionError")
            return
        except requests.HTTPError:
            self.logger.error("BadDragonApi : get_option_types_values : HTTPError")
            return
        except requests.TooManyRedirects:
            self.logger.error("BadDragonApi : get_option_types_values : TooManyRedirects")
            return
        except requests.URLRequired:
            self.logger.error("BadDragonApi : get_option_types_values : URLRequired")
            return
        except requests.RequestException:
            self.logger.error("BadDragonApi : get_option_types_values : RequestException")
            return
        if response.status_code == 200:
            return response.json()
        else:
            return None

    def number_of_toy(self):
        """Return the number of toy for the actual api response."""
        return self.total

    def get_toy(self, index):
        """Return the toy for the given index and api response."""
        if index >= self.total:
            self.logger.error("Can't find {}".format(index))
            return None
        return self.inventory[index]

    def get_product_list(self):
        self.logger.debug("BadDragonApi : getProductList")
        return self.products

    @staticmethod
    def print_data(data):
        """Beautiful print the api response."""
        print("New data :")
        print(json.dumps(data, indent=2, sort_keys=True))
