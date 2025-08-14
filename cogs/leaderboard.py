from math import ceil
import discord
from typing import Literal
from discord.ext import commands
import util

class MyView(discord.ui.View):
    def __init__(self, forward : bool, backward : bool, embed : discord.Embed, data : list, index : int, type:str, user:discord.Member):
        super().__init__()
        self._forward = forward
        self._backward = backward
        self._embed = embed
        self._index = index
        self._data = data
        self._pages =  ceil(len(data) / 10)
        self._type = type
        self._user = user
        self.arrow_backward  : discord.ui.Button = None
        self.arrow_forward : discord.ui.Button = None

        self.refreshButtons()

    def refreshButtons(self):
        self.remove_item(self.arrow_forward)
        self.remove_item(self.arrow_backward)

        self.arrow_backward = discord.ui.Button(label=':arrow_backward:', style=discord.ButtonStyle.blurple, disabled=not self._backward)
        self.arrow_backward.callback = self.on_arrow_backward_click
        self.add_item(self.arrow_backward)

        self.arrow_forward = discord.ui.Button(label=':arrow_forward:', style=discord.ButtonStyle.blurple, disabled=not self._forward)
        self.arrow_forward.callback = self.on_arrow_forward_click
        self.add_item(self.arrow_forward)

    async def on_arrow_backward_click(self, interaction: discord.Interaction):

        self._index = self._index - 1
        if (self._index == 0):self._backward = False
        data = self._data[self._index*10:(self._index*10)+10]
        i : int = 1 + (self._index*10)
        lbText = ""
        for userTuple in data:
            if (userTuple[0] == self._user.name): 
                lbText = lbText + f"{i}. **{userTuple[0]}**: {userTuple[1]} Messages **<-**\n"
            else:
                lbText = lbText + f"{i}. {userTuple[0]}: {userTuple[1]} Messages\n"

        newEmbed = discord.Embed(title=f"{self._user.guild.name} Messages Leaderboard ({self._index+1}/{self._pages})", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16), description=lbText)
        newEmbed.set_author(name=self._embed.author.name)
        newEmbed.set_footer(text=self._embed.footer.text, icon_url=self._embed.footer.icon_url)
        self._embed = newEmbed
        self._forward = True
        self.refreshButtons()
        await interaction.response.edit_message(embed=self._embed, view=self)

    
    async def on_arrow_forward_click(self, interaction:discord.Interaction):
        self._index = self._index + 1
        if (self._index >= self._pages-1):
            data = self._data[self._index*10:]
            self._forward = False
        else:
            data = self._data[self._index*10:(self._index*10)+10]
        i : int = 1 + (self._index*10)
        lbText = ""
        for userTuple in data:
            if (userTuple[0] == self._user.name): 
                lbText = lbText + f"{i}. **{userTuple[0]}**: {userTuple[1]} Messages **<-**\n"
            else:
                lbText = lbText + f"{i}. {userTuple[0]}: {userTuple[1]} Messages\n"

        newEmbed = discord.Embed(title=f"{self._user.guild.name} Messages Leaderboard ({self._index+1}/{self._pages})", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16), description=lbText)
        newEmbed.set_author(name=self._embed.author.name)
        newEmbed.set_footer(text=self._embed.footer.text, icon_url=self._embed.footer.icon_url)
        self._embed = newEmbed
        self._backward = True
        self.refreshButtons()

        await interaction.response.edit_message(embed=newEmbed, view=self)


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
    async def leaderboard(self, ctx, type : Literal["messages","joinDate"]):
        member : discord.Member = ctx.author
        guild = member.guild

        if (type == "messages"): 
            messages = util.DATABASE_REF.query("""SELECT username, messages FROM users""")
            i : int = 1
            lbText : str = ""
            fulldata = sorted(messages, key=lambda x:x[1], reverse=True)
            data = fulldata[:10]
            pages : int = ceil(len(fulldata) / 10)
            print(pages, len(data))

            for userTuple in data:
                if (userTuple[0] == member.name): 
                    lbText = lbText + f"{i}. **{userTuple[0]}**: {userTuple[1]} Messages **<-**\n"
                else:
                    lbText = lbText + f"{i}. {userTuple[0]}: {userTuple[1]} Messages\n"

            embed = discord.Embed(title=f"{guild.name} Messages Leaderboard (1/{pages})", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16), description=lbText)
            
            view = MyView(True, False, embed, fulldata, 0, "messages", member)
            
        else:
            data : list = []
            for mem in guild.members:
                mem : discord.Member = mem
                if (not mem.bot): data.append((mem.name, mem.joined_at))
                
            i : int = 1
            lbText : str = ""
            fulldata = sorted(messages, key=lambda x:x[1], reverse=True)
            data = fulldata[:10]
            pages : int = ceil(len(fulldata) / 10)
            for userTuple in sorted(data, key=lambda x:x[1])[:10]:
                if (userTuple[0] == member.name): 
                    lbText = lbText + f"{i}. **{userTuple[0]}**: Joined at {userTuple[1].strftime('%d/%m/%Y %H:%M:%S')} **<-**\n"
                else:
                    lbText = lbText + f"{i}. {userTuple[0]}: Joined at {userTuple[1].strftime('%d/%m/%Y %H:%M:%S')}\n"

            embed = discord.Embed(title=f"{guild.name} Time Joined Leaderboard (1/{pages})", color=int(util.CONFIG_DATA['embed_neuteral_color'], 16), description=lbText)

            view = MyView(True, False, embed, fulldata, 0, "joinDate", member)

            
        embed.set_author(name=util.CONFIG_DATA['author_tag'])
        embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])
        
        await ctx.send(embed=embed, view = view)


async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Leaderboard(bot))