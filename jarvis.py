import time
import speech_recognition as sr
import sounddevice as sd
import numpy as np
import threading
import os

#api key setup
apiKey = os.getenv('GEMINI_API_KEY')

#speach to text
r = sr.Recognizer()
'''
def callback(r, audio):
    with sr.Microphone() as source2:

        try:
            myText = ""
            #r.adjust_for_ambient_noise(source2)
            text = r.recognize_google(audio)
            #print(text)
            if "jarvis" in text.lower():
                myText += text + ' '
                print("Hello sir")
                while(True):
                    audio = r.listen(source2, None, 15)
                    if timeSilent <= 1:
                        myText += r.recognize_google(audio, language='en-US') + " "
                    else:
                        myText = ""
                        print("Done talking")
                        return
                    print(myText)
        except sr.UnknownValueError:
            pass

stop = r.listen_in_background(sr.Microphone(),callback)
'''
#doesnt work was tired help
def callback(r, audio):
    with sr.Microphone() as source2:

        try:
            myText = ""
            #r.adjust_for_ambient_noise(source2)
            while(timeSilent <= 2):
                audio2 = r.listen(audio)
                text = r.recognize_google(audio)
            #print(text)
                if "jarvis" in text.lower():
                    print("Hello sir")
                    myText += text + ' '
                    print(myText)
        except sr.UnknownValueError:
            pass

stop = r.listen_in_background(sr.Microphone(),callback)

#adjust for ambient noise
def noiseCheck():
    while True:
        with sr.Microphone() as source2:
            time.sleep(60)
            r.adjust_for_ambient_noise(source2)

#check time silent
mic_volume = 0.0
def audio_callback(indata, frames, time_info, status):
    global mic_volume  # round it to 4 decimal places
    volume = np.linalg.norm(indata)  # get the volume (RMS)
    mic_volume = round(volume, 1)
    #print(timeSilent)

stream = sd.InputStream(callback=audio_callback)
stream.start()
startTime=0
restartTime = time.time()
#stop when the bot is thinking.
while True:
    if mic_volume > 0.3:
        restartTime = time.time()
    else:
        startTime = time.time()
        global timeSilent
        timeSilent = round(startTime - restartTime, 1)

    time.sleep(0.1)
    #2.5



#threads to make them run symotaniously
threadSpeech = threading.Thread(target=audio_callback)
threadSilence = threading.Thread(target=callback)
threadNoise = threading.Thread(target=noiseCheck)

#start the treads
threadSpeech.start()
threadSilence.start()
#run gemeni
# To run this code you need to install the following dependencies:
# pip install google-genai
'''
from google import genai
from google.genai import types
import os

def generate():
    client = genai.Client(apiKey)

    contents = [
        types.Content(
            role="model",  # Use "system" role instead of "model" (API update)
            parts=[types.Part(text="You are JARVIS, a witty, polite AI assistant.")],
        ),
        types.Content(
            role="user",
            parts=[types.Part(text="What's the weather like today?")],
        ),
    ]

    config = types.GenerateContentConfig(
        temperature=0.5,         # Balanced creativity & reliability — JARVIS is smart but calm
        top_p=0.9,               # Nucleus sampling for more natural responses
        top_k=40,                # Limits token candidates to top 40 for smoother output
        max_output_tokens=512,   # Max length of response to keep it concise but complete
        response_mime_type="text/plain",  # Plain text output (good for most use cases)
    )

    for chunk in client.models.generate_content_stream(
        model="gemini-2.5-flash-lite-preview-06-17",
        contents=contents,
        config=config,
    ):
        print(chunk.text, end="")

if __name__ == "__main__":
    generate()
'''
