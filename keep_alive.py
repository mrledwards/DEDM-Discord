from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "I'm alive!!! </br> DEDM Discord bot </br><img src=https://i.imgur.com/XCL9PUZ.jpg>"

def run():
  app.run(host='0.0.0.0',port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()