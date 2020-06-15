# bad-dragon-watcher

bad-dragon-watcher  is a discord bot created in the idea to allow user to ask to receive
notice when a new toy is add to the clearance with filter.

This tool is in beta as with covid-19 I can't make many test as the shop is always empty.

## Requirements

You need python 3 and some library:

* discord
* request

## Installation

If you don't already have them use [pip](https://pip.pypa.io/en/stable/) to install the
needed library.

```bash
pip install discord requests
```

Then get the code

```bash
git clone https://github.com/pimani/bad-dragon-watcher
```

Modify the config file to add your key at the token line, and adjust the options
,for example.

```ini
[DEFAULT]
#Time between each call to bd api, don't set to low we don't wand to DDoS the api
timeBetweenCall = 120
database = database.db
token = NTYyOTDffGc3OTAwNTAwOT54.fM8C2A.kX2SgfdFgZR3EV7DFoPb7acrMbM
start = !

[LOG]
fileName = bdw.log
```


## Usage

The simplest way to use it is in the background using a tool like pm2, Supervisor or simply
screen.
```bash
screen -S badDiscord
python3 main.py
```
You can then leave using ctrl+a then ctrl+d

The bot check if new toy have been add to the clearance section every x time, by default every 120s
but this value can me modified in the conf.ini file.
When new toy are found, the bot will check every filter for every user and then send a notification
with the definition of the toy to the users.

You can access a help with the help command, by default !help.

## Roadmap

Test the multiple option of filter (aka wait for the end of covid-19 situation
and compulsive purchase finishing in empty store)

Actually tested:

* toy name
* size
* comparator
* condition
* hardness

Everything else can work or not

## Contributing
Pull requests are welcome. For major changes, please open an issue first to discuss what you would like to change.

Please make sure to update tests as appropriate.

## License
[CeCILL](http://cecill.info/licences/Licence_CeCILL_V2.1-en.html) 
(compatible with GNU GPL and the French laws related to copyright usage)