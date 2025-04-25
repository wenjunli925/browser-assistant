from dotenv import load_dotenv
import os
import speech_recognition as sr
import openai
from openai import OpenAI
# import pyttsx3
from elevenlabs import ElevenLabs, VoiceSettings
from elevenlabs import play

load_dotenv() 

clientOpenAI = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
clientElevenLabs = ElevenLabs(api_key=os.getenv("ELEVENLABS_API_KEY"))

# engine = pyttsx3.init()

def speak(text):
    # engine.say(text)
    # engine.runAndWait()
    audio = clientElevenLabs.generate(
        text=text,
        voice=os.getenv("VOICE_ID_JAMES"),
        model="eleven_monolingual_v1",
        voice_settings=VoiceSettings(stability=0.5, similarity_boost=0.5)
    )
    play(audio)

def listen():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        audio = r.listen(source)
    try:
        text = r.recognize_google(audio)
        print(f"You said: {text}")
        return text
    except sr.UnknownValueError:
        print("Sorry, I didn't catch that.")
        return None

def chat_with_gpt(prompt):
    response = clientOpenAI.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )
    reply = response.choices[0].message.content.strip()
    print(f"🤖 GPT: {reply}")
    return reply

# Main loop
while True:
    query = listen()
    if query:
        if "exit" in query.lower():
            speak("Goodbye!")
            break
        response = chat_with_gpt(query)
        speak(response)
