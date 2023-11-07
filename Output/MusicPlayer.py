import pyaimp
import time
import os


class MusicPlayer:
    assistant: object
    player: str
    input: str
    output: str

    def __init__(self, assistant, player: str, input: str, output: str):
        self.assistant = assistant
        self.player = player
        self.input = input
        self.output = output

    def toggleMusic(self):
        if self.player == "AIMP":
            return AIMP.toggle(AIMP(self.assistant, self.input, self.output))

    def infoMusic(self):
        if self.player == "AIMP":
            return AIMP.info(AIMP(self.assistant, self.input, self.output))

    def playMusic(self):
        if self.player == "AIMP":
            return AIMP.play(AIMP(self.assistant, self.input, self.output))

    def nextMusic(self):
        if self.player == "AIMP":
            return AIMP.next(AIMP(self.assistant, self.input, self.output))

    def prevMusic(self):
        if self.player == "AIMP":
            return AIMP.prev(AIMP(self.assistant, self.input, self.output))

    def muteMusic(self):
        if self.player == "AIMP":
            return AIMP.mute(AIMP(self.assistant, self.input, self.output))

    def shuffleMusic(self):
        if self.player == "AIMP":
            return AIMP.shuffle(AIMP(self.assistant, self.input, self.output))

    def volumeMusic(self):
        if self.player == "AIMP":
            return AIMP.volumeMusic(AIMP(self.assistant, self.input, self.output))

    def relativeVolumeMusic(self):
        if self.player == "AIMP":
            return AIMP.relativeVolume(AIMP(self.assistant, self.input, self.output))


class AIMP(MusicPlayer):
    client: pyaimp.Client

    def __init__(self, assistant, input: str, output: str):
        super().__init__(assistant, "AIMP", input, output)
        try:
            self.client = pyaimp.Client()
        except:
            raise Exception("Aimp currently not running")

    def toggle(self):
        self.client.play_pause()
        time.sleep(1)

        if self.client.get_playback_state() == pyaimp.PlayBackState.Paused:
            return self.output.split("|")[1].format(self.client.get_current_track_info()["title"])
        else:
            return self.output.split("|")[0].format(self.client.get_current_track_info()["title"])

    def info(self):
        return self.output.format(self.client.get_current_track_info()["title"])

    def play(self):
        filePath = self.assistant.databank.getConfig("music folder")

        self.client.add_to_playlist_and_play(
            getFilePath(filePath, self.input[self.input.index("song") + 5:] + ".mp3"))
        time.sleep(1)
        return self.output.format(self.client.get_current_track_info()["title"])

    def next(self):
        self.client.next()
        time.sleep(0.5)
        return self.output.format(self.client.get_current_track_info()["title"])

    def prev(self):
        self.client.prev()
        time.sleep(0.5)
        return self.output.format(self.client.get_current_track_info()["title"])

    def mute(self):
        if self.client.is_muted():
            self.client.set_muted(False)
            return self.output.split("|")[0]
        else:
            self.client.set_muted(True)
            return self.output.split("|")[1]

    def shuffle(self):
        if self.client.is_shuffled():
            self.client.set_shuffled(False)
            return self.output.split("|")[1]
        else:
            self.client.set_shuffled(True)
            return self.output.split("|")[0]

    def volume(self):
        volume = [int(i) for i in self.input.split() if i.isdigit()][0]
        if 0 <= volume <= 100:
            self.client.set_volume(volume)
            return self.output.split("|")[0].format(self.client.get_volume())
        else:
            return self.output.split("|")[1]

    def relativeVolume(self):
        if self.input.__contains__("up"):
            volume = self.client.get_volume() + 5
            if volume > 100:
                volume = 100
        else:
            volume = self.client.get_volume() - 5
            if volume < 0:
                volume = 0
        self.client.set_volume(volume)
        return self.output.format(volume)


def getFilePath(self, path: str, name: str):
    with os.scandir(path) as dirs:
        for e in dirs:
            if "lrc" not in e.name:
                if e.name == name:
                    return e
                elif os.path.isdir(f"{path}\{e.name}"):
                    try:
                        return self.getFilePath(f"{path}\{e.name}", name)
                    except:
                        continue

        raise Exception(f"{name} not found in {path}")