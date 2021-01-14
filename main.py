#!/usr/bin/env python3

import discord
from discord.ext.commands import bot
import json

with open("tokenfile", "r") as tokenfile:
    token=tokenfile.read()

client = discord.Client(intents=discord.Intents().all())

async def saveslapstats(saved, slappednum, slapnum):
    
    statslappedfile = open("statslapped.json", "rt")
    statslapped = json.loads(statslappedfile.read())
    statslappedfile.close()

    statslapfile = open("statslap.json", "rt")
    statslap = json.loads(statslapfile.read())
    statslapfile.close()
    
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
    
@client.event
async def on_ready():
    
    totalslaps = 0
    totalmembers = 0
    
    statslapfile = open("statslap.json", "rt")
    statslap = json.loads(statslapfile.read())
    statslapfile.close()
    
    for id in statslap:
        totalslaps += statslap[id]
    for server in client.guilds:
        totalmembers += len(server.members)
    print(f"we have {totalslaps} total slaps\nwe are in {len(client.guilds)} servers\nthere are {totalmembers} people slapping")
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{totalslaps} slaps, {len(client.guilds)} slapping servers, and {totalmembers} members slapping"))

prefix = "s!"

@client.event
async def on_message(message):

    helpmessage = discord.Embed(title="Commands", colour=discord.Colour(0xd084), description=f"**slap** - Slap Someone. args:\n    {prefix}slap <mention (optional)>\n\n**stats** - Get Stats. args:\n    {prefix}stats <mention (optional)>\n\n**bug** - Report a bug, __not for suggestions__. args:\n    {prefix}bug <report (required)>")

    helpmessage.set_author(name="Help")
    helpmessage.set_footer(text=f"{message.author.name}", icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")
    
    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bug = discord.utils.get(internetfunny.channels, id=782228427880267776)


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
    
    argsraw = message.content.lower().replace(prefix, "")
    args = argsraw.split(" ")

    if message.content.startswith(prefix):
        if (args[0] == "stats"):
            if message.mentions != []:
                StatsOn = message.mentions[0]
            else:
                StatsOn = message.author
            
            if StatsOn == client.user:
                await message.channel.send(f"we have {totalslaps} total slaps\nwe are in {len(client.guilds)} servers\nthere are {totalmembers} people slapping")
                return
            
            try:
                await message.channel.send(f"{StatsOn.name}'s stats are\nSlaps Dealt: `{statslap[str(StatsOn.id)]}`\nSlaps Recieved: `{statslapped[str(StatsOn.id)]}`")
            except KeyError:
                await message.channel.send(f"{StatsOn.name} has no stats. What a Nerd:tm:!")

        elif (args[0] == "slap"):
            slapper = message.author
        
            slapped = message.mentions
        
            if message.mention_everyone:
                await message.channel.send(f"{slapper.name} slapped everyone! what a powermove!")
                await saveslapstats(saved=slapper, slappednum=0, slapnum=len(message.guild.members))

            elif message.mentions == []:
                if (args[1] != ""):
                    await message.channel.send(f"{slapper.name} slapped {message.clean_content[6:]}")
                else:
                    await message.channel.send(f"{slapper.name} slapped the air")

            elif slapped[0] == slapper:
                await message.channel.send(f"{slapper.name} slapped themself")
                await saveslapstats(saved=slapper, slappednum=1, slapnum=1)

            elif slapped[0] == client.user:
                await message.channel.send("You cant slap me, I'm unslapable!")

            else:
                await message.channel.send(f"{slapper.name} slapped {slapped[0].name}")
                await saveslapstats(saved=slapper, slappednum=0, slapnum=1)
                await saveslapstats(saved=slapped[0], slappednum=1, slapnum=0)
                
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{totalslaps} slaps, {len(client.guilds)} slapping servers, and {totalmembers} members slapping"))

        elif (args[0] == "bug"):
            if (message.guild.id == 766848554899079218):
                return
            await message.add_reaction("🎷")
            await message.add_reaction("🐛")
            if (args[1:] == []):
                await message.channel.send(f"bro, you need to say what you are reporting. use {prefix}help to get help")
                return
            await bug.send(f'report from **{message.author.name}** in server **{message.guild.name}**:\n{" ".join(args[1:])}')

        elif (args[0] == "help"):
            await message.channel.send("Heres the list of commands", embed=helpmessage)

client.run(token)