import datetime
import sqlite3

import discord
from discord import Option
from discord.ext import commands

db = sqlite3.connect("sql-databases/log.sqlite")
bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
user_avatar = "bot-images/user_icon.png"


class log_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    log = discord.SlashCommandGroup("log")

    @log.command(
        description="📌 × Setze einen Logchannel auf deinem Server"
    )
    @commands.has_permissions(administrator=True)
    async def set(self, ctx, kanal: Option(discord.TextChannel, "Wähle einen Kanal", required=True)):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM log_setup WHERE guild_id = {ctx.guild.id}")
        log_channel = cur.fetchone()
        if log_channel is None:
            sql_content = "INSERT INTO log_setup(guild_id, channel_id) VALUES(?,?)"
            val = (ctx.guild.id, kanal.id)

        elif log_channel is not None:
            sql_content = "UPDATE log_setup SET channel_id = ? WHERE guild_id = ?"
            val = (kanal.id, ctx.guild.id)
        cursor.execute(sql_content, val)
        db.commit()

        embed = discord.Embed(
            description=f"{kanal.mention} wurde erfolgreich als neuer **Log-Chanel** gesetzt.",
            color=0x5e63ea
        )
        embed.set_author(name="LogChannel Update")
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=bot_avatar)
        await ctx.respond(embed=embed, ephemeral=True)

    @log.command(
        description="📌 × Entferne einen Logchannel vom deinem Server"
    )
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx, kanal: Option(discord.TextChannel, "Wähle einen Kanal", required=True)):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM log_setup WHERE guild_id = {ctx.guild.id}")
        log_channel = cur.fetchone()
        if log_channel is None:
            await ctx.respond("Dies ist kein LogChannel.")
        elif log_channel is not None:
            cursor.execute(f"DELETE FROM log_setup WHERE guild_id = {ctx.guild.id}")
            db.commit()

        embed = discord.Embed(
            description=f"{kanal.mention} wurde erfolgreich aus den LogChannels entfernt.",
            color=0x5e63ea
        )
        embed.set_author(name="LogChannel Update")
        embed.timestamp = datetime.datetime.now()
        embed.set_thumbnail(url=bot_avatar)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(log_module(bot))
