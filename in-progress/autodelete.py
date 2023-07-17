import datetime
import json
import sqlite3
from datetime import datetime

import discord
from discord.ext import commands
from discord import Option

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
db = sqlite3.connect("sql-databases/autodelete.sqlite")


class autodelete_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
	
    autodelete = discord.SlashCommandGroup("autodelete")
    
    @autodelete.command(
        description="📌 × Erstelle ein Autodelete in einem ausgewähltem Kanal"
    )
    @commands.has_permissions(administrator = True)
    async def add(self, ctx, channel: discord.TextChannel,
                              dauer: Option(str, "Wähle eine Zeit aus!", choices=[
                                  "15 Sekunden",
                                  "30 Sekunden",
                                  "1 Minute",
                                  "2 Minuten",
                                  "5 Minuten",
                                  "10 Minuten",
                                  "30 Minuten",
                                  "1 Stunde",
                                  "5 Sunden",
                                  "12 Stunden",
                                  "1 Tag"]),
                              message_limit: Option(int, "Wähle eine Anzahlaus!",
                                                    choices=[1, 2, 3, 4, 5, 6, 7, 8, 9])):

        time = 0
        if dauer == "15 Sekunden":
            time = 15
        if dauer == "30 Sekunden":
            time = 30
        if dauer == "1 Minute":
            time = 60
        if dauer == "2 Minuten":
            time = 120
        if dauer == "5 Minuten":
            time = 300
        if dauer == "10 Minuten":
            time = 600
        if dauer == "30 Minuten":
            time = 1800
        if dauer == "1 Stunde":
            time = 3600
        if dauer == "5 Stunden":
            time = 18000
        if dauer == "12 Stunden":
            time = 43200
        if dauer == "1 Tag":
            time = 86400
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM autodelete_channels WHERE guild_id = {ctx.guild.id}")
        autodel_channel = cur.fetchone()
        if autodel_channel is None:
            sql_content = "INSERT INTO autodelete_channels(guild_id, channel_id, time_count, limit_count) VALUES(?,?,?,?)"
            val = (ctx.guild.id, channel.id, time, message_limit)
            cursor.execute(sql_content, val)
            db.commit()
            embed = discord.Embed(
                description=f"{channel.mention} wurde erfolgreich als Autodelete Channel mit einer Dauer von `{time}s` eingerichtet.",
                color=0x5e63ea)
            embed.set_thumbnail(url=bot_avatar)
            embed.set_author(name="Autodelete hinzugefügt")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)

    @autodelete.command(
        description="📌 × Entferne einen Kanal welcher für Autodelete verwendet wird."
    )
    @commands.has_permissions(administrator = True)
    async def remove(self, ctx, channel: discord.TextChannel):
        db = sqlite3.connect('sql-databases/autodelete.sqlite')
        cursor = db.cursor()
        cursor.execute(f'SELECT guild_id FROM autodelete_channels WHERE guild_id = {ctx.guild.id}')
        resChannel = cursor.fetchone()
        if resChannel is None:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Kanal existiert nicht!",
                              ephemeral = True)
        else:
            cursor.execute(f"DELETE FROM autodelete_channels WHERE guild_id = {ctx.guild.id}")
            db.commit()
            embed = discord.Embed(
                description=f"<:fb_delete:1097445150092955679> **›** {channel.mention} wurde erfolgreich als Autodelete Channel entfernt.",
                color=0x5e63ea)
            embed.set_thumbnail(url=bot_avatar)
            embed.set_author(name="Autodelete entfernt")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)


def setup(bot):
    bot.add_cog(autodelete_module(bot))