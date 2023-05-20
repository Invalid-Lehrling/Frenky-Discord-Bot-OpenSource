import datetime
import json
import sqlite3

import discord
from discord import Option
from discord.ext import commands

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
db = sqlite3.connect('sql-databases/welcome.sqlite')
support = "https://discord.gg/PesnQYF5GJ"

with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())


class welcome_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    welcome = discord.SlashCommandGroup("welcome")

    @welcome.command(
        description="📌 × Setze einen Message Type für die Willkommensnachricht."
    )
    @commands.has_permissions(administrator=True)
    async def type(self, ctx,
                   typ: Option(str, "Wähle einen Typ aus", choices=["Normal", "Image"])):
        cursor = db.cursor()
        cursor.execute(f"SELECT typ FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
        resulti = cursor.fetchone()
        if resulti is None:
            sql = "INSERT INTO welcome_setup(guild_id, typ) VALUES(?,?)"
            val = (ctx.guild.id, typ)
            embed = discord.Embed(
                description=f"`{typ}` wurde als neuer Willkommensnachricht Typ gesetzt.",
                color=0x5e63ea
            )
            embed.set_author(name="Welcome Typ geändert")
            embed.set_thumbnail(url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        elif resulti is not None:
            sql = f"UPDATE welcome_setup SET typ = ? WHERE guild_id = ?"
            val = (typ, ctx.guild.id)
            embed = discord.Embed(
                description=f"`{typ}` wurde als neuer Willkommensnachricht Typ geändert.",
                color=0x5e63ea
            )
            embed.set_author(name="Welcome Typ geändert")
            embed.set_thumbnail(url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        cursor.execute(sql, val)
        db.commit()

    @welcome.command(
        description="📌 × Setze einen Willkommenskanal fest."
    )
    @commands.has_permissions(administrator=True)
    async def channel(self, ctx, channel: discord.TextChannel):
        cursor = db.cursor()
        cursor.execute(f"SELECT channel_id FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO welcome_setup(guild_id, channel_id, msg, typ, button) VALUES(?,?,?,?,?)"
            val = (ctx.guild.id, channel.id, "**Herzlich Willkommen** {mention}!", "Normal", "Button deaktiviert")
            embed = discord.Embed(
                description=f"{channel.mention} wurde als neuer Willkommenskanal geändert.",
                color=0x5e63ea
            )
            embed.set_author(name="Welcome Channel geändert")
            embed.set_thumbnail(url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        elif result is not None:
            sql = "UPDATE welcome_setup SET channel_id = ? WHERE guild_id = ?"
            val = (channel.id, ctx.guild_id)
            embed = discord.Embed(
                description=f"{channel.mention} wurde als neuer Willkommenskanal geändert.",
                color=0x5e63ea
            )
            embed.set_author(name="Welcome Channel geändert")
            embed.set_thumbnail(url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        cursor.execute(sql, val)
        db.commit()

    @welcome.command(
        description="📌 × Aktiviere den Begrüßungsbutton."
    )
    @commands.has_permissions(administrator=True)
    async def button(self, ctx, auswahl: Option(str, "Wähle eine Option.",
                                                             choices=["Button aktiviert", "Button deaktiviert"])):
        cursor = db.cursor()
        cursor.execute(f"SELECT button FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO welcome_setup(guild_id, button) VALUES(?,?)"
            val = (ctx.guild.id, auswahl)
            cursor.execute(sql, val)
        elif result is not None:
            sql = "UPDATE welcome_setup SET button = ? WHERE guild_id = ?"
            val = (auswahl, ctx.guild.id)
        embed = discord.Embed(
            description=f"Der neue Status des Begrüßungsbuttons ist: `{auswahl}`",
            color=0x5e63ea
        )
        embed.set_author(name="Welcome Channel geändert")
        embed.set_thumbnail(url=bot_avatar)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, ephemeral=True)
        cursor.execute(sql, val)
        db.commit()

    @welcome.command(
        description="📌 × Entferne das Welcome-Screening vom Server"
    )
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx):
        cursor = db.cursor()
        cursor.execute(f"SELECT button FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if result is None:
            await ctx.respond(
                "Auf diesem Server ist das Welcome System nicht eingerichtet.",
                ephemeral=True
            )
        elif result is not None:
            cursor.execute(f"DELETE FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
            db.commit()
            embed = discord.Embed(
                description=f"<:fb_delete:1097445150092955679> **›** Welcome Screening wurde erfolgreich entfernt.",
                color=0x5e63ea)
            embed.set_thumbnail(url=bot_avatar)
            embed.set_author(name="Welcome entfernt")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)

    @welcome.command(
        description="📌 × Nenne einen Text für die Willkommensnachricht."
    )
    @commands.has_permissions(administrator=True)
    async def text(self, ctx: discord.ApplicationContext):

        text_modal = normal_text_modal(title="Setze eine Nachricht")

        embed = discord.Embed(
            title="Frenky | Welcome-Setup (Text)",
            description="Hier stehene alle wichtigen Informationen, welche du benötigst"
                        "um die Willkommensnachricht für deinen Server zu verändern."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!",
            color=0x5e63ea
        )
        embed.add_field(
            name="<:fb_tag:1097481497918832771> | Die Variablen",
            value="> **User Ping:** `{mention}`\n"
                  "> **User Name:** `{name}`\n"
                  "> **Mitgliederanzahl:** `{count}`\n"
            	  "> **Server Name:** `{server}`"
        )
        embed.add_field(
            name="<:fb_information:1097190720038764695> | Wichtig",
            value="Bitte schreibe die Variablen immer mit `{}` Klammern!",
            inline=False
        )

        confirm_button = discord.ui.Button(
            label="Text Ändern",
            style=discord.ButtonStyle.blurple,
            emoji="<:fb_designs:1099338374919237702>"
        )

        async def confirm_button_callback(interaction: discord.Interaction):
            cursor = db.cursor()
            cursor.execute(f"SELECT typ FROM welcome_setup WHERE guild_id = {ctx.guild.id}")
            result1 = cursor.fetchone()

            if result1[0] == "Normal":
                await interaction.response.send_modal(text_modal)
            elif result1[0] == "Image":
                await interaction.response.send_modal(text_modal)

        confirm_button.callback = confirm_button_callback

        view = discord.ui.View()
        view.add_item(confirm_button)

        await ctx.respond(embed=embed, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(welcome_module(bot))


class normal_text_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Gebe hier den Text ein",
                placeholder="Schreibe hier...",
                required=True,
                style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        cursor = db.cursor()
        cursor.execute(f"SELECT msg FROM welcome_setup WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()
        if result is None:
            sql = "INSERT INTO welcome_setup(guild_id, msg) VALUES(?,?)"
            val = (interaction.guild.id, self.children[0].value)
            cursor.execute(sql, val)
        elif result is not None:
            sql = f"UPDATE welcome_setup SET msg = ? WHERE guild_id = ?"
            val = (self.children[0].value, interaction.guild_id)
            cursor.execute(sql, val)
        embed = discord.Embed(
            description="Willkommensnachricht wurde bearbeitet.",
            color=0x5e63ea
        )
        embed.add_field(
            name="Nachricht:",
            value=f"```{self.children[0].value}```"
        )
        await interaction.response.send_message(embed=embed, ephemeral=True)
        db.commit()
