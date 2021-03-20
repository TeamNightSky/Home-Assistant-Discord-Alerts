from flask import Flask


app = Flask(__name__)


@app.route('/')
def home():
    return 'You have found the home of a python program.'


if __name__ == '__main__':
    app.run('0.0.0.0', 8080)