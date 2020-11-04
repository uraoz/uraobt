from discord.ext import commands
import os
from os import system
import discord
from discord import FFmpegPCMAudio
from discord.utils import get
import asyncio
import random
import traceback
import time
import youtube_dl

youtube_dl.utils.bug_reports_message = lambda: ''


ytdl_format_options = {
    'format': 'bestaudio/best',
    'restrictfilenames': True,
    'noplaylist': True,
    'nocheckcertificate': True,
    'ignoreerrors': False,
    'outtmpl': 'tmp.mp3',
    'logtostderr': False,
    'quiet': True,
    'no_warnings': True,
    'default_search': 'ytsearch1:',
    'source_address': '0.0.0.0' # bind to ipv4 since ipv6 addresses cause issues sometimes
}


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
async def clear(ctx, amount=3):
    """無駄ログ消し デフォルトで3 amount=Nで量指定"""
    if amount>20:
        await ctx.send("やめなされやめなされ")
    else:
        await ctx.channel.purge(limit=amount)


@bot.command()
async def voicefile(ctx):
    """添付された音声を再生"""
    voice_state=ctx.author.voice
    if (not voice_state) or (not voice_state.channel):
        await ctx.send("VCはいれ")
        return
    if not ctx.message.attachments:
        await ctx.send("ファイル添付して")
        return
    channel = voice_state.channel
    try:
        await channel.connect()
    except:
        await ctx.send("もう参加してる")
    time.sleep(1)
    try:
        os.remove('tmp.mp3')
    except:
        pass
    await ctx.message.attachments[0].save("tmp.mp3")
    voice_client = ctx.message.guild.voice_client
    ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
    try:
        voice_client.play(ffmpeg_audio_source, after=voiceexit)
        await ctx.send("再生")
    except:
        await ctx.send("再生中")

@bot.command()
async def voiceurl(ctx, *args):
    """URLか検索文字列を再生 YoutubeのURL それ以外の文字列なら検索結果から 20分以下"""
    song_there = os.path.isfile("tmp.mp3")
    try:
        if song_there:
            os.remove("tmp.mp3")
    except PermissionError:
        await ctx.send("動いてたらバグるから一回とめて")
        return
    voice_state=ctx.author.voice
    arg=''.join(args)
    if (not voice_state) or (not voice_state.channel):
        await ctx.send("VCはいれ")
        return
    if not arg:
        await ctx.send("urlか文字列指定して")
        return
    channel = voice_state.channel
    try:
        await channel.connect()
    except:
        pass
    time.sleep(1)

    try:
        os.remove('tmp.mp3')
    except:
        pass
    
    ydl = youtube_dl.YoutubeDL(ytdl_format_options)
    info_dict = ydl.extract_info(arg, download=False)
    try:
        duration=info_dict["duration"]
    except:
        duration=info_dict["entries"][0]["duration"]
    if(int(duration))>1200:
        await ctx.send("長すぎ 20分未満で")
        return
    try:
        await ctx.send(info_dict['title']+")をロード")
    except:
        await ctx.send(info_dict['entries'][0]['title']+"(https://www.youtube.com/watch?v="+info_dict['entries'][0]['id']+")をロード")

    ydl.download([arg])
    for file in os.listdir("./"):
        if file.endswith(".mp3"):
            os.rename(file, 'tmp.mp3')
    voice_client = ctx.message.guild.voice_client
    ffmpeg_audio_source = discord.FFmpegPCMAudio("tmp.mp3")
    try:
        voice_client.play(ffmpeg_audio_source)

    except:
        await ctx.send("すでに再生中")



@bot.command()
async def voiceexit(ctx):
    """VCから切断"""
    voice_client = ctx.message.guild.voice_client
    try:
        await voice_client.disconnect()
        await ctx.send("切断")
    except:
        await ctx.send("参加してない")
    try:
        os.remove('tmp.mp3')
    except:
        pass

@bot.command()
async def apchar(ctx):
    """Apexのキャラクターのランセレ"""
    await ctx.send(random.choice(["Bangalore","Bloodhound","Caustic","Crypto","Gibraltar","Lifeline","Loba","Mirage","Octane","Pathfinder","Rampart","Revenant","Wattson","Wraith"]))

@bot.event
async def on_ready():
    await bot.change_presence(status = discord.Status.idle, activity = discord.Game("/help"))

bot.run(token)
