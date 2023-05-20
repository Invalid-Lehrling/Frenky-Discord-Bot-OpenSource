import json
import sqlite3

from discord.ext import commands
import discord
from PIL import Image, ImageFont, ImageDraw, ImageOps
from io import BytesIO
import io
import requests

db = sqlite3.connect('sql-databases/welcome.sqlite')
bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
user_avatar1 = "https://cdn.discordapp.com/attachments/1005884993245020163/1099321480942198834/7c8f476123d28d103efe381543274c25-modified.png"

with open("json-databases/autoroles.json", "r") as f:
    autorole_data = json.load(f)


class on_member_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        autorole_list = autorole_data[str(member.guild.id)]["roles"]

        if len(autorole_list) == 0:
            return
        else:
            roles = member.guild.roles
            role_ids = [role.id for role in roles]
            for role_id in autorole_list:
                if role_id in role_ids:
                    role = member.guild.get_role(role_id)
                    await member.add_roles(role)

    @commands.Cog.listener()
    async def on_member_join(self, member):

        #####################################
        user_avatar = member.avatar
        if not user_avatar:
            user_avatar = user_avatar1
        profile_picture_url = str(user_avatar)
        response = requests.get(profile_picture_url)
        profile_picture_bytes = BytesIO(response.content)
        profile = Image.open(profile_picture_bytes)
        if profile.mode != "RGB":
            profile = profile.convert("RGB")
        profile = profile.resize((225, 225))

        background = Image.open("bot-images/welcome_image.png").convert("RGBA")

        poppins1 = ImageFont.truetype(
            "fonts/UniSans.TTF", size=47)
        poppins = ImageFont.truetype(
            "fonts/Campton-LightDEMO.TTF", size=33
        )

        mask = Image.new("L", profile.size, 0)
        draw = ImageDraw.Draw(mask)
        draw.ellipse((0, 0) + profile.size, fill=255)
        mask_circle = ImageOps.fit(profile, mask.size, centering=(0.5, 0.5))
        mask_circle.putalpha(mask)
        background.paste(mask_circle, (527, 155), mask_circle)
        name = member.name
        members = len(member.guild.members)
        x = 0
        y = 0
        if members > 1 or members == 1:
            y = 543
            x = 564
        if members > 10 or members == 10:
            y = 543
            x = 556
        if members > 100 or members == 100:
            y = 543
            x = 547
        elif members > 1000 or members == 1000:
            y = 543
            x = 539
        if len(name) > 13:
            name = member.name[:13] + "..."
        draw = ImageDraw.Draw(background)
        name_width, _ = poppins1.getsize(name)
        name_x = 412 + (333 - name_width) / 2
        name_y = 467
        draw.text((name_x, name_y), f"{name}#{member.discriminator}", font=poppins1, fill="#ffffff")
        draw.text((x, y), f"{members}. Mitglied", font=poppins, fill="#ffffff")
        with io.BytesIO() as image_binary:
            background.save(image_binary, 'PNG')
            image_binary.seek(0)
            card = discord.File(fp=image_binary, filename="../bot-images/welcome_image.png")
        #####################################

        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM welcome_setup WHERE guild_id = {member.guild.id}")
        result = cursor.fetchone()
        cursor.execute(f"SELECT typ FROM welcome_setup WHERE guild_id = {member.guild.id}")
        result2 = cursor.fetchone()
        cursor.execute(f"SELECT button FROM welcome_setup WHERE guild_id = {member.guild.id}")
        result3 = cursor.fetchone()

        if result is None:
            return
        else:
            cursor.execute(f"SELECT msg FROM welcome_setup WHERE guild_id = {member.guild.id}")
            result1 = cursor.fetchone()

            members = len(list(member.guild.members))
            mention = member.mention
            name = member.name
            server=member.guild

            channel = self.bot.get_channel(result[0])
            view = discord.ui.View()
            button = discord.ui.Button(
                label = "Begrüßen",
                emoji = "👋",
                style = discord.ButtonStyle.blurple
            )


            view.add_item(button)

            choice = None
            if result3[0] == "Button aktiviert":
                choice = view
            elif result3[0] == "Button deaktiviert":
                choice = None

            if result2[0] == "Image":
                msg = await channel.send(
                    content=str(result1[0]).format(members=members, mention=mention, name=name, server=server), file=card, view = choice)
            elif result2[0] == "Normal":
                msg = await channel.send(
                    content=str(result1[0]).format(members=members, mention=mention, name=name, server=server), view = choice)

            async def begruessungsbutton_callback(interaction: discord.Interaction):
                if interaction.user is member:
                    await interaction.response.send_message("Du kannst dich nicht selber begrüßen!",
                                                           ephemeral = True)
                else:
                    button.disabled = True
                    await interaction.response.edit_message(view=view)
                    await msg.reply(f"👋 | {interaction.user} begrüßt herzlich **{member.name}**.")

            button.callback = begruessungsbutton_callback

def setup(bot):
    bot.add_cog(on_member_events(bot))
