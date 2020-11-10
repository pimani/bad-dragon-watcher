import time

import client
from argParser import ArgParser
from bddManagement import DatabaseManager
from extract import BadDragonApi
from OptionValues import OptionValues
from toy import Toy


class Statue:

    def __init__(self, database_name, time_between_call, logger):
        self.Database = DatabaseManager(database_name)
        self.TimeBetweenCall = time_between_call
        self.Logger = logger
        self.Options = OptionValues(BadDragonApi(self.Logger))
        self.UserFilter = {}
        self.ToyInShop = {}
        self.Parser = ArgParser(self.Options)
        self.toy_from_database()
        self.TwitterThread = []

    def start(self):
        self.Logger.info('Start get api')

    def add_filter(self, new_filter, user_id):
        new_filter.save_in_database(self.Database, user_id)

    @staticmethod
    def option_from_type(value_id, option_type):
        if value_id in option_type:
            return option_type[value_id]
        return value_id

    def toy_from_database(self):
        """Sync the toy list with the toy in the database."""
        data = self.Database.get_toys()
        self.Logger.debug('Toy in database : {}'.format(data))
        dic = {}
        for toy in data:
            dic[toy[0]] = Toy(
                self.option_from_type(toy[1], self.Options.ProductName),
                self.option_from_type(toy[3], self.Options.ProductType),
                self.option_from_type(toy[2], self.Options.SizeOptions),
                toy[4],
                self.option_from_type(toy[5], self.Options.FirmnessOptions),
                self.option_from_type(toy[6], self.Options.CumTubValues),
                self.option_from_type(toy[7], self.Options.SuctionCupValues),
                self.option_from_type(toy[8], self.Options.FlopOption),
                toy[9], toy[0])
        self.ToyInShop = dic

    def delete_filter(self, user_id, filter_name):
        """Wrap delete a filter kn the database"""
        self.Database.remove_filter(user_id, filter_name)

    async def on_new_toy(self, new_list):
        """Notify all object for the new toy."""
        for user in self.UserFilter:
            await self.UserFilter[user].new_toy(new_list)

    def actualise_toy_name(self):
        # TODO
        """Actualise the toy name list and the help to help find the toy code"""

        self.Parser.set_toy_list(list(self.Options.ProductName.keys()))

    async def actualise_shop(self):
        """Get all toy actually in the shop and compare to the actual."""
        temp = self.get_toy()
        new = []
        for i in temp:
            if i not in self.ToyInShop:
                new.append(temp[i])
        self.ToyInShop = temp
        self.Logger.info("{} new toy and {} in total in shop".format(len(new), len(self.ToyInShop)))
        for_database = []
        actual_time = time.time()
        for i in temp.values():
            for_database.append((i.get_id(),
                                 None if i.get_name() is None else i.get_name().option_id(),
                                 None if i.get_size() is None else i.get_size().option_id(),
                                 None if i.get_type() is None else i.get_type().option_id(),
                                 i.get_color(),
                                 None if i.get_firmness() is None else i.get_firmness().option_id(),
                                 None if i.get_cum_tube() is None else i.get_cum_tube().option_id(),
                                 None if i.get_suction_cup() is None else i.get_suction_cup().option_id(),
                                 None if i.get_flop() is None else i.get_flop().option_id(),
                                 None if i.get_description() is None else i.get_description(),
                                 actual_time))
        self.Database.set_toy(for_database)
        await self.on_new_toy(new)

    def get_toy(self):
        """Get all the actual toy in clearance."""
        self.Logger.debug("Start to get the toys")
        temp = {}
        extract = BadDragonApi(self.Logger)
        self.actualise_toy_name()
        self.Logger.debug("Start to parse the toys")
        for i in range(0, extract.number_of_toy()):
            toy = extract.get_toy(i)
            if toy['sku'].lower() in self.Options.ProductName:
                temp[toy['id']] = Toy(
                    self.option_from_type(toy['sku'], self.Options.ProductName),
                    self.Options.ProductType[toy['sku'].lower()],
                    self.option_from_type(toy['size'], self.Options.SizeOptions),
                    self.option_from_type(toy['colorTheme']['name'] if toy['colorTheme'] else None,
                                          self.Options.ColorOptions),
                    self.option_from_type(toy['firmness'], self.Options.FirmnessOptions),
                    self.option_from_type(toy['cumtube'], self.Options.CumTubValues),
                    self.option_from_type(toy['suction_cup'], self.Options.SuctionCupValues),
                    self.option_from_type(toy['is_flop'], self.Options.FlopOption),
                    toy['external_flop_reason'], toy['id'])
            else:
                self.Logger.warning("Error {} is not in the dictionary".format(toy['sku']))
        self.Logger.info("Get {} toy in stock".format(len(temp)))
        return temp

    def user_in(self, user):
        return user in self.UserFilter

    def add_user(self, user):
        if not self.user_in(user):
            self.UserFilter[user] = client.Client(user, self.Logger, self, self.Parser, self.ToyInShop)

    async def on_tweet(self):
        """When a tweet from bad-dragon is posted."""
        self.Logger.info("New tweet")
        await self.actualise_shop()

    async def on_time(self):
        """When the clock ring."""
        self.Logger.info("On Time Scan")
        await self.actualise_shop()
