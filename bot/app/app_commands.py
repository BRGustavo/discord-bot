import discord
from discord.ext import commands
from app.block_verify import verify_channel_allowed

class Comandos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.command()
    @verify_channel_allowed()
    async def ola(self, ctx:commands.Context) -> None:
        await ctx.send(f"Olá! {ctx.message.author.mention}")

    @commands.command()
    @commands.is_owner()
    async def shutup(self, ctx:commands.Context):
        await ctx.send("Entendi :c\nVou ficar calado.")

    @commands.command()
    @commands.is_owner()
    async def cc(self, ctx:commands.Context, qtd:int):
        await ctx.channel.purge(limit=qtd+1)
        

@commands.Cog.listener()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("Você não tem permissão para executar este comando neste canal.")

comandos_cog = Comandos