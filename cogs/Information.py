import datetime

import discord, datetime
import requests
from discord import Option
import time
from discord.ext import commands

bot_avatar = "https://images-ext-2.discordapp.net/external/TVnVWVWTWo5qlBFP0VkaoixXc0VYUqjiM71T36-EYXY/%3Fsize%3D1024/https/cdn.discordapp.com/avatars/1097176283198279820/fcdd5cf6e9021a8d468b97d862dfbd69.png?width=586&height=586"
startTime = time.time()


class Information_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    add = discord.SlashCommandGroup("add")

    @discord.slash_command(
        name="userinfo",
        description="👤 × Gibt dir eine Information zu einem Nutzer."
    )
    async def _user_info(self, ctx, member: discord.Member):
        top_role = member.roles[-1]
        if member not in ctx.guild.members:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Benutzer existiert nicht auf diesem Server.",
                              ephemeral=True)
        else:
            embed = discord.Embed(color=0x2b2d31)
            embed.description = f"> Dieser Benutzer/-in ist seit dem <t:{int(member.joined_at.timestamp())}:f> ein **Servermitglied**. " \
                                f"{member.name} ist zudem seit <t:{int(member.created_at.timestamp())}:R> ein Discord Nutzer/-in."

            embed.add_field(name="<:fb_chat:1097412236005363823> | Username", value=f"`{member.name}`", inline=False)

            if member.discriminator == "0":
                pass
            else:
                embed.add_field(name="<:fb_rocket:1097451173650370590> | User-Tag", value=f"`#{member.discriminator}`", inline=False)
            embed.add_field(name="<:fb_fire:1097223381235011728> | User-ID", value=f"`{member.id}`", inline=False)
            booster = ctx.guild.premium_subscriber_role
            badges = []

            if member is ctx.guild.owner:
                badges.append("<:fb_crown_2:1119929921465241712>")
            if member.public_flags.hypesquad_balance:
                badges.append("<:fb_balance:1097485032249098290>")
            if member.public_flags.hypesquad_bravery:
                badges.append("<:fb_bravery:1097485325749727232>")
            if member.public_flags.hypesquad_brilliance:
                badges.append("<:fb_brilliance:1097485193461366834>")
            if member.public_flags.verified_bot_developer:
                badges.append("<:fb_verifyed_dev:1119669952673230919>")
            if member.public_flags.active_developer:
                badges.append("<:fb_active_dev:1119670001683665026>")
            if member.avatar.is_animated() or member.banner:
                badges.append("<:fb_nitro_normal:1097488351671627868>")
            if booster in member.roles:
                badges.append("<:fb_booster_normal:1097488500519076031>")
            if member.public_flags.bug_hunter:
                badges.append("<:fb_bug_hunter:1119928635713925130>")
            if member.public_flags.bot_http_interactions:
                badges.append("<:fb_slash_command:1119929127013720134>")
            if member.public_flags.partner:
                badges.append("<:fb_partner:1119929557655507065>")
            if member.public_flags.staff:
                badges.append("<:fb_staff:1119930237430534154>")
            if member.public_flags.bot_http_interactions:
                badges.append("<:fb_slash_command:1119929127013720134>")

            if badges:
                badges_string = " ".join(badges)
                embed.add_field(name=f"<:fb_fire:1097223381235011728> | User Badges [{len(badges)}]",
                                value=badges_string, inline=False)
            if member.status == discord.Status.online:
                embed.add_field(name="\n<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_online:1097482477007798316> Online", inline=False)
            if member.status == discord.Status.dnd:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_dnd:1097482444459999293> Bitte nicht stören", inline=False)
            if member.status == discord.Status.idle:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_idle:1097482506799960216> Abwesend", inline=False)
            if member.status == discord.Status.offline:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_offline:1097482550953386074> Offline", inline=False)

            if booster in member.roles:
                embed.add_field(
                    name = "<:fb_booster:1097486055906750514> | Booster seit",
                    value = f"<t:{int(member.premium_since.timestamp())}:R>",
                    inline=False
                )
            else:
                pass

            if member.activity:
                embed.add_field(
                    name = "<:fb_idee:1097206098827686041> | Custom Status",
                    value = f"**{member.activity.name}**"
                )
            else:
                pass

            roles = []
            for role in member.roles[:15]:
                roles.append(f"<@&{role.id}>")
                roles.reverse()
            embed.add_field(name=f"<:fb_role:1097481602336034876> | Rollen [{len(member.roles)}]", value="".join(roles), inline=False)

            limit = ""
            if member.voice:
                if member.voice.channel.user_limit is None:
                    limit = "Kein Limit"
                else:
                    limit = f"{len(member.voice.channel.members)}/{member.voice.channel.user_limit}"

                embed.add_field(
                    name = "| Aktueller VoiceChannel",
                    value = f"{member.voice.channel.mention} `[{limit}]`"
                )

            view = discord.ui.View(timeout=None)

            image_button = \
                discord.ui.Button(
                    label="User Banner",
                    style=discord.ButtonStyle.blurple
                )

            activity_button = \
                discord.ui.Button(
                    label="User Activity",
                    style=discord.ButtonStyle.blurple
                )

            async def activity_button_callback(interaction: discord.Interaction):
                embed = discord.Embed(
                    title = f"Aktivität für {member.name}",
                    color = 0x2b2d31
                )
                if not any(activity.type in (discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.streaming) for activity in member.activities):
                    pass
                else:
                    if member.activities[1]:
                        if member.activities[1].type == discord.ActivityType.streaming:
                            embed.add_field(
                                name="Schaut gerade:",
                                value=f"```{member.activities[1].name}\n{member.activities[1].details}\n{member.activities[1].state}```"
                            )
                        elif member.activities[1].type == discord.ActivityType.playing:
                            embed.add_field(
                                name="Spiel gerade:",
                                value=f"```{member.activities[1].name}\n{member.activities[1].details}\n{member.activities[1].state}```"
                            )
                        elif member.activities[1].type == discord.ActivityType.listening:
                            embed.add_field(
                                name="Hört gerade:",
                                value=f"```{member.activities[1].name}\n{member.activities[1].title}\n{member.activities[1].artist}\n{member.activities[1].duration.seconds}```"
                            )
                        await interaction.response.send_message(embed = embed, ephemeral = True)

            async def image_button_callback(interaction: discord.Interaction):
                reqs = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
                banner_id = reqs["banner"]
                banner_url = f"https://cdn.discordapp.com/banners/{member.id}/{banner_id}?size=1024"
                embeds = discord.Embed(
                    title=f"Banner von {member.name}",
                    color = 0x2b2d31
                )
                embeds.set_image(url=banner_url)
                await interaction.response.send_message(embed=embeds, ephemeral=True)

            activity_button.callback = activity_button_callback
            image_button.callback = image_button_callback

            req = await self.bot.http.request(discord.http.Route("GET", "/users/{uid}", uid=member.id))
            banner_id = req["banner"]

            if not any(activity.type in (discord.ActivityType.playing, discord.ActivityType.listening, discord.ActivityType.streaming) for activity in member.activities):
                pass
            else:
                view.add_item(activity_button)
            if banner_id:
                view.add_item(image_button)

            embed.set_author(name=f"Userinfo von {member.name}", icon_url=bot_avatar)

            embed.set_thumbnail(url=member.display_avatar.url)

            await ctx.respond(embed=embed, view=view)

    @discord.slash_command(
        name="serverinfo",
        description="💾 × Zeigt dir alle Informationen über den Server."
    )
    async def _server_info(self, ctx):
        voice_channels = ctx.guild.voice_channels
        total_voice_channels = len(voice_channels)
        text_channels = ctx.guild.text_channels
        total_text_channels = len(text_channels)

        embed = discord.Embed(
            title="Serverinfo",
            description=f"> Dieser Server existiert seit dem <t:{int(ctx.guild.created_at.timestamp())}:f>. "
                        f"Der Inhaber*in dieses Servers ist {ctx.guild.owner.mention}",
            color=0x2b2d31
        )

        embed.add_field(name="<:fb_chat:1097412236005363823> | Server Name", value=ctx.guild.name)
        embed.add_field(name="<:fb_tag:1097481497918832771> | Server ID", value=ctx.guild.id, inline=False)
        embed.add_field(name="<:fb_booster:1097486055906750514> | Server Boosts",
                        value=f"**{ctx.guild.premium_subscription_count}/14** (Level: {ctx.guild.premium_tier})",
                        inline=False)
        embed.add_field(name="<:fb_rocket:1097451173650370590> | Emoji/Sticker",
                        value=f"Emojis: **{len(ctx.guild.emojis)}** | Sticker: **{len(ctx.guild.stickers)}**",
                        inline=False)
        embed.add_field(name="<:fb_users:1097505591997517844> | Server Mitglieder",
                        value=f"User: {len([member for member in ctx.guild.members if not member.bot])}  |  Bot: {len([member for member in ctx.guild.members if member.bot])}",
                        inline=False)
        embed.add_field(name="<:fb_server:1097203531049615512> | Server Kanäle",
                        value=f"Voice: {total_voice_channels}  |  Text: {total_text_channels}", inline=False)

        roles = []
        for role in ctx.guild.roles[:15]:
            roles.append(f"<@&{role.id}>")
            roles.sort()

        embed.add_field(name=f"<:fb_fire:1097223381235011728> | Server Rollen [{len(ctx.guild.roles)}]:",
                        value=f", ".join(roles), inline=False)
        if ctx.guild.icon is not None:
            embed.set_thumbnail(url=ctx.guild.icon.url)

        if ctx.guild.banner:
            banner_url = ctx.guild.banner.url
            embed.set_image(url=banner_url)

        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="avatar",
        description="🎭 × Gibt dir das Profilbild eines Nutzers aus."
    )
    async def _avatar(self, ctx, member: discord.Member):
        if member not in ctx.guild.members:
            return
        else:
            embed = discord.Embed(
                description=f"[Bild Datei]({member.avatar.url})",
                color=0x2b2d31
            )
            embed.set_author(name=f"Avatar von {member.name}", icon_url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url=member.avatar.url)
            await ctx.respond(embed=embed)

    @discord.slash_command(
        name="about",
        description="🤖 × Hier siehst du sämtliche Informationen des Bots."
    )
    async def _about(self, ctx):
        current_time = time.time()
        uptime = current_time - startTime
        uptime_delta = datetime.timedelta(seconds=int(uptime))
        embed = discord.Embed(
            description="> Hier stehen sämtliche Informationen, welche du zu diesem Bot erhalten kannst. "
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst "
                        "du dir **[hier](https://discord.gg/xsqv57JnF4)** hilfe suchen!",
            color=0x2b2d31)
        embed.add_field(
            name="<:fb_bot:1097223544598966353> | Bot Name",
            value=f"{self.bot.user.mention} `{self.bot.user.name}#{self.bot.user.discriminator}`"
        )
        embed.add_field(
            name="<:fb_tag:1097481497918832771> | Bot ID",
            value=f"`{self.bot.user.id}`"
        ),
        embed.add_field(
            name="<:fl_dev:1097195167825535006> | Developer",
            value=f"<@852878080447741952>\n<@916445145497489410>"
        ),
        embed.add_field(
            name="<:fb_tool:1099263351592325231> | Libary",
            value="`PyCord 2.4.1`"
        )
        embed.add_field(
            name="<:fb_role:1097481602336034876> | Bot Ping",
            value=f"`{round(self.bot.latency * 1000)}ms`"
        )
        embed.add_field(
            name="<:fb_users:1097505591997517844> | Bot Users",
            value=f"`{len(self.bot.users)}`"
        )
        embed.add_field(
            name="<:fb_news:1097554295580266556> | Bot Servers",
            value=f"`{len(self.bot.guilds)}`"
        )
        embed.add_field(
            name="<:fb_time:1097411948066386030> | Uptime",
            value=f"`{uptime_delta}`"
        )
        embed.add_field(
            name="<:fb_link:1097554647637561445> | Wichtige Links",
            value="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands)\n"
                  "[Support Link](https://discord.gg/xsqv57JnF4)\n"
                  "[Bot Vote](https://top.gg/bot/1097176283198279820)"
        )
        embed.set_author(name=f"Frenky Bot Info", icon_url=bot_avatar)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

    @add.command(
        description="⚡ × Füge ein ausgewähltes Emote zum Server hinzu."
    )
    @commands.has_permissions(manage_emojis=True)
    async def emoji(self, ctx, emoji_name: Option(str, "Schreibe einen Emoji namen."), emoji: discord.Emoji):
        response = requests.get(emoji.url)
        emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=response.content)
        embed = discord.Embed(
            description='<{1}:{0.name}:{0.id}> wurde mit dem namen **"{0.name}"** zum Server hinzugefügt!'.format(
                emoji,
                "a" if emoji.animated else ""),
            color=0x2b2d31)
        embed.set_author(name="Ein neues Emoji wurde hinzugefügt", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, delete_after=15)


def setup(bot):
    bot.add_cog(Information_module(bot))
