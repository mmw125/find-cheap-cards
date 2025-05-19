import discord
from discord.ext import tasks
import os
from dotenv import load_dotenv
from typing import Generator

from prices.listing import find_prices

load_dotenv(verbose=true)

DISCORD_AUTH_TOKEN = os.getenv('DISCORD_AUTH_TOKEN')
DISCORD_USER_ID = os.getenv("DISCORD_USER_ID")


async def on_message(message):
    print(f'Message from {message.author}: {message.content}')


class DiscordClient(discord.Client):
    def __init__(self, generator: Generator[int, None, None], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.logged_in = False
        self.other_user = None
        self.generator = generator

    async def on_ready(self):
        print(f'Logged on as {self.user}!')
        self.logged_in = True

    async def setup_hook(self) -> None:
        # start the task to run in the background
        self._send_message.start()

    @tasks.loop(seconds=5)  # task runs every 60 seconds
    async def _send_message(self):
        if not self.logged_in:
            return
        if not self.other_user:
            self.other_user = await self.fetch_user(DISCORD_USER_ID)
        card_id = next(self.generator)
        price, condition = find_prices(card_id, False)
        await self.other_user.send(str(price) + " " + condition)

    @_send_message.before_loop
    async def before_my_task(self):
        await self.wait_until_ready()  # wait until the bot logs in

    async def send_message(self, message: str):
        # self.message_queue.append(message)
        if not self.logged_in:
            return
        if not self.other_user:
            self.other_user = await self.fetch_user(DISCORD_USER_ID)
        for message in self.message_queue:
            await self.other_user.send(message)
        self.message_queue.clear()



async def run_discord_client(card_generator: Generator[int, None, None]):
    intents = discord.Intents.default()
    intents.message_content = True

    client = DiscordClient(intents=intents, generator=card_generator)
    await client.start(DISCORD_AUTH_TOKEN)
