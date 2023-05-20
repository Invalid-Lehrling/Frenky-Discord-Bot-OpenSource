import datetime
import json
import sqlite3

import discord
from discord.ext import commands

db = sqlite3.connect('sql-databases/welcome.sqlite')
db2 = sqlite3.connect('sql-databases/welcome_embed_text.sqlite')


class on_guild_events(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        embed = discord.Embed(
            description=f"> Vielen dank das du mich auf {guild.name} eingeladen hast. "
                        f"Alle meine Features werden mit `/` gesteuert.",
            color=0x5e63ea
        )
        embed.set_author(name="Neuer Server")
        embed.set_thumbnail(url=guild.icon.url)
        embed.set_footer(text="Neuer Server")
        embed.timestamp = datetime.datetime.now()

        button = discord.ui.Button(
            label = "Support Server",
            style = discord.ButtonStyle.url,
            url = "https://discord.gg/xsqv57JnF4"
        )

        view = discord.ui.View()
        view.add_item(button)

        await guild.owner.send(embed=embed, view = view)

        with open("json-databases/autoroles.json", "r") as f:
            autorole_data = json.load(f)
        with open("json-databases/prefixes.json", "r") as f:
            prefix_change = json.load(f)

        if guild.id in autorole_data:
            return
        else:
            autorole_data[str(guild.id)] = {}
            autorole_data[str(guild.id)]["roles"] = []

        if guild.id in prefix_change:
            return
        else:
            if guild.id not in prefix_change:
                prefix_change[str(guild.id)] = {}
                prefix_change[str(guild.id)]["name"] = str(guild.name)
                prefix_change[str(guild.id)]["prefix"] = "?"

        with open("json-databases/autoroles.json", "w") as f:
            json.dump(autorole_data, f, indent=4)
        with open("json-databases/prefixes.json", "w") as f:
            json.dump(prefix_change, f, indent=4)

        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id FROM welcome_setup WHERE guild_id = {guild.id}")
        result = cursor.fetchone()

        if result is None:
            sql2 = "INSERT INTO welcome_setup(guild_id, channel_id, typ, msg) VALUES(?,?,?,?)"
            val2 = (guild.id, 0, "Normal", "**Herzlich Willkommen {user_mention} auf {guild_name}!**")
            cursor.execute(sql2, val2)
            db.commit()

    @commands.Cog.listener()
    async def on_guild_remove(self, guild):

        cursor = db.cursor()
        cursor.execute(f"SELECT guild_id FROM welcome_setup WHERE guild_id = {guild.id}")
        result = cursor.fetchone()

        if result is None:
            cursor.execute(f"DELETE FROM welcome_setup WHERE guild_id = {guild.id}")
            db.commit()


def setup(bot):
    bot.add_cog(on_guild_events(bot))
