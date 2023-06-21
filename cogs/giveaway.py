import asyncio
import json
import random
import sqlite3
import time
from datetime import datetime

import discord
from discord import Option
from discord.ext import commands

messages_db = sqlite3.connect("sql-databases/messages.sqlite")
giveaway_db = sqlite3.connect("sql-databases/giveaway.sqlite")
voice_db = sqlite3.connect("sql-databases/voice.sqlite")


class giveaway_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    giveaway = discord.SlashCommandGroup("giveaway", "gw")

    @giveaway.command(
        name="start",
        description="🎉 × Starte die einrichtung eines neuen Gewinnspiels."
    )
    @commands.has_permissions(administrator=True)
    async def _giveaway_start(self, ctx, channel: discord.TextChannel,
                              dauer: Option(str, "Beispiel: 2d 1m", required=True),
                              preis: str, winners: int):

        cur = giveaway_db.cursor()
        result = cur.execute(
            f"SELECT channel_id, message_id, duration, winners, preis  FROM giveaway_setup WHERE guild_id = {ctx.guild.id}")
        res = result.fetchall()

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

        if duration_seconds <= 0:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Die Zeit muss länger als 0 sein.",
                              ephemeral=True)
            return
        if winners == 0:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Bitte gib mindestens 1 Gewinner an.",
                              ephemeral=True)
            return
        if winners > 10:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Die Gewinnerzahl darf nicht größer als 10 sein.",
                ephemeral=True)
            return

        num = random.randint(1000000000, 9999999999)

        sql = 'INSERT INTO giveaway_setup(guild_id, channel_id, message_id, duration, giveaway_id, winners, preis) VALUES(?,?,?,?,?,?,?)'
        val = (ctx.guild.id, channel.id, 0, duration_seconds, num, winners, preis)
        result.execute(sql, val)
        giveaway_db.commit()

        embeds = discord.Embed(
            title="Gewinnspiel | Einrichtung",
            description="> *Richtie hier wenn du sie benötigst ein, ob du Bedingungen für dieses Gewinnspiel setzen möchtest.*\n>"
                        " Wenn du keine Setzen möchtest klicke auf den Button",
            color=0x2b2d31
        )
        embeds.add_field(
            name="Giveaway-Channel",
            value=f"{channel.mention}"
        )
        embeds.add_field(
            name="Giveaway-Dauer",
            value=f"`{dauer}`"
        )
        embeds.add_field(
            name="Giveaway-Preis",
            value=f"**{preis}**"
        )
        embeds.add_field(
            name="Giveaway-Winners",
            value=f"**{winners}**"
        )

        einrichtungs_select = discord.ui.Select(
            placeholder="Wähle eine Option",
            options=[
                discord.SelectOption(
                    label="Benötigte Nachrichten",
                    value="msg"
                ),
                discord.SelectOption(
                    label="Benötigte Voice Zeit",
                    value="voice"
                ),
                discord.SelectOption(
                    label="Benötigte Rolle",
                    value="role"
                ),
                discord.SelectOption(
                    label="Darf Kein Nitro haben",
                    value="nitro"
                ),
                discord.SelectOption(
                    label="Custom Bedingung",
                    value="cb"
                ),
            ]
        )

        giveaway_start_button = discord.ui.Button(
            label="Giveaway Starten",
            style=discord.ButtonStyle.blurple
        )

        msgs_modal = discord.ui.Modal(title="Nachrichten Anzahl")
        msgs_modal.add_item(
            discord.ui.InputText(
                label="Nachrichten Anzahl",
                placeholder="Nachrichten...",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True
            )
        )

        voice_modal = discord.ui.Modal(title="Voice Zeit")
        voice_modal.add_item(
            discord.ui.InputText(
                label="Voice Zeit",
                placeholder="Beispiel: 1h 2m 5s",
                style=discord.InputTextStyle.short,
                min_length=1,
                required=True
            )
        )

        async def msgs_modal_callback(interaction: discord.Interaction):
            if int(msgs_modal.children[0].value) <= 0:
                await interaction.response.send_message(
                    "<:fb_warn:1097213764396384409> **›**  Die Anzahl der Nachrichten muss größer als 0 sein.",
                    ephemeral=True
                )
            else:
                embed = discord.Embed(
                    title="Nachrichten Bedingung gesetzt",
                    description=f"Du hast die Bedingungen für dieses Gewinnspiel auf `{msgs_modal.children[0].value}` Nachrichten"
                                f"gesetzt.",
                    color=0x2b2d31
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                sqls = f'UPDATE giveaway_setup SET msgs = ? WHERE guild_id = {interaction.guild.id} AND channel_id = {channel.id} AND giveaway_id = {num}'
                value = (int(msgs_modal.children[0].value),)
                result.execute(sqls, value)
                giveaway_db.commit()

        async def voice_modal_callback(interaction: discord.Interaction):
            duration_part = voice_modal.children[0].value.split()
            h = 0
            m = 0
            d = 0
            s = 0

            for parts in duration_part:
                if parts.endswith("h"):
                    h = int(parts[:-1])
                elif parts.endswith("m"):
                    m = int(parts[:-1])
                elif parts.endswith("d"):
                    d = int(parts[:-1])
                elif parts.endswith("s"):
                    s = int(parts[:-1])

            duration_second = d * 24 * 3600 + h * 3600 + m * 60 + s

            if duration_second <= 0:
                await interaction.response.send_message(
                    "<:fb_warn:1097213764396384409> **›**  Die Anzahl der Zeit muss größer als 0 sein.",
                    ephemeral=True
                )
            else:
                embed = discord.Embed(
                    title="Voice Zeit Bedingung gesetzt",
                    description=f"Du hast die Bedingungen für dieses Gewinnspiel auf `{h}h : {m}m : {s}s`"
                                f"gesetzt.",
                    color=0x2b2d31
                )
                await interaction.response.send_message(embed=embed, ephemeral=True)
                sqls = f'UPDATE giveaway_setup SET voice_time = ? WHERE guild_id = {interaction.guild.id} AND channel_id = {channel.id} AND giveaway_id = {num}'
                value = (int(duration_second),)
                result.execute(sqls, value)
                giveaway_db.commit()

        async def role_callback(interaction: discord.Interaction):
            return

        async def einrichtungs_callback(interaction: discord.Interaction):
            if "msg" in interaction.data["values"]:
                await interaction.response.send_modal(msgs_modal)
            if "voice" in interaction.data["values"]:
                await interaction.response.send_modal(voice_modal)
            if "role" in interaction.data["values"]:
                e_embed = discord.Embed(
                    title="Gewinnspiel | Einrichtung",
                    description="Gib die **ID** einer Role ein, welche als Bedingung gesetzt werden soll.",
                    color=0x2b2d31
                )

                v = discord.ui.View(timeout=None)

                role_select = discord.ui.role_select()

                await interaction.response.send_message(embed=e_embed, ephemeral=True, view=role_select)

                role_select.callback = role_callback

            if "nonitro" in interaction.data["values"]:
                return
            if "cb" in interaction.data["values"]:
                return
            if "kb" in interaction.data["values"]:
                return

        async def giveaway_start_callback(interaction: discord.Interaction):

            cursor = giveaway_db.cursor()
            erg = cursor.execute(
                f"SELECT msgs, role, no_nitro, voice_time, custom FROM giveaway_setup WHERE guild_id = {ctx.guild.id} AND giveaway_id = {num}")
            reqs = erg.fetchone()

            requirement_list = []

            if reqs[0] is not None:
                req = f"<:farbe_5e63ea:1097925629850177626> Nachrichten: **{reqs[0]}**\n"
                requirement_list.append(req)

            if reqs[3] is not None:
                hours = int(reqs[3]) // 3600
                minutes = (int(reqs[3]) % 3600) // 60
                seconds = int(reqs[3]) % 60

                req = f"<:farbe_5e63ea:1097925629850177626> Voice Zeit: **{hours}h** : **{minutes}m** : **{seconds}s**\n"
                requirement_list.append(req)

            requirement_list.append(
                "\n**›** Klicke auf <:fb_gewinnspiel:1115530409380429824> um am Gewinnspiel teilzunehmen.")

            giveaway_start_button.disabled = True

            embed = discord.Embed(
                title="Einrichtung Abgeschlossen",
                description=f"Das __Gewinnspiel__ wurde erfolgreich in {channel.mention} erstellt.",
                color=0x2b2d31
            )
            await interaction.response.send_message(embed=embed, ephemeral=True)

            # ------------------------------------------------------------------------------------------------------------------

            gw_embed = discord.Embed(title=f"{preis}",
                                     description="> *Lese dir folgende Schritte & Infos durch, damit du weißt,*\n> *was du bei diesem Gewinnspiel machen musst*\n> *und/ob es Bedingungen gibt!*",
                                     color=0x2b2d31)

            gw_embed.add_field(name="⠀",
                               value="<:fb_information:1115530377457573939> › siehe mit </stats user:1120687800463933440> deine aktuellen Statistiken ein!",
                               inline=False)

            gw_embed.add_field(name="Giveaway Infos",
                               value=f"<:fb_pfeil:1120710076957724672> Endet: <t:{py_dt}:R> [<t:{py_dt}:F>]\n"
                                     f"<:fb_pfeil:1120710076957724672> Gestartet von: {ctx.author.mention}\n"
                                     f"<:fb_pfeil:1120710076957724672> Gewinner: **{winners}**",
                               inline=False
                               )

            gw_embed.add_field(name="Bedingungen",
                               value=f"{' '.join(requirement_list)}")

            gw_embed.set_footer(text=f"Neues Gewinnspiel",
                                icon_url="https://cdn.discordapp.com/emojis/853941965547503626.gif?size=80")

            gw_embed.timestamp = datetime.now()

            msg = await channel.send(embed=gw_embed, view=teilnahme_view(timeout=None))

            # ------------------------------------------------------------------------------------------------------------------

            sqls = f'UPDATE giveaway_setup SET message_id = ? WHERE guild_id = {interaction.guild.id} AND channel_id = {channel.id} AND giveaway_id = {num}'
            value = (int(msg.id),)  # Tupel mit einem Element erstellen
            result.execute(sqls, value)
            giveaway_db.commit()

            # ------------------------------------------------------------------------------------------------------------------

            await ctx.respond("Gewinnspiel Gestartet", ephemeral=True)

            await asyncio.sleep(duration_seconds)

            cur14 = giveaway_db.cursor()
            result1 = cur14.execute(
                f"SELECT user_id FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}")
            res = result1.fetchall()

            user_ids = []
            for entries in res:
                integer_wert = ', '.join(map(str, entries))
                user_ids.append(integer_wert)

            if len(user_ids) == 0:
                cursor = giveaway_db.cursor()
                error = discord.Embed(description=f"Es hat niemand an diesem Gewinnspiel Teilgenommen", color=0x2b2d31)
                error.set_footer(text="Giveaway Beendet", icon_url=ctx.guild.icon.url)
                error.timestamp = datetime.now()
                await msg.edit(embed=error, view=None)
                cursor.execute(
                    f"DELETE FROM giveaway_setup WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id} AND message_id = {msg.id} AND giveaway_id = {num}")
                return

            winner_ids = random.sample(user_ids, winners)
            for winner_id in winner_ids:
                user = await self.bot.fetch_user(winner_id)
                winner_mentions = [f"<@{winner_id}>" for winner_id in winner_ids]
                gw_embed = discord.Embed(
                    title="Gewinnspiel ist Vorbei",
                    description="<:fb_link:1097554647637561445> **›** Lade den Bot [`hier`](https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands) ein",
                    color=0x2b2d31
                )
                gw_embed.add_field(
                    name="Gewinnspiel Infos",
                    value=f"**»** Preis: **{preis}**\n"
                          f"**»** Gewinner: {','.join(winner_mentions)}\n"
                          f"**»** Gestartet von: {ctx.author.mention}\n"
                          f"**»** Teilnehmer: **{len(user_ids)}**"
                )
                button = discord.ui.Button(
                    label="Gewinnspiel Beendet",
                    style=discord.ButtonStyle.grey,
                    disabled=True
                )

                view = discord.ui.View()
                view.add_item(button)

                await msg.edit(embed=gw_embed, view=view)

                await msg.reply(
                    content=f'<:fb_gewinnspiel:1097456715928178749> **Herzlichen Glückwunsch** {",".join(winner_mentions)} du/ihr hast/habt den Preis **{preis}** gewonnen!'
                            f'\n> <:fb_level:1115536399052066816> **›** Es haben insgesamt `{len(user_ids)}` User teilgenommen.')

                gw_embed = discord.Embed(
                    title="Gewinnspiel Gewonnen",
                    description="Herzlichen Glückwunsch, sie haben ein Gewinnspiel auf einem Server Gewonnen.",
                    color=0x2b2d31
                )
                gw_embed.add_field(
                    name="Gewinnspiel - Informationen",
                    value=f"<:farbe_5e63ea:1115288310282199181> Preis: **{preis}**\n"
                          f"<:farbe_5e63ea:1115288310282199181> Server: **{ctx.guild.name}**\n"
                          f"<:farbe_5e63ea:1115288310282199181> Gewinnspiel: {msg.jump_url}"
                )
                gw_embed.set_footer(
                    text="Gewinnspiel Gewonnen",
                    icon_url=ctx.guild.icon.url
                )
                gw_embed.timestamp = datetime.now()
                await user.send(embed=gw_embed)

                await asyncio.sleep(172800)

                cursor = giveaway_db.cursor()
                cursor.execute(
                    f"DELETE FROM giveaway_setup WHERE guild_id = {ctx.guild.id} AND channel_id = {channel.id} AND message_id = {msg.id} AND giveaway_id = {num}")
                cursor.execute(
                    f"DELETE FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}"
                )

        giveaway_db.commit()

        voice_modal.callback = voice_modal_callback
        msgs_modal.callback = msgs_modal_callback
        giveaway_start_button.callback = giveaway_start_callback
        einrichtungs_select.callback = einrichtungs_callback

        view = discord.ui.View()
        view.add_item(einrichtungs_select)
        view.add_item(giveaway_start_button)

        await ctx.respond(embed=embeds, ephemeral=True, view=view)

    @giveaway.command(
        name="end",
        description="❌ × Beende ein aktuell laufendes Gewinnspiel."
    )
    @commands.has_permissions(administrator=True)
    async def _giveaway_end(self, ctx, giveaway_id):
        msg = self.bot.get_message(int(giveaway_id))

        cur14 = giveaway_db.cursor()
        result1 = cur14.execute(
            f"SELECT user_id FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}")
        res = result1.fetchall()

        ress = cur14.execute(f"SELECT message_id FROM giveaway_setup WHERE guild_id = {ctx.guild.id}")
        resu = ress.fetchall()

        erg = cur14.execute(
            f"SELECT winners, preis FROM giveaway_setup WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}")
        ergs = erg.fetchone()

        giveaway_ids = []

        for entries in resu:
            integer_wert = ', '.join(map(str, entries))
            giveaway_ids.append(integer_wert)

        if res is None:
            await ctx.respond("An diesem Gewinnspiel hat niemand Teilgenommen.",
                              ephemeral=True)
        if giveaway_id not in giveaway_ids:
            await ctx.respond("Diese ID existiert nicht oder ist kein Gewinnspiel.",
                              ephemeral=True)
        elif giveaway_id in giveaway_ids:
            winners = ergs[0]
            user_ids = []

            for entries in res:
                integer_werts = ', '.join(map(str, entries))
                user_ids.append(integer_werts)

            print(winners)

            winner_ids = random.sample(user_ids, winners)
            for winner_id in winner_ids:
                user = await self.bot.fetch_user(winner_id)

                cur14.execute(
                    f"DELETE FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id} AND user_id = {user.id}")

                winner_mentions = [f"<@{winner_id}>" for winner_id in winner_ids]

                gw_embed = discord.Embed(
                    title="Gewinnspiel ist Vorbei",
                    description="<:fb_link:1097554647637561445> **›** Lade den Bot [`hier`](https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands) ein",
                    color=0x2b2d31
                )
                gw_embed.add_field(
                    name="Gewinnspiel Infos",
                    value=f"<:farbe_5e63ea:1115288310282199181> Preis: **{ergs[1]}**\n"
                          f"<:farbe_5e63ea:1115288310282199181> Gewinner: {','.join(winner_mentions)}\n"
                          f"<:farbe_5e63ea:1115288310282199181> Gestartet von: {ctx.author.mention}\n"
                          f"<:farbe_5e63ea:1115288310282199181> Teilnehmer: **{len(user_ids)}**"
                )
                button = discord.ui.Button(
                    label="Gewinnspiel Beendet",
                    style=discord.ButtonStyle.grey,
                    disabled=True
                )

                view = discord.ui.View(timeout=None)
                view.add_item(button)

                await msg.edit(embed=gw_embed, view=view)
                await msg.reply(
                    content=f'<:fb_gewinnspiel:1097456715928178749> **Herzlichen Glückwunsch** {",".join(winner_mentions)} du/ihr hast/habt den Preis **{ergs[0]}** gewonnen!'
                            f'\n> <:fb_level:1115536399052066816> **›** Es haben insgesamt `{len(user_ids)}` User teilgenommen.')

                gw_embed = discord.Embed(
                    title="Gewinnspiel Gewonnen",
                    description="Herzlichen Glückwunsch, sie haben ein Gewinnspiel auf einem Server Gewonnen.",
                    color=0x2b2d31
                )
                gw_embed.add_field(
                    name="Gewinnspiel - Informationen",
                    value=f"<:farbe_5e63ea:1115288310282199181> Preis: **{ergs[0]}**\n"
                          f"<:farbe_5e63ea:1115288310282199181> Server: **{ctx.guild.name}**\n"
                          f"<:farbe_5e63ea:1115288310282199181> Gewinnspiel: {msg.jump_url}"
                )
                gw_embed.set_footer(
                    text="Gewinnspiel Gewonnen",
                    icon_url=ctx.guild.icon.url
                )
                gw_embed.timestamp = datetime.now()
                await user.send(embed=gw_embed)
                await ctx.respond("<:fb_gewinnspiel:1097456715928178749> **›** Du hast das Gewinnspiel erfolgreich beendet.",
                                  ephemeral = True)
                cur14 = giveaway_db.cursor()
                cur14.execute(
                    f"DELETE FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id} AND user_id = {user.id}")
            giveaway_db.commit()

    @giveaway.command(
        name="delete",
        description="🗑 × Lösche ein ausgewähltes Gewinnspiel."
    )
    @commands.has_permissions(administrator=True)
    async def _giveaway_delete(self, ctx, giveaway_id):
        cursor = giveaway_db.cursor()
        res = cursor.execute(f"SELECT message_id FROM giveaway_setup WHERE guild_id = {ctx.guild.id}")
        results = res.fetchall()

        giveaway_ids = []
        for entries in results:
            integer_wert = ', '.join(map(str, entries))
            giveaway_ids.append(integer_wert)

        if giveaway_id not in giveaway_ids:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Diese Message ID ist kein Gewinnspiel",
                ephemeral=True
            )
        elif giveaway_id in giveaway_ids:

            embed = discord.Embed(
                title="Gewinnspiel wurde gelöscht",
                description=f"Du hast das Gewinnspiel `{giveaway_id}` erfolgreich gelöscht",
                color=0x2b2d31
            )
            await ctx.respond(embed=embed, ephemeral=True)

            msg = self.bot.get_message(int(giveaway_id))
            await msg.delete()

            cursor.execute(
                f"DELETE FROM giveaway_setup WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}")
            cursor.execute(
                f"DELETE FROM giveaway_entries WHERE guild_id = {ctx.guild.id} AND message_id = {msg.id}")
        giveaway_db.commit()


# ------------------------------------------------------------------------------------------------------------------


def setup(bot):
    bot.add_cog(giveaway_module(bot))


class teilnahme_view(discord.ui.View):
    @discord.ui.button(
        label="Teilnehmen",
        style=discord.ButtonStyle.blurple,
        emoji="<:fb_gewinnspiel:1097456715928178749>"
    )
    async def teilnahme_callback(self, button, interaction: discord.Interaction):
        req_cursor = giveaway_db.cursor()
        req_result = req_cursor.execute(
            f"SELECT msgs, no_nitro, role, voice_time, custom FROM giveaway_setup WHERE guild_id = {interaction.guild.id} AND message_id = {interaction.message.id}"
        )
        requirements = req_result.fetchone()

        cur1 = giveaway_db.cursor()
        result1 = cur1.execute(
            f"SELECT user_id FROM giveaway_entries WHERE guild_id = {interaction.guild.id} AND message_id = {interaction.message.id}")
        res = result1.fetchone()

        cur2 = messages_db.cursor()
        result2 = cur2.execute(
            f"SELECT messages FROM message_count WHERE guild_id = {interaction.guild.id} AND user_id = {interaction.user.id}")
        msgs = result2.fetchone()

        voice_req = requirements[3]
        msgs_req = requirements[0]
        no_nitro_req = requirements[1]
        role_req = requirements[2]

        if res is not None:
            await interaction.response.send_message(
                "<:fb_warn:1097213764396384409> **›** Du nimmst bereits an diesem **Gewinnspiel** teil. "
                "Wenn du die Teilnahme abbrechen willst klicke **Teilnahme entfernen** auf den Button.",
                ephemeral=True)
        elif res is None:
            if msgs_req is not None:
                if msgs[0] < msgs_req:
                    await interaction.response.send_message(
                        f"<:fb_warn:1097213764396384409> **›** Du hast nicht genügend nachrichten. `({msgs[0]}/{msgs_req})`",
                        ephemeral=True
                    )
            await interaction.response.send_message(
                "<:fb_yes:1097215591183548557> **›** Du nimmst erfolgreich an diesem Gewinnspiel teil.",
                ephemeral=True)
            sql = f'INSERT INTO giveaway_entries(guild_id, message_id, user_id) VALUES (?,?,?)'
            val = (interaction.guild.id, interaction.message.id, interaction.user.id)
            result1.execute(sql, val)
            giveaway_db.commit()

    # ------------------------------------------------------------------------------------------------------------------

    @discord.ui.button(
        label="Teilnahme entfernen",
        style=discord.ButtonStyle.red,
    )
    async def teilnahme_entfernen_callback(self, button, interaction: discord.Interaction):
        # user_list = giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"]
        #
        # if interaction.user.id not in user_list:
        #     await interaction.response.send_message(
        #         "<:fb_warn:1097213764396384409> **›** Du nimmst an diesem Gewinnspiel nicht teil.", ephemeral=True)
        # elif interaction.user.id in user_list:
        #     await interaction.response.send_message(
        #         "<:fb_yes:1097215591183548557> **›** Teilnahme erfolgreich entfernt.",
        #         ephemeral=True)
        #     giveaway_entries[str(interaction.guild.id)][interaction.message.id]["Teilnehmer"].remove(
        #         interaction.user.id)
        #
        # with open("json-databases/giveaway.json", "w") as f:
        #     json.dump(giveaway_entries, f, indent=4)
        return

    # ------------------------------------------------------------------------------------------------------------------
