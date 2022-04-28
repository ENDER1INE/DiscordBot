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
bot = commands.Bot(command_prefix=settings['prefix'], help_command=None, intents=discord.Intents.all())
users = {}

last_help_message_id = None
lasT_channel_if = None


def convert_id(id):
    return int(''.join([number for number in id if number.isdigit()]))


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
async def help(ctx):
    file = discord.File("help_menu.jpg")
    embed = discord.Embed(title='help_menu')
    await ctx.send(embed=embed, file=file)


@bot.command()
async def pic(ctx, animal):
    try:
        author = ctx.message.author
        responce = requests.get(f'https://some-random-api.ml/img/{animal}')
        json_data = json.loads(responce.text)
        try:
            if json_data['link'] in users.get(author.id).get('pictures'):
                await ctx.send(embed=discord.Embed(color=0xFF2B2B, title=f"Кажется, это фото вы уже видели,"
                                                                         f" сейчас подберем другое"))
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
async def addadmin(ctx, member):
    try:
        admin_list = [str(discord.utils.get(ctx.guild.members, id=convert_id(user)))
                      for user in (open("Admins.txt").read()).split('\n') if user]
        if str(ctx.message.author) in admin_list:
            member = str(convert_id(member))
            read_admin_list = open('Admins.txt').read()
            with open("Admins.txt", 'a') as admin_list:
                if member not in read_admin_list:
                    if not discord.utils.get(ctx.guild.members, id=convert_id(member)) == None:
                        admin_list.write(f'{member}\n')
                        member = discord.utils.get(ctx.guild.members, id=convert_id(member))
                        succes = f'Пользователь {member} назначен как администратор!'
                    else:
                        succes = 'Проверьте првильность введенных данных, найти пользователя не удалось!'
                else:
                    succes = f'Что то пошло не так, возможно данный пользователь уже администратор.'
            embed = discord.Embed(color=0xFF1870, title=succes)
            await ctx.send(embed=embed)
        else:
            await ctx.send(
                embed=discord.Embed(color=0xFF2918, title=f'{bot.get_emoji(964198996291751986)} Отказано в доступе, '
                                                          f'возможно у вас недостаточно прав!!!'))
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def addrole(ctx, member=None, role=None):
    try:
        author = ctx.message.author
        admin_list = [str(discord.utils.get(ctx.guild.members, id=convert_id(user)))
                      for user in (open("Admins.txt").read()).split('\n') if user]
        if str(author) in admin_list:
            member = discord.utils.get(ctx.guild.members, id=convert_id(member))
            role = discord.utils.get(ctx.guild.roles, id=convert_id(role))
            await member.add_roles(role)
            await ctx.send(embed=discord.Embed(color=0xFFCC00, title=f'{bot.get_emoji(964198996295942144)} Пользователю '
                                                                     f'{member} выдана роль {role}!'))
        else:
            await ctx.send(
                embed=discord.Embed(color=0xFF2918, title=f'{bot.get_emoji(964198996291751986)} Отказано в доступе, '
                                                          f'возможно у вас недостаточно прав!!!'))
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def delrole(ctx, member, role):
    try:
        author = ctx.message.author
        admin_list = [str(discord.utils.get(ctx.guild.members, id=convert_id(user)))
                      for user in (open("Admins.txt").read()).split('\n') if user]
        if str(author) in admin_list:
            member = discord.utils.get(ctx.guild.members, id=convert_id(member))
            role = discord.utils.get(ctx.guild.roles, id=convert_id(role))
            await member.remove_roles(role)
            await ctx.send(
                embed=discord.Embed(color=0xFFCC00, title=f'{bot.get_emoji(964198996295942144)} У пользователя '
                                                          f'{member} забрана роль {role}!'))
        else:
            await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'{bot.get_emoji(964198996291751986)} '
                                                                     f'Отказано в доступе, возможно '
                                                                     f'у вас недостаточно прав!!!'))
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def ban(ctx, member, reason='None'):
    try:
        author = ctx.message.author
        admin_list = [str(discord.utils.get(ctx.guild.members, id=convert_id(user)))
                      for user in (open("Admins.txt").read()).split('\n') if user]
        if str(author) in admin_list:
            member = discord.utils.get(ctx.guild.members, id=convert_id(member))
            await member.ban(reason=reason)
            embed = discord.Embed(color=0xFF0000,
                                  title=f'Пользователь {str(member).split("#")[0]} был забанен по причине {reason}!')
            await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def unban(ctx):
    try:
        banned_users = await ctx.guild.bans()
        for ban_entry in banned_users:
            user = ban_entry.user
            await ctx.guild.unban(user)

        embed = discord.Embed(color=0x00FF00,
                              title=f'Пользователь {str(user).split("#")[0]} был разбанен!')
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def kick(ctx, member, reason='None'):
    try:
        member = discord.utils.get(ctx.guild.members, id=convert_id(member))
        await member.kick(reason=reason)
        embed = discord.Embed(color=0x00FF00,
                             title=f'Пользователь {str(member).split("#")[0]} был исключен с'
                                   f' сервера по причине {reason}!')
        await ctx.send(embed=embed)
    except Exception:
        await ctx.send(embed=discord.Embed(color=0xFF2918, title=f'[ERROR] Вероятно вы где то допустили ошибку!!!'))


@bot.command()
async def hello(ctx):
    global last_help_message_id, last_channel_id, last_author
    last_author = ctx.message.author
    author = ctx.message.author
    guild = bot.get_guild(922501298111250493)
    people_role = guild.get_role(963432221421764618)
    meh_role = guild.get_role(964515540456575037)
    if people_role in author.roles or meh_role in author.roles:
        embed = discord.Embed(color=0x7FFFD4, title='.....Мы ждали вас!.....     \n'
                                                    'Добро пожаловать домой!')
        responce = requests.get(f'https://some-random-api.ml/animu/wink')
        json_data = json.loads(responce.text)
        embed.set_image(url=json_data['link'])
    else:
        embed = discord.Embed(color=0xFF3300, title=f'-------Приветствуем вас на сервере-------\n'
                                                    f'Пожалуйста подтвердите свою личность.\n'
                                                    f'\n'
                                                    f'{bot.get_emoji(964198996295942144)} - Я человек\n'
                                                    f'{bot.get_emoji(964198996291751986)} - Я машина')
        embed.set_image(url='https://c.tenor.com/WeazEANUhvMAAAAC/stop-funny-animal.gif')
    message_id = await ctx.send(embed=embed)
    last_help_message_id = message_id.id
    last_channel_id = message_id.channel.id


@bot.event
async def on_raw_reaction_add(payload):
    message_id = payload.message_id
    guild = bot.get_guild(922501298111250493)
    people_role = guild.get_role(963432221421764618)
    meh_role = guild.get_role(964515540456575037)
    if message_id == last_help_message_id:
        if payload.emoji.name == 'ALTCHECK':
            print(last_author)
            await last_author.add_roles(people_role)
        elif payload.emoji.name == 'MinecraftNo':
            await last_author.add_roles(meh_role)


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