import json
import sqlite3

import discord
from discord import Option
from discord.ext import commands
from datetime import datetime, time, timedelta
import discord
from discord.ext import commands
import asyncio
import random
import time
from discord.utils import format_dt

giveaway_db = sqlite3.connect("sql-databases/giveaway.sqlite")
with open("json-databases/giveaway.json", "r") as f:
    giveaway_entries = json.load(f)


class giveaway_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="gw-start",
        description="📌 × Starte die einrichtung eines neuen Gewinnspiels."
    )
    @commands.has_permissions(administrator=True)
    async def giveaway(self, ctx, channel: discord.TextChannel, dauer: Option(str, "Beispiel: 2d 1m", required=True),
                       preis: str, winners: int):

        cur = giveaway_db.cursor()
        result = cur.execute(
            f"SELECT channel_id, message_id, duration, winners, preis  FROM giveaway_setup WHERE guild_id = {ctx.guild.id}")
        result.fetchall()

        duration_parts = dauer.split()
        hours = 0
        minutes = 0
        days = 0
        seconds = 0

        for part in duration_parts:
            if part.endswith("h"):
                hours = int(part[:-1])
            elif part.endswith("m"):
                minutes = int(part[:-1])
            elif part.endswith("d"):
                days = int(part[:-1])
            elif part.endswith("s"):
                seconds = int(part[:-1])

        duration_seconds = days * 24 * 3600 + hours * 3600 + minutes * 60 + seconds
        py_dt = int(time.time() + duration_seconds)

        # ------------------------------------------

        if duration_seconds < 0:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Die Zeit muss länger als 0 sein.", ephemeral=True)
        if winners == 0:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Bitte gib mindestens 1 Gewinner an.",
                              ephemeral=True)
        if winners > 10:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Die Gewinnerzahl darf nicht größer als 10 sein.",
                              ephemeral=True)

        # ------------------------------------------

        embed = discord.Embed(title=f"{preis}",
                              description="> Lese dir folgende Schritte & Infos durch, damit du weißt,\n> was du bei diesem Gewinnspiel machen musst\n> und/ob es Nedingungen gibt!",
                              color=0x5e63ea)

        embed.add_field(name="⠀",
                        value="<:fb_information:1097190720038764695> › sehe mit `/profile` deine aktuellen Statistiken ein!",
                        inline=False)

        embed.add_field(name="Giveaway Infos",
                        value=f"<:farbe_5e63ea:1115288310282199181> Endet: <t:{py_dt}:R> [<t:{py_dt}:F>]\n"
                              f"<:farbe_5e63ea:1115288310282199181> Gestartet von: {ctx.author.mention}\n"
                              f"<:farbe_5e63ea:1115288310282199181> Gewinner: **{winners}**",
                        inline=False
                        )

        embed.add_field(name="Bedingungen",
                        value="**›** Klicke auf <:fb_gewinnspiel:1097456715928178749> um am Gewinnspiel teilzunehmen.")

        embed.set_footer(text=f"Neues Gewinnspiel",
                         icon_url="https://cdn.discordapp.com/emojis/853941965547503626.gif?size=80")

        embed.timestamp = datetime.now()

        msg = await channel.send(embed=embed, view=teilnahme_view())
        # ---------------------

        giveaway_entries[str(ctx.guild.id)] = {}
        giveaway_entries[str(ctx.guild.id)][int(msg.id)] = {
            "Teilnehmer": []
        }

        sql = 'INSERT INTO giveaway_setup(guild_id, channel_id, message_id, duration, winners, preis) VALUES(?,?,?,?,?,?)'
        val = (ctx.guild.id, channel.id, msg.id, duration_seconds, winners, preis)
        result.execute(sql, val)
        giveaway_db.commit()

        with open("json-databases/giveaway.json", "w") as f:
            json.dump(giveaway_entries, f, indent=4)

        # ----------------------

        users = giveaway_entries[str(ctx.guild.id)][msg.id]["Teilnehmer"]

        await ctx.respond("Gewinnspiel Gestartet", ephemeral=True)

        await asyncio.sleep(duration_seconds)

        if len(users) == 0:
            error = discord.Embed(description=f"Niemand hat an diesem Gewinnspiel teilgenommen.", color=0x5e63ea)
            await msg.edit(embed=error, view=None)
            return

        winner_ids = random.sample(users, winners)
        for winner_id in winner_ids:
            user = await self.bot.fetch_user(winner_id)
            winner_mentions = [f"<@{winner_id}>" for winner_id in winner_ids]

            embed = discord.Embed(
                title="Gewinnspiel ist Vorbei",
                color=0x5e63ea
            )
            embed.add_field(
                name="Gewinnspiel Infos",
                value=f"<:farbe_5e63ea:1115288310282199181> Preis: **{preis}**\n"
                      f"<:farbe_5e63ea:1115288310282199181> Gewinner: {','.join(winner_mentions)}\n"
                      f"<:farbe_5e63ea:1115288310282199181> Gestartet von: {ctx.author.mention}\n"
                      f"<:farbe_5e63ea:1115288310282199181> Teilnehmer: **{len(users)}**"
            )
            button = discord.ui.Button(label="Gewinnspiel Beendet",
                                       style=discord.ButtonStyle.grey,
                                       disabled=True)

            view = discord.ui.View()
            view.add_item(button)

            await msg.edit(embed=embed, view=view)

            await msg.reply(
                content=f'<:fb_gewinnspiel:1097456715928178749> **Herzlichen Glückwunsch an:** {",".join(winner_mentions)} du/ihr hast/habt den Preis **{preis}** gewonnen!')

            embed = discord.Embed(title="<a:party_blue:913078356172492800> › Gewinnspiel vorbei",
                                  description=f"> Du hast ein Gewinnspiel gewonnen!", color=0x5245C2)
            embed.add_field(name="\n\n<a:infoT:914834531096363039> __Info:__",
                            value=f"<:pfeil_blau:914246277309558825> **Server:** [{ctx.guild.name}](https://canary.discord.com/channels/865251517832626176/{channel.id})\n<:pfeil_blau:914246277309558825> **Gewinnspiel:** [Gewinnspiel-ID](https://canary.discord.com/channels/{ctx.guild.id}/{channel.id}/{msg.id})\n<:pfeil_blau:914246277309558825> Preis: `{preis}`")
            await user.send(embed=embed)


################################################################


def setup(bot):
    bot.add_cog(giveaway_module(bot))

class teilnahme_view(discord.ui.View):
    @discord.ui.button(
        label="Teilnehmen",
        style=discord.ButtonStyle.blurple,
        emoji="<:fb_gewinnspiel:1097456715928178749>"
    )
    async def teilnahme_callback(self, button, interaction: discord.Interaction):
        user_list = giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"]

        if interaction.user.id in user_list:
            await interaction.response.send_message(
                "<:fb_warn:1097213764396384409> **›** Du nimmst bereits an diesem **Gewinnspiel** teil. "
                "Wenn du die Teilnahme abbrechen willst klicke **Teilnahme entfernen** auf den Button.", ephemeral=True)
        elif interaction.user.id not in user_list:
            await interaction.response.send_message(
                "<:fb_yes:1097215591183548557> **›** Du nimmst erfolgreich an diesem Gewinnspiel teil.",
                ephemeral=True)
            giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"].append(
                interaction.user.id)

        with open("json-databases/giveaway.json", "w") as f:
            json.dump(giveaway_entries, f, indent=4)

    @discord.ui.button(
        label="Teilnahme entfernen",
        style=discord.ButtonStyle.red,
    )
    async def teilnahme_entfernen_callback(self, button, interaction: discord.Interaction):
        user_list = giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"]

        if interaction.user.id not in user_list:
            await interaction.response.send_message(
                "<:fb_warn:1097213764396384409> **›** Du nimmst an diesem Gewinnspiel nicht teil.", ephemeral=True)
        elif interaction.user.id in user_list:
            await interaction.response.send_message(
                "<:fb_yes:1097215591183548557> **›** Teilnahme erfolgreich entfernt.",
                ephemeral=True)
            giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"].remove(
                interaction.user.id)

        with open("json-databases/giveaway.json", "w") as f:
            json.dump(giveaway_entries, f, indent=4)
