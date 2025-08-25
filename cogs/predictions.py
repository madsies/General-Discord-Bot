import discord
from discord.ext import commands
import util

class Predictions(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None

    """
    
        User predictions:


    """

    @commands.hybrid_group(name="prediction", description="Prediction Commands")
    async def prediction(self, ctx):
        await ctx.send("Please specify more..")

    @prediction.command(name="create", description="Creates a new Prediction")
    async def create_prediction(self, ctx, question : str, duration : int,  option1 : str, option2 : str, option3 : str = None, option4 : str = None): # options 1/2 mandatory
        if (duration <= 0): await ctx.send("Invalid Duration"); return
        if (question == ""): await ctx.send("Please add a question"); return

        embed = discord.Embed(title=f"{question}", colour=int(util.CONFIG_DATA['embed_neuteral_color'], 16))


    @prediction.command(name="bet", description="Bet on an existing prediction")
    async def bet_prediction(self, ctx, pred : str, amount : int, guess : str):
        await ctx.send("wip")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Predictions(bot))