import discord
from discord.ext import commands
from app.block_verify import verify_channel_allowed, APICommunicate, LogChannel

class Comandos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.log = LogChannel("DiscordCommands")

    @commands.command()
    async def hello(self, ctx:commands.Context) -> None:
        await ctx.send(f"Hellow! {ctx.message.author.mention}")

    @commands.command()
    @commands.is_owner()
    async def cc(self, ctx:commands.Context, qtd:int=1):
        if qtd >= 1 and qtd <= 100:
            await ctx.channel.purge(limit=qtd+1)
        else:
            await ctx.send("The value of messages passed as a parameter is too high, please consider smaller values.")

    @commands.command()
    async def botcommands(self, ctx: commands.Context):
        try:
            embed = discord.Embed(
                title=f"Command List - {ctx.guild.name}",
                description=f"{ctx.author.mention}, here are some available commands:",
                color=discord.Color.blue()
            )

            command_info_msgs = """
            `!setwelcomechannel on/off` - Define default welcome messages.
            `!setleftchannel on/off` - Define default farewell messages.
            `!setrolechannel on/off` - Define default role update messages.
            """

            command_general_msgs = """
            `!cc {msg lines}` - Clear channel messages.
            """

            commands_interaction = """
            `!hello` - The bot says hello to you! :wave:
            """

            embed.add_field(name='Server Configuration Commands', value=command_info_msgs, inline=False)
            embed.add_field(name='Server General Commands', value=command_general_msgs, inline=False)
            embed.add_field(name='Server Interaction Commands', value=commands_interaction, inline=False)

            embed.set_footer(text='footer testeee')
            embed.set_thumbnail(url=ctx.guild.icon_url)

            await ctx.send(embed=embed)

        except Exception as e:
            self.log.send_message(f"An error occurred while sending a message with commands in the {ctx.guild.name} community: {str(e)}")

    @commands.command()
    @commands.is_owner()
    async def setwelcomechannel(self, ctx:commands.Context, parameter:str="None"):
        try:
            api_connection = APICommunicate()
            if parameter.lower() == "on":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_welcome_channel": True })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal foi atualizado para receber mensagens de boas-vindas!")

            elif parameter.lower() == "off":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_welcome_channel": False })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal não recebera mais mensagens boas-vindas!")
            else:
                await ctx.send("Use parametro on/off para ativar ou desativar as mensagens de boas-vindas.")

        except Exception as e:
            self.log.send_message(f"An error occurred while changing the channel that receives messages about welcome community {ctx.guild.name}: {str(e)}")

    @commands.command()
    @commands.is_owner()
    async def setleftchannel(self, ctx:commands.Context, parameter:str="None"):
        try:
            api_connection = APICommunicate()
            if parameter.lower() == "on":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_remove_channel": True })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal foi atualizado para receber mensagens de saida!")

            elif parameter.lower() == "off":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_remove_channel": False })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal não recebera mais mensagens de saida!")
            else:
                await ctx.send("Use parametro on/off para ativar ou desativar as mensagens de saida.")

        except Exception as e:
            self.log.send_message(f"An error occurred while changing the channel that receives messages about members leaving community {ctx.guild.name}: {str(e)}")

    @commands.command()
    @commands.is_owner()
    async def setrolechannel(self, ctx:commands.Context, parameter:str="None"):
        try:
            api_connection = APICommunicate()
            if parameter.lower() == "on":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_role_channel": True })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal foi atualizado para receber mensagens de atualização de cargos!")

            elif parameter.lower() == "off":
                response_value = await api_connection("PATCH", f"api/channel/{ctx.channel.id}/",{ "is_role_channel": False })

                if response_value.get("status", 500) == 200:
                    await ctx.send(f"{ctx.author.mention} esse canal não recebera mais mensagens de atualização de cargos!")
            else:
                await ctx.send("Use parametro on/off para ativar ou desativar as mensagens de atualização de cargos")

        except Exception as e:
            self.log.send_message(f"A error occurred while changing the channel that receives role change messages in community {ctx.guild.name}: {str(e)}")

    @commands.command()
    async def helper(self, ctx):
        embed = discord.Embed(
            description=f'{ctx.username} Teste',
            color=discord.Color.blue()
        )
        embed.add_field(name='Campo 1', value='Valor 1', inline=False)
        embed.add_field(name='Campo 2', value='Valor 2', inline=True)  
        embed.set_footer(text='footer testeee')
        embed.set_author(name=ctx.guild.name, icon_url=ctx.guild.icon_url)
        await ctx.send(embed=embed)


@commands.Cog.listener()
async def on_command_error(ctx, error):
    if isinstance(error, commands.CheckFailure):
        await ctx.send("You do not have permission to execute this command in this channel.")

comandos_cog = Comandos