import datetime
import sqlite3

import discord
from discord import Option
from discord.ext import commands

bot_avatar = "https://cdn.discordapp.com/attachments/1005884993245020163/1097443524712087552/logo.png"
support = "https://discord.gg/PesnQYF5GJ"
tempchannel_db = sqlite3.connect("sql-databases/tempchannel.sqlite")
tempvoice_erklaerung = "https://cdn.discordapp.com/attachments/1085694515031064606/1100595939871313992/voice_images.png"

bot = commands.Bot(command_prefix="?", intents=discord.Intents.all())


class tempchannel_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    tempvoice = discord.SlashCommandGroup("tempvoice")

    @tempvoice.command(
        description="📌 × Richte Temporäre Voicekanäle auf deinem Server ein"
    )
    @commands.has_permissions(administrator=True)
    async def setup(self, ctx,
                    text_channel: Option(discord.TextChannel, "Wähle einen Settingschannel"),
                    voice_channel: Option(discord.VoiceChannel, "Wähle einen Joinchannel"),
                    voice_kategorie: Option(discord.CategoryChannel, "Wähle eine Kategorie")):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT guild_id FROM tempchannel_setup WHERE guild_id = {ctx.guild.id}")
        result1 = cursor.fetchone()

        if result1 is None:
            sql = "INSERT INTO tempchannel_setup(guild_id, text_id, voice_id, voice_name, voice_category) VALUES(?,?,?,?,?)"
            val = (ctx.guild.id, text_channel.id, voice_channel.id, voice_channel.name, voice_kategorie.id)

            embed = discord.Embed(
                title="Frenky | Tempchannels",
                description="Hier wird beschrieben wie du **Tempchannels** auf diesem Server einrichten kannst. "
                            "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                            f"du dir **[hier]({support})** hilfe suchen!",
                color=0x5e63ea
            )
            embed.add_field(
                name="Settings Textkanal",
                value=f"<#{text_channel.id}>"
            )
            embed.add_field(
                name="Join Voicekanal",
                value=f"<#{voice_channel.id}>"
            )
            embed.add_field(
                name="Voice Kategorie",
                value=f"**{voice_kategorie.name}**"
            )
        elif result1 is not None:
            await text_channel.purge()
            sql = "UPDATE tempchannel_setup SET text_id = ?, voice_id = ?,voice_name = ?, voice_category = ? WHERE guild_id = ?"
            val = (text_channel.id, voice_channel.id, voice_channel.name, voice_kategorie.id, ctx.guild.id)
            embed = discord.Embed(
                title="Frenky | Tempchannels",
                color=0x5e63ea
            )
            embed.add_field(
                name="Settings Textkanal",
                value=f"<#{text_channel.id}>"
            )
            embed.add_field(
                name="Join Voicekanal",
                value=f"<#{voice_channel.id}>"
            )
            embed.add_field(
                name="Voice Kategorie",
                value=f"**<#{voice_kategorie.id}>**"
            )
        await ctx.respond(embed=embed, ephemeral=True)
        cursor.execute(sql, val)
        tempchannel_db.commit()

        embed = discord.Embed(
            title="Frenky | Tempchannel Settings",
            description="> Individualisiere deinen Eigenen Voice Kanal nach deinen Vorstellungen. "
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!",
            color=0x5e63ea
        )
        embed.set_image(url=tempvoice_erklaerung)
        await text_channel.send(embed=embed, view=tempchannel_settings_view())

    @tempvoice.command(
        description="📌 × Entferne das Tempovice System vom Server."
    )
    @commands.has_permissions(administrator=True)
    async def remove(self, ctx):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT guild_id FROM tempchannel_setup WHERE guild_id = {ctx.guild.id}")
        result1 = cursor.fetchone()

        if result1 is None:
            await ctx.respond(
                "Auf diesem Server ist das Tempvoice System nicht eingerichtet."
            )
        elif result1 is not None:
            cursor.execute(f"DELETE FROM tempchannel_setup WHERE guild_id = {ctx.guild.id}")
            tempchannel_db.commit()
            embed = discord.Embed(
                description=f"<:fb_delete:1097445150092955679> **›** Tempvoice wurde erfolgreich entfernt.",
                color=0x5e63ea)
            embed.set_thumbnail(url=bot_avatar)
            embed.set_author(name="Tempvoice entfernt")
            embed.timestamp = datetime.datetime.now()
            await ctx.respond(embed=embed, ephemeral=True)

    @commands.Cog.listener()
    async def on_ready(self):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT text_id FROM tempchannel_setup")
        channels = cursor.fetchall()

        for channel in channels:
            channel_id = channel[0]
            kanal = self.bot.get_channel(channel_id)

            embed = discord.Embed(
                title="Frenky | Tempchannel Settings",
                description="> Individualisiere deinen Eigenen Voice Kanal nach deinen Vorstellungen. "
                            "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                            f"du dir **[hier]({support})** hilfe suchen!",
                color=0x5e63ea
            )
            embed.timestamp = datetime.datetime.now()
            embed.set_image(url=tempvoice_erklaerung)

            await kanal.purge(limit=1)
            await kanal.send(embed=embed, view=tempchannel_settings_view(timeout=None))


def setup(bot):
    bot.add_cog(tempchannel_module(bot))


class tempchannel_settings_view(discord.ui.View):
    @discord.ui.select(
        placeholder="🟣 | Wähle eine Option",
        max_values=1,
        min_values=1,
        options=[
            discord.SelectOption(
                label="Kanal Umbenennen",
                value="rename",
                description="Ermöglicht dir den Kanalnamen zu ändern.",
                emoji="<:fb_chat:1100594836660305970>"
            ),
            discord.SelectOption(
                label="Kanal Limieren",
                value="limit",
                emoji="<:fb_rocket:1100523075377844234>",
                description="Hiermit kannst du deinen Kanal auf Nutzer Begrenzen."
            ),
            discord.SelectOption(
                label="Kanal Schließen",
                value="close",
                emoji="<:fb_lock:1100594957619822702>",
                description="Mache deinen Kanal für niemanden mehr zugänglich."
            ),
            discord.SelectOption(
                label="Kanal Freigeben",
                value="unclose",
                emoji="<:fb_unlock:1100595011143340062>",
                description="Gebe den Kanal wieder Frei für den Server."
            ),
            discord.SelectOption(
                label="User Kicken",
                value="kick",
                emoji="<:fb_kick:1100595154324303944>",
                description="Kicke einen User aus dem Kanal."
            ),
            discord.SelectOption(
                label="User Einladen",
                value="invite",
                emoji="<:fb_link:1100604538169331782>",
                description="Schicke einem Nutzer einen Invite zum Tempchannel."
            ),
            discord.SelectOption(
                label="Auswahl Abbrechen",
                emoji="❌",
                value="cancel"
            )
        ]
    )
    async def tempchannel_settings_view_callback(self, select, interaction: discord.Interaction):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT guild_id FROM tempchannel_setup WHERE guild_id = {interaction.guild.id}")
        result1 = cursor.fetchone()

        cursor.execute(f"SELECT voice_id FROM tempchannel_setup WHERE guild_id = {interaction.guild.id}")
        result2 = cursor.fetchone()[0]

        cursor.execute(f"SELECT user_id FROM tempchannel_user WHERE guild_id = {interaction.guild.id}")
        result4 = cursor.fetchone()

        channel_owner_id = result4[0]

        voice_state = interaction.user.voice
        if "invite" in interaction.data['values']:
            if interaction.user.voice is None:
                await interaction.response.send_message(
                    f"<:fb_warn:1100596446811660350> **›** Du musst erst in <#{int(result2)}> beitreten.",
                    ephemeral=True)
            await interaction.response.send_modal(invite_user_modal(title="User Einladen (Tempchannel)"))
        if "cancel" in interaction.data['values']:
            await interaction.response.edit_message(view=self)

        if "rename" in interaction.data['values']:
            if interaction.guild.id not in result1:
                return
            if voice_state is None:
                await interaction.response.send_message(
                    f"<:fb_warn:1100596446811660350> **›** Du musst erst in <#{int(result2)}> beitreten.",
                    ephemeral=True)
            if interaction.user.id != channel_owner_id:
                await interaction.response.send_message(
                    f"<:fb_warn:1097213764396384409> **›** Du bist nicht der Kanalinhaber.",
                    ephemeral=True)
            await interaction.response.send_modal(edit_tempchannel_name_modal(title="Namen Ändern (Tempchannel)"))

        if "limit" in interaction.data['values']:
            if voice_state is None:
                await interaction.response.send_message(
                    f"<:fb_warn:1100596446811660350> **›** Du musst erst in <#{int(result2)}> beitreten.",
                    ephemeral=True)
            if interaction.user.id != channel_owner_id:
                await interaction.response.send_message(
                    f"<:fb_warn:1097213764396384409> **›** Du bist nicht der Kanalinhaber.",
                    ephemeral=True)
            await interaction.response.send_modal(edit_channel_limit_modal(title="Limit Ändern (Tempchannel)"))

        if "close" in interaction.data['values']:
            if voice_state is None:
                await interaction.response.send_message(
                    f"<:fb_warn:1100596446811660350> **›** Du musst erst in <#{int(result2)}> beitreten.",
                    ephemeral=True)
                return
            if interaction.user.id != channel_owner_id:
                await interaction.response.send_message(
                    f"<:fb_warn:1097213764396384409> **›** Du bist nicht der Kanalinhaber.",
                    ephemeral=True)
            embed = discord.Embed(
                title="Frenky | Tempchannel Settings",
                description="Bestätige das du den Kanal **Schließen** willst.",
                color=0x5e63ea
            )
            await interaction.response.send_message(embed=embed, view=set_channel_permissions_button_closed(),
                                                    ephemeral=True)

        if "unclose" in interaction.data['values']:
            if voice_state is None:
                await interaction.response.send_message(
                    f"<:fb_warn:1100596446811660350> **›** Du musst erst in <#{int(result2)}> beitreten.",
                    ephemeral=True)
                return
            if interaction.user.id != channel_owner_id:
                await interaction.response.send_message(
                    f"<:fb_warn:1097213764396384409> **›** Du bist nicht der Kanalinhaber.",
                    ephemeral=True)
            embed = discord.Embed(
                title="Frenky | Tempchannel Settings",
                description="Bestätige das du den Kanal **Öffnen** willst.",
                color=0x5e63ea
            )
            await interaction.response.send_message(embed=embed, view=set_channel_permissions_button_open(),
                                                    ephemeral=True)


class edit_tempchannel_name_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Dein Tempchannel Name",
                style=discord.InputTextStyle.short,
                max_length=20,
                required=True
            )
        )

    async def callback(self, interaciton: discord.Interaction):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT channel_name FROM tempchannel_user WHERE user_id = {interaciton.user.id}")
        result1 = cursor.fetchone()

        cursor.execute(f"SELECT voice_name FROM tempchannel_setup WHERE guild_id = {interaciton.guild.id}")
        result2 = cursor.fetchone()

        if result1 is None:
            return
        elif result1 is not None:
            if result2[0] in self.children[0].value:
                await interaciton.response.send_message(
                    "<:fb_warn:1100596446811660350> **›** Du darfst deinen Kanal nicht wie den Joinchannel bennen.",
                    ephemeral=True
                )
            else:
                sql = "UPDATE tempchannel_user SET user_id = ?, channel_name = ? WHERE guild_id = ?"
                val = (interaciton.user.id, self.children[0].value, interaciton.guild.id)
                cursor.execute(sql, val)
                await interaciton.response.send_message(
                    f"Deine Kanalname wurde Erfolgreich in **{self.children[0].value}** geändert.",
                    ephemeral=True
                )
                await interaciton.user.voice.channel.edit(name=self.children[0].value)
        tempchannel_db.commit()


class edit_channel_limit_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Gebe eine Zahl ein",
                placeholder="Limit ...",
                style=discord.InputTextStyle.short,
                required=True,
                max_length=2
            )
        )

    async def callback(self, interaction: discord.Interaction):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT limit_int FROM tempchannel_user WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        if result is not None:
            sql = "UPDATE tempchannel_user SET limit_int = ? WHERE guild_id = ?"
            val = (int(self.children[0].value), interaction.guild.id)
            cursor.execute(sql, val)
            tempchannel_db.commit()

            await interaction.user.voice.channel.edit(user_limit=int(self.children[0].value))
            await interaction.response.send_message(
                f"**›** Das Userlimit für den Voice von {interaction.user.mention} wurde erfolgreich auf **{self.children[0].value}** gesetzt!",
                ephemeral=True
            )


class invite_user_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Gebe eine UserID an",
                placeholder="User ID",
                style=discord.InputTextStyle.short,
                required=True,
                min_length=16
            )
        )

    async def callback(self, interaction: discord.Interaction):
        user = discord.utils.get(interaction.guild.members, id=int(self.children[0].value))
        link = interaction.user.voice.channel.jump_url

        if user not in interaction.guild.members:
            await interaction.response.send_message(
                "<:fb_warn:1100596446811660350> **›** Dieser User exisistiert nicht auf diesem Server",
                ephemeral=True
            )
        elif user in interaction.guild.members:
            await interaction.response.send_message(
                f"Du hast erfolgreich <@{int(self.children[0].value)}> eine Einladung gesendet",
                ephemeral=True
            )
            embed_user = discord.Embed(
                title=f"{interaction.user.name} hat dich eingeladen",
                description=f"Tritt hier {interaction.user.voice.channel.mention} dem Voice von{interaction.user.mention} bei.",
                color=0x5e63ea
            )
            embed_user.timestamp = datetime.datetime.now()
            await user.send(embed=embed_user)


class set_channel_permissions_button_closed(discord.ui.View):
    @discord.ui.button(
        label="Bestätigen",
        emoji="<:fb_yes:1100767697161171006>",
        style=discord.ButtonStyle.blurple
    )
    async def confirm_callback(self, button, interaction: discord.Interaction):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT is_locked FROM tempchannel_user WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()
        if result == "True":
            await interaction.response.send_message(
                "**›** Du kannst keinen Kanal Schließen der bereits geschlossen ist!"
            )

        if result is not None:
            sql = "UPDATE tempchannel_user SET is_locked = ? WHERE guild_id = ?"
            val = ("True", interaction.guild.id)
            cursor.execute(sql, val)
            tempchannel_db.commit()

            await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, connect=False,
                                                                 speak=False)
            await interaction.response.send_message(
                content=f"<:fb_yes:1100767697161171006> **›** {interaction.user.mention} wurde erfolgreich auf **Private** gesetzt!",
                ephemeral=True
            )

    @discord.ui.button(
        label="Abbrechen",
        emoji="<:fb_no:1100767732137463878>",
        style=discord.ButtonStyle.blurple
    )
    async def abbrechen_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message("Interaktion erfolgreich abgebrochen!")


class set_channel_permissions_button_open(discord.ui.View):
    @discord.ui.button(
        label="Bestätigen",
        emoji="<:fb_yes:1100767697161171006>",
        style=discord.ButtonStyle.blurple
    )
    async def confirm_callback(self, button, interaction: discord.Interaction):
        cursor = tempchannel_db.cursor()
        cursor.execute(f"SELECT is_locked FROM tempchannel_user WHERE guild_id = {interaction.guild.id}")
        result = cursor.fetchone()

        cursor.execute(f"SELECT voice_category FROM tempchannel_setup WHERE guild_id = {interaction.guild.id}")
        result2 = cursor.fetchone()

        cat = discord.utils.get(interaction.guild.categories, id=result2[0])

        if result == "True":
            await interaction.response.send_message(
                "**›** Du kannst keinen Kanal Öffnen der nicht geschlossen ist!"
            )

        if result is not None:
            sql = "UPDATE tempchannel_user SET is_locked = ? WHERE guild_id = ?"
            val = ("False", interaction.guild.id)
            cursor.execute(sql, val)
            tempchannel_db.commit()
            perms = cat.overwrites_for(interaction.guild.default_role)
            await interaction.user.voice.channel.set_permissions(interaction.guild.default_role, overwrite=perms)

            await interaction.response.send_message(
                content=f"<:fb_yes:1100767697161171006> **›** {interaction.user.mention} wurde erfolgreich auf **Öffentlich** gesetzt!",
                ephemeral=True
            )

    @discord.ui.button(
        label="Abbrechen",
        emoji="<:fb_no:1100767732137463878>",
        style=discord.ButtonStyle.blurple
    )
    async def abbrechen_callback(self, button, interaction: discord.Interaction):
        await interaction.response.edit_message("Interaktion erfolgreich abgebrochen!")
