import datetime
import json
import random
import sqlite3

import discord
from discord import Option
from discord.ext import commands

db = sqlite3.connect("sql-databases/levelsystem.sqlite")

with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]
support = "https://discord.gg/xsqv57JnF4"

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())


class levelsystem(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    levelsystem = discord.SlashCommandGroup("levelsystem")

    @levelsystem.command(
        description="✅ × aktiviere das Levelsystem"
    )
    @commands.has_permissions(administrator=True)
    async def enable(self, ctx):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM servers WHERE guild_id = {ctx.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            print('datensatz nicht vorhanden')
            sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 1, 0)

        elif level_system is not None:
            print('datensatz vorhanden')
            sql_content = "UPDATE servers SET enabled = ? WHERE guild_id = ?"
            val = (1, ctx.guild.id)
        cursor.execute(sql_content, val)
        db.commit()
        print('datensatz aktualisiert')

        embed = discord.Embed(description="> <:fb_true:1109558619990655137> | Das Levelsystem wurde **aktiviert**",
                              color=0x2b2d31)
        embed.set_author(name="Levelsystem aktiviert", 
                         icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral = True)
    
    @levelsystem.command(
        description="❌ × deaktiviere das Levelsystem"
    )

    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM servers WHERE guild_id = {ctx.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            print('datensatz nicht vorhanden')
            sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 0, 0)

        elif level_system is not None:
            print('datensatz vorhanden')
            sql_content = "UPDATE servers SET enabled = ? WHERE guild_id = ?"
            val = (0, ctx.guild.id)
        cursor.execute(sql_content, val)
        db.commit()
        print('datensatz aktualisiert')

        embed = discord.Embed(description="> <:fb_false:1109558615393706114> | Das Levelsystem wurde **deaktiviert**",
                              color=0x2b2d31)
        embed.set_author(name="Levelsystem deaktiviert", 
                         icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral = True)
    
    levelup = discord.SlashCommandGroup("levelup")

    @levelup.command(
        description="✅ × lege fest, wie der User seine Levelup-Benachrichtigung erhalten soll"
    )

    @commands.has_permissions(administrator=True)
    async def type(self, ctx, type: Option(str, "Wähle einen Typ", choices=["Channel", "DM", "Default"])):
        if type == "DM":
            embed = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen per DM erhalten",
                                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - DM", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)

        elif type == "Default":
            embed = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen im Kanal der jeweils letzten gesendeten Nachricht erhalten",
                                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - default", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)

        elif type == "Channel":
            embed2 = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen in #kanal erhalten",
                                color=0x2b2d31)
            embed2.set_author(name="Level-Up Benachrichtigungen - Bestimmter Kanal", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed2.timestamp = datetime.datetime.now()
            embed = discord.Embed(title = "Frenky | Levelsystem Einrichtung", description = "Schreibe einen Kanal für die Levelup Message", color = 0x2b2d31)
            await ctx.respond(embed=embed, ephemeral = True)
        # die anderen cases noch hinzufügen + modal

# on_message event coden, bei dem die user xp bekommen und level aufsteigen
# server aus db removen + user aus db removen, wenn bot removed wird
def setup(bot):
    bot.add_cog(levelsystem(bot))