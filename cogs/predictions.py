import discord
from discord.ext import commands
import util
import asyncio
import time

class PredictionData():
    def __init__(self, question : str, duration : int,  options : list, host : int ):
        self.data : dict = {}
        self.pred = question
        self.duration = duration
        self.options = options
        self.host = host
        self.cancelled = False
        self.completed = False
        self.correct : str = ""
    
    def add_user(self,id:int, pred:str):
        self.data[id] = pred

    def has_user(self, id:int):
        return id in self.data
    
    def cancel(self):
        # Pay back all members
        self.cancelled = True

    def is_cancelled(self):
        return self.cancelled
    
    def is_completed(self):
        return self.completed
    
    def set_winner(self, value:str):
        self.completed = True
        self.correct = value
        # Pay out users accordingly


class PredsView(discord.ui.View):
    def __init__(self, data:PredictionData):
        super().__init__(timeout=data.duration)
        self.prediction_dropdown : discord.ui.Select = None
        self.prediction_value : discord.ui.TextInput = None
        self.prediction_confirm : discord.ui.Button = None
        self.predictions = data
        self.setup_buttons(self.predictions.options)
        self.timed_out = False
        print("Creating preds")
        
    def setup_buttons(self, vals : list):
        options = self.convert_to_options(vals)
        self.prediction_dropdown = discord.ui.Select(placeholder="Select an option", min_values=1, max_values=1, options=options)
        self.prediction_dropdown.callback = self.on_prediction_selection
        self.add_item(self.prediction_dropdown)

        self.prediction_confirm = discord.ui.Button(label="Predict", style=discord.ButtonStyle.blurple)
        self.prediction_confirm.callback = self.on_prediction_button_press
        self.add_item(self.prediction_confirm)

        # Dont work on views.
        #self.prediction_value = discord.ui.TextInput(label="Amount", default=100, required=True)
        #self.add_item(self.prediction_value)

    def on_timeout(self):
        self.remove_item(self.prediction_confirm)
        self.remove_item(self.prediction_dropdown)
        self.timed_out = True
        return super().on_timeout()

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

    async def on_prediction_selection(self, interaction:discord.Interaction):
        await interaction.response.defer()

    async def on_prediction_button_press(self, interaction : discord.Interaction):
        if (self.predictions.has_user(interaction.user.id)): await interaction.response.send_message("You have already predicted", silent=True, delete_after=10); return
        self.predictions.add_user(interaction.user.id, self.prediction_dropdown.values[0])
        await interaction.user.send(f"You have predicted '**{self.prediction_dropdown.values[0]}**'.")
        await interaction.response.defer()

class SelectView(discord.ui.View):
    def __init__(self, data:PredictionData):
        super().__init__(timeout=3600)
        self.prediction_dropdown : discord.ui.Select = None
        self.prediction_value : discord.ui.TextInput = None
        self.prediction_confirm : discord.ui.Button = None
        self.predictions = data
        self.setup_buttons(self.predictions.options)
        self.timed_out = False
        
    def setup_buttons(self, vals : list):
        options = self.convert_to_options(vals)
        self.prediction_dropdown = discord.ui.Select(placeholder="Select the correct prediction", min_values=1, max_values=1, options=options)
        self.prediction_dropdown.callback = self.on_prediction_selection
        self.add_item(self.prediction_dropdown)

        self.prediction_confirm = discord.ui.Button(label="Confirm", style=discord.ButtonStyle.blurple)
        self.prediction_confirm.callback = self.on_prediction_button_press
        self.add_item(self.prediction_confirm)


    def on_timeout(self):
        self.remove_item(self.prediction_confirm)
        self.remove_item(self.prediction_dropdown)
        self.timed_out = True
        return super().on_timeout()

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

    async def on_prediction_selection(self, interaction:discord.Interaction):
        await interaction.response.defer()

    async def on_prediction_button_press(self, interaction : discord.Interaction):
        self.predictions.set_winner(self.prediction_dropdown.values[0])
        await interaction.response.defer()

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

        

        options : list = [option1, option2]
        if (option3 != None): options.append(option3)
        if (option4 != None): options.append(option4)

        pred_data = PredictionData(question, duration, options, ctx.author.id)
        view = PredsView(pred_data)

        targetTime = int(time.time()) + duration
        choices = "**Choices:**\n"
        emojis = ['1️⃣','2️⃣','3️⃣','4️⃣']
        i = 0
        for choice in pred_data.options:
            choices = choices + emojis[i]+" "+choice+"\n"
            i = i+1

        embed = discord.Embed(title=f"Prediction: {question}", colour=int(util.CONFIG_DATA['embed_neuteral_color'], 16), 
                              description=f"Closing in <t:{targetTime}:R>\n\n"+choices)

        message = await ctx.send(embed=embed, view=view)

        # Send DM to creator, dropdown to select the correct response.

        await asyncio.sleep(duration)

        # Locked after this
        while not view.timed_out:
            await asyncio.sleep(1) # Just to deal with desync issues, checks every second
        
        await message.edit(view=None)

        view_dm = SelectView(pred_data)
        await ctx.author.send(f"Select the correct prediction for:\n**{question}**", view = view_dm)

        # Periodic checks
        while (not pred_data.is_cancelled()) and (not pred_data.is_completed()):
            await asyncio.sleep(1)

        if (pred_data.is_completed):
            await ctx.send(f"The correct prediction was {pred_data.correct}!")

        # Wait for result, after x with no response or cancel, refund users.


    @prediction.command(name="bet", description="Bet on an existing prediction")
    async def bet_prediction(self, ctx, pred : str, amount : int, guess : str):
        await ctx.send("wip")

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Predictions(bot))