import os
import discord
from discord.ext import commands
import random
import math
import games


PREFIX = '**'
BOT_COLOUR = 0x00effe
BOT_TOKEN = os.getenv('BOT_TOKEN')
BOT_PRESENCE = discord.Activity(name="over the Coffee Shop", type=discord.ActivityType.watching)


client = commands.Bot(command_prefix=PREFIX, case_insensitive=True, activity=BOT_PRESENCE)
client.remove_command("help")


def simple_embed(description):
    return discord.Embed(colour=BOT_COLOUR, description=description)

def list_to_string(items):
    return "\n".join([ f"• {item}" for item in items ])

def space(n = 1):
    magic = "‎ "
    return magic * n


@client.command()
async def gamers(ctx, got : int):

    # Fetch a list of available games matching the given player count
    available = [ game for game, players in games.games.items() if got in range(players[0], players[1]+1) ]
    found = len(available)

    # Return if no games are found
    if found == 0: return await ctx.send(embed=simple_embed(f"{ctx.author.mention} There are no games found with this player count"))

    # Split the available games list into two equal halves
    half = math.ceil(found / 2)
    first_half = list_to_string(available[:half])
    second_half = list_to_string(available[half:])

    # Choose a random game
    result = random.choice(available)

    # Format the discord.Embed    
    embed = discord.Embed(colour=BOT_COLOUR, title=f"{result}\n\u200b")
    embed.set_author(name="Game Picked:", icon_url=client.user.avatar_url)
    embed.add_field(name=f"__Available Games__‎ ‎‎({found}) {space(16)}", value=first_half, inline=True)
    if len(second_half) > 0: embed.add_field(name=space(48), value=second_half, inline=True)

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