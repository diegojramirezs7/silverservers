import speech_recognition as sr
import time
import record
import keyboard
from api_handler import AzureHandler, VoiceitHandler
import sys
from gtts import gTTS 
import os
from text_to_speech import tts

_pkey = "704c3dd99d09405f962d9dfce5719f13"
_endpoint= 'https://voice-recog.cognitiveservices.azure.com/spid/v1.0'

azure = AzureHandler(_endpoint, _pkey)
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")

r = sr.Recognizer()
m = sr.Microphone()
iterations = 3

#handler = identification.requestHandler("voice-recog-ss.cognitiveservices.azure.com",'b30c8294acd244e2babe4e2d1451018c')

#WORK ON IMPLEMENTING IDENTIFICATION.PY.... ENROLL USER

def start_voiceit_registration():
    try:
        voiceit_resp = voiceit.create_user()
        if voiceit_resp['responseCode'] == 'SUCC':
            voiceit_userId = voiceit_resp['userId']

        voiceit_phrases_resp = voiceit.get_supported_phrases()
        if voiceit_phrases_resp['responseCode'] == 'SUCC':
            voiceit_phrases = [x['text'] for x in voiceit_phrases_resp['phrases']]

        resp_dic = {
            'voiceitUserId': voiceit_userId,
            'voiceitPhrases': voiceit_phrases
        }

        return resp_dic
    except Exception as e:
        return "Error: {0}".format(e)

def file_to_text(filename):
    with sr.AudioFile(filename) as source:
        audio = r.record(source)
    
    try:
        s = r.recognize_google(audio)
        return s
    except Exception as e:
        return str(e)

def pretty_list(ls):
    s = ""
    for item in ls:
        s += "\t"+ item +"\n"
    return s

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
                #response = handler.create_profile()
                os.system('mpg321 ttsfiles/record.mp3')
                reg = start_voiceit_registration()
                uid = reg['voiceitUserId']
                phrases = reg['voiceitPhrases']
                print("user id: ", uid)
                
                print("supported phrases: \n", pretty_list(phrases))
            
                count = 1
                while count <= iterations:
                    os.system("mpg321 ttsfiles/countdown.mp3")
                    record.record(5, "test.wav")
                    phrase = file_to_text("test.wav")
                    res = voiceit.enroll_user(uid, phrase, "test.wav")
                    print("response message: ",res['message'])
                    print(phrase)
                    print("")
                    if res['responseCode'] == 'SUCC':
                        tts(res['message'], 'response', count)
                        count += 1
                os.system("mpg321 ttsfiles/EnrollmentSuccess.mp3")
                
            elif value == 'verify':
                print("")
                record.record(5,'identify.wav')
                res = voiceit.verify("usr_0d2f73a90e134498890109f9241624a1", file_to_text("identify.wav"), "identify.wav")
                print(res)
                print("")
            elif value == 'stop':
                sys.exit()
                
        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass


