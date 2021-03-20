import os
from discord.ext import commands
from .bot import Hotline
from docs import app
import threading

bot = Hotline(
    command_prefix=commands.when_mentioned_or('!'),
    help_command=None
)

for file in os.listdir('hotline/cogs'):
    path = os.path.join('hotline/cogs', file)
    if path.endswith('.py'):
        bot.load_extension(path.replace('.py', '').replace('/', '.'))

threading.Thread(target=app.run, args=['0.0.0.0', os.getenv('PORT')]).start()
bot.run(os.getenv('DISCORD_TOKEN'))
