import discord
from discord.ext import commands
from config import settings


bot = commands.Bot(command_prefix=settings['prefix'], help_command=None)


@bot.command()
async def hello(ctx):
    author = ctx.message.author
    await ctx.send(f"Привет {author.mention}")

@bot.command()
async def help(ctx):
    commands = [f'Вызов бота = "+"',
                f'⭕ hello: - команда приветстия',
                f'⭕ join: - подключение бота к голосовому чату',
                f'⭕ leave: - отключение бота от голосового чата']

    embed = discord.Embed(color=0xff9900, title=f'Вызов бота = ">"')
    embed.add_field(name='<<commands>>', value='\n'.join(commands), inline=True)
    await ctx.send(embed=embed)

bot.run(settings['token'])
