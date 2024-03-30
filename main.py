import discord
from discord.ext import commands
from app import eventos_cog, comandos_cog

intents = discord.Intents.default()
intents.messages = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando neste canal.")


bot.add_cog(eventos_cog(bot))
bot.add_cog(comandos_cog(bot))

bot.run('aoksdodkoaodkasao')    