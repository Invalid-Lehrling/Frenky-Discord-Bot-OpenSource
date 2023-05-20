import datetime

import discord
import requests
from discord import Option
from discord.ext import commands

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"


class Information_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    add = discord.SlashCommandGroup("add")

    @discord.slash_command(
        name="userinfo",
        description="📌 × Gibt dir eine Information zu einem Nutzer."
    )
    async def _user_info(self, ctx, member: discord.Member):
        top_role = ctx.author.roles[-1]
        if member not in ctx.guild.members:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Benutzer existiert nicht auf diesem Server.",
                              ephemeral=True)
        else:
            embed = discord.Embed(color=0x5e63ea)
            embed.description = f"> Dieser Benutzer ist seit dem <t:{int(member.joined_at.timestamp())}:f> ein **Servermitglied**. " \
                                f"{member.name} ist zudem seit <t:{int(member.created_at.timestamp())}:R> ein Discord Nutzer."

            embed.add_field(name="<:fb_chat:1097412236005363823> | Username", value=f"`{member.name}`")
            embed.add_field(name="<:fb_rocket:1097451173650370590> | User-Tag", value=f"`#{member.discriminator}`")
            embed.add_field(name="<:fb_fire:1097223381235011728> | User-ID", value=f"`{member.id}`")
            booster = ctx.guild.premium_subscriber_role
            badges = []

            if member.public_flags.hypesquad_balance:
                badges.append("<:fb_balance:1097485032249098290>")
            if member.public_flags.hypesquad_bravery:
                badges.append("<:fb_bravery:1097485325749727232>")
            if member.public_flags.hypesquad_brilliance:
                badges.append("<:fb_brilliance:1097485193461366834>")
            if member.premium_since is not None:
                badges.append("<:fb_nitro_normal:1097488351671627868>")
            if booster in member.roles:
                badges.append("<:fb_booster_normal:1097488500519076031>")

            if badges:
                badges_string = " ".join(badges)
                embed.add_field(name="<:fb_fire:1097223381235011728> | User Badges", value=badges_string)
            if member.status == discord.Status.online:
                embed.add_field(name="\n<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_online:1097482477007798316> Online")
            if member.status == discord.Status.dnd:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_dnd:1097482444459999293> Bitte nicht stören")
            if member.status == discord.Status.idle:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_idle:1097482506799960216> Abwesend")
            if member.status == discord.Status.offline:
                embed.add_field(name="<:fb_tag:1097481497918832771> | User Status",
                                value="<:fb_offline:1097482550953386074> Offline")
            embed.add_field(name=f"<:fb_role:1097481602336034876> | Höchste Rolle", value=top_role.mention)
            embed.set_author(name=f"Userinfo von {member}", icon_url=bot_avatar)
            if member.banner:
                embed.set_image(url=member.banner)
            else:
                pass
            if member.avatar is not None:
                embed.set_thumbnail(url=member.avatar.url)
            else:
                embed.set_thumbnail(url=bot_avatar)

            await ctx.respond(embed=embed)

    @discord.slash_command(
        name="serverinfo",
        description="📌 × Zeigt dir alle Informationen über den Server."
    )
    async def _server_info(self, ctx):

        voice_channels = ctx.guild.voice_channels
        total_voice_channels = len(voice_channels)
        text_channels = ctx.guild.text_channels
        total_text_channels = len(text_channels)
        embed = discord.Embed(
            description=f"> Dieser Server existiert seit dem <t:{int(ctx.guild.created_at.timestamp())}:f>."
                        f"Der Server Inhaber ist {ctx.guild.owner.mention}",
            color=0x5e63ea
        )
        embed.add_field(name="<:fb_chat:1097412236005363823> | Server Name:", value=ctx.guild.name)
        embed.add_field(name="<:fb_tag:1097481497918832771> | Server ID:", value=ctx.guild.id)
        embed.add_field(name="<:fb_users:1097505591997517844> | Server Mitglieder:",
                        value=f"User: {len([member for member in ctx.guild.members if not member.bot])}  |  Bot: {len([member for member in ctx.guild.members if member.bot])}")
        embed.add_field(name="<:fb_booster:1097486055906750514> | Server Boosts:",
                        value=f"{ctx.guild.premium_subscription_count}/14")
        embed.add_field(name="<:fb_server:1097203531049615512> | Server Kanäle:",
                        value=f"Voice: {total_voice_channels}  |  Text: {total_text_channels}")
        embed.add_field(name="<:fb_fire:1097223381235011728> | Server Rollen:", value=f"{len(ctx.guild.roles)}")
        embed.set_author(name=f"Serverinfo von {ctx.guild.name}")
        await ctx.respond(embed=embed)

    @discord.slash_command(
        name="avatar",
        description="📌 × Gibt dir das Profilbild eines Nutzers aus."
    )
    async def _avatar(self, ctx, member: discord.Member):
        if member not in ctx.guild.members:
            return
        else:
            embed = discord.Embed(
                description=f"[Bild Datei]({member.avatar.url})",
                color=0x5e63ea
            )
            embed.set_author(name=f"Avatar von {member.name}", icon_url=bot_avatar)
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url=member.avatar.url)
            await ctx.respond(embed=embed)

    @discord.slash_command(
        name="about",
        description="📌 × Hier siehst du sämtliche Informationen des Bots."
    )
    async def _about(self, ctx):
        embed = discord.Embed(
            description="> Hier stehen sämtliche Informationen, welche du zu diesem Bot erhalten kannst."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        "du dir **[hier](https://discord.gg/xsqv57JnF4)** hilfe suchen!",
            color=0x5e63ea)
        embed.add_field(
            name="<:fb_bot:1097223544598966353> | Bot Name",
            value=f"{self.bot.user.name}#{self.bot.user.discriminator}"
        )
        embed.add_field(
            name="<:fb_tag:1097481497918832771> | Bot ID",
            value=f"`{self.bot.user.id}`"
        ),
        embed.add_field(
            name="<:fl_dev:1097195167825535006> | Developer",
            value=f"InvalidLehrling#0187"
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
            name="<:fb_link:1097554647637561445> | Wichtige Links",
            value="[Invite Link](https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands)\n"
                  "[Support Link](https://discord.gg/xsqv57JnF4)"
        )
        embed.set_author(name=f"Frenky Bot Info", icon_url=bot_avatar)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed)

    @add.command(
        description="📌 × Füge ein ausgewähltes Emote zum Server hinzu."
    )
    @commands.has_permissions(manage_emojis=True)
    async def emoji(self, ctx, emoji_name: Option(str, "Schreibe einen Emoji namen."), emoji: discord.Emoji):
        response = requests.get(emoji.url)
        emoji = await ctx.guild.create_custom_emoji(name=emoji_name, image=response.content)
        embed = discord.Embed(
            description='<{1}:{0.name}:{0.id}> wurde mit dem namen **"{0.name}"** zum Server hinzugefügt!'.format(
                emoji,
                "a" if emoji.animated else ""),
            color=0x5e63ea)
        embed.set_author(name="Ein neues Emoji wurde hinzugefügt", icon_url=ctx.author.avatar.url)
        embed.timestamp = datetime.datetime.now()
        await ctx.respond(embed=embed, delete_after=15)


def setup(bot):
    bot.add_cog(Information_module(bot))
