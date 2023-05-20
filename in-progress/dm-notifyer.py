import datetime

import discord
from discord.ext import commands
import sqlite3


class dm_notifyer(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="dm-notify"
    )
    @commands.is_owner()
    async def _dm_notify(self, ctx):
        for member in ctx.guild.members:
            if not member.bot:
                await ctx.respond("Notify Erfolgreich gesendet!")
                
                embed = discord.Embed(
                    title="FRENKY DISCORD BOT | RELEASE BENACHRICHTIGUNG",
                    description="Endlich ist es so weit und <@1097176283198279820> ist ab jetzt für euch **verfügbar**!"
                                "Probiert seine Features und Funktionen aus und gebt uns gerne **positives** aber bitte"
                                "auch **negatives Feedback** wenn etwas nicht stimmt mit dem Bot.\n⠀\n",
                    color = 0x5e63ea
                )
                embed.add_field(
                    name="Worte vom 1. Developer",
                    value="InvalidLehrling: `„Ich bin froh das es nach Monaten so weit ist und wir unser Projekt, nicht nur ich als"
                          "Einzelperson, sondern mit dem gesamten Team präsentieren darf. Ich hoffe er entspricht euren Erwartungen"
                          "und ich hoffe auf eine gute Zukunft für dieses Projekt.“`"
                )
                embed.add_field(
                    name="Wichtige Links:",
                    value="- Support Server: [hier](https://discord.gg/xsqv57JnF4)\n"
                          "- Bot Invite: [hier](https://discord.com/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands)"
                          "- Frenky Docs: [hier](https://docs-frenky-bot.carrd.co)",
                    inline=False
                )
                await member.send(embed=embed)


def setup(bot):
    bot.add_cog(dm_notifyer(bot))
