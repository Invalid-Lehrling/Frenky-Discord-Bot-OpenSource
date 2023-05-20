import datetime
import sqlite3

import discord
from discord.ext import commands
 
db = sqlite3.connect("sql-databases/log.sqlite")
bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
user_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1099321480942198834/7c8f476123d28d103efe381543274c25-modified.png"


class log_event_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {member.guild.id}")
        log_channel = cur.fetchone()

        channel = self.bot.get_channel(log_channel[0])

        if log_channel is None:
            return
        else:
            embed = discord.Embed(
                title="Neues Mitglied",
                description=f"{member.mention} ist beigetreten.",
                color=0x5e63ea
            )
            embed.add_field(
                name="Log Infos",
                value=f"Account erstellt: <t:{int(member.created_at.timestamp())}:f>\n"
                      f"Server Beigetreten: <t:{int(member.joined_at.timestamp())}:f>"
            )
            embed.timestamp = datetime.datetime.now()
            if member.avatar is None:
                embed.set_thumbnail(url=user_avatar)
            else:
                embed.set_thumbnail(url=member.avatar.url)
            if member.avatar is None:
                embed.set_author(name=member, icon_url=user_avatar)
            else:
                embed.set_author(name=member, icon_url=member.avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_remove(self, member):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {member.guild.id}")
        log_channel = cur.fetchone()

        channel = self.bot.get_channel(log_channel[0])

        if log_channel is None:
            return
        else:
            embed = discord.Embed(
                title="Mitglied hat verlassen",
                description=f"{member.mention} hat den Server verlassen.",
                color=0x5e63ea
            )
            embed.add_field(
                name="Log Infos",
                value=f"Account erstellt: <t:{int(member.created_at.timestamp())}:f>\n"
                      f"Server verlassen: <t:{int(datetime.datetime.now().timestamp())}:f>"
            )
            embed.timestamp = datetime.datetime.now()
            if member.avatar is None:
                embed.set_thumbnail(url=user_avatar)
            else:
                embed.set_thumbnail(url=member.avatar.url)
            if member.avatar is None:
                embed.set_author(name=member, icon_url=user_avatar)
            else:
                embed.set_author(name=member, icon_url=member.avatar.url)
            await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_ban(self, guild, user):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {guild.id}")
        log_channel = cur.fetchone()

        channel = self.bot.get_channel(log_channel[0])
        async for entry in guild.audit_logs(limit=1, action=discord.AuditLogAction.ban):
            if entry.target == user:
                banning_user = entry.user

                embed = discord.Embed(
                    title = "Mitglied Gebannt",
                    description = f"Gebannt von: {banning_user.name}\n"
                                  f"Gebannt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                    color = 0x5e63ea
                )
                embed.add_field(
                    name = "Ban Infos",
                    value = f"User: {user.name}\n"
                            f"ID: {user.id}"
                )
                embed.timestamp = datetime.datetime.now()
                if user.avatar is None:
                    embed.set_thumbnail(url=user_avatar)
                else:
                    embed.set_thumbnail(url=user.avatar.url)
                if user.avatar is None:
                    embed.set_author(name=user, icon_url=user_avatar)
                else:
                    embed.set_author(name=user, icon_url=user.avatar.url)
                await channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_update(self, before, after):
        if before.roles != after.roles:
            cursor = db.cursor()
            cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.guild.id}")
            log_channel = cur.fetchone()

            channel = self.bot.get_channel(log_channel[0])

            added_roles = [role for role in after.roles if role not in before.roles]
            removed_roles = [role for role in before.roles if role not in after.roles]

            if log_channel is None:
                return
            else:
                embed = discord.Embed(
                    title="Rollen geändert",
                    color=0x5e63ea
                )
                if added_roles:
                    embed.description = f"{after.mention} wurde eine Rolle hinzugefügt." \
                                        f"\n> Rolle: {''.join([role.mention for role in added_roles])}"
                if removed_roles:
                    embed.description = f"{after.mention} wurde eine Rolle entfernt." \
                                        f"\n> **Rolle:** {''.join([role.mention for role in removed_roles])}"
                    embed.add_field(
                        name="Log Infos",
                        value=f"Account erstellt: <t:{int(after.created_at.timestamp())}:f>\n"
                              f"Server Beigetreten: <t:{int(datetime.datetime.now().timestamp())}:f>"
                    )
                embed.timestamp = datetime.datetime.now()
                if after.avatar is None:
                    embed.set_thumbnail(url=user_avatar)
                else:
                    embed.set_thumbnail(url=after.avatar.url)
                if after.avatar is None:
                    embed.set_author(name=after, icon_url=user_avatar)
                else:
                    embed.set_author(name=after, icon_url=after.avatar.url)
                await channel.send(embed=embed)

        if before.name != after.name:
            cursor = db.cursor()
            cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.guild.id}")
            log_channel = cur.fetchone()

            channel = self.bot.get_channel(log_channel[0])

            if log_channel is None:
                return
            else:
                embed = discord.Embed(
                    title="Mitglied Name geändert",
                    description=f"{after.mention} hat seinen Namen geändert.\n"
                                f"> **Vorher:** `{before.nick}` | **Nachher:** `{after.nick}`",
                    color=0x5e63ea
                )
                embed.add_field(
                    name="Log Infos",
                    value=f"Account erstellt: <t:{int(after.created_at.timestamp())}:f>\n"
                          f"Server Beigetreten: <t:{int(datetime.datetime.now().timestamp())}:f>"
                )
                embed.timestamp = datetime.datetime.now()
                if after.avatar is None:
                    embed.set_thumbnail(url=user_avatar)
                else:
                    embed.set_thumbnail(url=after.avatar.url)
                if after.avatar is None:
                    embed.set_author(name=after, icon_url=user_avatar)
                else:
                    embed.set_author(name=after, icon_url=after.avatar.url)
                await channel.send(embed=embed)

        if before.avatar != after.avatar:
            log_channel = await self.db.fetchval("SELECT channel_id FROM log_setup WHERE guild_id = $1",
                                                 before.guild.id)
            if not log_channel:
                return

            channel = self.bot.get_channel(log_channel)

            embed = discord.Embed(
                title="Mitglied Avatar geändert",
                description=f"{after.mention} hat sein/ihr Profilbild aktualisiert.\m"
                            f"> Neuer Avatar: [PNG]({after.avatar.url})",
                color=0x5e63ea
            )
            embed.add_field(
                name="Log Infos",
                value=f"Account erstellt: <t:{int(after.created_at.timestamp())}:f>\n"
                      f"Server Beigetreten: <t:{int(datetime.datetime.now().timestamp())}:f>"
            )
            embed.timestamp = datetime.datetime.now()

            if after.avatar is None:
                embed.set_thumbnail(url=after.default_avatar_url)
                embed.set_author(name=after, icon_url=after.default_avatar_url)
            else:
                embed.set_thumbnail(url=after.avatar.url)
                embed.set_author(name=after, icon_url=after.avatar.url)

            await channel.send(embed=embed)

        # Member - Settings

    @commands.Cog.listener()
    async def on_message_delete(self, message):

        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {message.guild.id}")
        log_channel = cur.fetchone()
        channel = self.bot.get_channel(log_channel[0])
        if message.author == self.bot.user:
            return
        else:
            if message.embeds:
                embedd = message.embeds[0]
                log_embed = discord.Embed(
                    title="Nachricht gelöscht (Embed)",
                    description=f"> Nachricht: [{message.id}]({message.jump_url}) wurde gelöscht.\n"
                                f"> Gelöscht am: <t:{int(datetime.datetime.now().timestamp())}:f>\n"
                                f"> Gelöscht von: {message.author.mention} (`{message.author}`)",
                    color=0x5e63ea
                )
                log_embed.add_field(
                    name="<:fb_message:1097549644403318804> | Embed Nachricht",
                    value=f"**{embedd.title}**\n⠀\n"
                          f"{embedd.description}\n"
                )
                log_embed.timestamp = datetime.datetime.now()
                log_embed.set_footer(text="Nachricht gelöscht")
                await channel.send(embed=log_embed)
            else:
                log_embed = discord.Embed(
                    title="Nachricht gelöscht (Nachricht)",
                    description=f"> Nachricht: [{message.id}]({message.jump_url}) wurde gelöscht.\n"
                                f"> Gelöscht am: <t:{int(datetime.datetime.now().timestamp())}:f>\n"
                                f"> Gelöscht von: {message.author.mention} (`{message.author}`)",
                    color=0x5e63ea
                )
                log_embed.add_field(
                    name="<:fb_message:1097549644403318804> | Embed Nachricht",
                    value=f"**{message.content}**"
                )
                log_embed.timestamp = datetime.datetime.now()
                log_embed.set_footer(text="Nachricht gelöscht")
                await channel.send(embed=log_embed)

    @commands.Cog.listener()
    async def on_message_edit(self, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.guild.id}")
        log_channel = cur.fetchone()
        channel = self.bot.get_channel(log_channel[0])

        if after.author == self.bot.user:
            return
        else:
            if before.embeds and after.embeds:
                before_embed = before.embeds[0]
                after_embed = after.embeds[0]
                if before_embed != after_embed:
                    log_embed = discord.Embed(
                        title="Nachricht bearbeitet (Embed)",
                        description=f"> Nachricht: {after.id} wurde bearbeitet."
                                    f"> Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>\n"
                                    f"> Bearbeitet von: {after.author.mention} (`{after.author}`)",
                        color=0x5e63ea
                    )
                    log_embed.add_field(
                        name="<:fb_message:1097549644403318804> | Embed Nachricht (Vorher)",
                        value=f"**Titel:** \n> {before_embed.title}"
                              f"\n**Beschreibung:** \n> T{before_embed.description}`\n⠀\n"
                    )
                    log_embed.add_field(
                        name="<:fb_message:1097549644403318804> | Embed Nachricht (Nachher)\n",
                        value=f"**Titel:** \n> {after_embed.title}"
                              f"\n**Beschreibung:** \n> {after_embed.description}",
                        inline=False
                    )
                    log_embed.timestamp = datetime.datetime.now()
                    log_embed.set_footer(text="Nachricht bearbeitet")
                    await channel.send(embed=log_embed)

            else:
                log_embed = discord.Embed(
                    title="Nachricht bearbeitet (Nachricht)",
                    description=f"> Nachricht: {after.id} wurde bearbeitet.\n"
                                f"> Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>\n"
                                f"> Bearbeitet von: {after.author.mention} (`{after.author}`)",
                    color=0x5e63ea
                )
                log_embed.add_field(
                    name="<:fb_message:1097549644403318804> | Nachricht (Vorher)",
                    value=f"**Nachricht:** \n> {before.content}"
                )
                log_embed.add_field(
                    name="<:fb_message:1097549644403318804> | Nachricht (Nachher)\n",
                    value=f"**Nachricht:** \n> {after.content}",
                    inline=False
                )
                log_embed.timestamp = datetime.datetime.now()
                log_embed.set_footer(text="Nachricht bearbeitet")
                await channel.send(embed=log_embed)

        # Message

    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.id}")
        log_channel = cur.fetchone()
        channel = self.bot.get_channel(log_channel[0])

        if before.name != after.name:
            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                if entry.target == after:
                    embed = discord.Embed(
                        title="Server Bearbeitet (Name)",
                        description=f"Bearbeitet von: {entry.user.mention}\n"
                                    f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                        color=0x5e63ea
                    )
                    embed.add_field(
                        name="<:fb_logging:1099332234051326043> | Bearbeitung",
                        value=f"Vorher: {before.name}\n"
                              f"Danach: {after.name}"
                    )
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Server Name geändert")
                    await channel.send(embed=embed)
        if before.icon.url != after.icon.url:
            async for entry in after.audit_logs(limit=1, action=discord.AuditLogAction.guild_update):
                if entry.target == after:
                    embed = discord.Embed(
                        title="Server Bearbeitet (Icon)",
                        description=f"Bearbeitet von: {entry.user.mention}\n"
                                    f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                        color=0x5e63ea
                    )
                    embed.add_field(
                        name="<:fb_logging:1099332234051326043> | Bearbeitung",
                        value=f"Neues Icon: [Icon]({after.icon.url})"
                    )
                    embed.set_image(url=after.icon.url)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Server Icon geändert")
                    await channel.send(embed=embed)

    # Guild

    @commands.Cog.listener()
    async def on_guild_channel_create(self, channel):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {channel.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        creator = channel.guild.me

        embed = discord.Embed(
            title=f"Kanal erstellt ({channel.type})",
            description=f"Erstellt von: **{creator.name}**\n"
                        f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
            color=0x5e63ea
        )
        embed.add_field(
            name="Kanal Infos",
            value=f"Name: {channel.name}\n"
                  f"ID: {channel.id}\n"
                  f"Mention: {channel.mention}"
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Kanal Erstellt")
        await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_channel_delete(self, channel):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {channel.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        creator = channel.guild.me

        embed = discord.Embed(
            title=f"Kanal gelöscht ({channel.type})",
            description=f"Gelöscht von: **{creator.name}**\n"
                        f"Gelöscht am: <t:{int(datetime.datetime.now().timestamp())}:f>",
            color=0x5e63ea
        )
        embed.add_field(
            name="Kanal Infos",
            value=f"Name: {channel.name}\n"
                  f"ID: {channel.id}\n"
                  f"Mention: {channel.mention}"
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Kanal gelöscht")
        await l_channel.send(embed=embed)

    # Channel

def setup(bot):
    bot.add_cog(log_event_module(bot))
