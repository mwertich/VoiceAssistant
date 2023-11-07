from Output.OutputFuncs import Output

from Speech import Speech
from Databank import Databank
from Processing import Processing

# general base modules
from dataclasses import dataclass
from typing import List


class Assistant:
    speech: Speech
    processing: Processing
    output: Output
    databank: Databank
    __lastCommand: List[str]
    __lastInput: str
    debugMode: bool

    def __init__(self, debugMode=False):
        self.databank = Databank()
        self.speech = Speech()
        self.processing = Processing(self.databank)
        self.output = Output(self)
        self.debugMode = debugMode

    def __del__(self):
        if not self.debugMode:
            self.databank.getDbConn().commit()
        self.databank.getDbConn().close()

    def getLastCommand(self):
        return self.__lastCommand

    def getLastInput(self):
        return self.__lastInput

    def assistVoice(self):
        self.assistText(self.speech.stt())
        #input = self.speech.stt().replace("'", "")
        #cmd = self.processing.inputProcessor(input)
        #self.speech.tts(self.output.callFunc(cmd))
        #self.__lastCommand = cmd
        #self.__lastInput = input

    def assistText(self, input: str):
        input = input.lower().replace("'", "")
        cmd = self.processing.inputProcessor(input)
        output = self.output.callFunc(cmd)
        print(output)
        if not self.debugMode:
            self.speech.tts(output)
        self.__lastCommand = cmd
        self.__lastInput = input


# weather plotten
# reminder, alarm etc
# calendar
# elaborate on more commands
# play podcasts
# translate
# news
# moodle?
# outlook working?
# teams
# wikipedia data object
# detailed daily weather graph
# add task features, sorted by priority/time remaining
# star wars jokes
# play music with pyglet
assistant = Assistant(False)
#assistant.databank.addCommand("triviaStarWars", "who is in star wars|what is in star wars", "{}")
assistant.assistText("who is obi wan kenobi in star wars")
