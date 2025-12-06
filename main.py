import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests
from dotenv import load_dotenv
import os
import google.generativeai as genai

# Load API keys from .env
load_dotenv()

newsapi = os.getenv("NEWS_API")
gemini_api = os.getenv("GEMINI_API")

recogniser = sr.Recognizer()
engine = pyttsx3.init()

# Text-to-speech
def speak(text):
    engine.say(text)
    engine.runAndWait()

# Configure Gemini API safely
genai.configure(api_key=gemini_api)
model = genai.GenerativeModel("models/gemini-2.5-flash")

def aiprocess(command):
    try:
        response = model.generate_content(command)
        if response.text:
            print(response.text)
            return response.text
        else:
            print(" No output. Check API key or quota.")
            return None
    except Exception as e:
        print(f"Error: {e}")
        return None

def processCommand(c):
    c = c.lower()

    if "open google" in c:
        webbrowser.open("https://google.com")
    elif "open facebook" in c:
        webbrowser.open("https://facebook.com")
    elif "open youtube" in c:
        webbrowser.open("https://youtube.com")
    elif "open linkedin" in c:
        webbrowser.open("https://linkedin.com")
    elif c.startswith("play"):
        song = c.split(" ")[1]
        link = musicLibrary.music.get(song)
        if link:
            webbrowser.open(link)
    elif "news" in c:
        r = requests.get(
            f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}"
        )
        if r.status_code == 200:
            data = r.json()
            articles = data.get("articles", [])
            print("📰 Top Headlines:\n")
            for article in articles:
                print(article['title'])
    else:
        output = aiprocess(c)
        if output:
            speak(output)
            print(output)

if __name__ == "__main__":
    speak("Initialising Jarvis...")
    while True:
        r = sr.Recognizer()
        print("recognising...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source, timeout=2, phrase_time_limit=2)
            word = r.recognize_google(audio)
            print("Heard word:", word)

            if "jarvis" in word.lower():
                print("Jarvis detected, speaking Yah...")
                speak("Yah!")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command = r.recognize_google(audio)
                    processCommand(command)

        except Exception as e:
            print(f"error: {e}")
