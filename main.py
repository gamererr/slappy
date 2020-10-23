#!/usr/bin/env/str python3

from time import sleep
import discord
from discord.ext.commands import bot
from discord.ext import commands
import asyncio
import random

intents = discord.Intents.all()

with open("tokenfile", "r") as tokenfile:
    token=tokenfile.read()

my_id = 571603546525663234


client = discord.Client(intents=intents)

@client.event
async def on_ready():
    print('hello world')

guncooldown = 0
gundmg = random.randrange(1, 100, 1)
@client.event
async def on_message(message):
    # linking status
    standowner = discord.utils.get(message.guild.members, id = my_id)
    try:
        if standowner.activity.name == "Spotify":
            await client.change_presence(status=standowner.status, activity=discord.Activity(name=standowner.activity.name, type=discord.ActivityType.listening))
    except AttributeError:
        await client.change_presence(status=standowner.status, activity=standowner.activity)
    
    
    async def unvist():
        if not (visitor in message.author.roles or dead_visitor in message.author.roles):
            return
        await message.author.remove_roles(visitor,reason="leaving")
        if dead_visitor in message.author.roles:
            await message.author.remove_roles(dead_visitor,reason="leaving")
            await message.author.add_roles(dead,reason="leaving")
        print('leaving')

    maxhealth = discord.utils.get(message.guild.roles, id = 714534974916919349)
    health9 = discord.utils.get(message.guild.roles, id = 714535185273847871)
    health8 = discord.utils.get(message.guild.roles, id = 714535298729640047)
    health7 = discord.utils.get(message.guild.roles, id = 714535324759621712)
    health6 = discord.utils.get(message.guild.roles, id = 714535348046266449)
    health5 = discord.utils.get(message.guild.roles, id = 714535379675644054)
    health4 = discord.utils.get(message.guild.roles, id = 714535405843775518)
    health3 = discord.utils.get(message.guild.roles, id = 714535436143558788)
    health2 = discord.utils.get(message.guild.roles, id = 714535460860330066)
    health1 = discord.utils.get(message.guild.roles, id = 714535481928319016)
    dead = discord.utils.get(message.guild.roles, id = 714535509279637525)
    visitor = discord.utils.get(message.guild.roles, id = 737149499364999179)
    dead_visitor = discord.utils.get(message.guild.roles, id = 747460046333673573)
    
    if message.author == client.user:
        return

    if message.content.startswith('Unfortunate attack'):
        if not (message.author.id == my_id):
            return
        await message.channel.send('Dorarararararararararararrarara')
        print(f'attacking {message.mentions[0]}')

    # Reality shift code
    if message.content.startswith('Unfortuante take me away'):
        if message.author.id != my_id:
            return
        if not dead in message.author.roles:
            await message.author.add_roles(visitor,reason="crossed over to dead realm")
            print('crossing over to dead realm')
            await asyncio.sleep(60)
        else:
            await message.author.add_roles(dead_visitor,reason="crossed over to living realm")
            await message.author.remove_roles(dead,reason="crossed over to living realm")
            print('crossing over to living realm')
            await asyncio.sleep(60)
        await unvist()
    if message.content.startswith('Unfortunate, Arival'):
        if message.author.id != my_id:
            return
        await unvist()
    
    # wild shot code
    global gundmg
    global guncooldown
    if message.content.startswith('Unfortunate Wild shot'):
        if guncooldown == 1:
            return
        if not (message.author.id == my_id):
            return
        gundmg = random.randrange(1, 100, 1)
        if message.author.id == message.mentions[0].id:
            gundmg = random.randrange(95, 96, 1)
        if gundmg in range(1, 50): #1 damage
            gundmg = 1
            if (maxhealth in message.mentions[0].roles):
                await message.mentions[0].remove_roles(maxhealth,reason="damaged")
                await message.mentions[0].add_roles(health9,reason="damaged")
            elif (health9 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health9,reason="damaged")
                await message.mentions[0].add_roles(health8,reason="damaged")
            elif (health8 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health8,reason="damaged")
                await message.mentions[0].add_roles(health7,reason="damaged")
            elif (health7 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health7,reason="damaged")
                await message.mentions[0].add_roles(health6,reason="damaged")
            elif (health6 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health6,reason="damaged")
                await message.mentions[0].add_roles(health5,reason="damaged")
            elif (health5 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health5,reason="damaged")
                await message.mentions[0].add_roles(health4,reason="damaged")
            elif (health4 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health4,reason="damaged")
                await message.mentions[0].add_roles(health3,reason="damaged")
            elif (health3 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health3,reason="damaged")
                await message.mentions[0].add_roles(health2,reason="damaged")
            elif (health2 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health2,reason="damaged")
                await message.mentions[0].add_roles(health1,reason="damaged")
            elif (health1 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health1,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
        if gundmg in range(51, 75): #2 damage
            gundmg = 2
            if (maxhealth in message.mentions[0].roles):
                await message.mentions[0].remove_roles(maxhealth,reason="damaged")
                await message.mentions[0].add_roles(health8,reason="damaged")
            elif (health9 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health9,reason="damaged")
                await message.mentions[0].add_roles(health7,reason="damaged")
            elif (health8 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health8,reason="damaged")
                await message.mentions[0].add_roles(health6,reason="damaged")
            elif (health7 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health7,reason="damaged")
                await message.mentions[0].add_roles(health5,reason="damaged")
            elif (health6 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health6,reason="damaged")
                await message.mentions[0].add_roles(health4,reason="damaged")
            elif (health5 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health5,reason="damaged")
                await message.mentions[0].add_roles(health3,reason="damaged")
            elif (health4 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health4,reason="damaged")
                await message.mentions[0].add_roles(health2,reason="damaged")
            elif (health3 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health3,reason="damaged")
                await message.mentions[0].add_roles(health1,reason="damaged")
            elif (health2 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health2,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health1 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health1,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
        if gundmg in range(76, 85): #3 damage
            gundmg = 3
            if (maxhealth in message.mentions[0].roles):
                await message.mentions[0].remove_roles(maxhealth,reason="damaged")
                await message.mentions[0].add_roles(health7,reason="damaged")
            elif (health9 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health9,reason="damaged")
                await message.mentions[0].add_roles(health6,reason="damaged")
            elif (health8 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health8,reason="damaged")
                await message.mentions[0].add_roles(health5,reason="damaged")
            elif (health7 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health7,reason="damaged")
                await message.mentions[0].add_roles(health4,reason="damaged")
            elif (health6 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health6,reason="damaged")
                await message.mentions[0].add_roles(health3,reason="damaged")
            elif (health5 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health5,reason="damaged")
                await message.mentions[0].add_roles(health2,reason="damaged")
            elif (health4 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health4,reason="damaged")
                await message.mentions[0].add_roles(health1,reason="damaged")
            elif (health3 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health3,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health2 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health2,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health1 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health1,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
        if gundmg in range(86, 91): #4 damage
            gundmg = 4
            if (maxhealth in message.mentions[0].roles):
                await message.mentions[0].remove_roles(maxhealth,reason="damaged")
                await message.mentions[0].add_roles(health6,reason="damaged")
            elif (health9 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health9,reason="damaged")
                await message.mentions[0].add_roles(health5,reason="damaged")
            elif (health8 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health8,reason="damaged")
                await message.mentions[0].add_roles(health4,reason="damaged")
            elif (health7 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health7,reason="damaged")
                await message.mentions[0].add_roles(health3,reason="damaged")
            elif (health6 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health6,reason="damaged")
                await message.mentions[0].add_roles(health2,reason="damaged")
            elif (health5 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health5,reason="damaged")
                await message.mentions[0].add_roles(health1,reason="damaged")
            elif (health4 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health4,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health3 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health3,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health2 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health2,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
            elif (health1 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health1,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
        if gundmg in range(92, 94): #5 damage
            gundmg = 5
            if (maxhealth in message.mentions[0].roles):
                await message.mentions[0].remove_roles(maxhealth,reason="damaged")
                await message.mentions[0].add_roles(health5,reason="damaged")
            elif (health9 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health9,reason="damaged")
                await message.mentions[0].add_roles(health4,reason="damaged")
            elif (health8 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health8,reason="damaged")
                await message.mentions[0].add_roles(health3,reason="damaged")
            elif (health7 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health7,reason="damaged")
                await message.mentions[0].add_roles(health2,reason="damaged")
                
            elif (health6 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health6,reason="damaged")
                await message.mentions[0].add_roles(health1,reason="damaged")
                
            elif (health5 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health5,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
                
            elif (health4 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health4,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
                
            elif (health3 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health3,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
                
            elif (health2 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health2,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")
                
            elif (health1 in message.mentions[0].roles):
                await message.mentions[0].remove_roles(health1,reason="killed")
                await message.mentions[0].add_roles(dead,reason="killed")        
        if gundmg in range(95, 100):
            gundmg = 0
            await message.channel.send("damnit, its a dud")
        if gundmg != 0:
            await message.channel.send(f"you did {gundmg} damage")
        print(f"using wild shot to attack {message.mentions[0].name} for {gundmg} damage")
        guncooldown = 1
        await asyncio.sleep(35)
        guncooldown = 0

        
@client.event
async def on_member_update(before, after):
    if after.id == my_id:
        try:
            if after.activity.name == "Spotify":
                await client.change_presence(status=after.status, activity=discord.Activity(name=after.activity.name, type=discord.ActivityType.listening))
        except AttributeError:
            await client.change_presence(status=after.status, activity=after.activity)

client.run(token)