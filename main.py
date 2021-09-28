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
client = commands.Bot(intents=intents, command_prefix="s!")
slash = SlashCommand(client, sync_commands=True)

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

@slash.slash(description="slap someone",name="slap")
async def slapslash(ctx, user:discord.Member):
    slapper = ctx.author

    await ctx.send(f"{slapper.display_name} slapped {user.mention}")

    await saveslapstats(saved=user, slappednum=1, slapnum=0)
    await saveslapstats(saved=slapper, slappednum=0, slapnum=1)

@slash.slash(description="get a user's stats",name="stats")
async def statsslash(ctx, user:discord.Member = None, hidden:bool=False):
    if user is None:
        user = ctx.author
    
    stats = await getstats(user)

    if user == client.user:
        await ctx.send(f"we have {stats['slaps']} total slaps\nwe are in {len(client.guilds)} servers\nthere are {stats['members']} people slapping", hidden=hidden)
    else:
        try:
            await ctx.send(f"{user.display_name}'s stats are\nSlaps Dealt: `{stats['slaps']}`\nSlaps Recieved: `{stats['slapped']}`", hidden=hidden)
        except KeyError:
            await ctx.send(f"{user.display_name} has no stats. What a Nerd:tm:!", hidden=hidden)

@slash.slash(description="report a bug",name="bug")
async def bugslash(ctx, bug, hidden:bool=True):
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send("reported!", hidden=hidden)
    await channel.send(f"bug from {ctx.author} in {ctx.guild}:\n`{bug}`")

@slash.slash(description="suggest a feature",name="suggestion")
async def suggestionslash(ctx, suggestion, hidden:bool=False):
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send("suggested!", hidden=True)
    await channel.send(f"suggestion from {ctx.author} in {ctx.guild}:\n`{suggestion}`", hidden=hidden)

@slash.slash(description="get the bot invite and support server invite",name="invite")
async def inviteslash(ctx, hidden:bool=False):
    await ctx.send("support server: https://discord.gg/HpsDgr9\nbot invite: https://discord.com/api/oauth2/authorize?client_id=798177958686097469&permissions=2048&scope=bot%20applications.commands", hidden=hidden)

@slash.slash(description="see the github repo",name="repo")
async def reposlash(ctx, hidden:bool=False):
    await ctx.send("here is the github repo: https://github.com/gamererr/slappy", hidden=hidden)

@slash.slash(description="get the bot's ping",name="ping")
async def pingslash(ctx, hidden:bool=False):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms', hidden=hidden)

@client.event
async def on_guild_join(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just joined a guild called **{guild.name}** and it has *{len(guild.members)}* members")
    
    for channel in guild.channels:
        try:
            await channel.send("thanks for adding me to your server!")
            break
        except:
            return

@client.event
async def on_guild_remove(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just left a guild called **{guild.name}** and it had *{len(guild.members)}* members")

@client.event
async def on_ready():
    print("hello world")

@client.event
async def on_slash_command(ctx):
    print(ctx.author, "in", ctx.guild, "used", ctx.data['name'])

    with open("statslapped.json", "rt") as statslappedfile:
        statslapped = json.loads(statslappedfile.read())
    with open("statslap.json", "rt") as statslapfile:
        statslap = json.loads(statslapfile.read())

    totalslaps = 0
    totalmembers = 0
    
    for id in statslap:
        totalslaps += statslap[id]
    for server in client.guilds:
        totalmembers += len(server.members)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{totalslaps} slaps, {len(client.guilds)} slapping servers, and {totalmembers} members slapping'))

@client.command(description="slap someone")
async def slap(ctx, *slapped):
    if slapped == ():
        await ctx.send("you need to name something to slap")
        return
    elif ctx.message.mentions == []:
        slapped = " ".join(slapped)
    elif ctx.message.mentions != []:
        slapped = ctx.message.mentions[0]
    slapper = ctx.author

    await ctx.send(f"{slapper.display_name} slapped {slapped}")

    if type(slapped) != str:
        await saveslapstats(saved=slapped, slappednum=1, slapnum=0)
        await saveslapstats(saved=slapper, slappednum=0, slapnum=1)

@client.command(description="get a user's stats")
async def stats(ctx, *user):
    if ctx.message.mentions == []:
        user = ctx.author
    else:
        user = ctx.message.mentions[0]
    
    stats = await getstats(user)

    if user == client.user:
        await ctx.send(f"we have {stats['slaps']} total slaps\nwe are in {len(client.guilds)} servers\nthere are {stats['members']} people slapping")
    else:
        try:
            await ctx.send(f"{user.display_name}'s stats are\nSlaps Dealt: `{stats['slaps']}`\nSlaps Recieved: `{stats['slapped']}`")
        except KeyError:
            await ctx.send(f"{user.display_name} has no stats. What a Nerd:tm:!")

@client.command(description="report a bug")
async def bug(ctx, *bug):
    bug = " ".join(bug)
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send(f"reported `{bug}`!")
    await channel.send(f"bug from {ctx.author} in {ctx.guild}:\n`{bug}`")

@client.command(description="make a suggestion")
async def suggest(ctx, *suggestion):
    suggestion = " ".join(suggestion)
    server = client.get_guild(766848554899079218)
    channel = server.get_channel(820023969834729572)
    await ctx.send(f"reported `{suggestion}`!")
    await channel.send(f"suggestion from {ctx.author} in {ctx.guild}:\n`{suggestion}`")

@client.command(description="get the bot invite and support server invite")
async def invite(ctx):
    await ctx.send("support server: https://discord.gg/HpsDgr9\nbot invite: https://discord.com/api/oauth2/authorize?client_id=798177958686097469&permissions=2048&scope=bot%20applications.commands")

@client.command(description="see the github repo")
async def repo(ctx):
    await ctx.send("here is the github repo: https://github.com/gamererr/slappy")

@client.command(description="get the bot's ping")
async def ping(ctx):
    await ctx.send(f'Pong! {round(client.latency*1000)} ms')


with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

client.run(token)