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

    # Neue Events, hinzugefügt von Semml

    @commands.Cog.listener()
    async def on_guild_channel_update(self, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])

        if before.name != after.name:
            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                if entry.target == after:
                    embed = discord.Embed(
                        title="Kanal bearbeitet (Name)",
                        description=f"Bearbeitet von: {entry.user.mention}\n"
                                    f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                        color=0x5e63ea
                    )
                    embed.add_field(
                        name="<:fb_logging:1099332234051326043> | Name",
                        value=f"Vorher: {before.name}\n"
                              f"Danach: {after.name}"
                    )
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Kanal Name geändert")
                    await l_channel.send(embed=embed)

        if before.category_id != after.category_id:
            old_category = self.bot.get_channel(before.category_id)
            new_category = self.bot.get_channel(after.category_id)

            #old_category = discord.utils.get(before.guild.categories, id=before.category_id)
            #new_category = discord.utils.get(after.guild.categories, id=after.category_id)

            async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                if entry.target == after:
                    embed = discord.Embed(
                        title="Kanal bearbeitet (Kategorie)",
                        description=f"Bearbeitet von: {entry.user.mention}\n"
                                    f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                        color=0x5e63ea
                    )
                    embed.add_field(
                        name="<:fb_logging:1099332234051326043> | Position",
                        value=f"Vorher: {old_category.name}\n"
                              f"Danach: {new_category.name}"
                    )
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Kanal Kategorie geändert")
                    await l_channel.send(embed=embed)
        if before.overwrites != after.overwrites:
            #async for entry in after.guild.audit_logs(limit=1, action=discord.AuditLogAction.channel_update):
                #print('0.2')
                #if entry.target == after:
                    #print('0.3')
            for bef, aft in zip(before.overwrites.items(), after.overwrites.items()):
                if bef[1] != aft[1]:
                    changed_overwrites = []
                    for perm in discord.Permissions.VALID_FLAGS:
                        before_permission = getattr(bef[1], perm)
                        after_permission = getattr(aft[1], perm)
                        if after_permission:
                            action = '<:fb_true:1109558619990655137>'
                        elif after_permission == None:
                            action = '<:fb_invalid:1109558618145177751>'
                        else:
                            action = '<:fb_false:1109558615393706114>'
                        if before_permission != after_permission:
                            changed_overwrites.append(f'**{perm.replace("_", " ").title()}**: {action}')
                    embed = discord.Embed(title='Kanal bearbeitet (Berechtigungen)',
                                                description=f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                                        color=0x5e63ea)
                    embed.add_field(name='<:fb_logging:1099332234051326043> | Berechtigungen',
                                            value=f'**Berechtigungen für** {aft[0].mention} **in** {after.mention}\n\n' + '\n'.join(changed_overwrites), inline=False)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Kanal Berechtigungen geändert")
                    await l_channel.send(embed=embed)
                    
                        #for target in aft:
                            #print(target)
                        #print(bef)
                        #print(aft)
                        #if bef==aft:
                        #    print('gleich')
                        #else:
                        #    embed = discord.Embed(
                        #        title="Kanal bearbeitet (Berechtigungen)",
                        #        description=f"Bearbeitet von: {entry.user.mention}\n"
                        #                    f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                        #        color=0x5e63ea
                        #    )
                        #    embed.add_field(
                        #        name="<:fb_logging:1099332234051326043> | Bearbeitung",
                        #        value=f"Berechtigungen für {after.overwrites}"
                        #            #f"Vorher: {before.overwrites}\n"
                        #            #f"Danach: {after.overwrites}"
                        #    )
                        #    embed.timestamp = datetime.datetime.now()
                        #    embed.set_footer(text="Kanal Berechtigungen geändert")
                        #    await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):

        if before.channel != after.channel:
            if after.channel == None:
                cursor = db.cursor()
                cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {before.channel.guild.id}")
                log_channel = cur.fetchone()
                l_channel = self.bot.get_channel(log_channel[0])
                embed = discord.Embed(title='Sprachkanal verlassen (Mitglied)',
                                    description=f"Verlassen von: {member.mention}\n"
                                                f"Verlassen am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Sprachkanal',
                                value=f'Sprachkanal vorher: {before.channel.mention}', inline=False)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Sprachkanal verlassen")
                await l_channel.send(embed=embed)
            if before.channel == None:
                cursor = db.cursor()
                cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {after.channel.guild.id}")
                log_channel = cur.fetchone()
                l_channel = self.bot.get_channel(log_channel[0])
                embed = discord.Embed(title='Sprachkanal beigetreten (Mitglied)',
                                    description=f"Beigetreten von: {member.mention}\n"
                                                f"Beigetreten am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Sprachkanal',
                                value=f'Aktueller Sprachkanal: {after.channel.mention}', inline=False)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Sprachkanal beigetreten")
                await l_channel.send(embed=embed)
            if before.channel != None and after.channel != None:
                cursor = db.cursor()
                cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {after.channel.guild.id}")
                log_channel = cur.fetchone()
                l_channel = self.bot.get_channel(log_channel[0])
                embed = discord.Embed(title='Sprachkanal gewechselt (Mitglied)',
                                    description=f"Gewechselt von: {member.mention}\n"
                                                f"Gewechselt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Sprachkanal',
                                value=f'Sprachkanal vorher: {before.channel.mention}\n'
                                    f'Aktueller Sprachkanal: {after.channel.mention}', inline=False)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Sprachkanal gewechselt")
                await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_create(self, invite):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {invite.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        max_uses = invite.max_uses
        if max_uses == 0:
            max_uses = 'keins'
        if invite.expires_at == None:
            embed = discord.Embed(title='Servereinladung erstellt (dauerhaft)',
                                description=f"Erstellt von: {invite.inviter.mention}\n"
                                            f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                color=0x5e63ea)
            embed.add_field(name='<:fb_logging:1099332234051326043> | Einladung',
                            value=f'Link: {invite.url}\n'
                                f'Limit: {max_uses}\n'
                                f'Kanal: {invite.channel.mention}', inline=False)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text="Servereinladung erstellt")
            await l_channel.send(embed=embed)
        else:
            embed = discord.Embed(title='Servereinladung erstellt (temporär)',
                                description=f"Erstellt von: {invite.inviter.mention}\n"
                                            f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                                color=0x5e63ea)
            embed.add_field(name='<:fb_logging:1099332234051326043> | Einladung',
                            value=f'Link: {invite.url}\n'
                                f'Läuft ab am: <t:{int(invite.expires_at.timestamp())}:F>\n'
                                f'Limit: {max_uses}\n'
                                f'Kanal: {invite.channel.mention}', inline=False)
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text="Servereinladung erstellt")
            await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_invite_delete(self, invite):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {invite.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        max_uses = invite.max_uses
        if max_uses == 0:
            max_uses = 'keins'
        embed = discord.Embed(title='Servereinladung gelöscht',
                            description=f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>",
                            color=0x5e63ea)
        embed.add_field(name='<:fb_logging:1099332234051326043> | Einladung',
                        value=f'Link: {invite.url}\n'
                            f'Limit: {max_uses}\n'
                            f'Kanal: {invite.channel.mention}', inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Servereinladung gelöscht")
        await l_channel.send(embed=embed)
        
    @commands.Cog.listener()
    async def on_guild_emojis_update(self, guild, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        if len(before)>len(after):
            for emoji in before:
                if emoji not in after:
                    embed = discord.Embed(title='Emoji wurde entfernt',
                                        description=f"Entfernt am am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                                        color=0x5e63ea)
                    embed.add_field(name='<:fb_logging:1099332234051326043> | Emoji',
                                    value=f'Name: `{emoji.name}`\n', inline=False)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Emoji gelöscht")
                    await l_channel.send(embed=embed)
        elif len(before)<len(after):
            for emoji in after:
                if emoji not in before:
                    embed = discord.Embed(title='Emoji wurde hinzugefügt',
                                        description=f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                                        color=0x5e63ea)
                    embed.add_field(name='<:fb_logging:1099332234051326043> | Emoji',
                                    value=f'Name: `{emoji.name}`\n'
                                        f'Emoji: {emoji}', inline=False)
                    embed.timestamp = datetime.datetime.now()
                    embed.set_footer(text="Emoji hinzugefügt")
                    await l_channel.send(embed=embed)
        else:
            names_before = []
            names_after = []
            for emoji in before:
                names_before.append(emoji.name)
            for emoji in after:
                names_after.append(emoji.name)

            for emoji in before:
                if emoji.name not in names_after:
                    em=emoji
                    name=emoji.name
            for emoji in after:
                if emoji.name not in names_before:
                    name_=emoji.name
            try:
                embed = discord.Embed(title='Emoji wurde umbenannt',
                                    description=f"Umbenannt am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Emoji',
                                value=f'Vorher: `{name}`\n'
                                    f'Nachher: `{name_}`\n'
                                    f'Emoji: {em}', inline=False)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Emoji umbenannt")
                await l_channel.send(embed=embed)
            except:
                embed = discord.Embed(title='Emoji wurde umbenannt',
                                    description=f"Umbenannt am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Emoji',
                                value=f'In den Emojis kommt bzw kam eine Doppelung der Emojinamen vor, daher konnten die Namen des veränderten Emojis nicht identifiziert werden. Überprüfe die Emojis nach Namendoppelungen und passe diese gegebenfalls an.\n', inline=False)
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Emoji umbenannt")
                await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_create(self, role):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {role.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        mention = role.mention
        id = role.id
        name = role.name

        embed = discord.Embed(title='Rolle wurde erstellt',
                            description=f"Erstellt am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                            color=0x5e63ea)
        embed.add_field(name='<:fb_logging:1099332234051326043> | Rolle',
                        value=f'Name: {name}\n'
                            f'Erwähnung: {mention}\n'
                            f'ID: {id}', inline=False)

        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Rolle erstellt")
        await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_update(self, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {after.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        hoist = '<:fb_false:1109558615393706114>'
        mentionable = '<:fb_false:1109558615393706114>'
        color = after.color
        mention = after.mention
        id = after.id
        name = after.name
        perms = []
        if after.hoist:
            hoist = '<:fb_true:1109558619990655137>'
        if after.mentionable:
            mentionable = '<:fb_true:1109558619990655137>'
        if before.name != after.name:
            name = f'{before.name} ➜ {after.name}'
        if before.color != after.color:
            color = f'{before.color} ➜ {after.color}'
        if before.mentionable != after.mentionable:
            perms.append(f'**Allow anyone to @mention this role**: {mentionable}')
        if before.hoist != after.hoist:
            perms.append(f'**Display role members separately from online members**: {hoist}')
        
        for perm in discord.Permissions.VALID_FLAGS:
                        before_permission = getattr(before.permissions, perm)
                        after_permission = getattr(after.permissions, perm)
                        if after_permission:
                            action = '<:fb_true:1109558619990655137>'
                        else:
                            action = '<:fb_false:1109558615393706114>'
                        if before_permission != after_permission:
                            perms.append(f'**{perm.replace("_", " ").title()}**: {action}')
        embed = discord.Embed(title='Rolle wurde bearbeitet',
                            description=f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>\n\n<:fb_logging:1099332234051326043> **| Perms**\n" +
                            f'\n'.join(perms),
                            color=0x5e63ea)
        embed.add_field(name='<:fb_logging:1099332234051326043> | Rolle',
                        value=f'Name: {name}\n'
                            f'Erwähnung: {mention}\n'
                            f'Farbe: {color}\n'
                            f'ID: {id}', inline=False)
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Rolle bearbeitet")
        await l_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_role_delete(self, role):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {role.guild.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        id = role.id
        name = role.name
        color = role.color

        embed = discord.Embed(title='Rolle wurde gelöscht',
                            description=f"Gelöscht am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                            color=0x5e63ea)
        embed.add_field(name='<:fb_logging:1099332234051326043> | Rolle',
                        value=f'Name: {name}\n'
                            f'Farbe: {color}\n'
                            f'ID: {id}', inline=False)

        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text="Rolle gelöscht")
        await l_channel.send(embed=embed)
    
    @commands.Cog.listener()
    async def on_guild_update(self, before, after):
        cursor = db.cursor()
        cur = cursor.execute(f"SELECT channel_id FROM log_setup WHERE guild_id = {after.id}")
        log_channel = cur.fetchone()
        l_channel = self.bot.get_channel(log_channel[0])
        vanity_bool = getattr(after.features, 'VANITY_URL')
        if vanity_bool:
            if before.vanity_invite() != after.vanity_invite():
                embed = discord.Embed(title='Vanity Invite wurde bearbeitet',
                                    description=f"Bearbeitet am: <t:{int(datetime.datetime.now().timestamp())}:f>\n",
                                    color=0x5e63ea)
                embed.add_field(name='<:fb_logging:1099332234051326043> | Invite',
                                value=f'Vorher: {before.vanity_invite()}\n'
                                    f'Nachher: {after.vanity_invite()}\n', inline=False)

                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text="Vanity Invite bearbeitet")
                await l_channel.send(embed=embed)



def setup(bot):
    bot.add_cog(log_event_module(bot))