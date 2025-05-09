from typing import AnyStr

import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv

load_dotenv()

DISCORD_AUTH_TOKEN = os.getenv('GCP_PROJECT_ID')
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")

class MyClient(discord.Client):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_in = False

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.logged_in = True

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self.send_message.start()

    async def on_message(self, message):
        print(f'Message from {message.author}: {message.content}')

    @tasks.loop(seconds=60)  # task runs every 60 seconds
    async def send_message(self):
        if not self.logged_in:
            return
        user = await self.fetch_user(DISCORD_USER_ID)
        await user.send("HI")

    @send_message.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in


intents = discord.Intents.default()
intents.message_content = True

client = MyClient(intents=intents)
client.run(DISCORD_AUTH_TOKEN)
