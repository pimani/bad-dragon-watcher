#! /usr/bin/env python3
# coding: utf-8
"""Bot that scan clearence toy from bad-dragon and send notification to user with filtering."""
import asyncio
import configparser
import logging
import sys
import time
from threading import Thread

import client
from argParser import ArgParser
from bddManagement import DatabaseManager
from discord import Embed
from discord.ext import commands
from extract import BadDragonApi
from filter import Filter
from timer import check_call
from toy import Toy

config = configparser.ConfigParser()
config.read('conf.ini')

timeBetweenCall = int(config['DEFAULT']['timeBetweenCall'])
database = config['DEFAULT']['database']
token = config['DEFAULT']['token']
start = config['DEFAULT']['start']

# Configure
logger = logging.getLogger(__name__)
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
handler = logging.FileHandler(filename=config['LOG']['fileName'], encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:'
                                       '%(message)s'))
logger.addHandler(handler)


class Statue:

    def __init__(self):
        self.Database = DatabaseManager(database)
        self.ToyType = {}
        self.ToyName = {}
        self.ToyNameString = {}
        self.UserFilter = {}
        self.ToyInShop = {}
        self.Parser = ArgParser(list(self.ToyName.keys()))
        self.toy_from_database()
        self.TwitterThread = []
        self.TimerThread = Thread(target=check_call, args=(timeBetweenCall, self, asyncio.get_event_loop()))
        self.TimerThread.daemon = True
        self.TimerThread.start()

    def add_filter(self, new_filter, user_id):
        self.Database.add_filter((user_id, new_filter.get_name(), new_filter.get_toy_name(), new_filter.get_size(),
                                  new_filter.get_comparator(), new_filter.get_type(), new_filter.get_color(),
                                  new_filter.get_firmness(), new_filter.get_cum_tube(), new_filter.get_suction_cup(),
                                  new_filter.get_condition(), ""))

    def toy_from_database(self):
        """Sync the toy list with the toy in the database."""
        data = self.Database.get_toys()
        logger.debug('Toy in database : {}'.format(data))
        dic = {}
        for toy in data:
            dic[toy[0]] = Toy(
                toy[1], toy[3],
                toy[2], toy[4], toy[5],
                toy[6], toy[7],
                toy[8], toy[9], toy[0])
        self.ToyInShop = dic

    def delete_filter(self, user_id, filter_name):
        """Wrap delete a filter kn the database"""
        self.Database.remove_filter(user_id, filter_name)

    async def on_new_toy(self, new_list):
        """Notify all object for the new toy."""
        for user in self.UserFilter:
            await self.UserFilter[user].new_toy(new_list)

    def actualise_toy_name(self, product):
        """Actualise the toy name list and the help to help find the toy code"""
        self.ToyNameString = {}
        for k in product:
            logger.debug('{} {}'.format(k['sku'], k['type']))
            self.ToyName[k['sku']] = k['name']
            self.ToyType[k['sku']] = k['type']
            if k['type'] in self.ToyNameString:
                text_list = self.ToyNameString[k['type']]
                if len(text_list[-1] + "{} : {}\n".format(k['name'], k['sku'])) > 1024:
                    text_list.append("{} : {}\n".format(k['name'], k['sku']))
                else:
                    text_list[-1] += "{} : {}\n".format(k['name'], k['sku'])
            else:
                self.ToyNameString[k['type']] = ["{} : {}\n".format(k['name'], k['sku'])]
        for i in self.ToyNameString.keys():
            embed_text = Embed(title="{} toy:".format(i), description="list of {} type of toy".format(i))
            part_number = 0
            for k in self.ToyNameString[i]:
                embed_text.add_field(name="List Part {}".format(part_number), value=k, inline=False)
                part_number += 1
            self.ToyNameString[i] = embed_text
        self.Parser.set_toy_list(list(self.ToyName.keys()))

    async def actualise_shop(self):
        """Get all toy actually in the shop and compare to the actual."""
        temp = self.get_toy()
        new = []
        for i in temp:
            if i not in self.ToyInShop:
                new.append(temp[i])
                logger.info(temp[i])
        logger.info("{} new toy".format(len(new)))
        self.ToyInShop = temp
        for_database = []
        actual_time = time.time()
        for i in temp.values():
            for_database.append((i.get_id(), i.get_name(), i.get_size(), i.get_type(),
                                 i.get_color(), i.get_firmness(), i.get_cum_tube(),
                                 i.get_suction_cup(), i.get_condition(), i.get_description(),
                                 actual_time))
        self.Database.set_toy(for_database)
        await self.on_new_toy(new)

    def get_toy(self):
        """Get all the actual toy in clearance."""
        temp = {}
        extract = BadDragonApi(logger)
        product = extract.get_product_list()
        self.actualise_toy_name(product)
        for i in range(0, extract.number_of_toy()):
            toy = extract.get_toy(i)
            if toy['sku'].lower() in self.ToyName:
                temp[toy['id']] = Toy(
                    toy['sku'], self.ToyType[toy['sku'].lower()],
                    toy['size'], toy['color'], toy['firmness'],
                    toy['cumtube'], toy['suction_cup'],
                    toy['type'], toy['flop_reason'], toy['id'])
            else:
                logger.debug("Error {} is not in the dictionary"
                             .format(toy['sku']))
                temp[toy['id']] = Toy(
                    toy['sku'], 'unknown',
                    toy['size'], toy['color'], toy['firmness'],
                    toy['cumtube'], toy['suction_cup'],
                    toy['type'], toy['flop_reason'], toy['id'])
        logger.info("Get {} toy in sold".format(len(temp)))
        return temp

    def user_in(self, user):
        return user in self.UserFilter

    def add_user(self, user):
        if not self.user_in(user):
            self.UserFilter[user] = client.Client(user, logger, self, self.Parser, self.ToyInShop)

    async def on_tweet(self):
        """When a tweet from bad-dragon is posted."""
        logger.info("New tweet")
        await self.actualise_shop()

    async def on_time(self):
        """When the clock ring."""
        logger.info("On Time Scan")
        await self.actualise_shop()


class BadDragonClient(commands.Bot):
    """Extended version of Discord Client."""

    def __init__(self, statue, *, loop=None, **options):
        super().__init__(loop=loop, **options)
        self.Statue = statue

    def filter_from_database(self):
        data = self.Statue.Database.get_filters()
        logger.debug('Filter in database : {}'.format(data))
        dic = {}
        for old_filter in data:
            user = self.get_user(old_filter[0])
            new_filter = Filter(old_filter[1], old_filter[2], old_filter[5], old_filter[3], old_filter[4],
                                old_filter[6], old_filter[7], old_filter[8], old_filter[9], old_filter[10])
            if user is not None and user in dic:
                dic[user].add_filter(new_filter)
            elif user is not None:
                dic[user] = client.Client(user, logger, self, self.Statue.Parser, self.Statue.ToyInShop)
                dic[user].add_filter(new_filter)
            else:
                logger.debug("user with id:{} don't exist".format(old_filter[0]))
        self.Statue.UserFilter = dic

    async def on_ready(self):
        """When the Client is ready."""
        logger.info('Logged in as')
        logger.info(self.user.name)
        logger.info(self.user.id)
        self.filter_from_database()

    async def on_message(self, message, **options):
        """When a message is see by the bot."""
        if self.Statue.user_in(message.author) and message.author != self.user:
            await self.process_commands(message)
        elif message.author != self.user:
            self.Statue.add_user(message.author)
            await self.process_commands(message)


Data = Statue()
help_text = "if no value you can enter whatever you want\n" \
                 "Ex: -N=Medium -s=medium\n" + Data.Parser.get_help()
Client = BadDragonClient(Data, command_prefix=start)


@Client.command(name='toyList', help="Show all the toy in shop")
async def _list(ctx):
    await Data.UserFilter[ctx.message.author].send_toy_list()
    pass


@Client.command(name='toyName', help="Show all toy name")
async def _toy_list(ctx):
    for i in Data.ToyNameString.keys():
        await Data.UserFilter[ctx.message.author].send_message(text=None, embed_text=Data.ToyNameString[i])
    pass


@Client.command(name='filter', brief="Create a filter", help=help_text)
async def _filter(ctx, *args):
    new_filter = await Data.UserFilter[ctx.message.author].new_filter(args)
    if new_filter is not None:
        Data.add_filter(new_filter, ctx.message.author.id)
    pass


@Client.command(name='deleteFilter', brief="deleteFilter a filter", help='ex: "!deleteFilter Medium" delete the filter'
                                                                         ' named Medium')
async def _delete_filter(ctx, arg):
    await Data.UserFilter[ctx.message.author].delete_filter(arg)
    Data.delete_filter(ctx.message.author.id, arg)
    pass


@Client.command(name='filterList', help="Show all your filter")
async def _filter_list(ctx):
    await Data.UserFilter[ctx.message.author].send_filter_list()
    pass


@Client.command(name='testToy', help="Test all the toy in shop with all your filter")
async def _test_toy(ctx):
    await Data.UserFilter[ctx.message.author].new_toy(list(Data.ToyInShop.values()))
    pass


if __name__ == "__main__":
    if config['DEFAULT']['token'] == "default":
        logger.error("Please enter a token in the conf.ini file")
        sys.exit()
    Client.run(token)
