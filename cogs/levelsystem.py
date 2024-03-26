import datetime
import json
import random
import sqlite3
from io import BytesIO
import io

import discord
from discord import Option
from discord.ext import commands
from PIL import Image, ImageDraw, ImageFont, ImageOps
import requests

db = sqlite3.connect("sql-databases/levelsystem.sqlite")

with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]

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
        cur = cursor.execute(f"SELECT guild_id FROM level_setup WHERE guild_id = {ctx.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            sql_content = "INSERT INTO level_setup VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 1, 0)
            cursor.execute(sql_content, val)
        elif level_system is not None:
            sql_content = "UPDATE level_setup SET enabled = ? WHERE guild_id = ?"
            val = (1, ctx.guild.id)
            cursor.execute(sql_content, val)
        db.commit()

        embed = discord.Embed(description="> <:fb_true:1109558619990655137> | Das Levelsystem wurde **aktiviert**",
                              color=0x2b2d31)
        embed.set_author(name="Levelsystem aktiviert",
                         icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral=True)

    @levelsystem.command(
        description="❌ × deaktiviere das Levelsystem"
    )
    @commands.has_permissions(administrator=True)
    async def disable(self, ctx):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM level_setup WHERE guild_id = {ctx.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            sql_content = "INSERT INTO level_setup VALUES(?,?,?,?)"
            val = (ctx.guild.id, "default", 0, 0)
            cursor.execute(sql_content, val)
        elif level_system is not None:
            sql_content = "UPDATE level_setup SET enabled = ? WHERE guild_id = ?"
            val = (0, ctx.guild.id)
            cursor.execute(sql_content, val)
        db.commit()

        embed = discord.Embed(description="> <:fb_false:1109558615393706114> | Das Levelsystem wurde **deaktiviert**",
                              color=0x2b2d31)
        embed.set_author(name="Levelsystem deaktiviert",
                         icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral=True)

    levelup = discord.SlashCommandGroup("levelup")

    @levelup.command(
        description="✅ × lege fest, wie der User seine Levelup-Benachrichtigung erhalten soll"
    )
    @commands.has_permissions(administrator=True)
    async def type(self, ctx, type: Option(str, "Wähle einen Typ", choices=["Channel", "DM", "Default"])):
        if type == "DM":

            cursor = db.cursor()
            cur = cursor.execute(f"SELECT guild_id FROM level_setup WHERE guild_id = {ctx.guild.id}")
            level_system = cur.fetchone()
            if level_system is None:
                sql_content = "INSERT INTO level_setup VALUES(?,?,?,?)"
                val = (ctx.guild.id, "dm", 0, 0)
                cursor.execute(sql_content, val)
            elif level_system is not None:
                sql_content = "UPDATE level_setup SET type = ?, channel = ? WHERE guild_id = ?"
                val = ("dm", 0, ctx.guild.id)
                cursor.execute(sql_content, val)
            db.commit()

            embed = discord.Embed(
                description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen per DM erhalten",
                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - DM",
                             icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)

        elif type == "Default":

            cursor = db.cursor()
            cur = cursor.execute(f"SELECT guild_id FROM level_setup WHERE guild_id = {ctx.guild.id}")
            level_system = cur.fetchone()
            if level_system is None:
                sql_content = "INSERT INTO level_setup VALUES(?,?,?,?)"
                val = (ctx.guild.id, "default", 0, 0)
                cursor.execute(sql_content, val)
            elif level_system is not None:
                sql_content = "UPDATE level_setup SET type = ?, channel = ? WHERE guild_id = ?"
                val = ("default", 0, ctx.guild.id)
                cursor.execute(sql_content, val)
            db.commit()

            embed = discord.Embed(
                description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen im Kanal der jeweils letzten gesendeten Nachricht erhalten",
                color=0x2b2d31)
            embed.set_author(name="Level-Up Benachrichtigungen - default",
                             icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)

        elif type == "Channel":
            embed = discord.Embed(title="Frenky | Levelsystem Einrichtung",
                                  description="Lege einen Kanal für die Levelup Message fest", color=0x2b2d31)
            await ctx.respond(embed=embed, ephemeral=True, view=select_the_channel())

    @commands.Cog.listener()
    async def on_message(self, message):
        level_system = LvlSystem(xp_multiplier=2)
        if message.author.bot:
            pass
        else:
            cursor = db.cursor()

            cur = cursor.execute(f"SELECT enabled FROM level_setup WHERE guild_id = {message.guild.id}")
            enabled = cur.fetchone()
            if enabled[0] == 1:
                cur = cursor.execute(
                    f"SELECT XP, level FROM level_users WHERE guild_id = {message.guild.id} AND user_id = {message.author.id}")
                user = cur.fetchone()
                if user is None:
                    sql_content = "INSERT INTO level_users VALUES(?,?,?,?)"
                    val = (message.guild.id, message.author.id, 0, 1)
                    cursor.execute(sql_content, val)
                    db.commit()
                elif user is not None:
                    random_number = random.randint(1, 2)
                    userxp = user[0] + random_number

                    if level_system.calculate_level(userxp) > user[1]:
                        level = level_system.calculate_level(userxp)
                        sql_content = "UPDATE level_users SET level = ?, XP = ? WHERE guild_id = ? AND user_id = ?"
                        val = (level, userxp, message.guild.id, message.author.id)
                        cursor.execute(sql_content, val)
                        db.commit()

                        cur = cursor.execute(
                            f'SELECT type, channel FROM level_setup WHERE guild_id = {message.guild.id}')
                        type = cur.fetchone()

                        if type[0] == 'dm':
                            try:
                                embed = discord.Embed(
                                    description=f'> :tada: | **Herzlichen Glückwunsch**, du hast Level **{level}** erreicht!',
                                    color=0x2b2d31)
                                embed.set_author(name="Level-Up",
                                                 icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.author.send(content=message.author.mention, embed=embed)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!',
                                    color=0x2b2d31)
                                embed.set_author(name="Level-Up",
                                                 icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.channel.send(content=message.author.mention, embed=embed)
                        elif type[0] == 'channel':

                            try:
                                channel = self.bot.get_channel(type[1])
                                embed = discord.Embed(
                                    description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!',
                                    color=0x2b2d31)
                                embed.set_author(name="Level-Up",
                                                 icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await channel.send(content=message.author.mention, embed=embed)
                            except discord.Forbidden:
                                embed = discord.Embed(
                                    description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!',
                                    color=0x2b2d31)
                                embed.set_author(name="Level-Up",
                                                 icon_url=message.author.avatar.url)
                                embed.timestamp = datetime.datetime.now()
                                await message.channel.send(content=message.author.mention, embed=embed)

                        else:
                            embed = discord.Embed(
                                description=f'> :tada: | **Herzlichen Glückwunsch**, {message.author.mention} hat Level **{level}** erreicht!',
                                color=0x2b2d31)
                            embed.set_author(name="Level-Up",
                                             icon_url=message.author.avatar.url)
                            embed.timestamp = datetime.datetime.now()
                            await message.channel.send(content=message.author.mention, embed=embed)

                    else:
                        sql_content = "UPDATE level_users SET XP = ? WHERE guild_id = ? AND user_id = ?"
                        val = (userxp, message.guild.id, message.author.id)
                        cursor.execute(sql_content, val)
                        db.commit()

    @discord.slash_command(name="rank")
    async def _level(self, ctx, member: discord.Member = None):
        await ctx.defer()
        user = None
        if member is None:
            user = ctx.author
        elif member is not None:
            user = member

        cursor = db.cursor()
        cursor.execute(
            f"SELECT user_id, level, XP FROM level_users WHERE guild_id = {ctx.guild.id} AND user_id = {user.id}")
        res = cursor.fetchone()

        if res is None:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Dieser User ist nicht in der Datenbank eingetragen.",
                ephemeral=True)
            return

        level = int((res[1]), )
        xp = int((res[2]), )
        level_system = LvlSystem(xp_multiplier=2)
        xp_ = xp - level_system.calculate_xp_required(level)

        background = Image.open("bot-images/rankcard2.png").convert("RGBA")

        user_avatar = user.display_avatar
        if not user_avatar:
            user_avatar = user.display_avatar
        profile_picture_url = str(user_avatar)
        response = requests.get(profile_picture_url)
        profile_picture_bytes = BytesIO(response.content)
        profile = Image.open(profile_picture_bytes)
        if profile.mode != "RGB":
            profile = profile.convert("RGB")
        profile = profile.resize((120, 120))

        poppins1 = ImageFont.truetype("fonts/UniSans.TTF", size=35)
        poppins2 = ImageFont.truetype("fonts/UniSans.TTF", size=25)

        mask = Image.new("L", profile.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile.size, fill=255)
        mask_circle = ImageOps.fit(profile, mask.size, centering=(0.5, 0.5))
        mask_circle.putalpha(mask)
        background.paste(mask_circle, (39, 76), mask_circle)
        required_xp = level_system.calculate_xp_required(level + 1)
        required_xp_ = required_xp - level_system.calculate_xp_required(level)

        name = user.name
        if len(name) > 16:
            name = user.name[:16] + "..."
        name_x = 185
        name_y = 101
        draw = ImageDraw.Draw(background)
        draw.text((name_x, name_y), name, font=poppins1, fill="#5e63ea")

        xp_text = f"{xp} / {required_xp}"
        xp_text_width, xp_text_height = poppins2.getsize(xp_text)

        xp_text_x = 535 + (333 - xp_text_width) // 2
        xp_text_y = 82

        draw.text((xp_text_x, xp_text_y), xp_text, font=poppins2, fill="white")

        x = 0
        y = 0
        if level > 0 or level == 0:
            y = 183
            x = 690
        if level > 1 or level == 1:
            y = 183
            x = 690
        if level > 10 or level == 10:
            y = 138
            x = 685
        if level > 100 or level == 100:
            y = 138
            x = 680
        elif level > 1000 or level == 1000:
            y = 138
            x = 675

        draw.text((x, y), f"{level}", font=poppins2, fil="#5e63ea")

        bar_x = 185
        bar_y = 140
        bar_width = 366
        bar_height = 24
        progress_percentage = xp_ / required_xp_
        fill_color = "#5e63ea"
        radius = 5

        bar_fill_width = int(bar_width * progress_percentage)

        bar_fill = (bar_x, bar_y, bar_x + bar_fill_width, bar_y + bar_height)
        draw.rounded_rectangle(bar_fill, fill=fill_color, outline=None, width=0, radius=radius)

        with io.BytesIO() as image_binary:
            background.save(image_binary, "PNG")
            image_binary.seek(0)
            card = discord.File(fp=image_binary, filename="bot-images/rankcard2.png")

        await ctx.respond(file=card)


def setup(bot):
    bot.add_cog(levelsystem(bot))


class select_the_channel(discord.ui.View):

    @discord.ui.select(
        select_type=discord.ComponentType.channel_select,
        channel_types=[discord.ChannelType.text, discord.ChannelType.voice]
    )
    async def select_callback(self, select, interaction):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT guild_id FROM level_setup WHERE guild_id = {self.message.guild.id}")
        level_system = cur.fetchone()
        if level_system is None:
            sql_content = "INSERT INTO level_setup VALUES(?,?,?,?)"
            val = (self.message.guild.id, "channel", 0, select.values[0].id)
            cursor.execute(sql_content, val)
        elif level_system is not None:
            print('datensatz vorhanden')
            sql_content = "UPDATE level_setup SET type = ?, channel = ? WHERE guild_id = ?"
            val = ("channel", select.values[0].id, self.message.guild.id)
            cursor.execute(sql_content, val)
        db.commit()

        embed2 = discord.Embed(
            description=f"> <:fb_true:1109558619990655137> | Die User werden ihre Benachrichtigungen in {select.values[0].mention} erhalten",
            color=0x2b2d31)
        embed2.set_author(name="Level-Up Benachrichtigungen - Bestimmter Kanal",
                          icon_url="https://cdn.discordapp.com/emojis/1097455801595084805.webp?size=96&quality=lossless")
        embed2.timestamp = datetime.datetime.now()
        await interaction.response.send_message(embed=embed2, ephemeral=True)
