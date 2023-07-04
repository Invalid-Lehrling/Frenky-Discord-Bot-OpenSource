import datetime
import sqlite3

import discord
from discord import Option
from discord.ext import commands

blacklist_db = sqlite3.connect("sql-databases/smallfeatures.sqlite")


class blacklist_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    blacklist = discord.SlashCommandGroup("blacklist")

    @commands.Cog.listener()
    async def on_message(self, message):

        cursor = blacklist_db.cursor()
        cursor.execute(f"SELECT word FROM blacklist_words WHERE guild_id = {message.guild.id}")
        blacklist_all = cursor.fetchall()

        words = []

        for w in blacklist_all:
            integer_werts = ''.join(map(str, w))
            words.append(integer_werts)

        if message.content.startswith(" "):
            return
        if blacklist_all is None:
            return
        else:
            if any(word in message.content.lower() for word in words):
                matched_words = [word for word in words if word in message.content.lower()]

                embed = discord.Embed(
                    title="Blacklist Wort erkannt",
                    description=f"{message.author.mention} hat eine Nachricht aus der Blacklist geschrieben.\n"
                                f"Beschreibung\n"
                                f"```ansi\n"
                                f"Nachricht: [2;34m{message.content}[0m\n"
                                f"Blacklist Wörter: [2;31m{', '.join(matched_words)}[0m"
                                "```",
                    color=0x2b2d31
                )
                embed.set_footer(text="Blacklist Wort erkannt")
                embed.timestamp = datetime.datetime.now()
                await message.channel.send(embed=embed, delete_after = 60)
                await message.delete()

    @blacklist.command(
        name="add",
        description="🧩 × Füge ein Wort Blacklist hinzu."
    )
    @commands.has_permissions(administrator=True)
    async def _balcklist_add(self, ctx):
        await ctx.send_modal(blacklist_add_modal(title="Blacklist Word hinzufügen"))

    @blacklist.command(
        name="remove",
        description="❌ × Entferne ein Blacklist Word aus der Liste."
    )
    @commands.has_permissions(administrator=True)
    async def _blacklist_remove(self, ctx):
        await ctx.send_modal(blacklist_remove_modal(title="Blacklist Word entfernen"))

    @blacklist.command(
        name="list",
        description="📋 × Lass dir die Liste aller Blacklist Wörten anzeigen."
    )
    @commands.has_permissions(administrator=True)
    async def _blacklist_list(self, ctx):
        cursor = blacklist_db.cursor()
        cursor.execute(f"SELECT word FROM blacklist_words WHERE guild_id = {ctx.guild.id}")
        blacklist_all = cursor.fetchall()

        words = []

        for w in blacklist_all:
            integer_werts = ''.join(map(str, w))
            words.append(integer_werts)

        embed = discord.Embed(
            title="Blacklist Words",
            description="Hier sind alle Wörter der Blacklist gelistet. "
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier](https://discord.gg/xsqv57JnF4)** hilfe suchen!\n⠀\n",
            color=0x2b2d31
        )

        if len(words) == 0:
            embed.add_field(
                name="Blacklist Words:",
                value="Keine Wörter in der Liste"
            )
        else:
            embed.add_field(
                name=f"Blacklist Words:",
                value='```ansi\n[2;31m{}[0m```'.format(
                    str(words).replace('(', '').replace(')', '').replace('[', '').replace(']', '').replace("'", ''))
            )
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(blacklist_module(bot))


class blacklist_remove_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Schreibe hier das Blacklist Word",
                style=discord.InputTextStyle.short,
                placeholder="...."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        cursor = blacklist_db.cursor()
        cursor.execute(f"SELECT word FROM blacklist_words WHERE guild_id = {interaction.guild.id}")
        blacklist_all = cursor.fetchall()

        words = [w[0] for w in
                 blacklist_all]

        if self.children[0].value not in words:
            await interaction.response.send_message(
                f"Das Wort `{self.children[0].value}` ist nicht in der Datenbank eingetragen.",
                ephemeral=True)
        else:
            embed = discord.Embed(
                title="Ein Blacklist Wort wurde entfernt",
                description=f"`{self.children[0].value}` wurde aus der Liste entfernt",
                color=0x2b2d31
            )
            if interaction.guild.icon is not None:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            cursor.execute(
                f"DELETE FROM blacklist_words WHERE guild_id = {interaction.guild.id} AND word = '{self.children[0].value}'")
        blacklist_db.commit()


class blacklist_add_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Schreibe hier das Blacklist Word",
                style=discord.InputTextStyle.short,
                placeholder="...."
            )
        )

    async def callback(self, interaction: discord.Interaction):
        cursor = blacklist_db.cursor()
        cursor.execute(f"SELECT word FROM blacklist_words WHERE guild_id = {interaction.guild.id}")
        blacklist_all = cursor.fetchall()

        words = []

        for w in blacklist_all:
            integer_werts = ', '.join(map(str, w))
            words.append(integer_werts)

        if len(words) >= 100:
            await interaction.response.send_message(f"Du hast die maximale Anzahl von 100 Wörtern erreicht.\n"
                                                    f"> Weitere Wörter kannst du hinzufügen in dem du [hier](https://top.gg/bot/1097176283198279820) Votest!",
                                                    ephemeral=True)
        if str(self.children[0].value) in words:
            await interaction.response.send_message(
                f"Das Wort `{self.children[0].value}` ist bereits in der Datenbank eingetragen.",
                ephemeral=True)
            return
        elif not str(self.children[0].value) in words:
            embed = discord.Embed(
                title="Ein neues Blacklist Wort hinzugefügt",
                description=f"`{self.children[0].value}` wurde zur liste hinzugefügt",
                color=0x2b2d31
            )
            if interaction.guild.icon is not None:
                embed.set_thumbnail(url=interaction.guild.icon.url)
            await interaction.response.send_message(embed=embed, ephemeral=True)
            sql = f'INSERT INTO blacklist_words(guild_id, word) VALUES(?,?)'
            val = (interaction.guild.id, self.children[0].value)
            cursor.execute(sql, val)
        blacklist_db.commit()
