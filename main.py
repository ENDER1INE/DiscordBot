import random
import discord
from discord.ext import commands
from config import settings
import requests
import json
from googletrans import Translator
import emoji
from newsapi import NewsApiClient
import requests


translator = Translator()
bot = commands.Bot(command_prefix=settings['prefix'], help_command=None)
users = {}


def update(user_id, key_name, value):
    if user_id in users:
        data = users[user_id]
        if key_name in data:
            data[key_name].add(value)
        else:
            data[key_name] = {value}
        users[user_id] = data
    else:
        users[user_id] = {}
        users[user_id][key_name] = {value}
    return users




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
        try:
            if city in users.get(author.id).get('weather'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Вы уже запрашивали погоду в этом городе"))
            else:
                update(author.id, 'weather', city)
        except Exception:
            update(author.id, 'weather', city)
        print(users)
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
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможно данного"
                                                                 " города не существует)"))


@bot.command()
async def pic(ctx, animal):
    try:
        author = ctx.message.author
        responce = requests.get(f'https://some-random-api.ml/img/{animal}')
        json_data = json.loads(responce.text)
        try:
            if json_data['link'] in users.get(author.id).get('pictures'):
                await ctx.send(embed=discord.Embed(color=0xFF2B2B, title=f"Кажется, это фото вы уже видели, сейчас подберем другое"))
                responce = requests.get(f'https://some-random-api.ml/img/{animal}')
                json_data = json.loads(responce.text)
            else:
                update(author.id, 'pictures', json_data['link'])
        except Exception:
            update(author.id, 'pictures', json_data['link'])
        embed = discord.Embed(color=0xff9900)
        embed.set_image(url=json_data['link'])
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможно данного"
                                                                 " животного не существует)"))



@bot.command()
async def fact(ctx, animal):
    try:
        author = ctx.message.author
        responce = requests.get(f'https://some-random-api.ml/animal/{animal}')
        json_data = json.loads(responce.text)
        try:
            if json_data['fact'] in users.get(author.id).get('facts'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Кажется этот факт вы уже слышали, сейчас подберем другой"))
                responce = requests.get(f'https://some-random-api.ml/facts/{animal}')
                json_data = json.loads(responce.text)
        except Exception:
            update(author.id, 'facts', json_data['fact'])
        responce_2 = requests.get(f'https://some-random-api.ml/animal/{animal}')
        json_data_2 = json.loads(responce_2.text)
        try:
            if json_data_2['image'] in users.get(author.id).get('pictures'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Кажется это фото вы уже видели, сейчас подберем другое"))
                responce_2 = requests.get(f'https://some-random-api.ml/animal/{animal}')
                json_data_2 = json.loads(responce_2.text)
            else:
                update(author.id, 'pictures', json_data_2['image'])
        except Exception:
            update(author.id, 'pictures', json_data_2['image'])
        result = translator.translate(json_data['fact'], dest='ru', src='en')
        embed_ru = discord.Embed(color=0xff9900, title=result.text)
        embed_en = discord.Embed(color=0xff9900, title=json_data['fact'])
        embed_en.set_image(url=json_data_2['image'])
        await ctx.send(embed=embed_en)
        await ctx.send(embed=embed_ru)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможно данного"
                                                                 " животного не существует)"))

@bot.command()
async def meme(ctx):
    try:
        author = ctx.message.author
        responce = requests.get('https://some-random-api.ml/meme')
        json_data = json.loads(responce.text)
        try:
            if json_data['image'] in users.get(author.id).get('memes'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Кажется этот мем вы уже видели, сейчас подберем другой"))
                responce = requests.get(f'https://some-random-api.ml/meme')
                json_data = json.loads(responce.text)
            else:
                update(author.id, 'memes', json_data['image'])
        except Exception:
            update(author.id, 'memes', json_data['image'])
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
        try:
            if json_data['joke'] in users.get(author.id).get('jokes'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Кажется эту шутку вы уже слышали, сейчас подберем другую"))
                responce = requests.get(f'https://some-random-api.ml/meme')
                json_data = json.loads(responce.text)
            else:
                update(author.id, 'jokes', json_data['joke'])
        except Exception:
            update(author.id, 'jokes', json_data['joke'])
        result = translator.translate(json_data['joke'], dest='ru', src='en')
        embed_ru = discord.Embed(color=0xff9900, title=result.text)
        embed_en = discord.Embed(color=0xff9900, title=json_data['joke'])
        await ctx.send(embed=embed_en)
        await ctx.send(embed=embed_ru)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка"))


@bot.command()
async def news(ctx):
    try:
        author = ctx.message.author
        url = (f'https://newsapi.org/v2/top-headlines?'
               f'country=ru&'
               f'apiKey=973085d982b24f93a43101b3fba958bd')
        responce = requests.get(url)
        json_data = json.loads(responce.text)
        number = random.randint(0, len(json_data['articles']) - 1)
        try:
            if json_data['articles'][number]['title'] in users.get(author.id).get('news'):
                await ctx.send(
                    embed=discord.Embed(color=0xFF2B2B, title=f"Кажется эту новость вы уже слышали, сейчас подберем другую"))
                if len(users.get(author.id).get('news')) == len(json_data['articles']):
                    raise MemoryError(
                        await ctx.send(
                            embed=discord.Embed(color=0xFF2B2B,
                                                title=f"Кажется новости на сегодня закончились")))
                else:
                    while json_data['articles'][number]['title'] in users.get(author.id).get('news'):
                        number = random.randint(0, len(json_data['articles']) - 1)
            else:
                update(author.id, 'news', json_data['articles'][number]['title'])
        except Exception:
            update(author.id, 'news', json_data['articles'][number]['title'])
        embed_2 = discord.Embed(color=0xff9900, title=json_data['articles'][number]['title'])
        embed_3 = discord.Embed(color=0xff9900, title=json_data['articles'][number]['url'])
        embed = discord.Embed(color=0xff9900)
        embed_2.add_field(name='<<news>>', value=json_data['articles'][number]['description'], inline=True)
        embed.set_image(url=json_data['articles'][number]['urlToImage'])
        if json_data['articles'][number]['urlToImage']:
                await ctx.send(embed=embed)
        await ctx.send(embed=embed_2)
        await ctx.send(embed=embed_3)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2B2B, title="Произошла непредвиденная ошибка, возможно сайт был удален"))


@bot.command()
async def help(ctx):
    t = ':hear-no-evil_monkey:'
    commands = [f'Действия:',
                f'  {emoji.emojize(t)}  weather город - вывод погоды в  определенном городе',
                f'  {emoji.emojize(t)}  pic животное - фото животного',
                f'  {emoji.emojize(t)}  fact животное - факт о животном',
                f'  {emoji.emojize(t)}  meme - мем',
                f'  {emoji.emojize(t)}  joke - шутка',
                f'  {emoji.emojize(t)}  news - новости']
    embed = discord.Embed(color=0xff9900, title=f'Действия')
    embed.add_field(name='<<commands>>', value='\n'.join(commands), inline=True)
    await ctx.send(embed=embed)

bot.run(settings['token'])
