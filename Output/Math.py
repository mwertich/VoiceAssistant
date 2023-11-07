import re
import math
import numpy as np
from HelpFuncs import roundFloat


class Math:
    assistant: object
    input: str
    output: str

    def __init__(self, assistant, input: str, output: str):
        self.assistant = assistant
        self.input = input
        self.output = output

    def add(self):
        numbers = [float(i) for i in re.findall(r'[\d]+', self.input)]
        result = sum(numbers)

        return self.output.format(roundFloat(result))

    def sub(self):
        numbers = [float(i) for i in re.findall(r'[\d]+', self.input)]
        result = numbers[0]

        for i in range(1, len(numbers)):
            result -= numbers[i]

        return self.output.format(roundFloat(result))

    def mult(self):
        result = np.prod([float(i) for i in re.findall(r'[\d]+', self.input)])

        return self.output.format(roundFloat(result))

    def div(self):
        numbers = ([float(i) for i in re.findall(r'[\d]+', self.input)])
        result = numbers[0]

        for i in range(1, len(numbers)):
            result /= numbers[i]

        return self.output.format(roundFloat(result))

    def pwrd(self):
        numbers = ([float(i) for i in re.findall(r'[\d]+', self.input)])
        if "squared" in self.input:
            result = math.pow(numbers[0], 2)
        else:
            result = math.pow(numbers[0], numbers[1])

        return self.output.format(roundFloat(result))


class ConvertUnits:
    assistant: object
    input: str
    output: str

    def __init__(self, assistant, input: str, output: str):
        self.assistant = assistant
        self.input = input
        self.output = output

    def callFunc(self):
        input = self.input.split(" ")
        number = input[input.index("convert") + 1]

        if "per" in input:
            unit = input[input.index("per") - 1] + " per " + input[input.index("per") + 1]
            funcUnit = unit.replace(" per hour", "ph").replace(" per second", "psec")
            targetUnit = input[[ind for ind, ele in enumerate(input) if ele == "per"][1] - 1] + " per " + input[input.index("per") + 1]
            funcTargetUnit = targetUnit.replace(" per hour", "ph").replace(" per second", "psec")
            print(f"{funcUnit}To{funcTargetUnit.capitalize()}")
        else:
            unit = funcUnit = input[input.index("to") - 1]
            targetUnit = funcTargetUnit = input[input.index("to") + 1]

            if unit == "kw" or unit == "kilowatts":
                unit = "kilowatts"
                funcUnit = "kw"
            elif targetUnit == "kw" or targetUnit == "kilowatts":
                targetUnit = "kilowatts"
                funcTargetUnit = "kw"
        try:
            if unit == targetUnit:
                return self.output.split("|")[2]
            return self.output.split("|")[0].format(number, unit, targetUnit, roundFloat(
                self.__getattribute__(f"{funcUnit}To{funcTargetUnit.capitalize()}")(float(number))))
        except:
            return self.output.split("|")[1]

    def kmphToMilesph(self, number: float):
        return number * 0.6213712

    def milesphToKmph(self, number: float):
        return number * (1 / 0.6213712)

    def kgToPounds(self, number: float):
        return number * 2.204623

    def pundsToKg(self, number: float):
        return number * (1 / 2.204623)

    def milesToKm(self, number: float):
        return number * 1.609344

    def kmToMiles(self, number: float):
        return number * (1 / 1.609344)

    def hpToKw(self, number: float):
        return number * 0.7456999

    def kwToHp(self, number: float):
        return number * (1 / 0.7456999)

    def mToKm(self, number: float):
        return number / 1000

    def kmToM(self, number: float):
        return number * 1000

    def mToMiles(self, number: float):
        return number * 0.0006213712

    def milesToM(self, number: float):
        return number * (1 / 0.0006213712)
