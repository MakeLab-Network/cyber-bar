#!pip install openai
#!pip install gtts # (google-text-to-speech)
#!pip install pygame

import openai
import os
import time
from gtts import gTTS
from pygame import mixer
from pydub import AudioSegment
from pydub.playback import play

mixer.init()
openai.api_key = os.environ.get("openai_key")
output_path = r"C:\temp\output.mp3"

def create_tts_file(text, output_path, end_line=True):
	try:
		text = text.rstrip().lstrip()
		while(mixer.music.get_busy()):
			# print("waiting for last answer...")
			pass
		mixer.music.unload()
		try:
			os.remove(output_path)
		except:
			pass
		tts = gTTS(text)
		tts.save(output_path)
		print(text, end=('\n' if end_line else ' '))
	except Exception as e:
		print(e)

def play_file(path):
	try:
		mixer.music.load(path)
		# print(text, end=('\n' if end_line else ' '))
		mixer.music.play()
	except Exception as e:
		print(e)

def minionify_voice(input_file, output_file):
    sound = AudioSegment.from_file(input_file, format="mp3")
    
    # Adjust speed (increase speed for Minion effect)
    sound = sound.speedup(playback_speed=1.5)

    # Adjust pitch (increase pitch for Minion effect)
    sound = sound._spawn(sound.raw_data, overrides={
       "frame_rate": int(sound.frame_rate * 1.5)
    }).set_frame_rate(sound.frame_rate)
    
    sound.export(output_file, format="mp3")

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
			create_tts_file(chunks, output_path, end_line=('\n' in chunks))
			play_tts(output_path)
			chunks = ""
			i = 0
	create_tts_file(chunks, output_path, end_line=('\n' in chunks))
	play_tts(output_path)
	# return all_chunks
	# return response_text

def ask_gpt3(prompt):
	ask_gpt(prompt, model="gpt-3.5-turbo")

def ask_gpt4(prompt):
	ask_gpt(prompt, model="gpt-4")