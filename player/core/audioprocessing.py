import speech_recognition as sr
import sounddevice as sd
import pyttsx3
engine = pyttsx3.init()


def text_to_speech(text:str):       
    engine.say(text)
    engine.runAndWait()

def play_back_audio(wav):
    sd.play(wav)
    sd.wait() 

def record_audio():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = recognizer.listen(source)
    return audio

def recognize_speech(audio):
    try:
        text = ''
        recognizer = sr.Recognizer()
        text = recognizer.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I couldn't understand that.")
        return text
    except sr.RequestError:
        print("Sorry, there was an error processing your request.")
        return text




    



