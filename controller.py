from Assistant import Assistant
import os


def controller(assistant):
    output = ""
    while True:
        os.system("cls" if os.name == "nt" else "clear")
        ConsoleInput = input("Enter a command or Press enter to use a voice command\n")
        if ConsoleInput == "":
            assistant.assistVoice()
        elif type(ConsoleInput) == str:
            assistant.assistText(ConsoleInput)


controller(assistant=Assistant())
