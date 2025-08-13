## Discord bot main
import discord
from datetime import datetime

import os
from dotenv import load_dotenv
load_dotenv()

class MyClient(discord.Client):
    async def on_ready(self):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Logged on as {self.user}")

    async def on_message(self, message):
        print(f"[{datetime.now().strftime('%H:%M:%S')}] Message by {message.author}: {message.content}")

def main():
    intents = discord.Intents.default()
    intents.message_content = True

    client = MyClient(intents=intents)
    client.run(os.environ.get('DISCORD_BOT_TOKEN'))



if __name__ == "__main__":
    main()