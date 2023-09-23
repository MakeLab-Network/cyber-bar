from gtts import gTTS
import os
import playsound
from pydub import AudioSegment


def speed_change(sound, speed=1.5):
    # Manually override the frame_rate. This will also change the pitch (unless `sound._spawn` is used).
    sound_with_altered_frame_rate = sound._spawn(sound.raw_data, overrides={
        "frame_rate": int(sound.frame_rate * speed)
    }).set_frame_rate(sound.frame_rate)
    return sound_with_altered_frame_rate


def say(text, block=False):
    tts = gTTS(text=text, lang='iw', slow=False)

    filename = "tmp-text.mp3"
    filename_fast = "tmp-text-fast.mp3"
    try:
        tts.save(filename)
        sound = AudioSegment.from_file(filename, format="mp3")
        # Speed up by 1.5 times (you can adjust the value to your liking)
        fast_sound = speed_change(sound, 1.5)
        fast_sound.export(filename_fast, format="mp3")
        playsound.playsound(filename_fast, block=block)
        os.remove(filename)
        os.remove(filename_fast)
    except Exception as e:
        print(f"fucking sound shit: {e}")


def minion_sound(sound_name, block=False):
    file_path = os.path.join("web_app", "sounds", f"{sound_name}.mp3")
    playsound.playsound(file_path, block=block)
