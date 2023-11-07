from gtts import gTTS
from audioplayer import AudioPlayer
import speech_recognition as sr
import os
from dataclasses import dataclass


@dataclass
class Speech:
    def tts(self, output: str):
        try:
            googltts = gTTS(output.splitlines()[0], lang="en", slow=False)
            googltts.save("audio/tts.mp3")
            AudioPlayer("audio/tts.mp3").play(block=True)
            os.remove("audio/tts.mp3")
        except:
            pass

    def stt(self):
        with sr.Microphone() as micro:
            speech_engine = sr.Recognizer()
            print("Recording...")
            audio = speech_engine.record(micro, duration=3)
            print("Recognition...")
            try:
                text = speech_engine.recognize_google(audio, language="en-GB")
                return text
            except:
                return "Couldn't detect any input"
