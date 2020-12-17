import os
import discord
from discord.ext import commands
import random
import games


PREFIX = '**'
BOT_TOKEN = os.getenv('BOT_TOKEN')

client = commands.Bot(command_prefix=PREFIX, case_insensitive=True, activity=discord.Activity(name="over the Coffee Shop", type=discord.ActivityType.watching))
client.remove_command("help")


bot_colour = 0x00effe

def simple_embed(description):
    return discord.Embed(colour=bot_colour, description=description)


@client.command()
async def gamers(ctx, got : int):

    available = []
    for (game, players) in games.games.items():
        if got in range(players[0], players[1]+1):
            available.append(game)

    found = len(available)
    half = int(found / 2)

    if found % 2 == 1:
        half = half+1

    first_half = "\n".join([ f"• {game}" for game in available[:half]])
    second_half = "\n".join([ f"• {game}" for game in available[half:]])\

    if found == 0:
        return await ctx.send(embed=simple_embed(f"{ctx.author.mention} There are no games found with this player count"))

    result = random.choice(available)
    
    embed = discord.Embed(colour=bot_colour, title=f"{result}\n\u200b")
    embed.set_author(name="Game Picked:", icon_url=client.user.avatar_url)
    embed.add_field(name=f"__Available Games__‎ ‎‎({found})‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ", value=first_half, inline=True)
    if len(second_half) != 0:
        embed.add_field(name="‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎  ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎ ‎‎ ‎ ‎ ", value=second_half, inline=True)

    await ctx.send(embed=embed)


@gamers.error
async def gamers_error(ctx, error):
    if isinstance(error, commands.MissingRequiredArgument):
        return await ctx.send(embed=simple_embed(f"{ctx.author.mention} You must enter the number of players\nEg: {ctx.prefix}{ctx.command.name} 5"))
    elif isinstance(error, commands.BadArgument):
        return await ctx.send(embed=simple_embed(f"{ctx.author.mention} The number of players must be a positive integer"))
    else:
        return await ctx.send(embed=simple_embed(f"{ctx.author.mention} Unexpected Error! CALL THE POOP POLICE! 🚨"))


client.run(BOT_TOKEN)