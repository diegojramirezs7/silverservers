import speech_recognition as sr
import time
import record
import keyboard
from api_handler import AzureHandler, VoiceitHandler
import sys
from gtts import gTTS 
import os
from text_to_speech import tts
from model import Model

_pkey = "704c3dd99d09405f962d9dfce5719f13"
_endpoint= 'https://voice-recog.cognitiveservices.azure.com/spid/v1.0'

azure = AzureHandler(_endpoint, _pkey)
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")

r = sr.Recognizer()
m = sr.Microphone()
iterations = 3

model = Model("localhost", 'admin', 'silverserver2020', 'voiceauth')

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    os.system("mpg321 ttsfiles/register.mp3") 
    #print("start by saying: register")
    while True:
        with m as source: audio = r.listen(source)

        try:
            # recognize speech using Google Speech Recognition
            print("say something")
            value = r.recognize_google(audio)
            if (value == "register"):
                os.system('mpg321 ttsfiles/record.mp3')
                reg = start_voiceit_registration()
                uid = reg['voiceitUserId']
                phrases = reg['voiceitPhrases']
                voiceit_verification(uid, phrases)
            elif value == 'verify':
                voiceit_verification("grp_bc595294f94341568dc66dd7a09790bc")
            elif value == 'stop':
                sys.exit()
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass
