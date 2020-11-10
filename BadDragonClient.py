import configparser

from discord.ext import commands
from discord.ext import tasks

import client
from filter import Filter


config = configparser.ConfigParser()
config.read('conf.ini')

timeBetweenCall = int(config['DEFAULT']['timeBetweenCall'])


class BadDragonClient(commands.Bot):
    """Extended version of Discord Client."""

    def __init__(self, statue, logger, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.Statue = statue
        self.Logger = logger
        self.job.start()

    @tasks.loop(seconds=timeBetweenCall)  # every x times
    async def job(self):
        await self.Statue.on_time()

    @staticmethod
    def option_from_type(value_id, option_type):
        if value_id is None:
            return
        if value_id in option_type:
            return option_type[value_id]
        return None

    def filter_from_database(self):
        data = self.Statue.Database.get_filters()
        self.Logger.debug('Filter in database : {}'.format(data))
        dic = {}
        for old_filter in data:
            user = self.get_user(old_filter[0])
            filter_name = old_filter[1]
            toy_color = old_filter[6]
            toy_name = self.option_from_type(old_filter[2], self.Statue.Options.product_name())
            toy_type = self.option_from_type(old_filter[5], self.Statue.Options.type_option())
            size = self.option_from_type(old_filter[3], self.Statue.Options.size_option())
            comparator = self.option_from_type(old_filter[4], self.Statue.Options.comparator_option())
            firmness = self.option_from_type(old_filter[7], self.Statue.Options.firmness_option())
            cum_tube = self.option_from_type(old_filter[8], self.Statue.Options.cum_tub_option())
            suction_cup = self.option_from_type(old_filter[9], self.Statue.Options.suction_cup_option())
            flop = self.option_from_type(old_filter[10], self.Statue.Options.flop_option())
            new_filter = Filter(filter_name, toy_name, toy_type, size, comparator, toy_color, firmness, cum_tube,
                                suction_cup, flop)
            if user is not None and user in dic:
                dic[user].add_filter(new_filter)
            elif user is not None:
                dic[user] = client.Client(user, self.Logger, self, self.Statue.Parser, self.Statue.ToyInShop)
                dic[user].add_filter(new_filter)
            else:
                self.Logger.debug("user with id:{} don't exist".format(old_filter[0]))
        self.Statue.UserFilter = dic

    async def on_ready(self):
        """When the Client is ready."""
        self.Logger.info('Logged in as')
        self.Logger.info(self.user.name)
        self.Logger.info(self.user.id)
        self.filter_from_database()
        self.Statue.start()

    async def on_message(self, message, **options):
        """When a message is see by the bot."""
        if self.Statue.user_in(message.author) and message.author != self.user:
            await self.process_commands(message)
        elif message.author != self.user:
            self.Statue.add_user(message.author)
            await self.process_commands(message)
