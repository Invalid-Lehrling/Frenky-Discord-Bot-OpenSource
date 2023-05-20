import asyncio
import datetime
import json
from datetime import datetime

import discord
from discord.ext import commands


with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())


class error_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        if isinstance(error, commands.CommandNotFound):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.add_field(name="Hilfe", value="Verwende lieber die `/` commands des Bots.", inline=False)
            embed.set_footer(text="Command nicht gefunden")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.send(embed=embed, delete_after = 15)
            await asyncio.sleep(15)
            await ctx.message.delete()

    @commands.Cog.listener()
    async def on_application_command_error(self, ctx: discord.ApplicationContext, error: discord.DiscordException):
        if isinstance(error, commands.MissingPermissions):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Fehlende Berechtigungen")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.MissingRole):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Fehlende Rolle")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.MissingRequiredArgument):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Fehlendes Argument")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.MemberNotFound):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Nicht existierendes Mitglied")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.ChannelNotFound):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Nicht existierender Kanal")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.MessageNotFound):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Nicht exisitierende Nachricht")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.BotMissingPermissions):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Fehlende Bot Berechtigungen")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.BotMissingRole):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.set_footer(text="Fehlende Bot Rolle")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
        if isinstance(error, commands.EmojiNotFound):
            embed = discord.Embed(
                description=f"**Ein Fehler wurde diagnostiziert,** bitte kontaktiere den [Support](https://discord.gg/xsqv57JnF4) oder versuche es erneut!",
                color=0x5e63ea)
            embed.add_field(name="Error", value=f"```py\n{error}```")
            embed.add_field(name="Hilfe", value="Stelle sicher das der Bot auf dem Server ist, auf welchem das Emoji ist", inline=False)
            embed.set_footer(text="Emoji nicht gefunden")
            embed.set_author(name="Command Error")
            embed.timestamp = datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)
def setup(bot):
    bot.add_cog(error_module(bot))