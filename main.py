import discord
import random
import os
import json
import threading
import re
from discord.ext import commands
from dotenv import load_dotenv

# Slack imports
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler

load_dotenv()

# Discord config
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
GUILD_ID = int(os.getenv("DISCORD_GUILD_ID"))

# Slack config
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Cargar frases desde frases.json
with open("frases.json", "r", encoding="utf-8") as f:
    FRASES_LOVE = json.load(f)["frases"]

# Discord Bot
class MyClient(discord.Client):
    def __init__(self):
        intents = discord.Intents.default()
        intents.message_content = True
        super().__init__(intents=intents)
        self.tree = discord.app_commands.CommandTree(self)

    async def setup_hook(self):
        @self.tree.command(name="love", description="El bot te tira una frase sarcástica sobre malo platform")
        async def love(interaction: discord.Interaction):
            frase = random.choice(FRASES_LOVE)
            await interaction.response.send_message(frase)

        await self.tree.sync(guild=discord.Object(id=GUILD_ID))

    async def on_message(self, message):
        if message.author == self.user:
            return
        contenido = message.content.strip().lower()
        if contenido == '!love' or 'malo' in contenido:
            frase = random.choice(FRASES_LOVE)
            await message.channel.send(frase)

def run_discord():
    client = MyClient()
    client.run(DISCORD_TOKEN)

# Slack Bot
app = App(token=SLACK_BOT_TOKEN)

@app.command("/love")
def handle_love_command(ack, respond):
    ack()
    frase = random.choice(FRASES_LOVE)
    respond(frase)

@app.message(re.compile(r"(!love|malo)", re.IGNORECASE))
def handle_love_message(message, say):
    frase = random.choice(FRASES_LOVE)
    say(frase)

def run_slack():
    handler = SocketModeHandler(app, SLACK_APP_TOKEN)
    handler.start()

if __name__ == "__main__":
    # Ejecutar ambos bots en hilos separados
    discord_thread = threading.Thread(target=run_discord)
    slack_thread = threading.Thread(target=run_slack)
    discord_thread.start()
    slack_thread.start()
    discord_thread.join()
    slack_thread.join()