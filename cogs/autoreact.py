import datetime

import discord
import sqlite3
from discord.ext import commands
import asyncio
from discord import Option

db = sqlite3.connect("sql-databases/autoreact.sqlite")


class autoreact_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    autoreact = discord.SlashCommandGroup("autoreact", "ar")

    @commands.Cog.listener()
    async def on_message(self, message):
        await self.bot.wait_until_ready()
        cursor = db.cursor()
        cursor.execute(
            f'SELECT autoreact_channel FROM autoreact_setup WHERE guild_id = {message.guild.id} AND autoreact_channel = {message.channel.id}')
        result = cursor.fetchone()
        if result is not None:
            channel = self.bot.get_channel(int(result[0]))
            if message.channel == channel:
                cursor.execute(
                    f'SELECT emote1 FROM autoreact_setup WHERE guild_id = {message.guild.id} AND  autoreact_channel = {message.channel.id}')
                emote1 = cursor.fetchone()
                e1 = emote1[0]
                if e1 is not None:
                    try:
                        await message.add_reaction(e1)
                    except discord.NotFound:
                        # Emoji nicht gefunden
                        return "Unbekanntes Emoji"
                    except discord.HTTPException as e:
                        # Fehler beim Hinzufügen des Reaktion
                        return f"Fehler beim Hinzufügen des Reaktion: {e}"
                cursor.execute(
                    f'SELECT emote2 FROM autoreact_setup WHERE guild_id = {message.guild.id} AND autoreact_channel = {message.channel.id}')
                emote2 = cursor.fetchone()
                e2 = emote2[0]
                if e2 is not None:
                    try:
                        await message.add_reaction(e2)
                    except discord.NotFound:
                        # Emoji nicht gefunden
                        return "Unbekanntes Emoji"
                    except discord.HTTPException as e:
                        # Fehler beim Hinzufügen des Reaktion
                        return f"Fehler beim Hinzufügen des Reaktion: {e}"
                cursor.execute(
                    f'SELECT emote3 FROM autoreact_setup WHERE guild_id = {message.guild.id} AND autoreact_channel = {message.channel.id}')
                emote3 = cursor.fetchone()
                e3 = emote3[0]
                if e3 is not None:
                    try:
                        await message.add_reaction(e3)
                    except discord.NotFound:
                        # Emoji nicht gefunden
                        return "Unbekanntes Emoji"
                    except discord.HTTPException as e:
                        # Fehler beim Hinzufügen des Reaktion
                        return f"Fehler beim Hinzufügen des Reaktion: {e}"

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM autoreact_setup WHERE guild_id = {guild.id}')
        db.commit()

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        cursor = db.cursor()
        cursor.execute(f'DELETE FROM autoreact_setup WHERE guild_id = {channel.guild.id}')
        db.commit()

    @autoreact.command(
        name="set",
        description="📌 × Setze einen Kanal und Emotes für das Autoreact."
    )
    @commands.has_permissions(administrator=True)
    async def add_channel(self, ctx, channel: discord.TextChannel,
                          emote1,
                          emote2=None,
                          emote3=None):
        cursor = db.cursor()
        cursor.execute(f'SELECT autoreact_channel FROM autoreact_setup WHERE guild_id = {ctx.guild.id}')
        resChannel = cursor.fetchone()
        if emote2 is None:
            emote2 = "None"
        if emote3 is None:
            emote3 = "None"
        if resChannel is not None:
            cursor.execute(f'DELETE FROM autoreact_setup WHERE autoreact_channel = {channel.id}')
            db.commit()
            sql = 'INSERT INTO autoreact_setup(guild_id, autoreact_channel, emote1, emote2, emote3) VALUES(?,?,?,?,?)'
            val = (ctx.guild.id, channel.id, emote1, emote2, emote3)
            cursor.execute(sql, val)
            embed = discord.Embed(color=0x5e63ea,
                                  description=f'Neue Emotes für {channel.mention} wurden festgelegt.')
            embed.set_author(name='Frenky | Autoreact')
            embed.add_field(name=f'Emotes:', value=f'{emote1}, {emote2}, {emote3}')
            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed)
        if resChannel is None:
            sql = 'INSERT INTO autoreact_setup(guild_id, autoreact_channel, emote1, emote2, emote3) VALUES(?,?,?,?,?)'
            val = (ctx.guild.id, channel.id, emote1, emote2, emote3)
            cursor.execute(sql, val)

            embed = discord.Embed(color=0x5e63ea,
                                  description=f'{channel.mention} ist jetzt ein AutoReact Channel.\n')
            embed.set_author(name='Frenky | Autoreact')
            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )
            embed.add_field(name=f'Emotes:', value=f'{emote1}, {emote2}, {emote3}')
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed)
        db.commit()

    @autoreact.command(name='remove')
    async def remove_channel(self, ctx, channel: discord.TextChannel):
        cursor = db.cursor()
        cursor.execute(f'SELECT autoreact_channel FROM autoreact_setup WHERE autoreact_channel = {channel.id}')
        resChannel = cursor.fetchone()
        if resChannel is None:
            embed = discord.Embed(color=0x5e63ea,
                                  description=f'{channel.mention} ist nicht als AutoReact Channel eingetragen.')
            embed.set_author(name='Frenky | Autoreact')
            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )
            await ctx.send(embed=embed)
        if resChannel is not None:
            cursor.execute(f'DELETE FROM autoreact_setup WHERE autoreact_channel = {channel.id}')
            embed = discord.Embed(color=0xffaa00,
                                  description=f'{channel.mention} ist jetzt kein AutoReact Channel mehr.')
            embed.set_author(name='Frenky | Autoreact')
            embed.set_thumbnail(
                url=self.bot.user.avatar.url
            )
            await ctx.send(embed=embed)
        db.commit()


def setup(bot):
    bot.add_cog(autoreact_module(bot))
