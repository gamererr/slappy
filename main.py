import discord
import json
import base64

bot = discord.Bot()

with open("tokenfile", "r") as tokenfile:
	token=tokenfile.read()

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
    if user == bot.user:
        stats = {}
        stats['slaps'] = 0
        stats['members'] = 0

        with open("statslapped.json","r") as file:
            slaps = json.loads(file.read())

        for x in slaps:
            stats['slaps'] += slaps[x]

        for x in bot.guilds:
            stats['members'] += x.member_count

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

tokensplit = token.split(".")
id = base64.b64decode(tokensplit[0])
if int(id) == 635956284981772289:
    print("using testing bot")
    guild_ids = [779090503341441054]
else:
    print("not using testing bot")
    guild_ids = None

@bot.event
async def on_ready():
    print("Hello World!")

@bot.slash_command(description="slap someone", guild_ids=guild_ids)
async def slap(ctx, user:discord.Member=None, slapped:str=None):
    print(guild_ids)
    if slapped != None and user != None:
        await ctx.respond("please only name one thing to slap",ephemeral=True)
    elif slapped == None and user != None:
        if user == bot.user:
            await ctx.respond("you cant slap me, im unslappable!",ephemeral=True)
            return
        slapper = ctx.author

        await ctx.respond(f"{slapper.display_name} slapped {user.mention}")

        await saveslapstats(saved=user, slappednum=1, slapnum=0)
        await saveslapstats(saved=slapper, slappednum=0, slapnum=1)
    elif user == None and slapped != None:

        slapper = ctx.author

        await ctx.respond(f"{slapper.display_name} slapped {slapped}")
    else:
        await ctx.respond("you need to give me something for you to slap", ephemeral=True)

@bot.slash_command(description="get a user's stats", guild_ids=guild_ids)
async def stats(ctx, user:discord.Member = None, hidden:bool=False):
    if user is None:
        user = ctx.author
    
    stats = await getstats(user)

    if user == bot.user:
        await ctx.respond(f"we have {stats['slaps']} total slaps\nwe are in {len(bot.guilds)} servers\nthere are {stats['members']} people slapping", ephemeral=hidden)
    else:
        try:
            await ctx.respond(f"{user.display_name}'s stats are\nSlaps Dealt: `{stats['slaps']}`\nSlaps Recieved: `{stats['slapped']}`", ephemeral=hidden)
        except KeyError:
            await ctx.respond(f"{user.display_name} has no stats. What a Nerd:tm:!", ephemeral=hidden)

@bot.slash_command(description="report a bug in the bot. NOT CONNECTED TO THE SERVER", guild_ids=guild_ids)
async def bug(ctx, bug:str, hidden:bool=True):
    server = bot.get_guild(987579392479858780)
    channel = server.get_channel(1023740794064097410)
    await ctx.respond("reported!", ephemeral=hidden)
    await channel.send(f"bug from {ctx.author} in {ctx.guild}:\n`{bug}`")

@bot.slash_command(description="suggest a feature for the bot. NOT CONNECTED TO THE SERVER", guild_ids=guild_ids)
async def suggestion(ctx, item:str, hidden:bool=True):
    server = bot.get_guild(987579392479858780)
    channel = server.get_channel(1023740794064097410)
    await ctx.respond("reported!", ephemeral=hidden)
    await channel.send(f"suggestion from {ctx.author} in {ctx.guild}:\n`{bug}`")

@bot.slash_command(desciption="get the bot invite", guild_ids=guild_ids)
async def invite(ctx, hidden:bool=True):
    await ctx.respond("support server: https://discord.gg/HpsDgr9\nbot invite: https://discord.com/api/oauth2/authorize?client_id=798177958686097469&permissions=2048&scope=bot%20applications.commands", ephemeral=hidden)

@bot.slash_command(description="get the link to the github repo", guild_ids=guild_ids)
async def repo(ctx, hidden:bool=True):
    await ctx.respond("here is the github repo: https://github.com/gamererr/slappy", ephemeral=hidden)

@bot.slash_command(description="get the bot's latency", guild_ids=guild_ids)
async def ping(ctx, hidden:bool=True):
    await ctx.respond(f'Pong! {round(bot.latency*1000)} ms', ephemeral=hidden)

bot.run(token)