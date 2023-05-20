import datetime
import json
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands
import asyncio

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
db_path = "sql-databases/autodelete.sqlite"


class autodelete_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message):
        def check(m):
            return not m.pinned

        with sqlite3.connect(db_path) as db:
            cursor = db.cursor()
            cursor.execute(f"SELECT time_count FROM autodelete_channels WHERE guild_id = {message.guild.id}")
            time = cursor.fetchone()
            cursor.execute(f"SELECT limit_count FROM autodelete_channels WHERE channel_id = {message.channel.id}")
            limit = cursor.fetchone()
            cursor.execute(f"SELECT channel_id FROM autodelete_channels WHERE channel_id = {message.channel.id}")
            channel = cursor.fetchone()
            cursor.execute(f"SELECT guild_id FROM autodelete_channels WHERE channel_id = {message.channel.id}")
            guild = cursor.fetchone()

            if guild is None:
                return
            if time is None:
                return
            if limit is None:
                return
            if channel is None:
                return
            if not message.content.startswith("!"):
                if message.channel.id in channel:
                    await asyncio.sleep(time[0])
                    await message.channel.purge(limit=limit[0], check=check)

        await self.bot.process_commands(message)


def setup(bot):
    bot.add_cog(autodelete_event(bot))
