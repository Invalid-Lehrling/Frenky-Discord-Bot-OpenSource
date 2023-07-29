import datetime

import discord
from discord.ext import commands
import sqlite3

ticket_db = sqlite3.connect("sql-databases/ticket.sqlite")

bot = commands.Bot(command_prefix="!", intents=discord.Intents.all())


class ticket_modul(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    ticket = discord.SlashCommandGroup("ticket")
    panel = ticket.create_subgroup("panel")

    @panel.command(
        name="settings",
        description="🎫 × Gewehe dir einen Einblick in dein Ticket Panel."
    )
    @commands.has_permissions(administrator=True)
    async def _open_panel(self, ctx):
        cursor = ticket_db.cursor()
        cursor.execute(f"SELECT guild_id FROM ticket_panel WHERE guild_id = {ctx.guild.id}")
        res = cursor.fetchone()

        if not res:
            cursor.execute(f'''INSERT INTO ticket_panel (
            guild_id, ticket_text, button_color, button_text) VALUES ({ctx.guild.id},
             'Klicke auf den Button um ein Ticket zu öffnen.', 'blurple', 'Ticket erstellen')''')
        embed = discord.Embed(
            title="Ticket Panel | Settings",
            description="> Du hast den Befehl zur Aufrufung des **Frenky - Ticket - Systems** ausgeführt. "
                        "Hier kannst du alles einstellen um deinen perfekten Support zu haben.",
            color=0x2b2d31
        )
        embed.set_footer(text="Ticket Panel | Settings")
        embed.timestamp = datetime.datetime.now()

        start_einrichtung_button = discord.ui.Button(
            label="Einrichtung öffnen",
            style=discord.ButtonStyle.blurple,
            emoji="<:fb_chat:1097549593052467290>"
        )

        view = discord.ui.View(timeout=None)
        view.add_item(start_einrichtung_button)

        async def start_einrichtung_callback(interaction: discord.Interaction):
            if not interaction.user.guild_permissions.administrator:
                await interaction.response.send_message("Du bist nicht berechtigt dies zu tun.", ephemeral=True)
            if interaction.user is not ctx.author:
                await interaction.response.send_message("Du bist nicht berechtigt dies zu tun.", ephemeral=True)

            cursor = ticket_db.cursor()
            cursor.execute(f"Select "
                           f"guild_id, "
                           f"ticket_channel, "
                           f"ticket_text, "
                           f"ping_role, "
                           f"ticket_category, "
                           f"team_role, "
                           f"button_color, "
                           f"button_text "
                           f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
            res = cursor.fetchone()

            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                            "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
                color=0x2b2d31
            )

            channel = ""

            if res[1]:
                channel = f"<#{res[1]}>"
            elif res[1] is None:
                channel = "None"
            embed.add_field(
                name="Ticket Channel",
                value=channel
            )
            embed.add_field(
                name="Ticket Text",
                value=res[2]
            )
            embed.add_field(
                name="Ping Role",
                value=res[3]
            )
            embed.add_field(
                name="Ticket Kategorie",
                value=res[4]
            )
            embed.add_field(
                name="Team Rolle",
                value=res[5]
            )
            embed.add_field(
                name="Ticket Button",
                value=f"Farbe: {res[6]}\nText: {res[7]}"
            )
            await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))

        start_einrichtung_button.callback = start_einrichtung_callback
        ticket_db.commit()
        await ctx.respond(embed=embed, view=view)


def setup(bot):
    bot.add_cog(ticket_modul(bot))


class ticket_channel_select(discord.ui.View):
    @discord.ui.channel_select(
        placeholder="Wähle einen Kanal",
        max_values=1,
        min_values=1,
        channel_types=[discord.ChannelType.text]
    )
    async def ticket_channel_select_callback(self, select, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(
            f'''UPDATE ticket_panel SET ticket_channel = {select.values[0].id} WHERE guild_id = {interaction.guild.id}''')
        embed = discord.Embed(
            title="Ticket Einrichtung | Ticket Channel",
            description=f"{select.values[0].mention} wurde erfolgreich als neuer Ticket-Channel gesetzt.",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=back_to_panel(timeout=None))
        ticket_db.commit()

    @discord.ui.button(
        label="Zurück",
        emoji="◀",
        style=discord.ButtonStyle.blurple
    )
    async def back_to_panel_callback(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"Select "
                       f"guild_id, "
                       f"ticket_channel, "
                       f"ticket_text, "
                       f"ping_role, "
                       f"ticket_category, "
                       f"team_role, "
                       f"button_color, "
                       f"button_text "
                       f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
            color=0x2b2d31
        )

        embed.add_field(
            name="Ticket Channel",
            value=res[1]
        )
        embed.add_field(
            name="Ticket Text",
            value=res[2]
        )
        embed.add_field(
            name="Ping Role",
            value=res[3]
        )
        embed.add_field(
            name="Ticket Kategorie",
            value=res[4]
        )
        embed.add_field(
            name="Team Rolle",
            value=res[5]
        )
        embed.add_field(
            name="Ticket Button",
            value=f"Farbe: {res[6]}\nText: {res[7]}"
        )

        await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))


class deleting_confirmation(discord.ui.View):
    @discord.ui.button(
        label="Ja",
        style=discord.ButtonStyle.green
    )
    async def yes(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"DELETE FROM ticket_panel WHERE guild_id = {interaction.guild.id}")

        embed = discord.Embed(
            title="Ticket Panal | Gelöscht",
            description="Deine gesamten Einstellungen wurden soeben gelöscht.",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=None)

    @discord.ui.button(
        label="Nein",
        style=discord.ButtonStyle.red
    )
    async def nein(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"Select "
                       f"guild_id, "
                       f"ticket_channel, "
                       f"ticket_text, "
                       f"ping_role, "
                       f"ticket_category, "
                       f"team_role, "
                       f"button_color, "
                       f"button_text "
                       f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
            color=0x2b2d31
        )

        channel = ""
        if res[1]:
            channel = f"<#{res[1]}>"
        elif res[1] is None:
            channel = "None"
        embed.add_field(
            name="Ticket Channel",
            value=channel
        )
        embed.add_field(
            name="Ticket Text",
            value=res[2]
        )
        embed.add_field(
            name="Ping Role",
            value=res[3]
        )
        embed.add_field(
            name="Ticket Kategorie",
            value=res[4]
        )
        embed.add_field(
            name="Team Rolle",
            value=res[5]
        )
        embed.add_field(
            name="Ticket Button",
            value=f"Farbe: {res[6]}\nText: {res[7]}"
        )

        await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))


class einrichtungs_buttons(discord.ui.View):
    @discord.ui.button(
        label="Einrichtung abbrechen",
        style=discord.ButtonStyle.red
    )
    async def cancel_callback(self, button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Die Einrichtung wurde erfolgreich abgebrochen.",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=None, delete_after=10)

    @discord.ui.button(
        label="Einrichtung löschen",
        style=discord.ButtonStyle.grey
    )
    async def delete_callback(self, button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panal | Löschung",
            description="Willst du deine gesamten Einstellungen löschen?",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=deleting_confirmation())

    @discord.ui.select(
        placeholder="Wähle eine Option",
        max_values=1,
        min_values=1,
        options=[
            discord.SelectOption(
                label="Ticket Channel",
                emoji="<:fb_channel:1097500461491290132>",
                description="Setze einen Channel für das Ticket",
                value="tch"
            ),
            discord.SelectOption(
                label="Ticket Kategorie",
                emoji="<:fb_tag:1097481497918832771>",
                description="Setze eine Kategorie für die Ticket Kanäle",
                value="tpk"
            ),
            discord.SelectOption(
                label="Ticket Button",
                emoji="<:fb_tool:1099263351592325231>",
                description="Bearbeite den Button nach deinen Vorstellungen",
                value="tpbu"
            ),
            discord.SelectOption(
                label="Ticket Text",
                emoji="<:fb_message:1097549644403318804>",
                description="Erstelle deinen eigenen Ticket - Text.",
                value="tpt"
            ),
            discord.SelectOption(
                label="Ping Rolle",
                emoji="<:fb_stats:1125539237203292161>",
                description="Wähle eine Rolle die im Ticket gepingt wird.",
                value="tpr"
            ),
            discord.SelectOption(
                label="Ticket Log",
                emoji="<:fb_logging:1099332234051326043>",
                description="Speichert das Ticket Transcript in einem Kanal.",
                value="tplc"
            ),
            discord.SelectOption(
                label="Ticket Format",
                emoji="<:fb_fire:1097482115882430474>",
                description="Setze ein Format für den Ticket Kanal.",
                value="tpcf"
            )
        ]
    )
    async def selections_callback(self, select, interaction: discord.Interaction):
        if "tch" in interaction.data["values"]:
            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Wähle einen Kanal aus, in welchem das Panel stehen soll.",
                color=0x2b2d31
            )
            await interaction.response.edit_message(embed=embed,
                                                    view=ticket_channel_select(timeout=None))

        if "tpt" in interaction.data["values"]:
            await interaction.response.send_modal(ticket_text_modal(title="Ticket Text"))

        if "tpbu" in interaction.data["values"]:
            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Bearbeite den Button nach deinen Vorstellungen.",
                color=0x2b2d31
            )

            await interaction.response.edit_message(embed=embed, view=button_customization(timeout=None))
        if "tpr" in interaction.data["values"]:
            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Setze eine Rolle welche in Tickets gepingt werden soll.",
                color=0x2b2d31
            )

            await interaction.response.edit_message(embed = embed, view=...)

    @discord.ui.button(
        label="Weiter  ▶",
        style=discord.ButtonStyle.blurple,
        custom_id="confirm"
    )
    async def confirm_callback(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(
            f"SELECT ticket_channel, ticket_text, ping_role, ticket_category, team_role, button_color, button_text, button_emoji FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        channel = res[0]
        text = res[1]
        ping_role = res[2]
        cat = res[3]
        team = res[4]
        btn_color = res[5]
        btn_text = res[6]
        btn_emoji = res[7]

        if channel is None:
            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Leider Fehlen bei der Einrichtung wichtige Parameter.\n"
                            "Der Bot gibt vor den **Ticket-Kanal, eine Ping Rolle und eine "
                            "Team Rolle** anzugeben.",
                color=0x2b2d31
            )
            await interaction.response.edit_message(embed=embed, view=back_to_panel(timeout=None))
        else:
            embed = discord.Embed(
                title="Ticket Panel | Einrichtung",
                description="Du hast alles **Wichtige** eingerichtet, möchtest du das Panel nun senden"
                            " oder weiter bearbeiten?",
                color=0x2b2d31
            )
            await interaction.response.edit_message(embed=embed, view=confirmation_sending(timeout=None),
                                                    delete_after=15)


class ping_role_view(discord.ui.View):
    @discord.ui.role_select(
        placeholder = "Wähle eine Rolle",
        min_values=1,
        max_values=1
    )
    async def role_select_callback(self, select, interaction: discord.Interaction):
        cursor = ticket_db.cursor()

        cursor.execute(f'''UPDATE ticket_panel SET ping_role = {select.values[0]} WHERE guild_id = {interaction.guild.id}''')
        ticket_db.commit()
        embed = discord.Embed(
            title = "Ticket Panel | Ping Rolle",
            description = f"{select.values[0]} wurde erfolgreich als **Ticket - Ping - Rolle** gesetzt.",
            color = 0x2b2d31
        )
        await interaction.response.edit_message(embed = embed, view = back_to_panel())

# -------------------------------------------- Ticket --------------------------------------------


class confirmation_sending(discord.ui.View):
    @discord.ui.button(
        label="Ticket Senden",
        style=discord.ButtonStyle.green
    )
    async def send_callback(self, button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Das Ticket wurde erfolgreich gesendet.\n Du kannst das Panel nun weiter bearbeiten.",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=back_to_panel(timeout=None))

        cursor = ticket_db.cursor()
        cursor.execute(
            f"SELECT ticket_channel, ticket_text, ping_role, ticket_category, team_role, button_color, button_text, button_emoji FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        channel = res[0]
        text = res[1]
        ping_role = res[2]
        cat = res[3]
        team = res[4]
        btn_color = res[5]
        btn_text = res[6]
        btn_emoji = res[7]

        channel1 = interaction.guild.get_channel(int(channel))
        embed = discord.Embed(
            title=f"{interaction.guild.name}'s Ticket Support",
            description=f"{text}",
            color=0x2b2d31
        )
        embed.set_thumbnail(url=interaction.guild.icon.url)
        embed.timestamp = datetime.datetime.now()

        view = discord.ui.View(timeout=None)

        emoji = None
        style = None
        if btn_color == "blurple":
            style = discord.ButtonStyle.blurple
        elif btn_color == "red":
            style = discord.ButtonStyle.red
        elif btn_color == "grey":
            style = discord.ButtonStyle.grey
        elif btn_color == "green":
            style = discord.ButtonStyle.green
        if btn_emoji:
            emoji = btn_emoji

        create_ticket_button = \
            discord.ui.Button(
                label=btn_text,
                style=style,
                emoji=emoji
            )

        async def create_ticket_callback(self, interaction: discord.Interaction):
            return

        view.add_item(create_ticket_button)
        await channel1.send(embed=embed, view=view)

# -------------------------------------------- Ticket --------------------------------------------

    @discord.ui.button(
        label="Zur Einrichtung",
        style=discord.ButtonStyle.grey
    )
    async def back_to_setup(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"Select "
                       f"guild_id, "
                       f"ticket_channel, "
                       f"ticket_text, "
                       f"ping_role, "
                       f"ticket_category, "
                       f"team_role, "
                       f"button_color, "
                       f"button_text "
                       f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
            color=0x2b2d31
        )

        channel = ""
        if res[1]:
            channel = f"<#{res[1]}>"
        elif res[1] is None:
            channel = "None"
        embed.add_field(
            name="Ticket Channel",
            value=channel
        )
        embed.add_field(
            name="Ticket Text",
            value=res[2]
        )
        embed.add_field(
            name="Ping Role",
            value=res[3]
        )
        embed.add_field(
            name="Ticket Kategorie",
            value=res[4]
        )
        embed.add_field(
            name="Team Rolle",
            value=res[5]
        )
        embed.add_field(
            name="Ticket Button",
            value=f"Farbe: {res[6]}\nText: {res[7]}"
        )

        await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))


class button_customization(discord.ui.View):
    @discord.ui.button(
        label="Zurück",
        emoji="◀",
        style=discord.ButtonStyle.blurple
    )
    async def back_to_panel_callback(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"Select "
                       f"guild_id, "
                       f"ticket_channel, "
                       f"ticket_text, "
                       f"ping_role, "
                       f"ticket_category, "
                       f"team_role, "
                       f"button_color, "
                       f"button_text "
                       f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
            color=0x2b2d31
        )

        channel = ""
        if res[1]:
            channel = f"<#{res[1]}>"
        elif res[1] is None:
            channel = "None"
        embed.add_field(
            name="Ticket Channel",
            value=channel
        )
        embed.add_field(
            name="Ticket Text",
            value=res[2]
        )
        embed.add_field(
            name="Ping Role",
            value=res[3]
        )
        embed.add_field(
            name="Ticket Kategorie",
            value=res[4]
        )
        embed.add_field(
            name="Team Rolle",
            value=res[5]
        )
        embed.add_field(
            name="Ticket Button",
            value=f"Farbe: {res[6]}\nText: {res[7]}"
        )

        await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))

    @discord.ui.button(
        label="Button Text",
        style=discord.ButtonStyle.grey
    )
    async def text_callback(self, button, interaction: discord.Interaction):
        await interaction.response.send_modal(button_text_change(title="Button Text"))

    @discord.ui.button(
        label="Button Farbe",
        style=discord.ButtonStyle.blurple
    )
    async def color_callback(self, button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panel | Button Farbe",
            description="Setze eine von 4 Button Farben.",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=button_color_change(timeout=None))


class ticket_text_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Ticket Text",
                placeholder="...",
                style=discord.InputTextStyle.long,
            )
        )

    async def callback(self, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(
            f'''UPDATE ticket_panel SET ticket_text = '{self.children[0].value}' WHERE guild_id = {interaction.guild.id}''')

        embed = discord.Embed(
            title="Ticket Panel | Ticket Text",
            description="Der **Ticket-Text** wurde erfolgreich aktualisiert.",
            color=0x2b2d31
        )
        embed.add_field(
            name="Neuer Text:",
            value=self.children[0].value
        )

        await interaction.response.send_message(embed=embed, ephemeral=True)

        ticket_db.commit()


class button_text_change(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Button Text",
                placeholder="...",
                style=discord.InputTextStyle.short,
                max_length=100,
                required=True
            )
        )

        self.add_item(
            discord.ui.InputText(
                label="Button Emoji (kein Pflichtfeld)",
                placeholder="<:example:12345678>",
                style=discord.InputTextStyle.short,
                required=False
            )
        )

    async def callback(self, interaction: discord.Interaction):
        emoji = str(self.children[1].value)

        embed = discord.Embed(
            title="Ticket Panel | Button Text",
            description=f"Text: {self.children[0].value}",
            color=0x2b2d31
        )

        if emoji is None:
            embed.description += f"\nEmoji: {self.children[1].value}"

        await interaction.response.edit_message(embed=embed, view=back_to_panel(timeout=None))


class button_color_change(discord.ui.View):
    @discord.ui.select(
        placeholder="Wähle eine Farbe",
        max_values=1,
        min_values=1,
        options=[
            discord.SelectOption(
                label="Blurple",
                value="blurple"
            ),
            discord.SelectOption(
                label="Rot",
                value="red"
            ),
            discord.SelectOption(
                label="Grau",
                value="grey"
            ),
            discord.SelectOption(
                label="Grün",
                value="green"
            )
        ]
    )
    async def button_callor_callback(self, select, interaction: discord.Interaction):
        cursor = ticket_db.cursor()

        if "blurple" in interaction.data["values"]:
            cursor.execute(f'''
            UPDATE ticket_panel SET button_color = 'blurple' WHERE guild_id = {interaction.guild.id}''')
        if "red" in interaction.data["values"]:
            cursor.execute(f'''
            UPDATE ticket_panel SET button_color = 'red' WHERE guild_id = {interaction.guild.id}''')
        if "grey" in interaction.data["values"]:
            cursor.execute(f'''
            UPDATE ticket_panel SET button_color = 'grey' WHERE guild_id = {interaction.guild.id}''')
        if "green" in interaction.data["values"]:
            cursor.execute(f'''
            UPDATE ticket_panel SET button_color = 'green' WHERE guild_id = {interaction.guild.id}''')

        embed = discord.Embed(
            title="Ticket Panel | Button Farbe",
            description=f"Die Farbe wurde erfolgreich zu {select.values[0]}",
            color=0x2b2d31
        )
        await interaction.response.edit_message(embed=embed, view=back_to_panel(timeout=None))

        ticket_db.commit()

    @discord.ui.button(
        label="Zurück",
        emoji="◀",
        style=discord.ButtonStyle.blurple
    )
    async def back_to_panel_callback(self, button, interaction: discord.Interaction):
        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Bearbeite den Button nach deinen Vorstellungen.",
            color=0x2b2d31
        )

        await interaction.response.edit_message(embed=embed, view=button_customization(timeout=None))


class back_to_panel(discord.ui.View):
    @discord.ui.button(
        label="Zurück",
        emoji="◀",
        style=discord.ButtonStyle.blurple
    )
    async def back_to_panel_callback(self, button, interaction: discord.Interaction):
        cursor = ticket_db.cursor()
        cursor.execute(f"Select "
                       f"guild_id, "
                       f"ticket_channel, "
                       f"ticket_text, "
                       f"ping_role, "
                       f"ticket_category, "
                       f"team_role, "
                       f"button_color, "
                       f"button_text "
                       f"FROM ticket_panel WHERE guild_id = {interaction.guild.id}")
        res = cursor.fetchone()

        embed = discord.Embed(
            title="Ticket Panel | Einrichtung",
            description="Herzlich Willkommen in der Einrichtung vom Ticket Panel. "
                        "Folge bitte jedem der Schritte die dir jetzt genannt werden.",
            color=0x2b2d31
        )

        channel = ""
        if res[1]:
            channel = f"<#{res[1]}>"
        elif res[1] is None:
            channel = "None"
        embed.add_field(
            name="Ticket Channel",
            value=channel
        )
        embed.add_field(
            name="Ticket Text",
            value=res[2]
        )
        embed.add_field(
            name="Ping Role",
            value=res[3]
        )
        embed.add_field(
            name="Ticket Kategorie",
            value=res[4]
        )
        embed.add_field(
            name="Team Rolle",
            value=res[5]
        )
        embed.add_field(
            name="Ticket Button",
            value=f"Farbe: {res[6]}\nText: {res[7]}"
        )

        await interaction.response.edit_message(embed=embed, view=einrichtungs_buttons(timeout=None))
