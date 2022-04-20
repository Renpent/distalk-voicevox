import asyncio
from email import message
import discord
from discord.ext import commands
import os
import traceback
import re
import emoji
import json

prefix = os.getenv('DISCORD_BOT_PREFIX', default='🦑')
token = os.environ['DISCORD_BOT_TOKEN']
voicevox_key = os.environ['VOICEVOX_KEY']
voicevox_speaker = os.getenv('VOICEVOX_SPEAKER', default='2')
client = commands.Bot(command_prefix=prefix)
with open('emoji_ja.json', encoding='utf-8') as file:
    emoji_dataset = json.load(file)

@client.event
async def on_ready():
    presence = f'{prefix}ヘルプ | 0/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@client.event
async def on_guild_join(guild):
    presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@client.event
async def on_guild_remove(guild):
    presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
    await client.change_presence(activity=discord.Game(name=presence))

@client.command()
async def c(ctx):
    if ctx.message.guild:
        if ctx.author.voice is None:
            await ctx.send('ボイスチャンネルに接続してから呼び出してください。')
        else:
            if ctx.guild.voice_client:
                if ctx.author.voice.channel == ctx.guild.voice_client.channel:
                    await ctx.send('接続済みです。')
                else:
                    await ctx.voice_client.disconnect()
                    await asyncio.sleep(0.5)
                    await ctx.author.voice.channel.connect()
            else:
                await ctx.author.voice.channel.connect()

@client.command()
async def dc(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        else:
            await ctx.voice_client.disconnect()

@client.command()
async def gmks(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('あﾞあﾞゴﾞミカスゥッ！！死ねぇえッッ！！')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("gmks.wav"), volume=0.5)
        ctx.voice_client.play(source)
        await ctx.send('カス')

@client.command()
async def tknmt(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('それって・・・')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("tknmt.mp3"), volume=1.4)
        ctx.voice_client.play(source)

@client.command()
async def zunda(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        if ctx.voice_client.is_playing():
            await ctx.send('ずんだもんラップを再生中です')
        source = discord.PCMVolumeTransformer(discord.FFmpegPCMAudio("Zunda_rap.mp3"), volume=0.8)
        ctx.voice_client.play(source)
        await ctx.send('ずんだもんラップを再生しています。')

@client.command()
async def zunda_stop(ctx):
    if ctx.message.guild:
        if ctx.voice_client is None:
            await ctx.send('ボイスチャンネルに接続していません。')
        if not ctx.voice_client.is_playing():
            await ctx.send('ずんだもんラップを再生していません')
        ctx.voice_client.stop()
        await ctx.send('ずんだもんラップを停止しました。')


@client.command()
async def ks(ctx, text):
    if ctx.message.guild:
        mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={voicevox_key}&speaker=19&intonationScale=1'
        while ctx.voice_client.is_playing():
            await asyncio.sleep(0.5)
        ctx.voice_client.play(discord.FFmpegPCMAudio(mp3url))
#コマンドでスピーカーを変更できるようにしたい！

@client.event
async def on_message(message):
    if message.guild.voice_client:
        if not message.author.bot:
            if not message.content.startswith(prefix):
                text = message.content

                # Add author's name
                # text = message.author.name + '、' + text
                '''
                id = message.author.id
                if id == 479188732080160770:
                    text = 'なないろのしゃふが' + '、' + text + 'といっています'

                if id == 510082622903418880:
                    text = 'がちのしゃふが' + '、' + text + 'と，ほざいています'
                
                if id == 697508502540648508:
                    text = 'しゃふが' + '、' + text + 'といっています'
                '''

                # Replace new line
                text = text.replace('\n', '、')

                # Replace mention to user
                pattern = r'<@!?(\d+)>'
                match = re.findall(pattern, text)
                for user_id in match:
                    user = await client.fetch_user(user_id)
                    user_name = f'、{user.name}へのメンション、'
                    text = re.sub(rf'<@!?{user_id}>', user_name, text)

                # Replace mention to role
                pattern = r'<@&(\d+)>'
                match = re.findall(pattern, text)
                for role_id in match:
                    role = message.guild.get_role(int(role_id))
                    role_name = f'、{role.name}へのメンション、'
                    text = re.sub(f'<@&{role_id}>', role_name, text)

                # Replace Unicode emoji
                text = re.sub(r'[\U0000FE00-\U0000FE0F]', '', text)
                text = re.sub(r'[\U0001F3FB-\U0001F3FF]', '', text)
                for char in text:
                    if char in emoji.UNICODE_EMOJI['en'] and char in emoji_dataset:
                        text = text.replace(char, emoji_dataset[char]['short_name'])

                # Replace Discord emoji
                pattern = r'<:([a-zA-Z0-9_]+):\d+>'
                match = re.findall(pattern, text)
                for emoji_name in match:
                    emoji_read_name = emoji_name.replace('_', ' ')
                    text = re.sub(rf'<:{emoji_name}:\d+>', f'、{emoji_read_name}、', text)

                # Replace URL
                pattern = r'https://tenor.com/view/[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '画像', text)
                pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+(\.jpg|\.jpeg|\.gif|\.png|\.bmp)'
                text = re.sub(pattern, '、画像', text)
                pattern = r'https?://[\w/:%#\$&\?\(\)~\.=\+\-]+'
                text = re.sub(pattern, '、URL', text)

                # Replace spoiler
                pattern = r'\|{2}.+?\|{2}'
                text = re.sub(pattern, '伏せ字', text)

                # Replace laughing expression
                if text[-1:] == 'w' or text[-1:] == 'W' or text[-1:] == 'ｗ' or text[-1:] == 'W':
                    while text[-2:-1] == 'w' or text[-2:-1] == 'W' or text[-2:-1] == 'ｗ' or text[-2:-1] == 'W':
                        text = text[:-1]
                    text = text[:-1] + '、ワラ'

                # Add attachment presence
                for attachment in message.attachments:
                    if attachment.filename.endswith((".jpg", ".jpeg", ".gif", ".png", ".bmp")):
                        text += '、画像'
                    else:
                        text += '、添付ファイル'

                mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={voicevox_key}&speaker={voicevox_speaker}&intonationScale=1.2'
                while message.guild.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                message.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    await client.process_commands(message)

@client.event
async def on_voice_state_update(member, before, after):
    if before.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            '''
            if member.guild.voice_client is None:
                await asyncio.sleep(0.5)
                await after.channel.connect()
            else:
            '''
            if member.guild.voice_client.channel is after.channel:
                text = member.name + 'さんが入室しました'
                mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={voicevox_key}&speaker={voicevox_speaker}&intonationScale=1.2'
                while member.guild.voice_client.is_playing():
                    await asyncio.sleep(0.5)
                member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif after.channel is None:
        if member.id == client.user.id:
            presence = f'{prefix}ヘルプ | {len(client.voice_clients)}/{len(client.guilds)}サーバー'
            await client.change_presence(activity=discord.Game(name=presence))
        else:
            if member.guild.voice_client:
                if member.guild.voice_client.channel is before.channel:
                    if len(member.guild.voice_client.channel.members) == 1:
                        await asyncio.sleep(0.5)
                        await member.guild.voice_client.disconnect()
                    else:
                        text = member.name + 'さんが退室しました'
                        mp3url = f'https://api.su-shiki.com/v2/voicevox/audio/?text={text}&key={voicevox_key}&speaker={voicevox_speaker}&intonationScale=1.2'
                        while member.guild.voice_client.is_playing():
                            await asyncio.sleep(0.5)
                        member.guild.voice_client.play(discord.FFmpegPCMAudio(mp3url))
    elif before.channel != after.channel:
        if member.guild.voice_client:
            if member.guild.voice_client.channel is before.channel:
                if len(member.guild.voice_client.channel.members) == 1 or member.voice.self_mute:
                    await asyncio.sleep(0.5)
                    await member.guild.voice_client.disconnect()
                    await asyncio.sleep(0.5)
                    await after.channel.connect()

@client.event
async def on_command_error(ctx, error):
    orig_error = getattr(error, 'original', error)
    error_msg = ''.join(traceback.TracebackException.from_exception(orig_error).format())
    await ctx.send(error_msg)

@client.command()
async def ヘルプ(ctx):
    message = f'''◆◇◆{client.user.name}の使い方◆◇◆
{prefix}＋コマンドで命令できます。
{prefix}接続：ボイスチャンネルに接続します。
{prefix}切断：ボイスチャンネルから切断します。
{prefix}zunda：ずんだもんラップを再生します。
{prefix}zunda_stop：ずんだもんラップを停止します。'''
    await ctx.send(message)

client.run(token)
