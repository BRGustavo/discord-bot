import discord
from discord.ext import commands
import json


def verify_channel_allowed():
    async def check(ctx):
        with open("./channels.json", "r") as file:
            channels_allowed = json.load(file)
            return str(ctx.channel.id) in channels_allowed.get("allowed_channels", [])
        
    return commands.check(check)
