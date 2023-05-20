import datetime

import discord
from discord.ext import commands

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"


class basic_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="invite",
        description="📌 × Gibt dir den Invite Link für den Bot."
    )
    async def _invite(self, ctx):
        embed = discord.Embed(
            description="Lade mich **[hier](https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands)** ein!",
            color=0x5e63ea
        )
        embed.set_footer(text="Invite Link")
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name="Frenky Bot Invite Link", icon_url=bot_avatar)
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        name="support",
        description="📌 × Gibt dir einen Link zum Support Server."
    )
    async def _support(self, ctx):
        embed = discord.Embed(
            description="Trete **[hier](https://discord.gg/xsqv57JnF4)** dem Support Server bei!",
            color=0x5e63ea
        )
        embed.timestamp = datetime.datetime.now()
        embed.set_author(name="Frenky Bot Support Server", icon_url=bot_avatar)
        await ctx.respond(embed=embed, ephemeral=True)

    @discord.slash_command(
        name="bot-guilds",
        description="📌 × Zeigt dem Bot Owner die Server Anzahl."
    )
    @commands.is_owner()
    async def _bot_guilds(self, ctx):
        servers = [guild.name for guild in self.bot.guilds]
        embed = discord.Embed(
            title="Auf diesen Servern bin ich.",
            color=0x5e63ea
        )
        embed.add_field(
            name="Guilds:",
            value= '\n '.join(servers)
        )
        await ctx.respond(embed=embed, ephemeral=True)


def setup(bot):
    bot.add_cog(basic_module(bot))
