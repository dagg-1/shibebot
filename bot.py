import json
from discord.ext import commands
import pymongo

configdata = open('./config.json')
config = json.load(configdata)

mongodb = pymongo.MongoClient(host=config["mongodb"]["ip"], port=config["mongodb"]["port"])
shibebot_db = mongodb["ShibeBot"]
prefixes = shibebot_db["prefixes"]
levels = shibebot_db["levels"]

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
        if levels.find({"id": key.id}).count() < 1:
            levels.insert_one({
                "name": key.name,
                "id": key.id
            })
            for userkey in key.members:
                levels.update_one({ "id": key.id },
                    {
                        "$set": {
                            f"{userkey.id}": {
                                "name": userkey.name,
                                "discriminator": userkey.discriminator,
                                "exp": 0,
                                "level": 0 
                            }
                        }
                    }
                )


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

@bot.command(aliases=["rank", "level"])
async def getuserlevel(ctx, *User_Tag):
    if not User_Tag:
        rank = levels.find_one({"id": ctx.guild.id})[f"{ctx.author.id}"]["level"]
        await ctx.send(f"Current rank for **{ctx.author.mention}** is {rank}")
    if User_Tag:
        convertedtag = str("".join(User_Tag))[3:-1]
        try:
            taggeduser = bot.get_user(int(convertedtag))
            rank = levels.find_one({"id": ctx.guild.id})[f"{taggeduser.id}"]["level"]
            await ctx.send(f"Current rank for **{taggeduser.name}** is {rank}")
        except:
            await ctx.send("Invalid user")

@bot.event
async def on_message(message):
    pass

tokensdata = open('./token.json')
tokens = json.load(tokensdata)
bot.run(tokens["bot_token"])