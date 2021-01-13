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
    
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{totalslaps} slaps, {len(client.guilds)} servers, {totalmembers} slapping"))

@client.event
async def on_message(message):
    
    statslappedfile = open("statslapped.json", "rt")
    statslapped = json.loads(statslappedfile.read())
    statslappedfile.close()

    statslapfile = open("statslap.json", "rt")
    statslap = json.loads(statslapfile.read())
    statslapfile.close()
    
    totalslaps = 0
    totalmembers = 0
    
    for id in statslap:
        totalslaps += statslap[id]
    for server in client.guilds:
        totalmembers += len(server.members)
    
    if message.content.startswith("!"):
        if (message.content[1:6] == "stats"):
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
            
        elif (message.content[1:5] == "slap"):
            slapper = message.author
        
            slapped = message.mentions
        
            if message.mention_everyone:
                await message.channel.send(f"{slapper.name} slapped everyone! what a powermove!")
                await saveslapstats(saved=slapper, slappednum=0, slapnum=len(message.guild.members))

            elif message.mentions == []:
                if (message.content[5:] != ""):
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
                
            await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=f"{totalslaps} slaps, {len(client.guilds)} servers, {totalmembers} slapping"))

client.run(token)