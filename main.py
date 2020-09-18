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
        if message.mentions == []:
            await message.channel.send(f"{message.author.mention} slapped the air")
        elif message.mentions[0] == message.author:
            await message.channel.send(f"{message.author.mention} slapped themself")
        elif message.mentions[0].id == 756387237796642856:
            await message.channel.send("You cant slap me, I'm unslapable!")
        elif message.mentions[0] != message.author and message.mentions != [] and message.mentions[0].id != 756387237796642856:
            await message.channel.send(f"{message.author.mention} slapped {message.mentions[0].mention}")
    
client.run(token)