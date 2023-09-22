from gtts import gTTS
import os
import playsound


def say(text, block=False):
    tts = gTTS(text=text, lang='iw', slow=False)

    filename = "tmp-text.mp3"
    tts.save(filename)
    playsound.playsound(filename, block=block)
    os.remove(filename)


def minion_sound(sound_name, block=False):
    file_path = os.path.join("web_app", "sounds", f"{sound_name}.mp3")
    playsound.playsound(file_path, block=block)
