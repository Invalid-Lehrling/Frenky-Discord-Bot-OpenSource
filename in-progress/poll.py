import discord
from discord.ext import commands

class basic_module(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

  poll = discord.SlashCommandGroup("poll")     
   
  @discord.slash_command(
    name = "create",
    description = ""
  )        
  @commands.has_permission(administrator = True)
  async def _create_poll(self, ctx, channel: discord.TextChannel):
    
