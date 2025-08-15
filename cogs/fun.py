import random
import discord
from typing import Literal, Optional
from discord.ext import commands
import requests

"""

    Fun Commands
    - Poke: Good example of grouped commands used in hybrid

"""


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="poke")
    async def poke(self, ctx):
        await ctx.send("Please specify 'user' or 'random'.")

    @poke.command(name="user")
    async def poke_user(self, ctx, user : discord.Member, silent: Literal["True", "False"] = "True"):
        print(user)
        sender : discord.Member = ctx.author
        if (user == sender): 
            await ctx.send(f"{sender.mention} tried to poke themselves...")
            await sender.send(f"Why are you poking yourself...")#
        else:
            if (silent == "True"):  await ctx.send(f"{sender.mention} Poked {user.display_name}!")
            else: await ctx.send(f"{sender.mention} Poked {user.mention}!")

    @poke.command(name="random")
    async def poke_random(self, ctx, silent: Literal["True", "False"] = "True"):
        sender : discord.Member = ctx.author
        members = [member for member in ctx.guild.members if member != sender]
        user : discord.Member = random.choice(members)
        
        if (silent == "True"):  await ctx.send(f"{sender.mention} Poked {user.display_name}!")
        else: await ctx.send(f"{sender.mention} Poked {user.mention}!")

    @commands.hybrid_group(name="dog", description="Sends Dog pictures")
    async def dog(self, ctx):
        await ctx.send("Please specify 'dog breed' or 'random'.")

    @dog.command(name= "random", description="Returns a random dog image")
    async def dog_random(self, ctx):
        reply = requests.get("https://dog.ceo/api/breeds/image/random")
        if reply.json()["status"] != "success":
            await ctx.send("There is an issue with the dog api :(")
            return
        url = reply.json()["message"]
        await ctx.send(url)

    @dog.command(name="choose", description="Choose the breed of dog in the image")
    async def dog_choose(self, ctx, breed : Literal["akita","boxer", "beagle", "collie/border", "dalmation", "doberman", "husky", "labrador", "bernese", "pug", "retriever/golden", "spaniel/cocker"]):
        reply = requests.get(f"https://dog.ceo/api/breed/{breed}/images/random")
        if reply.json()["status"] != "success":
            await ctx.send("There is an issue with the dog api :(")
            return
        url = reply.json()["message"]
        await ctx.send(url)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FunCommands(bot))