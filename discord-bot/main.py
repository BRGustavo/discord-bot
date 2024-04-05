import discord
from discord.ext import commands
from app import eventos_cog, comandos_cog
from dotenv import load_dotenv
import os
from app import block_verify

load_dotenv()
intents = discord.Intents.all()

bot_gustavo = commands.Bot(command_prefix='!', intents=intents)

@bot_gustavo.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando neste canal.")
        
@bot_gustavo.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.NotOwner):
        await ctx.send(f"{ctx.message.author.mention} Quem você acha que é para tentar fazer isso?")
        
bot_gustavo.add_cog(eventos_cog(bot_gustavo))
bot_gustavo.add_cog(comandos_cog(bot_gustavo))

bot_gustavo.run(str(os.getenv("TOKEN_DISCORD")).strip())    
