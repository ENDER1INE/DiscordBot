import discord
from discord.ext import commands
from config import settings
import requests
import json
from googletrans import Translator
import emoji


translator = Translator()
bot = commands.Bot(command_prefix=settings['prefix'], help_command=None)
jokes = {}
facts = {}
cities = {}
pictures = {}
memes = {}
city_list = []
fact_list = []
joke_list = []
pic_list = []
mem_list = []



@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет {author.mention}")
    await help(ctx)


@bot.command()
async def weather(ctx, *city):
    try:
        author = ctx.message.author
        city = ' '.join(city)
        if author.id not in cities.keys():
            city_list.append(city)
            cities[author.id] = city_list
        elif city in cities.get(author.id):
            await ctx.send(embed=discord.Embed(color=0xFF2B2B, title=f"Вы уже запрашивали погоду в городе {city}"))
        else:
            city_id = cities.get(author.id)
            city_id.append(city)
            cities[author.id] = city_id
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


@bot.command()
async def pic(ctx, animal):
    try:
        author = ctx.message.author
        responce = requests.get(f'https://some-random-api.ml/img/{animal}')
        json_data = json.loads(responce.text)
        if author.id not in pictures.keys():
            pic_list.append(json_data['link'])
            pictures[author.id] = pic_list
        elif json_data['link'] in pictures.get(author.id):
            await ctx.send(embed=discord.Embed(color=0xFF2B2B, title=f"Кажется это фото вы уже видели, сейчас подберем другое"))
            responce = requests.get(f'https://some-random-api.ml/img/{animal}')
            json_data = json.loads(responce.text)
        else:
            pic_id = pictures.get(author.id)
            pic_id.append(json_data['link'])
            pictures[author.id] = pic_id
        embed = discord.Embed(color=0xff9900)
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможного данного"
                                                                 " животного не существует)"))



@bot.command()
async def fact(ctx, animal):
    try:
        author = ctx.message.author
        responce = requests.get(f'https://some-random-api.ml/animal/{animal}')
        json_data = json.loads(responce.text)
        if author.id not in facts.keys():
            fact_list.append(json_data['fact'])
            facts[author.id] = fact_list
        elif json_data['fact'] in facts.get(author.id):
            await ctx.send(
                embed=discord.Embed(color=0xFF2B2B, title=f"Кажется этот факт вы уже слышали, сейчас подберем другой"))
            responce = requests.get(f'https://some-random-api.ml/facts/{animal}')
            json_data = json.loads(responce.text)
        else:
            fact_id = facts.get(author.id)
            fact_id.append(json_data['fact'])
            facts[author.id] = fact_id
        responce_2 = requests.get(f'https://some-random-api.ml/animal/{animal}')
        json_data_2 = json.loads(responce_2.text)
        if author.id not in pictures.keys():
            pic_list.append(json_data['image'])
            pictures[author.id] = pic_list
        elif json_data['image'] in pictures.get(author.id):
            await ctx.send(
                embed=discord.Embed(color=0xFF2B2B, title=f"Кажется это фото вы уже видели, сейчас подберем другое"))
            responce_2 = requests.get(f'https://some-random-api.ml/animal/{animal}')
            json_data_2 = json.loads(responce_2.text)
        else:
            pic_id = pictures.get(author.id)
            pic_id.append(json_data['image'])
            pictures[author.id] = pic_id
        result = translator.translate(json_data['fact'], dest='ru', src='en')
        embed_ru = discord.Embed(color=0xff9900, title=result.text)
        embed_en = discord.Embed(color=0xff9900, title=json_data['fact'])
        embed_en.set_image(url=json_data_2['image'])
        await ctx.send(embed=embed_en)
        await ctx.send(embed=embed_ru)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможного данного"
                                                                 " животного не существует)"))

@bot.command()
async def meme(ctx):
    try:
        author = ctx.message.author
        responce = requests.get('https://some-random-api.ml/meme')
        json_data = json.loads(responce.text)
        if author.id not in memes.keys():
            mem_list.append(json_data['image'])
            memes[author.id] = mem_list
        elif json_data['image'] in memes.get(author.id):
            await ctx.send(
                embed=discord.Embed(color=0xFF2B2B, title=f"Кажется этот мем вы уже видели, сейчас подберем другой"))
            responce = requests.get(f'https://some-random-api.ml/meme')
            json_data = json.loads(responce.text)
        else:
            mem_id = memes.get(author.id)
            mem_id.append(json_data['image'])
            pictures[author.id] = mem_id
        embed = discord.Embed(color=0xff9900)
        embed.set_image(url=json_data['image'])
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка"))


@bot.command()
async def joke(ctx):
    try:
        author = ctx.message.author
        responce = requests.get('https://some-random-api.ml/joke')
        json_data = json.loads(responce.text)
        if author.id not in jokes.keys():
            joke_list.append(json_data['joke'])
            jokes[author.id] = joke_list
        elif json_data['joke'] in jokes.get(author.id):
            await ctx.send(
                embed=discord.Embed(color=0xFF2B2B, title=f"Кажется эту шутку вы уже слышали, сейчас подберем другую"))
            responce = requests.get(f'https://some-random-api.ml/meme')
            json_data = json.loads(responce.text)
        else:
            joke_id = jokes.get(author.id)
            joke_id.append(json_data['joke'])
            jokes[author.id] = joke_id
        result = translator.translate(json_data['joke'], dest='ru', src='en')
        embed_ru = discord.Embed(color=0xff9900, title=result.text)
        embed_en = discord.Embed(color=0xff9900, title=json_data['joke'])
        await ctx.send(embed=embed_en)
        await ctx.send(embed=embed_ru)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка"))


@bot.command()
async def help(ctx):
    t = ':hear-no-evil_monkey:'
    commands = [f'Действия:',
                f'  {emoji.emojize(t)}  weather город - вывод погоды в  определенном городе',
                f'  {emoji.emojize(t)}  pic животное - фото животного',
                f'  {emoji.emojize(t)}  fact животное - факт о животном',
                f'  {emoji.emojize(t)}  meme - мем',
                f'  {emoji.emojize(t)}  joke - шутка']
    embed = discord.Embed(color=0xff9900, title=f'Действия')
    embed.add_field(name='<<commands>>', value='\n'.join(commands), inline=True)
    await ctx.send(embed=embed)

bot.run(settings['token'])