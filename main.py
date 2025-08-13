## Discord bot main
import discord
from discord.ext import commands

#Cogs
import cogs.Greetings
from os import listdir

## Logging Modules
import logging
from datetime import datetime

## Key Privacy
import os
from dotenv import load_dotenv
load_dotenv()

class MyBot(commands.Bot):
    async def on_ready(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged on as {self.user}")

    async def on_message(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message by {message.author}: {message.content}")

    async def load_extension(self, name, *, package = None):
        return await super().load_extension(name, package=package)

    async def setup_hook(self):
        for cog in listdir('./cogs'):
            if cog.endswith('.py') == True:
                print(f"LOADING: cogs.{cog[:-3]}")
                await self.load_extension(f'cogs.{cog[:-3]}')
        return await super().setup_hook()    


def main():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

    INTENTS = discord.Intents.default()
    INTENTS.message_content = True

    client = MyBot(command_prefix='>', intents=INTENTS)
    
    client.run(os.environ.get('DISCORD_BOT_TOKEN'), log_handler=handler)

if __name__ == "__main__":
    main()