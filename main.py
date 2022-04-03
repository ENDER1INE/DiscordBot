import discord
from discord.ext import commands
from config import settings
import requests
import json

bot = commands.Bot(command_prefix=settings['prefix'], help_command=None)


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет {author.mention}")


@bot.command()
async def weather(ctx, city):
    key = "4404863c7b41019dcdccb79c8d750ac8"
    url = f"http://api.openweathermap.org/data/2.5/find?q={city}&type=like&APPID={key}"
    response = requests.get(url).json()

    response = response["list"][0]
    weather = \
        {
            "Скорость ветра": f"{response['wind']['speed']} м/с",
            "Дождь": response["rain"],
            "Облачность": response["clouds"],
            "Снег": response["snow"],
            "Минимальная температура": int(response["main"]["temp_min"]) - 273,
            "Максимальная температура": int(response["main"]["temp_max"]) - 273
        }

    color = 0xFF6500
    embed = discord.Embed(
        title=f"Погода в городе {city}",
        color=color
    )
    print(weather)
    for key in weather:
        print(key)
        embed.add_field(
            name=key,
            value=str(weather[key]),
            inline=False
        )

    print(123)
    await ctx.send(embed=embed)


bot.run(settings['token'])
