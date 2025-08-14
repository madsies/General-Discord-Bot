## Discord bot main
import discord
from discord.ext import commands

# Cogs
from os import listdir
import util

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

        for guild in self.guilds:
            for user in guild.members:
                if (user != self):
                    util.DATABASE_REF.add_user(user);
        return await super().on_ready()

    async def on_message(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message by {message.author}: {message.content}")
        return await super().on_message(message) # I'm an idiot and forgot to add this from original class.....

    async def load_extension(self, name, *, package = None):
        return await super().load_extension(name, package=package)

    async def setup_hook(self):
        for cog in listdir('./cogs'):
            if cog.endswith('.py') == True:
                print(f"LOADING: cogs.{cog[:-3]}")
                await self.load_extension(f'cogs.{cog[:-3]}')
                
        await self.tree.sync() # Updates Slash Commands
        return await super().setup_hook()    


def main():
    handler = logging.FileHandler(filename='discord.log', encoding='utf-8', mode='w')

    INTENTS = discord.Intents.default()
    INTENTS.message_content = True

    #util.DATABASE_REF.query("""DROP TABLE users;""")

    util.DATABASE_REF.query("""CREATE TABLE IF NOT EXISTS users (
                   id BIGINT,
                   username varchar(32),
                   messages integer,
                   PRIMARY KEY (id));""")

    client = MyBot(command_prefix='!', intents=INTENTS)
    
    client.run(os.environ.get('DISCORD_BOT_TOKEN'), log_handler=handler)

    

if __name__ == "__main__":
    main()