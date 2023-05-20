import datetime
import json
import random

import discord
from discord.ext import commands

with open("json-runfile/runfile.json", "r") as f:
    runfile_data = json.load(f)

command_prefix = runfile_data["standard-prefix"]
support = "https://discord.gg/xsqv57JnF4"

bot = commands.Bot(command_prefix=command_prefix, intents=discord.Intents.all())


class help_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @discord.slash_command(
        name="help",
        description="📌 × Führe diesen Befehl aus um eine liste aller Befehle des Bots zu erhalten.",
    )
    async def _help_command(self, ctx):
        with open("json-databases/prefixes.json", "r") as f:
            prefix_get = json.load(f)

        guild_prefix = prefix_get[str(ctx.guild.id)]["prefix"]

        embed_start = discord.Embed(
            description="> `💡` × Hier findest du **alle wichtigen Informationen** zu sämtlichen Befehlen, "
                        "welche dieser Discord Bot besitzt. Diese **Liste** kann dir bei der Nutzung dieses "
                        "Bots **helfen**. Wenn du **Fragen** hast oder **Hilfe** brauchst kannst "
                        "du dir **[hier](https://discord.gg/xsqv57JnF4)** hilfe suchen!\n⠀\n"
                        "**⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯**",
            color=0x5e63ea)
        embed_start.add_field(name="<:fb_information:1097190720038764695>  |  Grundlegende Infos",
                              value=f"**›** Gesamte Server: `{len(self.bot.guilds)}`\n"
                                    f"**›** Gesamte Nutzer: `{len(self.bot.users)}`\n"
                                    f"**›** Frenky's Ping: `{f'{round(self.bot.latency * 1000)}ms'}`")
        embed_start.add_field(name="<:fb_server:1097203531049615512>  |  Serverspezifische Infos",
                              value=f"**›** Server Prefix: `{guild_prefix}` & `/`\n"
                                    f"**›** Server Owner: `{ctx.guild.owner}`\n")
        embed_start.add_field(name="**⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯⎯**\n⠀\n",
                              value="> <:fb_idee:1097206098827686041> **›** Du kannst durch das **Klicken** in den unten angehefteten Select die gesamten Befehlskategorieen sehen!",
                              inline=False)
        embed_start.set_thumbnail(url=self.bot.user.avatar.url)
        embed_start.set_footer(text="Frenky | Help Menü")
        embed_start.timestamp = datetime.datetime.now()
        embed_start.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # Embed Moderation

        embed_mtc = discord.Embed(
            description="> `📛` × Hier findest du **alle befehle** zur *Kategorie* **Moderation-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_mtc.add_field(
            name="</ban:1099080904107905064>",
            value="Banne ein ausgewähltes Mitglied von diesem Server."
        )
        embed_mtc.add_field(
            name="</kick:1097396421629575208>",
            value="Ein ausgewähltes Mitglied wird vom Server gekickt.",
            inline=False
        )
        embed_mtc.add_field(
            name="</timeout set:1097396421629575210>",
            value="Versetze einen Nutzer in den Timeout für eine Zeit.",
            inline=False
        )
        embed_mtc.add_field(
            name="</timeout remove:1097396421629575210>",
            value="Hole ein Nutzer wieder aus dem Timeout zurück.",
            inline=False
        )
        embed_mtc.add_field(
            name="</purge:1099092051401908234>",
            value="Lösche eine Anzahl an Nachrichten in einem Kanal.",
            inline=False
        )
        embed_mtc.add_field(
            name="</add emoji:1101175657142173786>",
            value="Fügt ein ausgewähltes Emoji zum Server hinzu",
            inline=False
        )
        embed_mtc.set_thumbnail(url=self.bot.user.avatar.url)
        embed_mtc.set_footer(text="Frenky | Help Menü")
        embed_mtc.timestamp = datetime.datetime.now()
        embed_mtc.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # Embed Usercommands

        embed_usc = discord.Embed(
            description="> `📚` × Hier findest du **alle befehle** zur *Kategorie* **User & Info-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_usc.add_field(
            name="</userinfo:1097479637765996554>",
            value="Gibt dir eine Auskunft über einen Nutzer."
        )
        embed_usc.add_field(
            name="</serverinfo:1097489921180172389>",
            value="Zeigt dir eine Info des aktuellen Servers.",
            inline=False
        )
        embed_usc.add_field(
            name="</avatar:1097552265889468507>",
            value="Hiermit kannst du den Avatar eines Nutzers sehen.",
            inline=False
        )
        embed_usc.add_field(
            name="</about:1097554916567953514>",
            value="Zeigt Informationen über diesen Bot.",
            inline=False
        )
        embed_usc.set_thumbnail(url=self.bot.user.avatar.url)
        embed_usc.set_footer(text="Frenky | Help Menü")
        embed_usc.timestamp = datetime.datetime.now()
        embed_usc.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # Embed Roles

        embed_rlc = discord.Embed(
            description="> `🎨` × Hier findest du **alle befehle** zur *Kategorie* **Role-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_rlc.add_field(
            name="</autorole-add:1097435041702891620>",
            value="Füge eine Autorole in die Rollenliste des Servers hinzu."
        )
        embed_rlc.add_field(
            name="</autorole-remove:1097445381970858014>",
            value="Lösche eine Autorole aus der Rollenliste des Servers.",
            inline=False
        )
        embed_rlc.add_field(
            name="</autorole-list:1097448413919973426>",
            value="Lass dir die Liste aller Autoroles anzeigen.",
            inline=False
        )
        embed_rlc.set_thumbnail(url=self.bot.user.avatar.url)
        embed_rlc.set_footer(text="Frenky | Help Menü")
        embed_rlc.timestamp = datetime.datetime.now()
        embed_rlc.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        embed_log = discord.Embed(
            description="> `💾` × Hier findest du **alle befehle** zur *Kategorie* **Logging-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_log.add_field(
            name="</log set:1101176343951056976>",
            value="Setze einen LogChannel auf dem Server."
        )
        embed_log.add_field(
            name="</log remove:1101176343951056976>",
            value="Entferne einen LogChannel vom Server.",
            inline=False
        )
        embed_log.set_thumbnail(url=self.bot.user.avatar.url)
        embed_log.set_footer(text="Frenky | Help Menü")
        embed_log.timestamp = datetime.datetime.now()
        embed_log.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # Embed Message

        embed_mgc = discord.Embed(
            description="> `💬` × Hier findest du **alle befehle** zur *Kategorie* **Message-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_mgc.add_field(
            name="</autodelete add:1101176035183181967>",
            value="Erstelle ein Autodelete in diesem Kanal."
        )
        embed_mgc.add_field(
            name="</autodelete remove:1101176035183181967>",
            value="Entferne einen Kanel der als Autodelete Eingestellt war.",
            inline=False
        )
        embed_mgc.set_thumbnail(url=self.bot.user.avatar.url)
        embed_mgc.set_footer(text="Frenky | Help Menü")
        embed_mgc.timestamp = datetime.datetime.now()
        embed_mgc.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # Embed Welcome

        embed_wec = discord.Embed(
            description="> `👋` × Hier findest du **alle befehle** zur *Kategorie* **Welcome-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_wec.add_field(
            name="</welcome channel:1101175657142173788>",
            value="Lege einen Willkommenskanal für den Server fest."
        )
        embed_wec.add_field(
            name="</welcome text:1101175657142173788>",
            value="Lege eine eigene Willkommensnachricht fest.",
            inline=False
        )
        embed_wec.add_field(
            name="</welcome type:1101175657142173788>",
            value="Setze einen von drei Typen für deine Nachricht.",
            inline=False
        )
        embed_wec.add_field(
            name="</welcome button:1101175657142173788>",
            value="Bestimme ob der Begrüßungsbutton aktiviert ist oder nicht.",
            inline=False
        )
        embed_wec.add_field(
            name="</welcome remove:1101175657142173788>",
            value="Entferne das Welcome Screening vom Server.",
            inline=False
        )
        embed_wec.set_thumbnail(url=self.bot.user.avatar.url)
        embed_wec.set_footer(text="Frenky | Help Menü")
        embed_wec.timestamp = datetime.datetime.now()
        embed_wec.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # tempvoice embed

        embed_tec = discord.Embed(
            description="> `🔊` × Hier findest du **alle befehle** zur *Kategorie* **Tempvoice-Commands**."
                        "Wenn du **Fragen** hast oder **Hilfe** brauchst kannst"
                        f"du dir **[hier]({support})** hilfe suchen!\n⠀\n",
            color=0x5e63ea)
        embed_tec.add_field(
            name="</tempvoice setup:1101174102988947488>",
            value="Richte hiermit das Tempvoice System auf dem Server ein."
        )
        embed_tec.add_field(
            name="</tempvoice remove:1101175657142173788>",
            value="Entferne das Tempvoice System vom Server.",
            inline=False
        )
        embed_tec.set_thumbnail(url=self.bot.user.avatar.url)
        embed_tec.set_footer(text="Frenky | Help Menü")
        embed_tec.timestamp = datetime.datetime.now()
        embed_tec.set_author(name="Frenky-Bot | Help Menü", icon_url=self.bot.user.avatar.url)

        # help Select

        selects = (
            discord.ui.Select(
                placeholder="📚 | Wähle eine Kategorie",
                min_values=1,
                max_values=1,
                row=0,
                options=[
                    discord.SelectOption(
                        label="Startseite",
                        description="Kehre zurück zur Ersten Seite des Menüs",
                        emoji="<:fb_home:1097194608871616634>",
                        value="sts"
                    ),
                    discord.SelectOption(
                        label="User Commands",
                        description="Befehle die jeder Nutzer verwenden kann.",
                        emoji="<:fb_userhead:1097194422594191390>",
                        value="usc"
                    ),
                    discord.SelectOption(
                        label="Moderator Commands",
                        description="Wichtige Befehle im Bereich der Moderation",
                        emoji="<:fb_moderator:1097388199376068679>",
                        value="mtc"
                    ),
                    discord.SelectOption(
                        label="Message Commands",
                        description="Sämtliche Nachrichten Befehle findest du hier.",
                        emoji="<:fb_message:1097549644403318804>",
                        value="mgc"
                    ),
                    discord.SelectOption(
                        label="Logging Commands",
                        description="Setze das Log System auf deinem Server ein.",
                        emoji="<:fb_logging:1099332234051326043>",
                        value="log"
                    ),
                    discord.SelectOption(
                        label="Welcome Commands",
                        description="Ermöglicht es dir Willkommensnachrichten anzuzeigen.",
                        emoji="<:fb_message:1097549644403318804>",
                        value="wec"
                    ),
                    discord.SelectOption(
                        label="Tempvoice Commands (Temporär Deaktiviert)",
                        description="Richte hiermit das Tempchannel System ein.",
                        emoji="<:fb_voice:1097500430071758978>",
                        value="nonetec"
                    ),
                    discord.SelectOption(
                        label="Role Commands (Temporär Deaktiviert)",
                        description="Benutze sie um Einstellungen für Rollen zu tätigen.",
                        emoji="<:fb_rocket:1097451173650370590>",
                        value="nonerole"
                    ),
                    discord.SelectOption(
                        label="Level Commands (soon)",
                        description="Hiermit kannst du das Levelsystem einrichten.",
                        emoji="<:fb_level:1097455801595084805>",
                        value="none2"
                    ),
                    discord.SelectOption(
                        label="Giveaway Commands (soon)",
                        description="Hier stehen alle Infos für Gewinnspiele.",
                        emoji="<:fb_gewinnspiel:1097456715928178749>",
                        value="none3"
                    )
                ]
            )
        )

        async def help_callback(interaction: discord.Interaction):
            if "sts" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_start)
            if "usc" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_usc)
            if "mtc" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_mtc)
            if "mgc" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_mgc)
            if "log" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_log)
            if "rlc" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_rlc)
            if "wec" in interaction.data["values"]:
                await interaction.response.edit_message(embed=embed_wec)
            if "tec" in interaction.data['values']:
                await interaction.response.edit_message(embed=embed_tec)

        selects.callback = help_callback

        view = discord.ui.View()
        start_button = discord.ui.Button(emoji="<:fb_home:1097194608871616634>", style=discord.ButtonStyle.blurple,
                                         row=1)
        idee = discord.ui.Button(label="Idee/Bug", style=discord.ButtonStyle.blurple, row=1)

        async def start_button_callback(interaction: discord.Interaction):
            await interaction.response.edit_message(embed=embed_start)

        async def vorschlag_callback(interaction: discord.Interaction):
            modal = vorschlag_modal(title="Reiche einen Vorschlag hier ein")
            await interaction.response.send_modal(modal)

        start_button.callback = start_button_callback
        idee.callback = vorschlag_callback

        view.add_item(discord.ui.Button(label="Support", style=discord.ButtonStyle.url, row=1,
                                        url=f"{support}"))
        view.add_item(discord.ui.Button(label="Invite", style=discord.ButtonStyle.url, row=1,
                                        url="https://discord.com/api/oauth2/authorize?client_id=1097176283198279820&permissions=8&scope=bot%20applications.commands"))
        view.add_item(
            discord.ui.Button(label="Docs", style=discord.ButtonStyle.url, row=1, url="https://docs-frenky-bot.carrd.co/"))
        view.add_item(start_button)
        view.add_item(selects)
        view.add_item(idee)
        await ctx.respond(embed=embed_start, view=view, ephemeral=True)


def setup(bot):
    bot.add_cog(help_module(bot))


class vorschlag_modal(discord.ui.Modal):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.add_item(
            discord.ui.InputText(
                label="Dein Vorschlag",
                placeholder="Schreibe hier...",
                style=discord.InputTextStyle.long
            )
        )

    async def callback(self, interaction: discord.Interaction):
        with open("json-databases/bot-ideen.json", "r") as f:
            vorschlag_data = json.load(f)

        num = random.randint(100000, 999999)

        if interaction.user.id in vorschlag_data:
            await interaction.response.send_message(
                "<:fb_warn:1097213764396384409> **›** Du kannst maximal einen Vorschlag einreichen!", ephemeral=True)
            return
        else:
            if interaction.user.id not in vorschlag_data:
                vorschlag_data[str(interaction.user.id)] = {}
                vorschlag_data[str(interaction.user.id)]["Vorschlag"] = self.children[0].value
                vorschlag_data[str(interaction.user.id)]["id"] = num

            with open("json-databases/bot-ideen.json", "w") as f:
                json.dump(vorschlag_data, f, indent=4)

            channel = discord.utils.get(interaction.guild.channels, id=1097211869711831060)
            embed = discord.Embed(title=f"Ein neuer Vorschlag von {interaction.user.name}",
                                  description=f"```fix\n{self.children[0].value}```",
                                  color=0x5e63ea)
            embed.set_footer(text=f"id = {num}")
            embed.timestamp = datetime.datetime.now()
            await channel.send(embed=embed)

            await interaction.response.send_message(
                "<:fb_yes:1097215591183548557> **›** Dein Vorschlag wurde erfolgreich eingereicht, das Team wird ihn sich demnächst ansehen",
                ephemeral=True)
