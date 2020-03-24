import json
from discord.ext import commands
import pymongo

configdata = open('./config.json')
config = json.load(configdata)

mongodb = pymongo.MongoClient(host=config["mongodb"]["ip"], port=config["mongodb"]["port"])
shibebot_db = mongodb["ShibeBot"]
prefixes = shibebot_db["prefixes"] 

def get_prefix(bot, msg):
    if msg.guild:
        return prefixes.find_one({"id": msg.guild.id})["prefix"]
    else:
        return config["global_prefix"]

bot = commands.Bot(command_prefix=get_prefix, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}#{bot.user.discriminator}")
    for key in bot.guilds:
        if prefixes.find({"id": key.id}).count() < 1:
            prefixes.insert_one({
                "name": key.name,
                "id": key.id,
                "prefix": config["global_prefix"]
            })

@bot.command(aliases=["hello","hi"])
async def helloworld(ctx):
    await ctx.send(f"Hello {ctx.author.name}")

@bot.command(aliases=["spre", "set", "prefix"])
@commands.guild_only()
async def setprefix(ctx, *prefix):
    if not prefix:
        await ctx.send(f"Current prefix for this server is {str(get_prefix(bot, ctx))[2:-2]}")
    else:
        prefixes.update_one({"id" : ctx.guild.id}, {"$set": {"prefix": prefix }})
        await ctx.send(f"New server prefix is {str(get_prefix(bot, ctx))[2:-2]}")

tokensdata = open('./token.json')
tokens = json.load(tokensdata)
bot.run(tokens["bot_token"])