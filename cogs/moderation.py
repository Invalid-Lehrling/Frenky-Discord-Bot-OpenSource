import asyncio
from datetime import datetime, timedelta
import json

import datetime
import discord
from discord.ext import commands
from discord import Option

with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())


class moderation_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    timeout = discord.SlashCommandGroup("timeout")

    @discord.slash_command(
        name="kick",
        description="📌 × Benutze diesen Befehl um ein Mitglied zu Kicken."
    )
    @commands.has_permissions(kick_members=True)
    async def _kick_member(self, ctx, member: discord.Member,
                           grund: Option(str, "Schreibe einen Grund (Optional)", required=False)):
        if grund is None:
            grund = "Kein Grund angegeben."
        if member not in ctx.guild:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Nutzer ist nicht auf diesem Server")
            return
        else:
            embed = discord.Embed(
                description=f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n"
                            f"<:fb_pin:1097481392666972160> **›** Grund: {grund}"
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"{member} wurde von {ctx.author} gekickt")
            embed.set_author(name=f"{member.name} wurde gekickt", icon_url=member.avatar.url)
            await member.kick()

    @discord.slash_command(
        name="ban",
        description="📌 × Banne mit diesem Befehl ein ausgewähltes Mitglied."
    )
    @commands.has_permissions(ban_members=True)
    async def _ban_member(self, ctx, member: discord.Member,
                          grund: Option(str, "Schreibe einen Grund (Optional)", required=False)):
        if grund is None:
            grund = "Kein Grund angegeben."
        embed = discord.Embed(
            description=f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_pin:1097481392666972160> **›** Grund: {grund}",
            color=0x5e63ea
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_footer(text=f"{member} wurde von {ctx.author} gebannt")
        embed.set_author(name=f"{member.name} wurde gebannt", icon_url=member.avatar.url)
        await member.ban()
        await ctx.respond(embed=embed)
        await member.send(embed=embed)

    @timeout.command(
        description="📌 × Ermöglicht es dir ein Mitglied zu Timeouten."
    )
    @commands.has_permissions(moderate_members=True)
    async def set(self, ctx, member: discord.Member,
                  dauer: Option(str, "Wähle eine Zeit", choices=[
                      "5 Minuten",
                      "10 Minuten",
                      "20 Minuten",
                      "30 Minuten",
                      "40 Minuten",
                      "50 Minuten",
                      "1 Stunde",
                      "1 Tag",
                      "1 Woche"]),
                  grund: Option(str, "Wähle einen Grund", choices=[
                      "Keinen Grund",
                      "Verbreitung von Spam oder unerwünschter Werbung.",
                      "Veröffentlichung von beleidigenden oder diffamierenden Inhalten.",
                      "Verletzung des Urheberrechts.",
                      "Verletzung der Privatsphäre anderer Nutzer.",
                      "Veröffentlichung von illegalen oder unangemessenen Inhalten.",
                      "Verwendung eines gefälschten Kontos oder einer falschen Identität.",
                      "Belästigung oder Stalking anderer Nutzer.",
                      "Eigenwerbung unangebrachtes verbreiten von Werbeinhalten.",
                      "Verstoß gegen die Nutzungsbedingungen der Plattform."
                  ])):
        now = datetime.datetime.now()
        minuten = 0

        embed = discord.Embed(color=0x5e63ea)
        desc = ""
        if member not in ctx.guild.members:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Nutzer ist nicht auf diesem Server")
            return
        if member.timeout:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieses Mitglied befindet sich bereits im Timeout!",
                              ephemeral=True)
            return
        else:
            if dauer == "5 Minuten":
                minuten = 5
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `5 Minuten`"
            if dauer == "10 Minuten":
                minuten = 10
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `10 Minuten`"
            if dauer == "20 Minuten":
                minuten = 20
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `20 Minuten`"
            if dauer == "30 Minuten":
                minuten = 30
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `30 Minuten`"
            if dauer == "40 Minuten":
                minuten = 40
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `40 Minuten`"
            if dauer == "50 Minuten":
                minuten = 50
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `50 Minuten`"
            if dauer == "1 Stunde":
                minuten = 60
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `1 Stunde`"
            if dauer == "3 Stunde":
                minuten = 1440
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `1 Tag`"
            if dauer == "1 Woche":
                minuten = 10080
                desc = f"<:fb_userhead:1097194422594191390> **›** User: {member.mention}\n<:fb_chat:1097412236005363823> **›** Grund: **{grund}**\n<:fb_time:1097411948066386030> **›** Dauer: `1 Woche`"

            embed.description = desc
            embed.timestamp = datetime.datetime.now()
            embed.set_footer(text=f"{member} wurde von {ctx.author} in den Timeout versetzt")
            embed.set_author(name=f"{member.name} wurde getimeoutet")
            timeout_until = now + timedelta(minutes=minuten)
            await member.timeout_for(duration=timeout_until - now, reason=grund)
            await ctx.respond(content=f"{member.mention}", embed=embed)

    @timeout.command(
        description="📌 × Ermöglicht es dir ein Mitglied aus dem Timeouten zu entfernen."
    )
    @commands.has_permissions(moderate_members=True)
    async def remove(self, ctx, member: discord.Member):
        if member not in ctx.guild.members:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Nutzer ist nicht auf diesem Server")
            return
        else:
            if not member.timeout:
                await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieses Mitglied befindet sich nicht im Timout!")
            else:
                embed = discord.Embed(
                    description=f"<:fb_yes:1097215591183548557> **›** {member.mention} wurde erfolgreich aus dem Timeout entfernt!",
                    color=0x5e63ea
                )
                embed.set_author(name=f"{member.name} ist wieder zurück")
                embed.timestamp = datetime.datetime.now()
                embed.set_footer(text=f"{member} wurde von {ctx.author} aus dem Timeout entfernt")
                await member.remove_timeout()
                await ctx.respond(content=member.mention, embed=embed)

    @discord.slash_command(
        name="purge",
        description="📌 × Löscht eine Anzahl an Nachrichten in einem Kanal."
    )
    @commands.has_permissions(manage_messages=True)
    async def _purge(self, ctx,
                     anzahl: Option(int, "Schreibe eine Anzahl (Optional)", required=True)):
        messages = await ctx.channel.history(limit=anzahl).flatten()
        if anzahl > 1001:
            await ctx.respond("<:fb_warn:1097213764396384409> **›** Die maximale Anzahl beträgt **1001** Nachrichten.",
                              ephemeral=True)
        elif len(messages) == 0:
            await ctx.respond(
                "<:fb_warn:1097213764396384409> **›** In diesem Kanal sind keine Nachrichten die gelöscht werden können.",
                ephemeral=True)
            return
        else:
            messages = await ctx.channel.history(limit=anzahl + 1).flatten()
            deleted_messages_count = len(messages) if messages else 0

            embed = discord.Embed(
                description=f"{deleted_messages_count} Nachrichten wurden von {ctx.author.mention} gelöscht.",
                color=0x5e63ea
            )
            embed.set_author(name="Kanal wurde gesäubert.")
            embed.timestamp = datetime.datetime.now()
            await ctx.channel.purge(limit=anzahl + 1)
            await ctx.respond(embed=embed, ephemeral=False, delete_after=20)


def setup(bot):
    bot.add_cog(moderation_module(bot))
