import pyttsx3
import threading


def speak(text):
    def speak_thread(text):
        engine = pyttsx3.init()
        engine.say(text)
        engine.runAndWait()
        # Create a new thread to run the text-to-speech engine
    t = threading.Thread(target=speak_thread, args=(text,))
    t.start()
