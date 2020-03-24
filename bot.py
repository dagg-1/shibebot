import json
from discord.ext import commands

bot = commands.Bot(command_prefix="!", help_command=None)

@bot.event
async def on_ready():
    print(f"Logged on as {bot.user.name}#{bot.user.discriminator}")

@bot.command(aliases=["hello","hi"])
async def helloworld(ctx):
    await ctx.send(f"Hello {ctx.author.name}")

tokensdata = open('./token.json')
tokens = json.load(tokensdata)
bot.run(tokens["Discord Bot Token"])