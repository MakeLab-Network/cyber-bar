import openai
import os
import time
from gtts import gTTS
# from speak import speak
from pygame import mixer

# openai.api_key = os.environ.get("openai_key")


all_chunks = ""

mixer.init()
openai.api_key = os.environ.get("openai_key")
print(f"key: {os.environ.get('openai_key')}")


def play_tts(text, end_line=True):
    try:
        text = text.rstrip().lstrip()
        while (mixer.music.get_busy()):
            # print("waiting for last answer...")
            pass
        mixer.music.unload()
        try:
            os.remove("tts.mp3")
        except:
            pass
        tts = gTTS(text, lang='iw')
        tts.save("tts.mp3")
        mixer.music.load("tts.mp3")
        print(text, end=('\n' if end_line else ' '))
        mixer.music.play()
    except:
        pass


def ask_gpt(prompt, model="gpt-3.5-turbo"):
    # print("debug, ask gpt")
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0, stream=True)
    chunks = ""
    all_chunks = ""
    i = 0
    for chunk in response:
        i += 1
        response_text = chunk.choices[0].delta.get("content", "")
        # print(response_text)
        chunks += response_text
        all_chunks += response_text
        if '\n' in chunks or '.' in chunks or i > 100:
            print(chunks)
            play_tts(chunks, end_line=('\n' in chunks))
            # speak(chunks)
            chunks = ""
            i = 0
    play_tts(chunks)
    while(mixer.music.get_busy()):
            # print("waiting for last answer...")
            time.sleep(0.1)
    #speak(chunks)
    # return all_chunks
    # return response_text


def ask_gpt3(prompt):
    ask_gpt(prompt, model="gpt-3.5-turbo")


def ask_gpt4(prompt):
    ask_gpt(prompt, model="gpt-4")
