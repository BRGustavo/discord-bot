import discord
from discord.ext import commands
import json
import os
import asyncio
import aiohttp
from aiohttp.client_exceptions import ContentTypeError
from logging import getLogger


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
                
                response_status = 500
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

class LogChannel:
    def __init__(self, system:str):
        self.__logger_menu = getLogger(system)
 
    def send_message(self, message:str, msg_type:str="info"):
        msg_types_functions = {
            "info": self.__logger_menu.info,
            "warning": self.__logger_menu.warning,
            "error": self.__logger_menu.error,
            "critical": self.__logger_menu.critical
        } 
        msg_types_functions[msg_type](message)


def verify_channel_allowed():
    async def check(ctx):
        with open("./channels.json", "r") as file:
            channels_allowed = json.load(file)
            return str(ctx.channel.id) in channels_allowed.get("allowed_channels", [])
        
    return commands.check(check)
