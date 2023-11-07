import matplotlib.pyplot as plt
import requests
from HelpFuncs import sortDays


class Weather:
    assistant: object
    input: str
    output: str

    def __init__(self, assistant, input: str, output: str):
        self.assistant = assistant
        self.input = input
        self.output = output

    def todays(self):
        weather = getWeather(self.assistant, self.input, 0)
        return self.output.format(weather[1], weather[2], weather[0]).lower()

    def tomorrows(self):
        weather = getWeather(self.input, 1)
        return self.output.format(weather[1], weather[2], weather[0]).lower()

    def rainToday(self):
        weather = getWeather(self.assistant, self.input, 0)
        return self.output.format(weather[0], weather[3])

    def rainTomorrow(self):
        weather = getWeather(self.assistant, self.input, 1)
        return self.output.format(weather[0], weather[3])

    def windToday(self):
        weather = getWeather(self.assistant, self.input, 0)
        return self.output.format(weather[4])

    def windTomorrow(self):
        weather = getWeather(self.assistant, self.input, 1)
        return self.output.format(weather[4])

    def gustsToday(self):
        weather = getWeather(self.assistant, self.input, 0)
        return self.output.format(weather[5])

    def gustsTomorrow(self):
        weather = getWeather(self.assistant, self.input, 1)
        return self.output.format(weather[5])

    def week(self):
        weather = getWeekWeather(self.assistant, self.input)

        days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
        x = sortDays(days)
        y1 = [weather[i][0] for i in range(len(weather))]
        y2 = [weather[i][1] for i in range(len(weather))]

        fig, ax = plt.subplots()
        ax.plot(x, y1, color="r", label="Temperature (C)")
        ax.plot(x, y2, color="b", label="Precipitation(%)")
        ax.set(xlabel="day", ylabel="weather", title="weather next 7 days")
        ax.legend()
        ax.grid()
        plt.show()

        return self.output


def getWeather(assistant, input: str, offset: int):
    """returns weather for given offset from today"""
    apiKey = assistant.databank.getConfig("weather api key")

    try:
        city = input[input.index("weather in ") + 11:].split(" ")[0]
    except:
        city = assistant.databank.getConfig("default location")

    url = f"https://api.weatherbit.io/v2.0/forecast/daily?city={city}&key={apiKey}"
    data = requests.get(url).json()["data"]
    temp = int(data[offset]["high_temp"])
    weather = data[offset]["weather"]["description"]
    rain = data[offset]["pop"]
    wind = int(data[offset]["wind_spd"] * 3.6)
    gusts = int(data[offset]["wind_gust_spd"] * 3.6)

    return city, temp, weather, rain, wind, gusts


def getWeekWeather(assistant, input: str):
    """returns a graph of the weather for the next 7 days"""
    weather = []
    for day in range(7):
        weather.append(getWeather(assistant, input, day))

    weather = [(weather[i][1], weather[i][3]) for i in range(len(weather))]
    return weather
