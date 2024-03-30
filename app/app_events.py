import discord
from discord.ext import commands

class Eventos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        await self.bot.change_presence(
            activity=discord.Game("Grand Theft Auto San Andreas")
        )

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user and "Just joined the server From" in message.content:
            await message.channel.send("!m wb")

        elif message.author == self.bot.user:
            return 
        
        print(f"{message.author}: {message.content}", flush=True)

eventos_cog = Eventos