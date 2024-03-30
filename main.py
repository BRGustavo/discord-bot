import discord
from discord.ext import commands
from app import eventos_cog, comandos_cog

intents = discord.Intents.all()

bot_gustavo = commands.Bot(command_prefix='!', intents=intents)

@bot_gustavo.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando neste canal.")
        
bot_gustavo.add_cog(eventos_cog(bot_gustavo))
bot_gustavo.add_cog(comandos_cog(bot_gustavo))

with open("password.txt", "r") as file:
    bot_gustavo.run(str(file.read()).strip())    