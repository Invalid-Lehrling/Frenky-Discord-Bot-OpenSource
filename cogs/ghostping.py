import sqlite3

import discord
from discord import Option
from discord.ext import commands

ghostping_db = sqlite3.connect("sql-databases/smallfeatures.sqlite")


class ghostping_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    gohstping = discord.SlashCommandGroup("ghostping")

    @gohstping.command(
        name="set",
        description="👻 × Setze oder entferne das Ghostping System."
    )
    @commands.has_permissions(administrator=True)
    async def _ghostping_setup(self, ctx,
                               status: Option(str, "Wähle einen Status", choices=["Aktivieren", "Deaktivieren"])):
        cursor = ghostping_db.cursor()
        cursor.execute(f"SELECT guild_id FROM ghost_ping WHERE guild_id = {ctx.guild.id}")
        result = cursor.fetchone()

        if status == "Aktivieren":
            if result is not None:
                await ctx.respond("<:fb_warn:1097213764396384409> **›** Dieser Server ist bereits in der Datenbank",
                                  ephemeral = True)
            elif result is None:
                cursor.execute(f"INSERT INTO ghost_ping (guild_id) VALUES ({ctx.guild.id})")
                ghostping_db.commit()
                embed = discord.Embed(
                    title="Ghostping wurde eingerichtet",
                    description="Du hast erfolgreich das Ghostping System eingerichtet.",
                    color=0x2b2d31
                )
                if ctx.guild.icon is not None:
                    embed.set_thumbnail(url=ctx.guild.icon.url)
                await ctx.respond(embed=embed)
        if status == "Deaktivieren":
            if result is None:
                await ctx.respond(
                    "<:fb_warn:1097213764396384409> **›** Dieser Server hier ist nich in der Datenbank eingetragen",
                    ephemeral=True)
            elif result is not None:
                embed = discord.Embed(
                    title="Ghostping entfernt",
                    description=f"`{ctx.guild.name}` wurde aus der Datenbank entfernt.\nDas System ist nun nicht mehr aktiv.",
                    color=0x2b2d31
                )
                await ctx.respond(embed=embed, delete_after=20)
                cursor.execute(f"DELETE FROM ghost_ping WHERE guild_id = {ctx.guild.id}")
            ghostping_db.commit()

    @commands.Cog.listener()
    async def on_message_delete(self, message):
        if message.guild is None or message.channel is None:
            return

        cursor = ghostping_db.cursor()
        cursor.execute(f"SELECT guild_id FROM ghost_ping WHERE guild_id = {message.guild.id}")
        result = cursor.fetchone()

        if result is None:
            return
        if message.author.bot:
            return
        if message.mentions:
            mention_list = []
            name_list = []
            for mention in message.mentions:
                user = self.bot.get_user(mention.id)
                mention_list.append(user.mention)
                name_list.append(user.name)
            mention_string = ", ".join(mention_list)
            name_string = ', '.join(name_list)
            embed = discord.Embed(
                title=f"Ghostping von {message.author.name}",
                description=f"{mention_string} wurde/wurden gepingt",
                color = 0x2b2d31
            )
            embed.add_field(
                name = "<:fb_pin:1097481392666972160> | Details",
                value = f"> ```{name_string}```"
            )
            await message.channel.send(embed=embed, delete_after = 160)


def setup(bot):
    bot.add_cog(ghostping_module(bot))
