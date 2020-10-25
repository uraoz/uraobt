from discord.ext import commands
import os
import random
import traceback

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    await ctx.send('pong')

@bot.command()
async def roll(ctx, arg):
    mes = ""
    arg = arg.split(sep='d',maxsplit=1)
    for i in range(int(arg[0])):
        mes=mes+str(random.choice(range(int(arg[1])))+1)+" "
    await ctx.send(mes)

@bot.command()
async def shuffle(ctx, arg):
    l=list(range(int(arg)))
    l=random.shuffle(l)
    for i in range(int(arg)):
        await ctx.send(str(l[i])+" ")


@bot.command()
async def choice(ctx, *args):
    await ctx.send(random.choice(args))

@bot.command()
async def vachar(ctx):
    await ctx.send(random.choice(["BRIMSTONE","PHOENIX","SAGE","SOVA","VIPER","CYPHER","REYNA","KILLJOY","BREACH","OMEN","JETT","RAZE","SKYE"]))

@bot.command()
async def apchar(ctx):
    await ctx.send(random.choice(["Bangalore","Bloodhound","Caustic","Crypto","Gibraltar","Lifeline","Loba","Mirage","Octane","Pathfinder","Rampart","Revenant","Wattson","Wraith"]))

bot.run(token)
