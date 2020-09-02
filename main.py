#! /usr/bin/env python3
# coding: utf-8
"""Bot that scan clearance toy from bad-dragon and send notification to user with filtering."""
import configparser
import logging
import sys

from BadDragonClient import BadDragonClient
from discord import Embed
from Statue import Statue

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
ch.setLevel(logging.DEBUG)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - '
                              '%(message)s')
ch.setFormatter(formatter)
logger.addHandler(ch)
handler = logging.FileHandler(filename=config['LOG']['fileName'], encoding='utf-8', mode='a')
handler.setFormatter(logging.Formatter('%(asctime)s:%(levelname)s:%(name)s:'
                                       '%(message)s'))
logger.addHandler(handler)

Data = Statue(database, timeBetweenCall, logger)
Client = BadDragonClient(Data, logger, command_prefix=start)


@Client.command(name='toyList', help="Show all the toy in shop")
async def _list(ctx):
    await Data.UserFilter[ctx.message.author].send_toy_list()
    pass


async def option_help(title, description, source, ctx):
    embed_text = Embed(title=title, description=description)
    temp_text = ""
    for i in source.keys():
        temp_text += "Name: {} Value:{}\n".format(source[i].display_name(), source[i].value())
    embed_text.add_field(name="list", value=temp_text, inline=False)
    await Data.UserFilter[ctx.message.author].send_message(text=None, embed_text=embed_text)


@Client.command(name='toyName', help="Show all toy names")
async def _name_list(ctx):
    for i in Data.Options.ToyNameString.keys():
        await Data.UserFilter[ctx.message.author].send_message(text=None, embed_text=Data.Options.ToyNameString[i])
    pass


@Client.command(name='toyType', help="Show all toy Types")
async def _type_list(ctx):
    await option_help("Type List", "List of all toy type", Data.Options.TypeValues, ctx)
    pass


@Client.command(name='toySize', help="Show all toy sizes")
async def _size_list(ctx):
    await option_help("Size List", "List of all toy size", Data.Options.SizeOptions, ctx)
    pass


@Client.command(name='toyFirmness', help="Show all toy Firmness")
async def _firmness_list(ctx):
    await option_help("Firmness List", "List of all toy firmness", Data.Options.FirmnessOptions, ctx)
    pass


@Client.command(name='toyFlop', help="Show all toy option for flop")
async def _flop_list(ctx):
    await option_help("Flop List", "List of all flop option", Data.Options.FlopOption, ctx)
    pass


@Client.command(name='sizeComparator', help="Show all toy comparator")
async def _comparator_list(ctx):
    await option_help("Comparator List", "List of all toy comparator", Data.Options.ComparatorOption, ctx)
    pass


@Client.command(name='toyCumTube', help="Show all toy SuctionCup options")
async def _cum_tube_list(ctx):
    await option_help("CumTube List", "List of all toy cumTube options", Data.Options.CumTubValues, ctx)
    pass


@Client.command(name='toySuctionCup', help="Show all SuctionCup options")
async def _suction_cup_list(ctx):
    await option_help("SuctionCup List", "List of all toy SuctionCup options", Data.Options.SuctionCupValues, ctx)
    pass


help_text = "if the help for a give you no option you can enter any value, else you have to pick a option in the" \
            "list\nEx: -N=Medium -s=medium\n" + Data.Parser.get_help()


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
