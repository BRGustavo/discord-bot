import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp
from aiohttp.client_exceptions import ContentTypeError
from app.block_verify import APICommunicate, LogChannel
from logging import basicConfig, DEBUG, INFO, FileHandler, StreamHandler    

class Eventos(commands.Cog):
    def __init__(self, bot:commands.Bot):
        self.bot = bot
        self.api_endpoint = os.getenv("API_ENDPOINT")
        self.log = LogChannel("DiscordEvents")

    @commands.Cog.listener()
    async def on_ready(self) -> None:
        """Função chamada quando o robô inicia.
        """
        await self.bot.change_presence(
            activity=discord.Game("Grand Theft Auto San Andreas")
        )
        basicConfig(
            level=INFO,
            format="[%(levelname)s] %(asctime)s - %(name)s - %(message)s",
            handlers=[FileHandler(r"log.txt", "a", "utf-8")]
        )
        await asyncio.sleep(1)
        await self.save_community_info()
        
    @commands.Cog.listener()
    async def on_member_remove(self, member:discord.Member):
        guild = member.guild 
        channel = member.guild.system_channel

        api_connection = APICommunicate()
        response_values = await api_connection("GET", f"api/channel/?community={guild.id}", {})

        if response_values.get("status", 0) == 200:
            for response_item in response_values.get("values", []):
                if response_item.get("is_remove_channel", False):
                    embed = discord.Embed(
                        description=f'{member.mention} Deixou o servidor!',
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Até mais colega^!", value="", inline=True)  

                    embed.set_footer(text=f'{guild.name} :P')
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=guild.name, icon_url=guild.icon_url)
                    msg_channel = await self.bot.fetch_channel(response_item.get("channel", 0))            
                    await msg_channel.send(embed=embed)

    @commands.Cog.listener()
    async def on_member_join(self, member:discord.Member):
        guild = member.guild 
        channel = member.guild.system_channel

        api_connection = APICommunicate()
        response_values = await api_connection("GET", f"api/channel/?community={guild.id}", {})

        if response_values.get("status", 0) == 200:
            for response_item in response_values.get("values", []):
                if response_item.get("is_welcome_channel", False):
                    embed = discord.Embed(
                        description=f'{member.mention} Entrou no canal!',
                        color=discord.Color.blue()
                    )
                    embed.add_field(name="Seja bem-vindo!", value="", inline=True)  

                    embed.set_footer(text=f'{guild.name} :P')
                    embed.set_thumbnail(url=member.avatar_url)
                    embed.set_author(name=guild.name, icon_url=guild.icon_url)
                    msg_channel = await self.bot.fetch_channel(response_item.get("channel", 0))            
                    await msg_channel.send(embed=embed)
        else:
            self.log.send_message(f"An error occurred while sending the welcome message: Status: {response_values['status']} Error: {response_values.get('values')}", "error")

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

        if "set me" in message.content.lower() or "veteran" in message.content.lower() or "set me veteran" in message.content.lower() or "veteran member" in message.content.lower():
            await message.channel.send("no.")

        if message.guild is None:
            self.log.send_message(f"{message.author} no canal privado: {message.content}", "info")

    @commands.Cog.listener()
    async def on_member_update(self, before:discord.Member, after:discord.Member):
        
        if before.nick != after.nick:
            await self.send_messge_adm(f"""
                Opa! Passando para te avisar que o usuário {before.nick} alterou o nick para {after.nick}, verifique atividades suspeitas.
            """)

        if before.roles != after.roles:
            roles_removed = [role.name for role in before.roles if role not in after.roles]
            roles_added = [role.name for role in after.roles if role not in before.roles]

            embed = discord.Embed(
                description=f'{before.mention} has been updated.',
                color=discord.Color.blue()
            )
            if len(roles_added) >= 1:
                embed.add_field(name='Roles Add', value='\n'.join(roles_added), inline=False)
            if len(roles_removed):
                embed.add_field(name='Roles Removed', value='\n'.join(roles_removed), inline=True)  

            embed.set_footer(text=f'{before.guild.name} :P')
            embed.set_thumbnail(url=before.avatar_url)
            embed.set_author(name=before.guild.name, icon_url=before.guild.icon_url)

            api_connection = APICommunicate()
            response_values = await api_connection("GET", f"api/channel/?community={before.guild.id}", {})

            if response_values.get("status", 0) == 200:
                for response_item in response_values.get("values", []):
                    if response_item.get("is_role_channel", False):
                        msg_channel = await self.bot.fetch_channel(response_item.get("channel", 0)) 
                
                        await msg_channel.send(embed=embed)
            else:
                self.log.send_message(f"An error occurred while locating the community's channels. {before.guild.name}.", "error")            

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
                if response_value.get("status", 0) != 201:
                    self.log.send_message(f"Status different when inserting channel {response_value.get('status', 0)}", "error")

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
            if response_value.get("status", 0) != 201:
                self.log.send_message(f"Status diferente ao inserir canal {response_value.get('status', 0)}", "error")
            

eventos_cog = Eventos