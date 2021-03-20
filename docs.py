from flask import Flask
import os
import threading


app = Flask(__name__)


@app.route('/')
def home():
    return 'You have found the home of a python program.'


from hotline.__main__ import bot

threading.Thread(
    target=bot.run,
    args=[os.getenv('DISCORD_TOKEN')]
).start()



if __name__ == '__main__':
    app.run('0.0.0.0', 8080)