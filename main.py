import discord
from discord.ext import commands
from config import settings
import requests
import json
from googletrans import Translator
import emoji


translator = Translator()
bot = commands.Bot(command_prefix=settings['prefix'], help_command=None, intents=discord.Intents.all())

last_help_message_id = None
lasT_channel_if = None


def convert_id(id):
    return int(''.join([number for number in id if number.isdigit()]))


def check_members(member):
    with open("Moders.txt") as moders:
        print(moders)


@bot.command()
async def help(ctx):
    t = '✅'
    commands = [f'Действия:',
                f'  {emoji.emojize(t)}  weather город - вывод погоды в  определенном городе',
                f'  {emoji.emojize(t)}  pic животное - фото животного',
                f'  {emoji.emojize(t)}  fact животное - факт о животном',
                f'  {emoji.emojize(t)}  meme - мем',
                f'  {emoji.emojize(t)}  joke - шутка']
    embed = discord.Embed(color=0xff9900, title=f'Действия')
    embed.add_field(name='<<commands>>', value='\n'.join(commands), inline=True)
    print(check_members(123))


@bot.command()
async def addrole(ctx, member, role):
    member = discord.utils.get(ctx.guild.members, id=convert_id(member))
    role = discord.utils.get(ctx.guild.roles, id=convert_id(role))
    await member.add_roles(role)


@bot.command()
async def delrole(ctx, member, role):
    member = discord.utils.get(ctx.guild.members, id=convert_id(member))
    role = discord.utils.get(ctx.guild.roles, id=convert_id(role))
    await member.remove_roles(role)


@bot.command()
async def ban(ctx, member, reason='None'):
    member = discord.utils.get(ctx.guild.members, id=convert_id(member))
    await member.ban(reason=reason)
    embed = discord.Embed(color=0xFF0000,
                          title=f'Пользователь {str(member).split("#")[0]} был забанен по причине {reason}!')
    await ctx.send(embed=embed)


@bot.command()
async def unban(ctx, member):
    banned_users = await ctx.guild.bans()
    for ban_entry in banned_users:
        user = ban_entry.user
        await ctx.guild.unban(user)

    embed = discord.Embed(color=0x00FF00,
                          title=f'Пользователь {str(user).split("#")[0]} был разбанен!')
    await ctx.send(embed=embed)


@bot.command()
async def kick(ctx, member, reason='None'):
    member = discord.utils.get(ctx.guild.members, id=convert_id(member))
    print(member)
    await member.kick(reason=reason)
    embed = discord.Embed(color=0x00FF00,
                         title=f'Пользователь {str(member).split("#")[0]} был исключен с сервера по причине {reason}!')
    await ctx.send(embed=embed)


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
    channel = bot.get_channel(payload.channel_id)
    guild = bot.get_guild(922501298111250493)
    people_role = guild.get_role(963432221421764618)
    meh_role = guild.get_role(964515540456575037)
    if message_id == last_help_message_id:
        if payload.emoji.name == 'ALTCHECK':
            print(last_author)
            await last_author.add_roles(people_role)
        elif payload.emoji.name == 'MinecraftNo':
            await last_author.add_roles(meh_role)


@bot.event 
async def on_raw_reaction_remove(payload):
    print("reaction_removed")

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


@bot.command()
async def pic(ctx, animal):
    responce = requests.get(f'https://some-random-api.ml/img/{animal}')
    json_data = json.loads(responce.text)
    embed = discord.Embed(color=0xff9900)
    embed.set_image(url=json_data['link'])
    await ctx.send(embed=embed)


@bot.command()
async def fact(ctx, animal):
    responce = requests.get(f'https://some-random-api.ml/facts/{animal}')
    json_data = json.loads(responce.text)
    responce_2 = requests.get(f'https://some-random-api.ml/animal/{animal}')
    json_data_2 = json.loads(responce_2.text)
    result = translator.translate(json_data['fact'], dest='ru', src='en')
    embed_ru = discord.Embed(color=0xff9900, title=result.text)
    embed_en = discord.Embed(color=0xff9900, title=json_data['fact'])
    embed_en.set_image(url=json_data_2['image'])
    await ctx.send(embed=embed_en)
    await ctx.send(embed=embed_ru)


@bot.command()
async def meme(ctx):
    responce = requests.get('https://some-random-api.ml/meme')
    json_data = json.loads(responce.text)
    embed = discord.Embed(color=0xff9900)
    embed.set_image(url=json_data['image'])
    await ctx.send(embed=embed)


@bot.command()
async def joke(ctx):
    responce = requests.get('https://some-random-api.ml/joke')
    json_data = json.loads(responce.text)
    result = translator.translate(json_data['joke'], dest='ru', src='en')
    embed_ru = discord.Embed(color=0xff9900, title=result.text)
    embed_en = discord.Embed(color=0xff9900, title=json_data['joke'])
    await ctx.send(embed=embed_en)
    await ctx.send(embed=embed_ru)

bot.run(settings['token'])