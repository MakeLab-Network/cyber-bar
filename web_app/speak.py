from gtts import gTTS
import os
import playsound


def speak(text):
    tts = gTTS(text=text, lang='fr')

    filename = "tmp-text.mp3"
    tts.save(filename)
    playsound.playsound(filename, block=False)
    os.remove(filename)
