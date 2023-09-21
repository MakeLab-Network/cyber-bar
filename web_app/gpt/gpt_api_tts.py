
import openai
import os
import time
from gtts import gTTS
from ..speak import speak

openai.api_key = os.environ.get("openai_key")


all_chunks = ""


def ask_gpt(prompt, model="gpt-3.5-turbo"):
    messages = [{"role": "user", "content": prompt}]
    response = openai.ChatCompletion.create(
        model=model, messages=messages, temperature=0, stream=True)
    chunks = ""
    all_chunks = ""
    i = 0
    for chunk in response:
        i += 1
        response_text = chunk.choices[0].delta.get("content", "")
        chunks += response_text
        all_chunks += response_text
        if '\n' in chunks or '.' in chunks or ',' in chunks or i > 100:
            play_tts(chunks, end_line=('\n' in chunks))
            chunks = ""
            i = 0
    speak(chunks)
    # return all_chunks
    # return response_text


def ask_gpt3(prompt):
    ask_gpt(prompt, model="gpt-3.5-turbo")


def ask_gpt4(prompt):
    ask_gpt(prompt, model="gpt-4")
