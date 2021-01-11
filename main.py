#!/usr/bin/env python3

import discord
from discord.ext.commands import bot

with open("tokenfile", "r") as tokenfile:
    token=tokenfile.read()

client = discord.Client()

@client.event
async def on_ready():
    await client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="the beautiful sound of slaps"))
    print('hello world')

@client.event
async def on_message(message):
    if message.content.startswith("!slap"):
        
        slapper = message.author
        
        slapped = message.mentions
        
        if message.mention_everyone:
            await message.channel.send(f"{slapper.name} slapped everyone! what a powermove!")
        elif message.mentions == []:
            if (message.content[5:] != ""):
                await message.channel.send(f"{slapper.name} slapped {message.content[6:]}")
            else:
                await message.channel.send(f"{slapper.name} slapped the air")
        elif slapped[0] == slapper:
            await message.channel.send(f"{slapper.name} slapped themself")
        elif slapped[0] == client.user:
            await message.channel.send("You cant slap me, I'm unslapable!")
        else:
            await message.channel.send(f"{slapper.name} slapped {slapped[0].name}")
    
client.run(token)