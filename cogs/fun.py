from random import Random
import discord
from typing import Literal, Optional
from discord.ext import commands
import util


class FunCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.hybrid_group(name="poke")
    async def poke(self, ctx):
        await ctx.send("Please specify 'user' or 'random'.")

    @poke.command(name="user")
    async def poke_user(self, ctx, user: discord.Member, silent: Literal[True, False] = False):
        if (silent):  await ctx.send(f"Poking {user.nick}!")
        else: await ctx.send(f"Poking {user.mention}!")

    @poke.command(name="random")
    async def poke_random(self, ctx, silent: Literal[True, False] = False):
        user : discord.Member = ctx.guild.members[Random.randint(0, len(ctx.guild.members) - 1)]
        if (silent):  await ctx.send(f"Poking {user.nick}!")
        else: await ctx.send(f"Poking {user.mention}!")
            


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(FunCommands(bot))