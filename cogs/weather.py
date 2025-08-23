import discord
from discord.ext import commands
import requests
import json
import util

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
    
    def get_dir(self, deg : int):
        directions = ['North', 'North-East', 'East', 'South-East', 'South', 'South-West', 'West', 'North-West']
        idx = round(deg / 45) % 8
        return directions[idx]
    
    async def verify_location(self, city: str, country : str, ctx):
        if (city == None): await ctx.reply("This command requires a city/town name.")
        if (country == None): country = ""

        http_reply = requests.get(f"http://api.openweathermap.org/geo/1.0/direct?q={city},,{country}&limit={1}&appid={os.environ.get('WEATHER_API_KEY')}")

        if (http_reply.status_code != 200):
            await ctx.send(f'There has been an error with the API.')
            return None

        if (len(http_reply.content) < 10):
            await ctx.send(f"Location not found, Make sure the country code is valid, i.e. GB, US, DE")
            return None
        
        locData = http_reply.json()[0]
        return  (locData['lat'], locData['lon'])



    @commands.hybrid_group(name="weather", description="Command for weather")
    async def weather(self, ctx):
        await ctx.send("Please specify more..")

    @weather.command("current", description="Get the current weather")
    async def current_weather(self, ctx, *, city : str, country : str = None):
        latlong = await self.verify_location(city, country, ctx)
        if latlong == None: return # Guard Clause, if fail

        weather_reply = requests.get(f"https://api.openweathermap.org/data/2.5/weather?lat={latlong[0]}&lon={latlong[1]}&appid={os.environ.get('WEATHER_API_KEY')}")
        weather_data = weather_reply.json()
        nameData = (weather_data["name"], weather_data["sys"]["country"])
        print(weather_reply.json())

        embed : discord.Embed = discord.Embed(title=f"Weather for {nameData[0]}, {nameData[1]}")
        embed.set_thumbnail(url=f"https://openweathermap.org/img/wn/{weather_data['weather'][0]['icon']}@2x.png")
        embed.add_field(name=weather_data["weather"][0]["main"], value=weather_data["weather"][0]["description"], inline=False)
        embed.add_field(name="Current Temperature", value=f"Actual: {self.kelvin_to_celcius(weather_data['main']['temp'])} °C\n Feels Like: {self.kelvin_to_celcius(weather_data['main']['feels_like'])} °C")
        embed.add_field(name="High and Lows", value=f"Minimum: {self.kelvin_to_celcius(weather_data['main']['temp_min'])} °C\nMaximum: {self.kelvin_to_celcius(weather_data['main']['temp_max'])} °C")
        embed.add_field(name="Humidity :droplet:", value=f"{weather_data['main']['humidity']}%", inline=False)
        embed.add_field(name="Wind",value=f"Speed: {weather_data['wind']['speed']}m/s\nDir: {weather_data['wind']['deg']}° ({self.get_dir(weather_data['wind']['deg'])})", inline=True)


        embed.set_author(name=util.CONFIG_DATA['author_tag'])
        embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])

        await ctx.send(embed=embed)

    @weather.command("hourly", description="Get the 3 hourly weather forecast")
    async def hourly_weather(self, ctx, *, city:str, country:str = None):
        latlong = await self.verify_location(city, country, ctx)
        if latlong == None: return # Guard Clause, if fail

        weather_reply = requests.get(f"https://api.openweathermap.org/data/2.5/forecast?lat={latlong[0]}&lon={latlong[1]}&appid={os.environ.get('WEATHER_API_KEY')}")
        nameData = (weather_reply.json()["city"]["name"], weather_reply.json()["city"]["country"])
        weather_data = weather_reply.json()["list"][0:8]

        print(weather_data)
        embed : discord.Embed = discord.Embed(title=f"Weather for {nameData[0]}, {nameData[1]}")

        for data in weather_data:
            embed.add_field(name=data['dt_txt'], value=f"""**Weather:** {data['weather'][0]['main']}
                            **Temperature:** {self.kelvin_to_celcius(data['main']['temp'])} °C
                            **Lo-Hi:** {self.kelvin_to_celcius(data['main']['temp_min'])} - {self.kelvin_to_celcius(data['main']['temp_max'])} °C
                            **Feels:** {self.kelvin_to_celcius(data['main']['feels_like'])} °C""")

        embed.set_author(name=util.CONFIG_DATA['author_tag'])
        embed.set_footer(text=util.CONFIG_DATA['footer_text'], icon_url=util.CONFIG_DATA['owner_pfp'])
        await ctx.send(embed=embed)






async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(Weather(bot))