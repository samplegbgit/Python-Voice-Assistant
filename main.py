import speech_recognition as sr
import webbrowser
import pyttsx3
import musicLibrary
import requests

recogniser=sr.Recognizer()
engine=pyttsx3.init()
newsapi="97f35a298ae9403faec419c83fc32c90"

def speak(text):
    engine.say(text)
    engine.runAndWait()

import google.generativeai as genai


genai.configure(api_key="AIzaSyCgWELq-jrAZdlvrLNY1v40TxBOBUV6rxs")


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
    if "open google" in c.lower():
        webbrowser.open("https://google.com")
    elif "open facebook" in c.lower():
        webbrowser.open("https://facebook.com")
    
    elif "open youtube" in c.lower():
        webbrowser.open("https://youtube.com")
    
    elif "open linkedin" in c.lower():
        webbrowser.open("https://linkedin.com")
    
    elif c.lower().startswith("play"):
        song=c.lower().split(" ")[1]
        link= musicLibrary.music[song]
        webbrowser.open(link)

    elif "news" in c.lower():
        r=requests.get(f"https://newsapi.org/v2/top-headlines?country=us&apiKey={newsapi}")
        if r.status_code == 200:
            data = r.json()
            
    
            articles = data.get("articles", [])
            
            print("📰 Top Headlines:\n")
            for article in articles:
                print(article['title'])
    else:

       output= aiprocess(c)
       speak(output)
       print(output)


if __name__ =="__main__":
    speak("Initialising Jarvis...")
    while True:
    
        r = sr.Recognizer()
        

        print("recognising...")
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = r.listen(source,timeout=2,phrase_time_limit=2)
            word=r.recognize_google(audio)
            print("Heard word:", word)
            if "jarvis" in word.lower():
                print("Jarvis detected, speaking Yah...")
                speak("Yah!")
                with sr.Microphone() as source:
                    print("Jarvis active...")
                    audio = r.listen(source)
                    command=r.recognize_google(audio)

                    processCommand(command)

        except Exception as e:
            print("error; {0}".format(e))