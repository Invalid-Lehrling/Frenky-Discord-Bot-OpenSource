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

class LvlSystem:
    def __init__(self, xp_multiplier=1.5):
        self.xp_multiplier = xp_multiplier

    def calculate_level(self, xp):
        level = 0
        while xp >= self.calculate_xp_required(level + 1):
            level += 1
        return level

    def calculate_xp_required(self, level):
        return int(100 * (self.xp_multiplier ** (level - 1)))

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
            sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 1, 0)

        elif level_system is not None:
            sql_content = "UPDATE servers SET enabled = ? WHERE guild_id = ?"
            val = (1, ctx.guild.id)
        cursor.execute(sql_content, val)
        db.commit()

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
            sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 0, 0)

        elif level_system is not None:
            sql_content = "UPDATE servers SET enabled = ? WHERE guild_id = ?"
            val = (0, ctx.guild.id)
        cursor.execute(sql_content, val)
        db.commit()

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

            cursor = db.cursor()
            cur = cursor.execute(f"SELECT guild_id FROM servers WHERE guild_id = {ctx.guild.id}")
            level_system = cur.fetchone()
            if level_system is None:
                sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
                val = (ctx.guild.id, "dm", 0, 0)

            elif level_system is not None:
                sql_content = "UPDATE servers SET type = ?, channel = ? WHERE guild_id = ?"
                val = ("dm", 0, ctx.guild.id)
            cursor.execute(sql_content, val)
            db.commit()

            embed = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen per DM erhalten",
                                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - DM", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)

        elif type == "Default":

            cursor = db.cursor()
            cur = cursor.execute(f"SELECT guild_id FROM servers WHERE guild_id = {ctx.guild.id}")
            level_system = cur.fetchone()
            if level_system is None:
                sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
                val = (ctx.guild.id, "default", 0, 0)

            elif level_system is not None:
                sql_content = "UPDATE servers SET type = ?, channel = ? WHERE guild_id = ?"
                val = ("default", 0, ctx.guild.id)
            cursor.execute(sql_content, val)
            db.commit()

            embed = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen im Kanal der jeweils letzten gesendeten Nachricht erhalten",
                                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - default", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral = True)

        elif type == "Channel":
            embed = discord.Embed(title = "Frenky | Levelsystem Einrichtung", description = "Lege einen Kanal für die Levelup Message fest", color = 0x2b2d31)
            await ctx.respond(embed=embed, ephemeral = True, view = select_the_channel())

    @commands.Cog.listener()
    async def on_message(self, message):
        level_system = LvlSystem(xp_multiplier=2)
        if message.author.bot:
            pass
        else:
            cursor = db.cursor()

            cur = cursor.execute(f"SELECT enabled FROM servers WHERE guild_id = {message.guild.id}")
            enabled = cur.fetchone()
            if enabled[0] == 1:
                cur = cursor.execute(f"SELECT xp, level FROM users WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}")
                user = cur.fetchone()
                if user is None:
                    sql_content = "INSERT INTO users VALUES(?,?,?,?)"
                    val = (message.guild.id, message.author.id, 0, 3)
                    cursor.execute(sql_content, val)
                    db.commit()
                elif user is not None:
                    random_number = random.randint(10,20)
                    userxp = user[0] + random_number
                    if level_system.calculate_level(userxp) > user[1]:

                        level = level_system.calculate_level(userxp)
                        sql_content = "UPDATE users SET level = ?, xp = ? WHERE guild_id = ? AND user_id = ?"
                        val = (level, userxp, message.guild.id, message.author.id)
                        cursor.execute(sql_content, val)
                        db.commit()

                        cur = cursor.execute(f'SELECT type, channel FROM servers WHERE guild_id = {message.guild.id}')
                        type = cur.fetchone()

                        if type[0] == 'dm':
                            try:
                                embed = discord.Embed(description=f'> :tada: | **Herzlichen Glückwunsch**, du hast Level **{level}** erreicht!', color=0x2b2d31)
                                embed.set_author(name="Level-Up", 
                                                icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.author.send(content=message.author.mention, embed=embed)
                            except discord.Forbidden:
                                embed = discord.Embed(description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!', color=0x2b2d31)
                                embed.set_author(name="Level-Up", 
                                                icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.channel.send(content=message.author.mention, embed=embed)
                        elif type[0] == 'channel':
                            
                            try:
                                channel = self.bot.get_channel(type[1])
                                embed = discord.Embed(description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!', color=0x2b2d31)
                                embed.set_author(name="Level-Up", 
                                                icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await channel.send(content=message.author.mention, embed=embed)
                            except discord.Forbidden:
                                embed = discord.Embed(description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!', color=0x2b2d31)
                                embed.set_author(name="Level-Up", 
                                                icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.channel.send(content=message.author.mention, embed=embed)

                        else:
                            embed = discord.Embed(description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!', color=0x2b2d31)
                            embed.set_author(name="Level-Up", 
                                            icon_url=message.author.avatar.url)
                            embed.timestamp = datetime.datetime.now()
                            await message.channel.send(content=message.author.mention, embed=embed)

                    else:
                        sql_content = "UPDATE users SET xp = ? WHERE guild_id = ? AND user_id = ?"
                        val = (userxp, message.guild.id, message.author.id)
                        cursor.execute(sql_content, val)
                        db.commit()
                    
# server aus db removen + user aus db removen, wenn bot removed wird
def setup(bot):
    bot.add_cog(levelsystem(bot))

class select_the_channel(discord.ui.View):

    @discord.ui.select(
        select_type=discord.ComponentType.channel_select,
        channel_types=[discord.ChannelType.text, discord.ChannelType.voice]
    )
    async def select_callback(self, select, interaction):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM servers WHERE guild_id = {self.message.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            sql_content = "INSERT INTO servers VALUES(?,?,?,?)"
            val = (self.message.guild.id, "channel", 0, select.values[0].id)

        elif level_system is not None:
            print('datensatz vorhanden')
            sql_content = "UPDATE servers SET type = ?, channel = ? WHERE guild_id = ?"
            val = ("channel", select.values[0].id, self.message.guild.id)
        cursor.execute(sql_content, val)
        db.commit()

        embed2 = discord.Embed(description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen in {select.values[0].mention} erhalten",
                                color=0x2b2d31)
        embed2.set_author(name="Level-Up Benachrichtigungen - Bestimmter Kanal", 
                            icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed2.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed2, ephemeral=True)
