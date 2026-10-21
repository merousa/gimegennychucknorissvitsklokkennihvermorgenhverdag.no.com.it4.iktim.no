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
    jokeText = response.json()["value"]
    return Joke(joke=jokeText)

def jokeInVault(date):
    if not date:
        date = datetime.datetime.today().strftime("%d.%m.%Y")
    try:
        with open("jokeVault","r") as vault:
            data = json.load(vault)
            if date in data:
                return data[date]["joke"]
    except (FileNotFoundError, json.JSONDecodeError):
        pass

def addToVault(date,joke):
    try:

        with open("jokeVault","r+") as vault:
            data = json.load(vault)
    except (FileNotFoundError, json.JSONDecodeError):
        data = {}

    data[date] = {"joke": joke}

    with open("jokeVault","w") as vault:
        json.dump(data,vault,indent=4)

def timeForNewJoke():
    date = datetime.datetime.now()
    hour = date.hour
    if hour >= 9:
        return True
    else:
        return False

def getJokeFromDate(date):
    if not timeForNewJoke():
        date = (datetime.datetime.now() - datetime.timedelta(days=1)).strftime("%d.%m.%Y")
    savedJoke = jokeInVault(date)
    if savedJoke:
        print("Joke found")
        return Joke(joke=savedJoke)

    print("Joke not found")
    newJoke = getFromAPI()
    addToVault(date,newJoke.joke)
    return newJoke

app = Flask(__name__)

@app.route("/")
def home():
    date = datetime.datetime.today().strftime("%d.%m.%Y")
    joke = getJokeFromDate(date)
    print(date,joke)
    return render_template("index.html", joke=joke.joke)

if __name__ == "__main__":
    try:
        open("jokeVault","x").write("{}")
    except FileExistsError:
        pass
    app.run(host="0.0.0.0",port=5000)