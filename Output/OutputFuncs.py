# general base modules
from datetime import datetime
from dataclasses import dataclass
from typing import List
import random
import numpy as np
import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning


from Output.MusicPlayer import MusicPlayer
from Output.Weather import Weather
from Output.Math import Math, ConvertUnits
from Output.Task import Task
from Output.Accounting import Accounting

# plot data
import matplotlib.pyplot as plt

# Wikipedia
import wikipedia

# jokes
import pyjokes
from dadjokes import Dadjoke

# dictionary
from PyDictionary import PyDictionary

# web search
from duckduckpy import secure_query



@dataclass
class Output:
    assistant: object

    def __init__(self, assistant: object):
        """instanziert databank und helpFunc zum Nutzen"""
        self.assistant = assistant

    def callFunc(self, cmd: List):
        """Übersetzt String zu Funktion/Class mit richtigen Argumenten"""
        if "Music" in cmd[0]:
            return MusicPlayer.__getattribute__(MusicPlayer, cmd[0])(
                MusicPlayer(self.assistant, self.assistant.databank.getConfig("music player"), cmd[1], cmd[2]))
        elif "Task" in cmd[0]:
            return Task.__getattribute__(Task, cmd[0][:-4])(Task(self.assistant, cmd[1], cmd[2]))
        elif "Math" in cmd[0]:
            return Math.__getattribute__(Math, cmd[0][:-4])(Math(self.assistant, cmd[1], cmd[2]))
        elif "Weather" in cmd[0]:
            return Math.__getattribute__(Weather, cmd[0][:-7])(Weather(self.assistant, cmd[1], cmd[2]))
        elif "convertUnits" in cmd[0]:
            return ConvertUnits.callFunc(ConvertUnits(self.assistant, cmd[1], cmd[2]))
        elif "Accounting" in cmd[0]:
            return Accounting.__getattribute__(Accounting, cmd[0][0:-10])(Accounting(self.assistant, cmd[1], cmd[2]))
        else:
            return getattr(self, cmd[0])(cmd[1], cmd[2])

    def error(self, input: str, output: str):
        return output

    def time(self, input: str, output: str):
        return output.format(datetime.now().strftime('%H:%M'))

    def greeting(self, input: str, output: str):
        out = output.split("|")
        return out[random.randint(0, len(out) - 1)]

    def commandUsage(self, input: str, output: str):
        dbCursor = self.assistant.databank.getDbConn().cursor()
        dbCursor.execute("SELECT name,usage FROM commands")
        rows = dbCursor.fetchall()

        y = np.array([], dtype="i")
        x = np.array([], dtype="i")
        for e in rows:
            x = np.append(x, e[0])
            y = np.append(y, e[1])

        plt.barh(x, y, align="center", alpha=0.8)
        plt.xticks(range(np.max(y) + 1))
        plt.xlabel("USAGE")
        plt.title("command usage")
        plt.show()
        return output

    def wikipedia(self, input: str, output: str):
        try:
            return wikipedia.summary(input[input.index("search wikipedia for") + 18:]).split(".")[0]
        except:
            return output

    def joke(self, input: str, output: str):
        theme = random.randint(0, 1)
        if theme == 0:
            return pyjokes.get_joke()
        else:
            return Dadjoke().joke

    def synonym(self, input: str, output: str):
        if input.__contains__("synonyms"):
            word = input.split(" ")
            word = word[word.index("synonyms") + 1]
        elif input.__contains__("synonym"):
            word = input.split(" ")
            word = word[word.index("synonym") + 1]
        else:
            word = input.split("synonym for")
            word = word[word.index("") + 1]

        synonym = PyDictionary().synonym(word)[0:3]
        return output.format(word, str(synonym)[1:-1])

    def define(self, input: str, output: str):
        word = input.split(" ")
        word = word[word.index("define") + 1]
        definition = PyDictionary().meaning(word)["Noun"][0]
        return output.format(word, definition)

    def websearch(self, input: str, output: str):
        searchterm = input[input.index("search for") + 11:]
        result = secure_query(searchterm).abstract.split(".")[0]
        return output.format(result)

    def diceRoll(self, input: str, output: str):
        return output.format(random.randint(0, 6))

    def coinFlip(self, input: str, output: str):
        coin = ["heads", "tails"]
        return output.format(coin[random.randint(0, 1)])

    def randNumber(self, input: str, output: str):
        min = input.split(" ")[input.split(" ").index("between") + 1]
        max = input.split(" ")[input.split(" ").index(min) + 2]
        return output.format(random.randint(int(min), int(max)))

    def spellWord(self, input: str, output: str):
        word = [char for char in input[input.index("spell") + 6:]]
        return output.format(str(word)[1:-1])

    def elaborate(self, input: str, output: str):
        lastCmd = self.assistant.getLastCommand()
        lastInput = self.assistant.getLastInput()
        if lastCmd[0] == "wikipedia":
            article = wikipedia.summary(lastInput[lastInput.index("search wikipedia for") + 18:]).split(".")
            output = f"{article[1]}.{article[2]}"

        return output

    def quote(self, input: str, output: str):
        theme = random.randint(0, 1)
        if theme == 0:
            quote = requests.get("https://api.kanye.rest/").json()["quote"]
            quote += " - Kanye West"
        else:
            requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
            quote = requests.get("https://swquotesapi.digitaljedi.dk/api/SWQuote/RandomStarWarsQuote", verify=False).json()["content"]
        return output.format(f"{quote}")

    def triviaStarWars(self, input: str, output: str):
        return output

    def exit(self, input: str, output: str):
        print(output)
        exit()
