from pathlib import Path
from typing import Literal, Tuple
import discord
from discord.ext import commands
import requests
import json

import os
from dotenv import load_dotenv
load_dotenv()

class Weather(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self._last_member = None
        """
        self.COUNTRY_CODES : Tuple
        with open(Path(__file__).parent / "../resources/countryCodes.json", "r", encoding="utf-8") as f:
            data = json.load(f)
            for entry in data:
                self.COUNTRY_CODES.append(entry["Code"])
        """

    def kelvin_to_celcius(self, temp : int):
        return round(temp - 273.15,2)
    

    @commands.hybrid_command(name="weather", description="Command for weather")
    async def weather(self, ctx, *, city : str, country : str = None):
        member : discord.Member = ctx.author
        
        if (city == None): await ctx.reply("This command requires a city/town name.")
        if (country == None): country = ""

        print(country)

        http_reply = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},,{country}&limit={1}&appid={os.environ.get('WEATHER_API_KEY')}")

        if (http_reply.status_code != 200):
            await ctx.send(f'There has been an error with the API.')
            return

        if (len(http_reply.content) < 10):
            await ctx.send(f"Location not found, Make sure the country code is valid, i.e. GB, US, DE")
            return
        
        locData = http_reply.json()[0]
        latlong = (locData['lat'], locData['lon'])

        weather_reply = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latlong[0]}&lon={latlong[1]}&appid={os.environ.get('WEATHER_API_KEY')}")
        weather_data = weather_reply.json()
        nameData = (weather_data["name"], weather_data["sys"]["country"])
        print(weather_reply.json())

        embed : discord.Embed = discord.Embed(title=f"Weather for {nameData[0]}, {nameData[1]}")
        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png")
        embed.add_field(name=weather_data["weather"][0]["main"], value=weather_data["weather"][0]["description"])
        embed.add_field(name="Current Temperature", value=f"Actual: {self.kelvin_to_celcius(weather_data['main']['temp'])} °C\n Feels Like: {self.kelvin_to_celcius(weather_data['main']['feels_like'])}°C", inline=False)

        await ctx.send(embed=embed)

        




async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Weather(bot))