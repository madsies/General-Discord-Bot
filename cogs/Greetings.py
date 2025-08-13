import discord
from discord.ext import commands
import util

class Greetings(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    """
    
        User Welcome Message
        - Embedded
        - Uses users pfp
        - User number, etc.

    """
    @commands.Cog.listener()
    async def on_member_join(self, member):
        welcome_channel = member.guild.system_channel
        embed = discord.Embed(title=f"Welcome {member.display_name}", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16))
        embed.set_author(name=util.CONFIG_DATA['author_tag'])
        embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])
        embed.set_thumbnail(url=member.avatar)
        await welcome_channel.send(embed=embed);

        if welcome_channel is not None:
            await welcome_channel.send(embed=embed);
    
    @commands.hybrid_command(name="hello", description="Greetings Message")
    async def hello(self, ctx, *, member: discord.Member = None):
        member = member or ctx.author
        await ctx.send(f'GRRRRReeeeetings {member.name} :3')




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Greetings(bot))