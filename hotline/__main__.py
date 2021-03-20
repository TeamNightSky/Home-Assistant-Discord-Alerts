import os
from discord.ext import commands
from .bot import Hotline

bot = Hotline(
    command_prefix=commands.when_mentioned_or('!'),
    help_command=None
)

for file in os.listdir('hotline/cogs'):
    path = os.path.join('hotline/cogs', file)
    if path.endswith('.py'):
        bot.load_extension(path.replace('.py', '').replace('/', '.'))

