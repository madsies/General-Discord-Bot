import discord
from discord.ext import commands
import util
import asyncio

class PredsView(discord.ui.View):
    def __init__(self, values : list):
        super().__init__()
        self.prediction_dropdown : discord.ui.Select = None
        self.prediction_value : discord.ui.TextInput = None
        self.prediction_confirm : discord.ui.Button = None
        self.selected_pred : dict = {}
        self.predictions : dict = {}
        self.setup_buttons(values)
        
    def setup_buttons(self, vals : list):
        options = self.convert_to_options(vals)
        self.prediction_dropdown = discord.ui.Select(placeholder="Select an option", min_values=1, max_values=1, options=options)
        self.add_item(self.prediction_dropdown)

        self.prediction_confirm = discord.ui.Button(label="Predict", style=discord.ButtonStyle.blurple)
        self.prediction_confirm.callback = self.on_prediction_button_press
        self.add_item(self.prediction_confirm)

        # Dont work on views.
        #self.prediction_value = discord.ui.TextInput(label="Amount", default=100, required=True)
        #self.add_item(self.prediction_value)

    """
        Converts to the correct format for discord dropdown/selections
    """

    def convert_to_options(self, vals:list):
        converted = []
        emojis = ['1️⃣','2️⃣','3️⃣','4️⃣']
        i = 0
        for answer in vals:
            converted.append(discord.SelectOption(label=answer, emoji=emojis[i]))
            i = i+1
        return converted


    async def on_prediction_button_press(self, interaction : discord.Interaction):
        if (interaction.user.id in self.predictions.keys()): await interaction.command_failed("You have already predicted"); return
        #if (isnumeric(self.prediction_value.))
        self.predictions[interaction.user.id] = self.prediction_dropdown.values[0]
        print(f"Predicted {self.prediction_dropdown.values[0]}")


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

        embed = discord.Embed(title=f"Prediction: {question}", colour=int(util.CONFIG_DATA['embed_neuteral_color'], 16))

        options : list = [option1, option2]
        if (option3 != None): options.append(option3)
        if (option4 != None): options.append(option4)

        view = PredsView(options)

        await ctx.send(embed=embed, view=PredsView(options))

        await asyncio.sleep(duration)

        # Locked after this

        await ctx.send("over")

        # Wait for result, after x with no response or cancel, refund users.


    @prediction.command(name="bet", description="Bet on an existing prediction")
    async def bet_prediction(self, ctx, pred : str, amount : int, guess : str):
        await ctx.send("wip")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Predictions(bot))