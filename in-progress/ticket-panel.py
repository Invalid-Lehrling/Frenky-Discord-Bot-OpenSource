import datetime

import discord
from discord.ext import commands
import sqlite3

ticket_db = sqlite3.connect("sql-databases/ticket.sqlite")


class ticket_modul(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    panel = discord.SlashCommandGroup("panel")

    @discord.slash_command(
        name="open",
        description="📌 × Gewehe dir einen Einblick in dein Ticket Panel."
    )
    @commands.has_permissions(administrator=True)
    async def _open_panel(self, ctx):
        ticket_cursor = ticket_db.cursor()
        ticket_cursor.execute(
            f"SELECT guild_id, ticket_channel, ticket_text FROM ticket_setup WHERE guild_id = {ctx.guild.id}")
        ticket_result = ticket_cursor.fetchall()

        if ticket_result is None:
            embed = discord.Embed(
                title="Ticket Panel | Settings",
                description="Das Ticket-System ist auf diesem Server noch nicht eingerichtet,"
                            "also wenn du das System hier einrichten möchtest klicke unten auf den"
                            "Button und starte die Einrichtung.",
                color=0x5e63ea
            )
            embed.set_footer(text="Ticket Panel | Settings")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, view=start_einrichtung_button())


def setup(bot):
    bot.add_cog(ticket_modul(bot))


class start_einrichtung_button(discord.ui.View):
    @discord.ui.button(
        label="Einrichtung Starten",
        style=discord.ButtonStyle.blurple,
        emoji="<:fb_chat:1097549593052467290>"
    )
    async def start_einrichtung_callback(self, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel."
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden."
        )
        embed.add_field(
            name="Ticket Embed Beschreibung",
            value="None"
        )
        embed.add_field(
            name="Ticket Channel",
            value="None"
        )
        await interaction.edit_original_response(embed=embed)


class einrichtungs_buttons(discord.ui.View):
    @discord.ui.button(
        label="Ticket Channel Setzen",
        style=discord.ButtonStyle.blurple,
        emoji="<:fb_channel:1097500461491290132>"
    )
    async def einrichtungs_buttons_callback_1(self, button, interaction: discord.Interaction):
        ticket_cursor = ticket_db.cursor()
        ticket_cursor.execute(
            f"SELECT guild_id, ticket_channel, ticket_text FROM ticket_setup WHERE guild_id = {interaction.guild.id}")
        ticket_result = ticket_cursor.fetchall()

