from discord.ext import commands
import os
import discord
import random
import traceback
import time

bot = commands.Bot(command_prefix='/')
token = os.environ['DISCORD_BOT_TOKEN']

@bot.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, "original", error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@bot.command()
async def ping(ctx):
    """ping"""
    await ctx.send(str(round(bot.latency, 2)))

@bot.command()
async def roll(ctx, arg):
    """NdNを引数とする"""
    mes = ""
    arg = arg.split(sep='d',maxsplit=1)
    for i in range(int(arg[0])):
        mes=mes+str(random.choice(range(int(arg[1])))+1)+" "
    await ctx.send(mes)

@bot.command()
async def shuffle(ctx, arg):
    """N番までの値を入れ替える"""
    l=list(range(int(arg)))
    random.shuffle(l)
    mes=""
    for i in range(int(arg)):
        mes=mes+str(l[i]+1)+" "
    await ctx.send(mes)

@bot.command()
async def shufflist(ctx, *args):
    """N個の引数を入れ替える"""
    args=list(args)
    random.shuffle(args)
    await ctx.send(' '.join(args))

@bot.command()
async def choice(ctx, *args):
    """N個の引数から一つ取り出す"""
    await ctx.send(random.choice(args))

@bot.command()
async def vachar(ctx):
    """Valorantのキャラクターのランセレ"""
    await ctx.send(random.choice(["BRIMSTONE","PHOENIX","SAGE","SOVA","VIPER","CYPHER","REYNA","KILLJOY","BREACH","OMEN","JETT","RAZE","SKYE"]))

@bot.command()
async def clear(ctx, amount=5):
    """無駄ログ消し デフォルトで5"""
    if amount>20:
        await ctx.send("やめなされやめなされ")
    else:
        await ctx.channel.purge(limit=amount)

@bot.command()
async def voicejoin(ctx):
    """test"""

    voice_state=ctx.author.voice
    if (not voice_state) or (not voice_state.channel):
        await ctx.send("VCはいれ")
        return
    channel = voice_state.channel
    await channel.connect()
@bot.command()
async def voicerun(ctx):
    
    if not ctx.message.attachments:
        await ctx.send("ファイルが添付されていません。")
        return
    await ctx.message.attachments[0].save("tmp.mp3")
    voice_client = ctx.message.guild.voice_client
    ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
    voice_client.play(ffmpeg_audio_source)

    await ctx.send("再生しました。")
@bot.command()
async def voiceexit(ctx):
    voice_client = ctx.message.guild.voice_client
    await voice_client.disconnect()
    await ctx.send("ボイスチャンネルから切断しました。")

@bot.command()
async def apchar(ctx):
    """Apexのキャラクターのランセレ"""
    await ctx.send(random.choice(["Bangalore","Bloodhound","Caustic","Crypto","Gibraltar","Lifeline","Loba","Mirage","Octane","Pathfinder","Rampart","Revenant","Wattson","Wraith"]))

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("/help"))

bot.run(token)
