import datetime
import json
import sqlite3

import discord
from discord.ext import commands

db = sqlite3.connect('sql-databases/welcome.sqlite')
db2 = sqlite3.connect('sql-databases/welcome_embed_text.sqlite')

invites = {}


class on_guild_send_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        invite = await guild.text_channels[0].create_invite()
        create = guild.created_at.timestamp()
        joined = datetime.datetime.now().timestamp()

        embed = discord.Embed(
            title="Frenky wurde auf einem Neuen Server hinzugefügt",
            description="> Ein weiterer Server hat mich als Bot Eingeladen, daher haltet bitte als Team im Blick das"
                        "Bugs und Ideen von ihnen kommen können.",
            color=0x5e63ea
        )
        embed.add_field(
            name="<:fb_server:1097203531049615512> | Servername",
            value=f"**{guild.name}**"
        )
        embed.add_field(
            name="<:fb_crown:1099271064594423859> | Serverowner",
            value=f"{guild.owner}",
            inline=False
        )
        embed.add_field(
            name="<:fb_link:1097554647637561445> | Serverinvite",
            value=f"[{guild.name} - Invite]({invite})",
            inline=False
        )
        embed.add_field(
            name="<:fb_chat:1097549593052467290> | Server Erstellt",
            value=f"<t:{int(create)}:f>",
            inline=False
        )
        embed.add_field(
            name="<:fb_plus:1097223502802718861> | Bot Eingeladen",
            value=f"<t:{int(joined)}:f>",
            inline=False
        )
        embed.set_footer(text="Ein neuer Server")
        embed.timestamp = datetime.datetime.now()
        await self.bot.get_channel(1099259526110257213).send(embed=embed)

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):
        create = guild.created_at.timestamp()
        joined = datetime.datetime.now().timestamp()

        embed = discord.Embed(
            title="Frenky wurde von einem Server entfernt",
            description="> Leider wurde ich von einem weiteren Server entfernt, daher haltet bitte als Team im Blick das"
                        "Bugs und Ideen von ihnen kommen können.",
            color=0x5e63ea
        )
        embed.add_field(
            name="<:fb_server:1097203531049615512> | Servername",
            value=f"**{guild.name}**"
        )
        embed.add_field(
            name="<:fb_crown:1099271064594423859> | Serverowner",
            value=f"{guild.owner}",
            inline=False
        )
        embed.add_field(
            name="<:fb_link:1097554647637561445> | ServerID",
            value=f"{guild.id}",
            inline=False
        )
        embed.add_field(
            name="<:fb_chat:1097549593052467290> | Server Erstellt",
            value=f"<t:{int(create)}:f>",
            inline=False
        )
        embed.add_field(
            name="<:fb_plus:1097223502802718861> | Bot Entfernt",
            value=f"<t:{int(joined)}:f>",
            inline=False
        )
        embed.set_footer(text="Ein neuer Server")
        embed.timestamp = datetime.datetime.now()
        await self.bot.get_channel(1099264757162319967).send(embed=embed)


def setup(bot):
    bot.add_cog(on_guild_send_event(bot))
