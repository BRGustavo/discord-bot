import discord
from discord.ext import commands
import json


class Eventos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Função chamada quando o robô inicia.
        """
        await self.bot.change_presence(
            activity=discord.Game("Grand Theft Auto San Andreas")
        )
        
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        guild = member.guild 
        channel = member.guild.system_channel

        await channel.send(f"O usuário {member.mention} saiu do servidor!")     

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        guild = member.guild 
        channel = member.guild.system_channel

        await channel.send(f"O usuário {member.mention} entrou do servidor! Seja Bem-Vindo(a)!")        

    @commands.Cog.listener()
    async def on_message(self, message:discord.Message) -> None:
        """Função chamada toda vez que algúem envia uma mensagem dentro de um canal que o bot faz parte.
        Args:
            message (discrod.Message): Objeto contendo informações da mensagem.
        """
        if message.author == self.bot.user and ("Just joined the server From" in message.content or "Has joined the Zombie Survival Mode" in message.content):
            await message.channel.send("!m wb")

        elif message.author == self.bot.user:
            return 

        if message.guild is None:
            print(f"{message.author} no canal privado: {message.content}", flush=True)

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        
        if before.nick != after.nick:
            await self.send_messge_adm(f"""
                Opa! Passando para te avisar que o usuário {before.nick} alterou o nick para {after.nick}, verifique atividades suspeitas.
            """)

        if before.roles != after.roles:
            roles_removed = [role.name for role in before.roles if role not in after.roles]
            roles_added = [role.name for role in after.roles if role not in before.roles]

            await self.send_messge_adm(f"""
                Opa! Passando para te avisar que os lvls do usuário {before.display_name} foram alterados!! Fique de olho em alterações suspeitas.
            """)

    async def send_messge_adm(self, message:str) -> None:
        """Função responsável por enviar msgs de alerta para administradoes da comunidade a respeito de mudança no servidor.
        Args:
            message (str): Mensagem a ser enviada para equipe de Adm.
        """
        with open("./channels.json") as file:
            users_list = json.loads(file.read())
        
            for adm_info in users_list.get("report_activities", []):
                user = await self.bot.fetch_user(adm_info) 
                await user.send(message)

eventos_cog = Eventos