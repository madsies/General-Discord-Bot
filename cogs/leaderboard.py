import discord
from typing import Literal
from discord.ext import commands
import util

class Leaderboard(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    """
    
        Leaderboard
        - Messages
        - JoinDate
        - User number, etc.

    """
    @commands.hybrid_command(name="leaderboard", description="Leaderboards of user stats", first="Type of Leaderboard")
    async def server_info(self, ctx, type : Literal["messages","joinDate"]):
        member : discord.Member = ctx.author
        guild = member.guild
        if (type == "messages"): 
            messages = util.DATABASE_REF.query("""SELECT username, messages FROM users""")
            i : int = 1
            lbText : str = ""
            for userTuple in sorted(messages, key=lambda x:x[1], reverse=True):
                if (userTuple[0] == member.name): 
                    lbText = lbText + f"{i}. **{userTuple[0]}**: {userTuple[1]} Messages **<-**\n"
                else:
                    lbText = lbText + f"{i}. {userTuple[0]}: {userTuple[1]} Messages\n"

            embed = discord.Embed(title=f"{guild.name} Messages Leaderboard", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16), description=lbText)
            embed.set_author(name=util.CONFIG_DATA['author_tag'])
            embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])
        else:
            print("umm")

        await ctx.send(embed=embed)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))