import asyncio
import datetime
import sqlite3

import discord
from discord import Option
from discord.ext import commands

messages_db = sqlite3.connect("sql-databases/messages.sqlite")
voice_db = sqlite3.connect("sql-databases/voice.sqlite")


class messages_counter_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    stats = discord.SlashCommandGroup("stats")

    @commands.Cog.listener()
    async def on_message(self, message):
        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id FROM message_count WHERE guild_id = ? AND user_id = ?",
            (message.guild.id, message.author.id)
        )
        result = cur.fetchone()

        if message.author.bot:
            return
        else:
            if message.content.startswith('-'):
                return
            if result is None:
                sql = "INSERT INTO message_count(guild_id, user_id, messages) VALUES(?,?,?)"
                val = (message.guild.id, message.author.id, 1)
                cursor.execute(sql, val)
            else:
                sql = "UPDATE message_count SET messages = messages + 1 WHERE guild_id = ? AND user_id = ?"
                val = (message.guild.id, int(message.author.id))
                cursor.execute(sql, val)
            messages_db.commit()
            await self.bot.process_commands(message)

    @stats.command(
        name="voice",
        description="🔊 × Lese die Voice Statistik eines Users ein"
    )
    async def _voice_time(self, ctx, member: discord.Member):
        cursor = voice_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id, voice_time FROM voice_count WHERE guild_id = ? AND user_id = ?",
            (member.guild.id, member.id)
        )
        result = cur.fetchone()
        if member.id not in result:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Dieser User ist nicht in der Datenbank eingetragen.",
                ephemeral=True)
        if member.id in result:
            secs_in_time = datetime.timedelta(seconds=result[1])
            hours = secs_in_time.total_seconds() // 3600
            minutes = (secs_in_time.total_seconds() % 3600) // 60
            seconds = secs_in_time.total_seconds() % 60

            embed = discord.Embed(
                description=f"{member.mention} hat insgesamt **{int(hours)}h {int(minutes)}min {int(seconds)}s** im Voice verbracht.",
                color=0x2b2d31
            )
            embed.set_author(name=f"Voice Zeit von {member.name}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.respond(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        cursor = voice_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id FROM voice_count WHERE guild_id = ? AND user_id = ?",
            (member.guild.id, member.id)
        )
        result = cur.fetchone()

        if member.bot:
            return
        if result is None:
            voice_join_time = 0
            sql = "INSERT INTO voice_count(guild_id, user_id, voice_time) VALUES(?,?,?)"
            val = (member.guild.id, member.id, voice_join_time)
            cursor.execute(sql, val)
        elif result is not None:
            await asyncio.sleep(60)
            sql = "UPDATE voice_count SET voice_time = voice_time + 1 WHERE guild_id = ? AND user_id = ?"
            val = (member.guild.id, member.id)
            cursor.execute(sql, val)
        voice_db.commit()

    # ------------------------------------------------------------------------------------------------------------------

    @stats.command(
        name="reset",
        description="📛 × Setze die Nachrichten oder Voice Zeit eines Nutzers zurück."
    )
    async def _stats_reset_user(self, ctx, member: discord.Member, kategorie: Option(str, "Wähle eine Option",
                                                                                     choices=["🔊 × Voice Zeit",
                                                                                              "💬 × Nachrichten"])):
        if kategorie == "💬 × Nachrichten":
            cursor = messages_db.cursor()
            cur = cursor.execute(
                f"SELECT user_id FROM message_count WHERE guild_id = {ctx.guild.id}",
            )
            res = cur.fetchall()

            user_ids = []

            for entries in res:
                integer_wert = ', '.join(map(str, entries))
                user_ids.append(int(integer_wert))

            if member.id not in user_ids:
                await ctx.respond(
                    "<:fb_warn:1097213764396384409> **›** Dieser Nutzer ist nicht in der Datenbank eingetragen.",
                    ephemeral=True)

            elif member.id in user_ids:

                cursor.execute(f"DELETE FROM message_count WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}")

                embed = discord.Embed(
                    title="Nachrichten zurückgesetzt | Frenky",
                    description=f"Du hast die Nachrichten von **{member.name}** auf 0 gesetzt.",
                    color=0x2b2d31
                )
                await ctx.respond(embed=embed, ephemeral=True)

                messages_db.commit()

        if kategorie == "🔊 × Voice Zeit":
            cursor = voice_db.cursor()
            cur = cursor.execute(
                f"SELECT user_id FROM voice_count WHERE guild_id = {ctx.guild.id}",
            )
            res = cur.fetchall()

            user_ids = []

            for entries in res:
                integer_wert = ', '.join(map(str, entries))
                user_ids.append(int(integer_wert))

            if member.id not in user_ids:
                await ctx.respond(
                    "<:fb_warn:1097213764396384409> **›** Dieser Nutzer ist nicht in der Datenbank eingetragen.",
                    ephemeral=True)
            cursor.execute(f"DELETE FROM voice_count WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}")

            embed = discord.Embed(
                title="Voice Zeit zurückgesetzt | Frenky",
                description=f"Du hast die Voice Zeit von **{member.name}** zurückgesetzt.",
                color=0x2b2d31
            )
            await ctx.respond(embed=embed, ephemeral=True)

            voice_db.commit()

    # ------------------------------------------------------------------------------------------------------------------

    @stats.command(
        name="messages",
        description="💬 × Lese die Voice Statistik eines Users ein."
    )
    async def _messages(self, ctx, member: discord.Member):
        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id, messages FROM message_count WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}",
        )
        result = cur.fetchone()

        if not member.id in result:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Dieser User ist nicht in der Datenbank eingetragen.",
                ephemeral=True)
        if member.id in result:
            embed = discord.Embed(
                description=f"{member.mention} hat insgesamt **{result[1]}** Nachrichten geschrieben.",
                color=0x2b2d31
            )
            embed.set_author(name=f"Nachrichten von {member.name}")
            embed.set_thumbnail(url=member.display_avatar.url)
            await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        name="leaderboard",
        description="🏆 × Lass dir die Bestenliste des Servers anzeigen."
    )
    async def _leaderboard(self, ctx, kategorie: Option(str, "Wähle eine Kategorie",
                                                        choices=["💬 × Nachrichten", "🔊 × Voice Zeit"])):
        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id, messages FROM message_count WHERE guild_id = {ctx.guild.id} ORDER BY messages DESC"
        )
        results = cur.fetchall()

        cursors = voice_db.cursor()
        curf = cursors.execute(
            f"SELECT user_id, voice_time FROM voice_count WHERE guild_id = {ctx.guild.id} ORDER BY voice_time DESC")
        result = curf.fetchall()

        if not results:
            await ctx.respond("Es gibt keine Daten im Leaderboard.", ephemeral=True)
            return

        start_index = (1 - 1) * 10
        end_index = start_index + 10
        paginated_results = results[start_index:end_index]
        paginated_results2 = result[start_index:end_index]

        embed = discord.Embed(color=0x2b2d31)

        if kategorie == "💬 × Nachrichten":
            embed.title = "Nachrichten Leaderboard"
            rank = start_index + 1
            msg = ''
            for resulti in paginated_results:
                member = self.bot.get_user(resulti[0])
                if member:
                    if rank == 1:
                        msg += f"> 🏅 × {member.mention} | Nachrichten: `{resulti[1]}`\n"
                    elif rank == 2:
                        msg += f"> 🥈 × {member.mention} | Nachrichten: `{resulti[1]}`\n"
                    elif rank == 3:
                        msg += f"> 🥉 × {member.mention} | Nachrichten: `{resulti[1]}`\n⠀\n"
                    else:
                        msg += f"> `{rank}.` × {member.mention} | Nachrichten: `{resulti[1]}`\n"
                    embed.description = f"> Hier siehst du das Ranking, welches **die User** zeigt,\n> die die **meisten Nachrichten** haben!\n\n {msg}"
                    rank += 1

        if kategorie == "🔊 × Voice Zeit":
            embed.title = "Voice Zeit Leaderboard"
            rank = start_index + 1
            msg = ''
            for result in paginated_results2:
                member = self.bot.get_user(result[0])
                secs_in_time = datetime.timedelta(seconds=result[1])
                hours = secs_in_time.total_seconds() // 3600
                minutes = (secs_in_time.total_seconds() % 3600) // 60
                seconds = secs_in_time.total_seconds() % 60
                if member:
                    if rank == 1:
                        msg += f"> 🏅 × {member.mention} | Zeit: **{int(hours)}h {int(minutes)}min {int(seconds)}s**\n"
                    elif rank == 2:
                        msg += f"> 🥈 × {member.mention} | Zeit: **{int(hours)}h {int(minutes)}min {int(seconds)}s**\n"
                    elif rank == 3:
                        msg += f"> 🥉 × {member.mention} | Zeit: **{int(hours)}h {int(minutes)}min {int(seconds)}s**\n⠀\n"
                    else:
                        msg += f"> `{rank}.` × {member.mention} | Zeit: **{int(hours)}h {int(minutes)}min {int(seconds)}s**`n"
                    embed.description = f"> Hier siehst du das Ranking, welches **die User** zeigt,\n> welche die **meiste Zeit im Voice verbracht** haben!\n\n {msg}"
                    rank += 1

        embed.add_field(
            name="⠀",
            value=f"Leaderboard von `{ctx.guild.name}`",
            inline=False
        )

        total_pages = len(results) // 10 + 1
        current_page = start_index // 10 + 1
        page_indicator = f"Seite {current_page}/{total_pages}"

        view = discord.ui.View(timeout=None)

        previous_page = discord.ui.Button(
            label="◀",
            style=discord.ButtonStyle.blurple,
            custom_id="previous_page",
            disabled=current_page == 1
        )

        next_page = discord.ui.Button(
            label="▶",
            style=discord.ButtonStyle.blurple,
            custom_id="next_page",
            disabled=current_page == total_pages
        )

        page_indicator_button = discord.ui.Button(
            label=page_indicator,
            style=discord.ButtonStyle.blurple,
            custom_id="page_indicator",
            disabled=True
        )

        async def previous_page_callback(button, interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.message.edit(view=self.create_new_view(button.custom_id))

        async def next_page_callback(button, interaction: discord.Interaction):
            await interaction.response.defer()
            await interaction.message.edit(view=self.create_new_view(button.custom_id))

        previous_page.callback = previous_page_callback
        next_page.callback = next_page_callback

        view.add_item(previous_page)
        view.add_item(page_indicator_button)
        view.add_item(next_page)

        await ctx.respond(embed=embed, view=view, ephemeral=True)

    @stats.command(
        name="user",
        description="📊 × Zeigt die gesamten Statistiken eines Users."
    )
    async def _Stats_user(self, ctx, member: discord.Member):
        cursors = voice_db.cursor()
        curf = cursors.execute(
            f"SELECT voice_time FROM voice_count WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}")
        result = curf.fetchone()

        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT messages FROM message_count WHERE guild_id = {ctx.guild.id} AND user_id = {member.id}"
        )
        results = cur.fetchone()

        if result is None or results is None:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** Dieser Benutzer ist nicht in der Datenbank eingetragen.",
                ephemeral=True)

        secs_in_time = datetime.timedelta(seconds=result[0])
        hours = secs_in_time.total_seconds() // 3600
        minutes = (secs_in_time.total_seconds() % 3600) // 60
        seconds = secs_in_time.total_seconds() % 60

        embed = discord.Embed(
            description=f"Hier werden alle Statistiken von {member.mention} angezeigt.",
            color=0x2b2d31
        )
        embed.add_field(
            name="> __Statistiken__",
            value=f"<:fb_chat:1097412236005363823> **›** Nachrichten: **{results[0]}**\n"
                  f"<:fb_voice:1097500430071758978> **›** Voice Zeit: **{int(hours)}h {int(minutes)}min {int(seconds)}s**\n",
            inline=False
        )
        embed.add_field(
            name="> __Userinfo__",
            value=f"<:fb_home:1097194608871616634> **›** Mitglied seit: <t:{int(member.joined_at.timestamp())}:f> \n"
                  f"<:fb_link:1097554647637561445> **›** Account erstellt: <t:{int(member.created_at.timestamp())}:f> \n"
        )
        embed.set_thumbnail(url=member.display_avatar.url)
        embed.set_author(name=f"Profil von {ctx.author.name}",
                         icon_url=member.display_avatar.url)
        await ctx.respond(embed=embed, ephemeral=True)

    # ------------------------------------------------------------------------------------------------------------------

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT user_id FROM message_count WHERE guild_id = {member.guild.id}"
        )
        result = cur.fetchone()

        if result is None:
            return
        else:
            if result is not None:
                cursor.execute(
                    f"DELETE FROM message_count WHERE guild_id = {member.guild.id} and user_id = {member.id}"
                )
        messages_db.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        cursor = messages_db.cursor()
        cur = cursor.execute(
            f"SELECT guild_id FROM message_count WHERE guild_id = {guild.id}"
        )
        result = cur.fetchone()

        if result is None:
            return
        else:
            if result is not None:
                cursor.execute(
                    f"DELETE FROM message_count WHERE guild_id = {guild.id}"
                )
        messages_db.commit()


def setup(bot):
    bot.add_cog(messages_counter_module(bot))
