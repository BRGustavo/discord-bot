import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp
from aiohttp.client_exceptions import ContentTypeError


class APICommunicate:

    def __init__(self):
        self.api_base_url = os.getenv("API_ENDPOINT")

        self.__api_token = "0"
        self.api_refresh_token = ""

    async def generate_api_token(self) -> str:
        """Função chamada para realizar a chamada do token de acesso ao API
        Returns:
            str: JWT Token access
        """
        return_value = ""
        try:
            async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
                async with session.post(
                    url=self.api_base_url+"/api/token/", 
                    headers={"Host":"discordapp"},
                    json={
                        "username": os.getenv("API_USERNAME"),
                        "password": os.getenv("API_PASSWORD")
                    }
                ) as response:
                    
                    if response.status == 200:
                        value_response = await response.json()
                        return_value = value_response.get("access","")
                        self.api_refresh_token = value_response.get("refresh", "")
                        self.__api_token = return_value

        except Exception as e:
            return_value = str(e)
        finally:
            return return_value

    async def __call__(self, method:str="GET", endpoint:str="", json_content=None, header_values={"Content-Type": "application/json"}):
        if len(self.api_base_url) <=0:
            os.getenv("API_ENDPOINT")
        
        if self.__api_token == "0":
            valor = await self.generate_api_token()

        async with aiohttp.ClientSession(connector=aiohttp.TCPConnector(ssl=False)) as session:
            async with session.request(
                method, 
                f"{self.api_base_url}/{endpoint}", 
                headers={
                    **header_values,
                    "Authorization": f"Bearer {self.__api_token}",
                    "Host":"discordapp"
                }, 
                json=json_content
            ) as response:
                
                try:
                    response_values = await response.json()
                    response_status = response.status

                except ContentTypeError as e:
                    response_content = await response.text()
                    with open("remover.html", "w") as file:
                        file.write(str(response_content))

                    response_values = {}
                    response_status = response.status

                finally:
                    return {
                        "status": int(response_status),
                        "values": response_values
                    }

class Eventos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.api_endpoint = os.getenv("API_ENDPOINT")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Função chamada quando o robô inicia.
        """
        await self.bot.change_presence(
            activity=discord.Game("Grand Theft Auto San Andreas")
        )
        await asyncio.sleep(1)
        await self.save_community_info()
        
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

    async def save_community_info(self):
        bot_guilds = self.bot.guilds

        api_connection = APICommunicate()
        """Inserindo comunidades que o bot faz parte no banco."""
        for guild_item in bot_guilds:
            response_value = await api_connection("POST", "api/community/", json_content={
                "community": str(guild_item.id),
                "name": str(guild_item.name),
                "owner_name": str(guild_item.owner),
                "created_at": str(guild_item.created_at.strftime("%Y-%m-%d"))
            })
            if response_value.get("status", "") == 201:
                await self.save_community_members(guild_item)
                await self.save_community_channels(response_value.get("values",{}).get("id", None), guild_item)
    
    async def save_community_channels(self, db_id, guild):
        api_connection = APICommunicate()
        for channel_info in guild.channels:
            
            is_news_value = is_nsfw_value = False
            try:
                topic_value = channel_info.topic
                is_news_value = channel_info.is_news
                is_nsfw_value = channel_info.is_nsfw

            except AttributeError:
                topic_value = "Not set"
            finally:
                response_value = await api_connection("POST", "api/channel/", json_content={
                "community_id": int(db_id),
                "channel": str(channel_info.id),
                "name": str(channel_info.name),
                "topic": str(topic_value),
                "is_news": bool(is_news_value),
                "is_nsfw": bool(is_nsfw_value),
                "position": int(channel_info.position),
                "type": str(channel_info.type)              
                })
            

    async def save_community_members(self, guild):
        api_connection = APICommunicate()
        for member_info in guild.members:
            response_value = await api_connection("POST", "api/member/", json_content={
                "id_member": str(member_info.id),
                "nick": str(member_info.nick),
                "name": str(member_info.name),
                "descriminator": str(member_info.discriminator),
                "is_bot": member_info.bot
            })

            

eventos_cog = Eventos