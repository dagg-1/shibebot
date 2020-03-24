import json
from discord.ext import commands
import pymongo

configdata = open('./config.json')
config = json.load(configdata)

mongodb = pymongo.MongoClient(host=config["mongodb"]["ip"], port=config["mongodb"]["port"])
bot = commands.Bot(command_prefix=config["global_prefix"], help_command=None)

mongo = pymongo.MongoClient()

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}#{bot.user.discriminator}")

@bot.command(aliases=["hello","hi"])
async def helloworld(ctx):
    await ctx.send(f"Hello {ctx.author.name}")

tokensdata = open('./token.json')
tokens = json.load(tokensdata)
bot.run(tokens["bot_token"])