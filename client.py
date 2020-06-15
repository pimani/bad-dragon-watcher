"""Object to represent a discord client (channel or user)."""
import discord
from discord import Embed
from embedlib import long_embed
from filter import Filter


class Client:
    """Object to represent a discord channel."""

    def __init__(self, message_destination, logger, client, parser, toy_dictionary=None):
        """Init function for the object."""
        if toy_dictionary is None:
            toy_dictionary = {}
        self.Filter = {}  # Name of the filter and filter object
        self.ToyInShop = toy_dictionary
        self.Logger = logger
        self.Parser = parser
        self.MessageDestination = message_destination
        self.DiscordClient = client
        self.Tell = False
        self.Logger.info("New Client")

    async def send_message(self, text=None, embed_text=None):
        """Wrap function for the object."""
        if text is not None and embed_text is not None:
            self.Logger.debug("Channel {} send text and embed not specified".format(self.MessageDestination))
            return None
        if text == "":
            self.Logger.debug("Channel {} send text cannot be empty string".format(self.MessageDestination))
            return None
        if text is None and embed_text is None:
            return None
        if text is not None and len(text) > 2000:
            self.Logger.debug("Channel {} send text to long start cutting".format(self.MessageDestination))
            temp_text = text
            while len(temp_text) > 2000:
                self.Logger.debug("Channel {} send text cut".format(self.MessageDestination))
                temp = temp_text[:2000]
                temp_text = temp_text[2000:]
                await self.send_message(text=temp)
            text = temp_text
        try:
            tmp = await self.MessageDestination.send(content=text, embed=embed_text)
            self.Logger.debug("Channel {} send message {} and embed {}".format(self.MessageDestination, text,
                                                                               embed_text))
            return tmp
        except discord.Forbidden as e:
            self.Logger.error("Channel {} Send Forbidden : {}".format(self.MessageDestination, e.args))
        except discord.HTTPException as e:
            self.Logger.error("Channel {} Send HTTPException : {}".format(self.MessageDestination, e.args))
        except discord.InvalidArgument as e:
            self.Logger.error("Channel {} Send InvalidArgument : {}".format(self.MessageDestination, e.args))

    async def edit_message(self, message, text=None, embed_text=None):
        """Wrap function for the object."""
        if text is not None and embed_text is not None:
            self.Logger.debug("Channel {} send text and embed specified".format(self.MessageDestination))
            return None
        if text is None and embed_text is None:
            return None
        if text is not None and len(text) > 2000:
            self.Logger.debug("Channel {} send text to long".format(self.MessageDestination))
            return None
        try:
            tmp = await message.edit(content=text, embed=embed_text)
            self.Logger.debug("Channel {} : edit message {}".format(self.DiscordClient, text))
            return tmp
        except discord.HTTPException as e:
            self.Logger.info("Channel {} Edit HTTPException : {}".format(self.DiscordClient, e.args))
        except discord.InvalidArgument as e:
            self.Logger.error("Channel {} Edit InvalidArgument : {}".format(self.DiscordClient, e.args))
        except discord.DiscordException as e:
            self.Logger.warning("Channel {} : edit message {} fail {}".format(self.DiscordClient, message, e.args))

    async def remove_message(self, message, delay):
        """Wrap function Delete a message."""
        try:
            await message.delete(delay=delay)
        except discord.Forbidden as e:
            self.Logger.info("Channel {} remove Forbidden : {}".format(self.DiscordClient, e.args))
        except discord.NotFound as e:
            self.Logger.info("Channel {} remove NotFound : {}".format(self.DiscordClient, e.args))
        except discord.HTTPException as e:
            self.Logger.info("Channel {} remove HTTPException : {}".format(self.DiscordClient, e.args))

    async def new_toy(self, toy_list):
        """Show the toy_list to the channel."""
        for i in self.Filter:
            temp = ""
            for k in toy_list:
                if self.Filter[i].test_toy(k):
                    temp += k.__str__() + "\n"
            if temp != "":
                await self.send_message(text="New toy with {} : \n".format(str(i))+temp)

    async def new_filter(self, arg_list):
        """Add a new filter to the dictionary with parser value."""
        self.Parser.passe(arg_list)
        if not self.Parser.get_correct():
            await self.send_message(text="Error: {}".format(self.Parser.get_error()))
            return
        name = self.Parser.get_name() if self.Parser.get_name() is not None else "Default"
        toy_name = self.Parser.get_toy_name()
        category = self.Parser.get_type()  # cant use type for variable name
        size = self.Parser.get_size()
        comparator = self.Parser.get_comparator()
        color = self.Parser.get_color()
        firmness = self.Parser.get_firmness()
        cum_tube = self.Parser.get_cum_tube()
        suction_cup = self.Parser.get_suction_cup()
        condition = self.Parser.get_condition()
        new_filter = Filter(name, toy_name, category, size, comparator, color, firmness, cum_tube, suction_cup, condition)
        self.Logger.debug("new filter: {}".format(new_filter))
        if new_filter.get_name() in self.Filter:
            embed_text = Embed(title="Error", description="Filter named already exist")
            embed_text.add_field(name="Response", value="Filter named {} already exist".format(new_filter.get_name()),
                                 inline=False)
            await self.send_message(text=None, embed_text=embed_text)
            return None
        self.Filter[new_filter.get_name()] = new_filter
        return new_filter

    def add_filter(self, new_filter):
        """Add a filter in the list"""
        if new_filter.get_name() in self.Filter:
            self.Logger.warning("add filter: filter with {} name already exist".format(new_filter.get_name()))
            return
        self.Filter[new_filter.get_name()] = new_filter

    async def delete_filter(self, name):
        text = "Can't find filter with name: {}".format(name)
        if name in self.Filter:
            del self.Filter[name]
            text = "Filter {} deleted".format(name)
        embed_text = Embed(title="Filter delete", description="Response")
        embed_text.add_field(name="Response", value=text, inline=False)
        await self.send_message(embed_text=embed_text)

    async def send_toy_list(self):
        """Show all the toy for all the filter."""
        #   text = ""
        #   for k in self.ToyInShop:
        #       text += "{}\n".format(str(self.ToyInShop[k]))
        toy_list = []
        for k in self.ToyInShop:
            toy_list.append(str(self.ToyInShop[k]) + "\n")
        embed_list = long_embed(toy_list, title="List of toy", description="List of toy", fields_title="Part")
        for k in embed_list:
            await self.send_message(text=None, embed_text=k)

    async def send_filter_list(self):
        """Show all the filter of the client."""
        #   text = ""
        #   for k in self.Filter:
        #       text += "{}\n\n".format(self.Filter[k])
        filter_list = []
        for k in self.Filter:
            filter_list.append(str(self.Filter[k]) + "\n")
        embed_list = long_embed(filter_list, title="List of filter", description="List of filter", fields_title="Part")
        for k in embed_list:
            await self.send_message(text=None, embed_text=k)
