#!/usr/bin/env python3

import discord
from discord.ext.commands import bot
import json
import time

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

shadowban = [431978032094380043]

@client.event
async def on_message(message):

    prefixesraw = open("prefixes.json", "rt")
    prefixes = json.loads(prefixesraw.read())
    prefixesraw.close()

    try:
        prefix = prefixes[str(message.guild.id)]
    except KeyError:
        prefix = "s!"

    helpmessage = discord.Embed(title="Commands", colour=discord.Colour(0xd084), description=f"**slap** - Slap Someone. use:```{prefix}slap <mention (optional)>```\n**stats** - Get Stats. use:```{prefix}stats <mention (optional)>```\n**bug** - Report a bug, __not for suggestions__. use:```{prefix}bug <report (required)>```\n**suggest** - Make a Suggestion:tm:, __not for bug reports__. use:```{prefix}suggest <suggestion (required)>```\n**invite** - Get an invite to The Server: use:```{prefix}invite```\n**prefix** - Change the server prefix. use:```{prefix}prefix <prefix to chage to - optional>```\n**repo** - get a link to the github repo. use:```{prefix}repo```\n**ping** - Get the latency. use:```{prefix}ping```")

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
    
    argsraw = message.clean_content.lower().replace(prefix, "")
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
                try:
                    if (args[1] != ""):
                        await message.channel.send(f"{slapper.name} slapped {' '.join(args[1:])}")
                except IndexError:
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
            if (message.author.id in shadowban):
                await message.channel.send(f"im sorry, but because you have spammed the suggestion and bug report commands with annoying nonsense, you have been ban from making bug reports and suggestions through the bot. you may continue using the bot's other features, just not this one. you may join the support server (get invite with {prefix}invite) to make suggestions less-anonymously.")
                return
            await message.add_reaction("🎷")
            await message.add_reaction("🐛")
            if (args[1:] == []):
                await message.channel.send(f"bro, you need to say what you are reporting. use {prefix}help to get help")
                return
            await bug.send(f'report from **{message.author.name}** in server **{message.guild.name}**:\n{" ".join(args[1:])}')
            await message.channel.send("just a friendly reminder not to shitpost into the suggestion and bug report commands as it is very annoying")
                           
        elif (args[0] == "suggest"):
            if (message.guild.id == 766848554899079218):
                return
            if (message.author.id in shadowban):
                await message.channel.send(f"im sorry, but because you have spammed the suggestion and bug report commands with annoying nonsense, you have been ban from making bug reports and suggestions through the bot.\n\nyou may continue using the bot's other features, just not this one. you may join the support server to make suggestions less-anonymously.")
                return
            await message.add_reaction("🎷")
            await message.add_reaction("🐛")
            if (args[1:] == []):
                await message.channel.send(f"bro, you need to say what you are suggesting. use {prefix}help to get help")
                return
            await bug.send(f'suggestion from **{message.author.name}** in server **{message.guild.name}**:\n{" ".join(args[1:])}')
            await message.channel.send("just a friendly reminder not to shitpost into the suggestion and bug report commands as it is very annoying")

        elif (args[0] == "invite"):
            await message.channel.send("support server: https://discord.gg/HpsDgr9\nbot invite: https://discord.com/api/oauth2/authorize?client_id=798177958686097469&permissions=2048&scope=bot")

        elif (args[0] == "repo"):
            await message.channel.send("here is the github repo: https://github.com/gamererr/slappy")

        elif (args[0] == "prefix"):
            try:
               prefixes[str(message.guild.id)] = args[1]

               prefixesraw = open("prefixes.json", "wt")
               prefixesraw.write(json.dumps(prefixes))
               prefixesraw.close()

               await message.channel.send(f"prefix has been changed to {prefixes[str(message.guild.id)]}")
            except IndexError:
                await message.channel.send(f"server prefix is `{prefix}`")

        elif (args[0] == "help"):
            await message.channel.send("Heres the list of commands", embed=helpmessage)

        elif (args[0] == "ping"):
            before = time.monotonic()
            pingmessage = await message.channel.send("Pong!")
            ping = (time.monotonic() - before) * 1000
            ping = str(ping).split(".")

            await pingmessage.edit(content=f"Pong! `{ping[0]} ms`")

    elif (client.user in message.mentions):
        await message.channel.send(f"server prefix is `{prefix}`", embed=helpmessage)

@client.event
async def on_guild_join(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just joined a guild called **{guild.name}** and it has *{len(guild.members)}* members")

@client.event
async def on_guild_remove(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just left a guild called **{guild.name}** and it had *{len(guild.members)}* members")


client.run(token)