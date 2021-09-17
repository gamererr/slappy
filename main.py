from operator import truediv
from asyncio import sleep
import time
import discord
from discord.ext import commands
from discord_slash import SlashCommand, SlashContext
from discord_slash.utils.manage_components import create_button, create_actionrow, wait_for_component, ComponentContext, create_select_option, create_select
from discord_slash.utils.manage_commands import create_permission
from discord_slash.model import ButtonStyle, SlashCommandPermissionType

import random
import json

intents = discord.Intents.all()
client = commands.Bot(intents=intents, command_prefix="eat my nuts")
slash = SlashCommand(client, sync_commands=True,debug_guild=766848554899079218)

async def saveslapstats(saved, slappednum, slapnum):

    statslappedfile = open("statslapped.json", "rt")
    statslapped = json.loads(statslappedfile.read())
    statslappedfile.close()

    statslapfile = open("statslap.json", "rt")
    statslap = json.loads(statslapfile.read())
    statslapfile.close()

    precountslaps = 0
    for id in statslap:
        precountslaps += statslap[id]

    id = str(saved.id)


    try:
        statslapped[id] += slappednum
        statslap[id] += slapnum
    except KeyError:

        statslapped[id] = 0
        statslap[id] = 0

        statslapped[id] += slappednum
        statslap[id] += slapnum

    statslapfile = open("statslap.json", "wt")
    statslapfile.write(json.dumps(statslap))
    statslapfile.close()

    statslappedfile = open("statslapped.json", "wt")
    statslappedfile.write(json.dumps(statslapped))
    statslappedfile.close()

    totalslaps = 0
    for id in statslap:
        totalslaps += statslap[id]

async def getstats(user):
    if user == client.user:
        stats = {}
        stats['slaps'] = 0
        stats['members'] = 0

        with open("statslapped.json","r") as file:
            slaps = json.loads(file.read())

        for x in slaps:
            stats['slaps'] += slaps[x]

        for x in client.guilds:
            stats['members'] += len(x.members)

        return stats
    else:
        id = str(user.id)

        try:
            with open("statslapped.json","r") as file:
                slapped = json.loads(file.read())
                slapped = slapped[id]
            with open("statslap.json","r") as file:
                slaps = json.loads(file.read())
                slaps = slaps[id]
        except KeyError:
            return {}

        stats = {}
        stats['slapped'] = slapped
        stats['slaps'] = slaps

        return stats

@slash.slash()
async def slap(ctx, user:discord.Member):
    slapper = ctx.author

    await ctx.send(f"{slapper.display_name} slapped {user.mention}")

    await saveslapstats(saved=user, slappednum=1, slapnum=0)
    await saveslapstats(saved=slapper, slappednum=0, slapnum=1)

@slash.slash()
async def stats(ctx, user:discord.Member = None):
    if user is None:
        user = ctx.author
    
    stats = await getstats(user)

    if user == client.user:
        await ctx.send(f"we have {stats['slaps']} total slaps\nwe are in {len(client.guilds)} servers\nthere are {stats['members']} people slapping")
    else:
        try:
            await ctx.send(f"{user.display_name}'s stats are\nSlaps Dealt: `{stats['slaps']}`\nSlaps Recieved: `{stats['slapped']}`")
        except KeyError:
            await ctx.send(f"{user.display_name} has no stats. What a Nerd:tm:!")

@slash.slash()
async def bug(ctx, bug):
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send("reported!", hidden=True)
    await channel.send(f"bug from {ctx.author} in {ctx.guild}:\n`{bug}`")

@slash.slash()
async def suggestion(ctx, suggestion):
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send("suggested!", hidden=True)
    await channel.send(f"suggestion from {ctx.author} in {ctx.guild}:\n`{suggestion}`")

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

client.run(token)