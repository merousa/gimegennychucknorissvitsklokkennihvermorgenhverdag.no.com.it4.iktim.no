from flask import Flask,render_template
import requests
import schedule
import json
import datetime
from dataclasses import dataclass

@dataclass
class Joke:
    joke: str = None

def getFromAPI():
    response = requests.get("https://api.chucknorris.io/jokes/random")
    return Joke(joke=response.json()["value"])

def jokeInVault(date):
    joke = None
    if not date:
        date = datetime.datetime.today().strftime("%d.%m.%Y")
    with open("jokeVault","r") as vault:
        data = json.load(vault)
        if date in data:
            joke = data[date]["joke"]
    return Joke(joke = joke)

def addToVault(date,joke):
    with open("jokeVault","r+") as vault:
        data = json.load(vault)
        data[date] = {"joke": joke}
        vault.seek(0)
        json.dump(data, vault, indent=4)

def getJokeFromDate(date):
    if jokeInVault(date):
        return jokeInVault(date)
    else:
        joke = getFromAPI()
        addToVault(date,joke.joke)
        return joke

app = Flask(__name__)

@app.route("/")
def home():
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    joke = getJokeFromDate(date)
    return render_template("index.html", joke=joke.joke)

if __name__ == "__main__":
    app.run(debug=True)