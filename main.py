#!/usr/bin/env python3

import discord
from discord.ext.commands import bot
import json
import time

with open("tokenfile", "r") as tokenfile:
    token=tokenfile.read()

async def attachments_to_files(attached,spoiler=False):
	filelist = []
	for i in attached:
		file = await i.to_file()
		filelist.insert(len(filelist),file)
	return filelist

client = discord.Client(intents=discord.Intents().all())

async def saveslapstats(message, saved, slappednum, slapnum, milestone):
    
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

    if totalslaps >= milestone and precountslaps < milestone:
        try:
            print(f"{message.author} dealt the {milestone}th slap on {message.mentions[0]}!")
            await message.channel.send(f"you got the {milestone}th slap! join the support server and the dev will give you a special role!")
        except IndexError:
            print(f"{message.author} dealt the {milestone}th slap on everyone in their server!")
            await message.channel.send(f"you got the {milestone}th slap! join the support server and the dev will give you a special role!")
    
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

milestone = 1500
shadowban = []

@client.event
async def on_message(message):

    prefixesraw = open("prefixes.json", "rt")
    prefixes = json.loads(prefixesraw.read())
    prefixesraw.close()

    try:
        prefix = prefixes[str(message.guild.id)]
    except KeyError:
        prefix = "s!"

    helpmessage = discord.Embed(title="Commands", colour=discord.Colour(0xd084), description=f"**slap** - Slap Someone. use:```{prefix}slap <mention (optional)>```\n**stats** - Get Stats. use:```{prefix}stats <mention (optional)>```\n**bug** - Report a bug, __not for suggestions__. use:```{prefix}bug <report (required)>```\n**suggest** - Make a Suggestion:tm:, __not for bug reports__. use:```{prefix}suggest <suggestion (required)>```\n**invite** - Get an invite to The Server: use:```{prefix}invite```\n**repo** - get a link to the github repo. use:```{prefix}repo```\n**ping** - Get the latency. use:```{prefix}ping```\n**settings** - Change the bot settings. use:```{prefix}settings <prefix/announcement>```")
    helpmessage.set_author(name="Help")
    helpmessage.set_footer(text=f"{message.author.name}", icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")

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

    if message.content.startswith(prefix):

        # Set up

        announcementsraw = open("announcements.json", "rt")
        announcements = json.loads(announcementsraw.read())
        announcementsraw.close()

        helpmessage = discord.Embed(title="Commands", colour=discord.Colour(0xd084), description=f"**slap** - Slap Someone. use:```{prefix}slap <mention (optional)>```\n**stats** - Get Stats. use:```{prefix}stats <mention (optional)>```\n**bug** - Report a bug, __not for suggestions__. use:```{prefix}bug <report (required)>```\n**suggest** - Make a Suggestion:tm:, __not for bug reports__. use:```{prefix}suggest <suggestion (required)>```\n**invite** - Get an invite to The Server: use:```{prefix}invite```\n**repo** - get a link to the github repo. use:```{prefix}repo```\n**ping** - Get the latency. use:```{prefix}ping```\n**settings** - Change the bot settings. use:```{prefix}settings <prefix/announcement>```")
        helpmessage.set_author(name="Help")
        helpmessage.set_footer(text=f"{message.author.name}", icon_url=f"https://cdn.discordapp.com/avatars/{message.author.id}/{message.author.avatar}.png")
    
        internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
        bug = discord.utils.get(internetfunny.channels, id=782228427880267776)

        argsraw = message.clean_content.lower().replace(prefix, "")
        args = argsraw.split(" ")

        # Commands
        if (args[0] == "stats"):
            if message.mentions != []:
                StatsOn = message.mentions[0]
            else:
                StatsOn = message.author
            
            if StatsOn == client.user:
                await message.channel.send(f"we have {totalslaps} total slaps\nwe are in {len(client.guilds)} servers\nthere are {totalmembers} people slapping\n{len(announcements)} servers with announcements enabled")
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
                await saveslapstats(saved=slapper, slappednum=0, slapnum=len(message.guild.members), message=message, milestone=milestone)

            elif message.mentions == []:
                try:
                    if (args[1] != ""):
                        await message.channel.send(f"{slapper.name} slapped {' '.join(args[1:])}")
                except IndexError:
                    await message.channel.send(f"{slapper.name} slapped the air")

            elif slapped[0] == slapper:
                await message.channel.send(f"{slapper.name} slapped themself")
                await saveslapstats(saved=slapper, slappednum=1, slapnum=1, message=message, milestone=milestone)

            elif slapped[0] == client.user:
                await message.channel.send("You cant slap me, I'm unslapable!")

            else:
                await message.channel.send(f"{slapper.name} slapped {slapped[0].name}")
                await saveslapstats(saved=slapper, slappednum=0, slapnum=1, message=message, milestone=milestone)
                await saveslapstats(saved=slapped[0], slappednum=1, slapnum=0, message=message, milestone=milestone)
            

            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{totalslaps} slaps, {len(client.guilds)} slapping servers, and {totalmembers} members slapping'))

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

        elif (args[0] == "help"):
            await message.channel.send("Heres the list of commands", embed=helpmessage)

        elif (args[0] == "ping"):
            before = time.monotonic()
            pingmessage = await message.channel.send("Pong!")
            ping = (time.monotonic() - before) * 1000
            ping = str(ping).split(".")

            await pingmessage.edit(content=f"Pong! `{ping[0]} ms`")

        elif (args[0] == "settings") or (args[0] == "set"):
            
            if (args[1] == "prefix") or (args[1] == "p"):

                if not (message.channel.permissions_for(message.author).manage_guild):
                    await message.channel.send("you dont have the permision to do that")
                    return

                try:
                    prefixes[str(message.guild.id)] = args[2]

                    prefixesraw = open("prefixes.json", "wt")
                    prefixesraw.write(json.dumps(prefixes))
                    prefixesraw.close()

                    await message.channel.send(f"prefix has been changed to {prefixes[str(message.guild.id)]}")
                except IndexError:
                    await message.channel.send(f"server prefix is `{prefix}`")

            if (args[1] == "announcements") or (args[1] == "a"):

                if not (message.channel.permissions_for(message.author).manage_guild):
                    await message.channel.send("you dont have the permision to do that")
                    return
                
                id = str(message.guild.id)
                channelid = message.channel_mentions[0].id

                announcements[id] = channelid

                announcementsraw = open("announcements.json", "wt")
                announcementsraw.write(json.dumps(announcements))
                announcementsraw.close()

                await message.channel.send(f"announcement channel set to <#{channelid}>")

        elif (args[0] == "announce"):
            if (message.author.id != 312292633978339329):
                return
            
            for guild in announcements:
                server = discord.utils.get(client.guilds, id=int(guild))
                channel = discord.utils.get(server.channels, id=announcements[guild])

                argsraw = message.clean_content.replace(prefix, "")
                args = argsraw.split(" ")

                announce = " ".join(args[1:])

                await channel.send(announce, files=await attachments_to_files(message.attachments,True))

    elif (client.user in message.mentions):
        await message.channel.send(f"server prefix is `{prefix}`", embed=helpmessage)

    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f'{totalslaps} slaps, {len(client.guilds)} slapping servers, and {totalmembers} members slapping'))

@client.event
async def on_guild_join(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just joined a guild called **{guild.name}** and it has *{len(guild.members)}* members")
    
    for channel in guild.channels:
        try:
            await channel.send("thanks for adding me to your server! you can use `s!settings announcements <channel mention>` to follow the announcements")
            break
        except:
            print("")

@client.event
async def on_guild_remove(guild):

    internetfunny = discord.utils.get(client.guilds, id=766848554899079218)
    bots = discord.utils.get(internetfunny.channels, id=782228427880267776)

    await bots.send(f"i just left a guild called **{guild.name}** and it had *{len(guild.members)}* members")

    announcementsraw = open("announcements.json", "rt")
    announcements = json.loads(announcementsraw.read())
    announcementsraw.close()

    prefixesraw = open("prefixes.json", "rt")
    prefixes = json.loads(prefixesraw.read())
    prefixesraw.close()

    announcements.pop(str(guild.id))  
    prefixes.pop(str(guild.id))    

    announcementsraw = open("announcements.json", "rt")
    announcementsraw.write(json.dumps(announcements))
    announcementsraw.close()

    prefixesraw = open("prefixes.json", "rt")
    prefixesraw.write(json.dumps(prefixes))
    prefixesraw.close()


client.run(token)