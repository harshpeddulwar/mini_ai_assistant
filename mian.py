import os
from groq import Groq 
import speech_recognition as sr
import pyttsx3
from dotenv import load_dotenv
load_dotenv()

groq_api_key = os.getenv("GROQ_API_KEY")
client = Groq(api_key=groq_api_key)
recognizer = sr.Recognizer()

engine = pyttsx3.init()

def speak(text):
    engine.say(text)
    engine.runAndWait()

def listen():
    with sr.Microphone() as source:
        print("Listenning....")
        audio = recognizer.listen(source, timeout=5)
        try:
            print("Recognizing....")
            query = recognizer.recognize_google(audio)
            print(f" You said {query}")
            return query
        except sr.UnknownValueError:
            print("Could not understand audio")
            speak("Could not understand audio")
            return ""
        except sr.RequestError as e:
            print("Speech unavailabel")
            speak("Speech service is unavailabel")
            return ""
        except sr.WaitTimeoutError:
            print("No speech detected")
            return ""

def ask_gpt(question):
        try:
             response = client.chat.completions.create(
                  model="meta-llama/llama-4-scout-17b-16e-instruct",
                  messages=[
                       {"role": "system", "content": "You are a helpful assistant. Keep responses concise and small for voice interaction. "},
                       {"role": "user", "content": question}
                  ],
                  max_tokens=100,
                  temperature=0.7
             )
             answer = response.choices[0].message.content
             return answer
        except Exception as e:
             print(f"Groq api error{e}")
             return "Sorry, having trouble connecting to groq"

def main():
     speak("Hello!, I am your assistant. How can i help you?")
     while True:
          query = listen()
          if query.lower() in ["exit","quit","stop","bye"]:
           speak("goodbye!")
           break
        
          if query:
            answer = ask_gpt(query)
            print(f"Assistant:{answer}")
            speak(answer)

if __name__ == "__main__":
     main()