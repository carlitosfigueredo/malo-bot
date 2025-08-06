import discord
import random
import os
import json
from discord.ext import commands
from dotenv import load_dotenv

load_dotenv()

TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

# Cargar frases desde frases.json
with open("frases.json", "r", encoding="utf-8") as f:
    FRASES_LOVE = json.load(f)["frases"]

class MyClient(discord.Client):
    def __init__(self):
        super().__init__(intents=discord.Intents.default())
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        @self.tree.command(name="love", description="El bot te tira una frase sarcástica sobre malo platform")
        async def love(interaction: discord.Interaction):
            frase = random.choice(FRASES_LOVE)
            await interaction.response.send_message(frase)

        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

    async def on_message(self, message):
        # Evitar que el bot se responda a sí mismo
        if message.author == self.user:
            return
        if message.content.strip().lower() == '!love':
            frase = random.choice(FRASES_LOVE)
            await message.channel.send(frase)


client = MyClient()
client.run(TOKEN)
