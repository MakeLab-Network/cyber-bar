#!pip install openai
#!pip install gtts # (google-text-to-speech)
#!pip install pygame

import openai
import os
import time
from gtts import gTTS
from pygame import mixer
mixer.init()
openai.api_key = os.environ.get("openai_key")

def play_tts(text, end_line=True):
	try:
		text = text.rstrip().lstrip()
		while(mixer.music.get_busy()):
			# print("waiting for last answer...")
			pass
		mixer.music.unload()
		try:
			os.remove("tts.mp3")
		except:
			pass
		tts = gTTS(text)
		tts.save("tts.mp3")
		mixer.music.load("tts.mp3")
		print(text, end=('\n' if end_line else ' '))
		mixer.music.play()
	except:
		pass

all_chunks=""
def ask_gpt(prompt, model="gpt-3.5-turbo"):
	messages = [{"role": "user", "content": prompt}]
	response = openai.ChatCompletion.create(model=model, messages=messages, temperature=0, stream=True)
	chunks = ""
	all_chunks=""
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
	play_tts(chunks)
	# return all_chunks
	# return response_text

def ask_gpt3(prompt):
	ask_gpt(prompt, model="gpt-3.5-turbo")

def ask_gpt4(prompt):
	ask_gpt(prompt, model="gpt-4")