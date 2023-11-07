from dataclasses import dataclass
from Databank import Databank

@dataclass
class Processing:
    databank: Databank

    def __init__(self, databank: Databank):
        self.databank = databank

    def inputProcessor(self, input: str):
        """Fetches keywords from database to compare them to input and determines output string"""
        rows = self.databank.getTable("commands")
        for i in range(len(rows)):
            keywords = rows[i][1].split("|")
            for j in range(len(keywords)):
                if all(e in input.split(" ") for e in keywords[j].split(" ")):
                    self.databank.useCommand(rows[i][0])
                    return [rows[i][0], input, rows[i][2]]
        else:
            if input == "Couldn't detect any input":
                return ["error", "", input]
            else:
                print(f"not recognized: {input}")
                return ["error", "", "excuse me, i couldnt understand you"]