import pyttsx3
import datetime
import speech_recognition as sr
import wikipedia
import webbrowser
import os
import smtplib
import random
from pytube import YouTube
from pytube.cli import on_progress

edge_path ="C:\\Program Files (x86)\\Microsoft\\Edge\\Application\\msedge.exe"
webbrowser.register('edge', None, webbrowser.BackgroundBrowser(edge_path))

#initialising engine
engine =pyttsx3.init('sapi5')
voices = engine.getProperty('voices')

engine.setProperty('voice',voices[2].id)

# initialising speech
def speak(audio):
    engine.say(audio)
    engine.runAndWait()

name ="your name"
#wishme function - for startup
def wishMe():
    hour = int(datetime.datetime.now().hour)
    if hour>=0 and hour<12:
        speak(f"Good morning {name}!")

    elif hour>=12 and hour<18:
        speak(f"Good afternoon {name}")
    
    else:
        speak("Good evening!")
    
    speak('I am jarvis sir, please tell me how may i help you')

def takeCommand():
    #it takes microphone input from the user and returns string

    r = sr.Recognizer()
    #creating a source
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        print("Listening...")
        r.pause_threshold = 1
        #seconds of non speaking audio 
        audio = r.listen(source)
        
    try:
        print('Recognizing...')
        #select recognising engine
        query = r.recognize_google(audio , language = 'en-in')
        print(f"User said: {query}\n")

    except Exception as e:
        print(e)
        print(" Say that again Please .. ")
        return "None"   

    return query

def sendEmail(to,content):
    server = smtplib.SMTP('smtp.gmail.com',587)
    server.ehlo()
    server.starttls()
    server.login('yourname@gmail.com','prassword')
    server.sendmail('yourname@gmail.com',to,content)
    server.close()

def random_song(num):
    return random.randint(0,num)

def viddwnld():
    speak("Enter url in the console")
    url = input("Enter url in the console:")
    yt = YouTube(url,on_progress_callback=on_progress)
    speak(f'Downloading.. {yt.title}')
    print("Downloading")
    streams = yt.streams.filter(progressive =True,res='720p')
    if len(streams) == 0:
        stream = yt.streams.filter(progressive = True).first()
        
    else:
        stream =streams[0]
    
    stream.download("C:\\Users\\pranavajay\\Videos\\")
    print("Downloaded")
    speak("Video downloaded succesfully!")

def musdwnld():
    speak("Enter url in the console")
    url = input("Enter url in the console:")
    yt = YouTube(url,on_progress_callback=on_progress)
    speak(f'Downloading.. {yt.title}')
    print("Downloading song ")
    stream = yt.streams.filter(only_audio=True).first()
    output = stream.download("C:\\Users\\pranavajay\\Music\\")
    base,ext = os.path.splitext(output)
    new_file = base +'.mp3'
    os.rename(output, new_file)
    print("Downloaded")
    speak("Song downloaded succesfully!")



if __name__ == '__main__':
    wishMe()
    while True:
        query = takeCommand().lower()
    #logic for executing tasks based on query
        if 'wikipedia' in query:
            print('Searching wikipedia...')
            query = query.replace("wikipedia","")
            results = wikipedia.summary (query, sentences =2)
            speak("According to wikipedia")
            print(results)
            speak(results)
        
        elif 'open youtube' in query:
            speak("Opening YouTube")
            webbrowser.get('edge').open('http://www.youtube.com')

        elif 'open twitter' in query:
            speak("Opening Twitter")
            webbrowser.get('edge').open('http://www.twitter.com')
        
        elif 'open google' in query:
            speak("Opening google")
            webbrowser.get('edge').open('http://www.google.com')
        
        elif 'play music' in query:
            music_dir = 'C:\\Users\\pranavajay\\Music'
            songs = os.listdir(music_dir)
            
            print(songs)
            os.startfile(os.path.join(music_dir,songs[random_song(len(songs)-1)]))


        elif 'time' in query:
            strtime = datetime.datetime.now().strftime("%H:%M:%S")
            speak(f"pranav , the time is {strtime}")

        elif 'open code' in query:
            path = 'C:\\Users\\pranavajay\\AppData\\Local\\Programs\\Microsoft VS Code\\Code.exe'
            os.startfile(path)

        elif 'open spotify' in query:
            path = 'C:\\Program Files\\WindowsApps\\SpotifyAB.SpotifyMusic_1.161.583.0_x86__zpdnekdrzrea0\\Spotify.exe' 
            os.startfile(path)

        elif 'email to pranav' in query:
            try:
                speak('What should io say?')
                content = takeCommand()
                to = "sentmail@gmail.com"
                sendEmail(to,content)
                speak("Email has been sent")

            except Exception as e:
                print(e)
                speak(f"Sorry {name} i was unabvle to sent the mail")

            
        elif 'close' in query:
            speak('Thanks for your valuable time..')
            speak('Quitting..')
            exit(1)

        elif 'hi' in query:
            speak('Hello , {name}what can i do for you, today')

        elif 'download video' in query:
            viddwnld()
        
        elif 'download music' in query:
            musdwnld()