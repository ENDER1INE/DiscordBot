import discord
from discord.ext import commands
from config import settings
import requests


bot = commands.Bot(command_prefix=settings['prefix'], help_command=None)


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет {author.mention}")


@bot.command()
async def weather(ctx, city):
    key = "4404863c7b41019dcdccb79c8d750ac8"
    response = requests.get(f"http://api.openweathermap.org/data/2.5/find?q={city}&type=like"
                            f"&APPID={key}").json()
    response = response["list"][0]

    wind = response["wind"]
    rain = response["rain"]
    clouds = response["clouds"]
    snow = response["snow"]
    temperature = int(response["main"]["temp"]) - 273
    print(temperature)
    print(response)
    await ctx.send(f"Температура в {response['name']} сейчас {temperature}")


bot.run(settings['token'])
