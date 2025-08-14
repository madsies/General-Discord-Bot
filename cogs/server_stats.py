import discord
from discord.ext import commands
import util

class ServerStats(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    """
    
        User Welcome Message
        - Embedded
        - Uses users pfp
        - User number, etc.

    """
    
    @commands.hybrid_command(name="server_info", description="General Server information")
    async def server_info(self, ctx):
        member = ctx.author
        guild = member.guild
        embed = discord.Embed(title=f"{guild.name} Stats!", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16))
        embed.set_author(name=util.CONFIG_DATA['author_tag'])
        embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])
        embed.set_thumbnail(url=guild.icon)
        embed.add_field(name=f"Member Count:", value=f"**{guild.member_count}**")
        embed.add_field(name=f"Created On: ", value=f"{guild.created_at.strftime('%d/%m/%Y')}", inline=False)
        embed.add_field(name=f"Number of Channels:", value=f"{len(guild.text_channels)+ len(guild.voice_channels)}", inline=False) 
        await ctx.send(embed=embed)


    @commands.Cog.listener()
    async def on_message(self, message : discord.Message):
        user = message.author
        # Check user exists in DB
        util.DATABASE_REF.add_user(user);

        # Fetch Message count from DB
        sql = """SELECT messages FROM users WHERE id = %s"""
        val = [user.id]
        messages = util.DATABASE_REF.queryTuple(sql, val)

        # Write Updated Message Count back to db
        sql = """UPDATE users SET messages = %s WHERE id = %s"""
        val = (messages[0][0]+1, user.id)
        util.DATABASE_REF.queryTuple(sql, val)



async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ServerStats(bot))