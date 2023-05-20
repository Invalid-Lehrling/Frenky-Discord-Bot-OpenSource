import asyncio

import discord
from discord.ext import commands
import sqlite3
from discord import PermissionOverwrite

tempchannel_db = sqlite3.connect("sql-databases/tempchannel.sqlite")
bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
support = "https://discord.gg/PesnQYF5GJ"


class tempchannel_event(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT voice_id FROM tempchannel_setup WHERE guild_id = {member.guild.id}")
        result1 = cursor.fetchall()
        # get channel
        cursor.execute(
            f"SELECT user_id, channel_name, limit_int, is_locked FROM tempchannel_user WHERE guild_id = {member.guild.id}")
        result2 = cursor.fetchall()

        cursor.execute(
            f"SELECT channel_name FROM tempchannel_user WHERE guild_id = {member.guild.id} AND user_id = {member.id}"
        )
        result5 = cursor.fetchone()

        cursor.execute(
            f"SELECT limit_int FROM tempchannel_user WHERE user_id = {member.id} AND guild_id = {member.guild.id}"
        )
        result6 = cursor.fetchone()

        cursor.execute(f"SELECT voice_category FROM tempchannel_setup WHERE guild_id = {member.guild.id}")
        result7 = cursor.fetchone()

        cursor.execute(f"SELECT is_locked FROM tempchannel_user WHERE guild_id = {member.guild.id} AND user_id = {member.id}")
        result8 = cursor.fetchone()

        cursor.execute(
            f"SELECT channel_name FROM tempchannel_user WHERE user_id = {member.id} AND guild_id = {member.guild.id}"
        )
        result9 = cursor.fetchone()
        # get user data
        cat = discord.utils.get(member.guild.categories, id=result7[0])

        kanal = self.bot.get_channel(result1[0])

        if result1 is None:
            return
        elif result1 is not None:
            if before.channel and before.channel.name == result5[0] and len(before.channel.members) == 0:
                await before.channel.delete()
            if before.channel is kanal:
                if after.channel:
                    channel_name = result9[0]
                    limits = result6[0]

                    after_channels = [c for c in member.guild.voice_channels if c.name and after.channel.name == channel_name and c.category == cat]

                    for c in after_channels:
                        print(1)
                        if c != after.channel:
                            print(2)
                            for user in c.members:
                                print(3)
                                if user == member:
                                    return

                    after_channel_else = await member.guild.create_voice_channel(name=f"{channel_name}", category=cat)

                    if result8[0] == "False":
                        perms = PermissionOverwrite(connect = True)
                        await after_channel_else.set_permissions(member.guild.default_role, overwrite=perms)
                    elif result8[0] == "True":
                        perms = PermissionOverwrite(connect = False)
                        await after_channel_else.set_permissions(member.guild.default_role, overwrite=perms)

                    await after_channel_else.edit(user_limit=limits)

                    for users in result2:
                        if member is not users[0]:
                            await member.move_to(after_channel_else)


def setup(bot):
    bot.add_cog(tempchannel_event(bot))
