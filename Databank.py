# sql
import sqlite3

# config
from configparser import ConfigParser

# general base modules
from dataclasses import dataclass


@dataclass
class Databank:
    __dbConn: sqlite3.Connection

    def __init__(self):
        self.__dbConn = sqlite3.connect("assets/databanks/database.db")

    def getDbConn(self):
        return self.__dbConn

    def getCommandUsage(self, name: str):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute(f"SELECT usage FROM commands WHERE name = '{name}'")
        return dbCursor.fetchall()[0][0]

    def useCommand(self, name: str):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute(f"UPDATE commands SET usage = usage + 1 WHERE name = '{name}'")

    def addCommand(self, name: str, keywords: str, output: str):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute("SELECT name FROM commands")
        if name not in str(dbCursor.fetchall()):
            dbCursor.execute("INSERT INTO commands (name, keywords, output, usage) VALUES (?, ?, ?, 0)",
                             (name, keywords, output))
        else:
            print("command is already in database")

    def delCommmand(self, name: str):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute(f"DELETE FROM commands WHERE name = '{name}'")

    def updateCommand(self, name: str, newName: str, keywords="", output=""):
        dbCursor = self.__dbConn.cursor()
        if newName != "":
            dbCursor.execute(f"UPDATE commands SET name = '{newName}' WHERE name = '{name}'")
        if keywords != "":
            dbCursor.execute(f"UPDATE commands SET keywords = '{keywords}' WHERE name = '{name}'")
        if output != "":
            dbCursor.execute(f"UPDATE commands SET output = '{output}' WHERE name = '{name}'")

    def getTable(self, name: str):
        dbCursor = self.getDbConn().cursor()
        dbCursor.execute(f"SELECT * FROM {name}")
        return dbCursor.fetchall()

    def addTask(self, name: str, date: str):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute("INSERT INTO tasks (name, date, done) VALUES (?, ?, ?)", (name, date, 0))

    def delTask(self, name):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute(f"DELETE FROM tasks WHERE name = '{name}'")

    def taskDone(self, name):
        dbCursor = self.__dbConn.cursor()
        dbCursor.execute(f"UPDATE tasks SET done = 1 WHERE name = '{name}'")

    def defaultConfig(self):
        config_object = ConfigParser()
        config_object["CONFIG"] = {
            "music player": "AIMP",
            "music folder": "F:\Data\Music",
            "default location": "Mainz",
            "weather api key": "b2a39070b9ee41e29258d45e327d6e4b"
        }

        with open("assets/config.ini", "w") as conf:
            config_object.write(conf)

    def getConfig(self, attribute: str):
        config_object = ConfigParser()
        config_object.read("assets/config.ini")
        config = config_object["CONFIG"]
        return config[attribute]

    def updateConfig(self, attribute: str, value: str):
        config_object = ConfigParser()
        config_object.read("config.ini")
        config = config_object["CONFIG"]
        config[attribute] = value

        with open("assets/config.ini", "w") as conf:
            config_object.write(conf)
