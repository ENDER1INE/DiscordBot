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
async def weather(ctx, *city):
    try:
        city = ' '.join(city)
        key = "4404863c7b41019dcdccb79c8d750ac8"
        url = f"http://api.openweathermap.org/data/2.5/find?q={city}&type=like&APPID={key}"
        response = requests.get(url).json()["list"][0]
        country = response["sys"]["country"]
        if country == "RU":
            geocoder_response = requests.get(f"https://geocode-maps.yandex.ru/1.x/?apikey=40d1649f-0493-4b70-"
                                             f"98ba-98533de7710b&geocode={response['coord']['lon']},"
                                             f"{response['coord']['lat']}&format=json").json()
            geocoder_response = geocoder_response["response"]["GeoObjectCollection"]["featureMember"][0]["GeoObject"] \
                ["metaDataProperty"]["GeocoderMetaData"]["Address"]["Components"][2]["name"]
            country = f"{country}, {geocoder_response}"
        rain = "No rain observed " if not response["rain"] else "Chance of rain"
        snow = "No snowfall observed " if not response["snow"] else "Snowfall possible "
        weather = \
            {
                "Скорость ветра": f"{response['wind']['speed']} м/с",
                "Дождь": rain,
                "Снег": snow,
                "Минимальная температура": int(response["main"]["temp_min"]) - 273,
                "Максимальная температура": int(response["main"]["temp_max"]) - 273
            }
        color = 0x00FFFF
        embed = discord.Embed(
            title=f"Погода в городе {city.capitalize()}({country})",
            description=f"{response['weather'][0]['description']}",
            color=color
        )
        for key in weather:
            embed.add_field(
                name=key,
                value=str(weather[key]),
                inline=False
            )
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможного данного"
                                                                 " города не существует)"))


bot.run(settings['token'])
