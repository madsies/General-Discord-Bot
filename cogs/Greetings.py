import discord
from discord.ext import commands

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.system_channel
        if welcome_channel is not None:
            await welcome_channel.send(f'GRRRRRReetings {member.mention}!!')

    @commands.command(name="hello")
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f'GRRRRReeeeetings {member.name}~')


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Greetings(bot))