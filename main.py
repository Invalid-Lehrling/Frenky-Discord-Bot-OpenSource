import asyncio
import json
import os

import discord
from discord.ext import commands, tasks

import sqlite3

with open("json-runfile/runfile.json", "r") as f:
    run_settings = json.load(f)
bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"

command_prefix = run_settings["standard-prefix"]
run_token = run_settings["run-token"]

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())
bot.remove_command("help")

if os.path.exists('sql-databases/autodelete.sqlite'):
    conn1 = sqlite3.connect("sql-databases/autodelete.sqlite")
    c1 = conn1.cursor()
    pass
else:
    connect_database1 = sqlite3.connect('sql-databases/autodelete.sqlite')
    cur1 = connect_database1.cursor()
    cur1.execute(
        '''CREATE TABLE IF NOT EXISTS autodelete_channels(guild_id INTEGER, channel_id INTEGER, time_count INTEGER, limit_count INTEGER)''')

if os.path.exists('sql-databases/welcome.sqlite'):
    conn2 = sqlite3.connect("sql-databases/welcome.sqlite")
    c2 = conn2.cursor()
    pass
else:
    connect_database2 = sqlite3.connect('sql-databases/welcome.sqlite')
    cur2 = connect_database2.cursor()
    cur2.execute(
        '''CREATE TABLE IF NOT EXISTS welcome_setup(guild_id INTEGER, channel_id INTEGER, msg TEXT, typ TEXT, button TEXT)''')

if os.path.exists('sql-databases/log.sqlite'):
    conn3 = sqlite3.connect("sql-databases/log.sqlite")
    c = conn3.cursor()
    pass
else:
    connect_database3 = sqlite3.connect('sql-databases/log.sqlite')
    cur3 = connect_database3.cursor()
    cur3.execute(
        '''CREATE TABLE IF NOT EXISTS log_setup(guild_id INTEGER, channel_id INTEGER)''')

if os.path.exists('sql-databases/ticket.sqlite'):
    conn2 = sqlite3.connect("sql-databases/ticket.sqlite")
    c2 = conn2.cursor()
    pass
else:
    connect_database2 = sqlite3.connect('sql-databases/ticket.sqlite')
    cur2 = connect_database2.cursor()
    cur2.execute(
        '''CREATE TABLE IF NOT EXISTS ticket_panel(guild_id INTEGER, ticket_channel INTEGER,ticket_text TEXT)''')
    cur2.execute(
        '''CREATE TABLE IF NOT EXISTS ticket_panel_component(guild_id INTEGER)''')

if os.path.exists('sql-databases/ticket.sqlite'):
    conn2 = sqlite3.connect("sql-databases/tempchannel.sqlite")
    c2 = conn2.cursor()
    pass
else:
    connect_database2 = sqlite3.connect('sql-databases/tempchannel.sqlite')
    cur2 = connect_database2.cursor()
    cur2.execute(
        '''CREATE TABLE IF NOT EXISTS tempchannel_setup(guild_id INTEGER, voice_id INTEGER, voice_name TEXT, text_id INTEGER, voice_category INTEGER)''')
    cur2.execute(
        '''CREATE TABLE IF NOT EXISTS tempchannel_user(guild_id INTEGER, user_id INTEGER, channel_name TEXT, limit_int INTEGER, is_locked Text)''')


async def status_task():
    while True:
        guild = bot.get_guild(1000024183457202266)
        await bot.change_presence(activity=discord.Game(name=f"auf {len(bot.guilds)} Server"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name=f"mit {len(bot.users)} Nutzer"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name=f"mit InvalidLehrling"))
        await asyncio.sleep(30)
        await bot.change_presence(activity=discord.Game(name=f"type /help"))
        await asyncio.sleep(60)


async def bot_counts():
    await asyncio.sleep(3600)
    await bot.get_channel(1109205925660725278).edit(name=f"Benutzer: {len(bot.users)}")
    await bot.get_channel(1109206292830101625).edit(name=f"Server: {len(bot.guilds)}")


@bot.event
async def on_ready():
    print("Bot ist Bereit")
    bot.loop.create_task(status_task())
    bot.loop.create_task(bot_counts())


for filename in os.listdir("./cogs"):
    if filename.endswith(".py"):
        bot.load_extension(f"cogs.{filename[:-3]}")
        print(f"Cog {filename[:-3]}.py Loaded!")

bot.run(run_token)
