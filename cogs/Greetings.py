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

    @commands.command()
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        print("test")
        #if self._last_member is None or self._last_member.id != member.id:
        await ctx.send(f'GRRRRReeeeetings {member.name}~')
        #self._last_member = member 


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Greetings(bot))