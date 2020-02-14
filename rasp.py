import speech_recognition as sr
import record
import http.client, urllib.request, urllib.parse, urllib.error, base64

r = sr.Recognizer()
m = sr.Microphone()

register = [
    'register', 'register user', 'enroll', 'enroll user', 'new user', 
    'create new user', 'add user', 'create user', 'add new user',
]

try:
    print("A moment of silence, please...")
    with m as source: r.adjust_for_ambient_noise(source)
    print("Set minimum energy threshold to {}".format(r.energy_threshold))
    while True:
        print("Say something!")
        with m as source: audio = r.listen(source)
        try:
            value = r.recognize_google(audio)
            if value in register:
                record.record(30, "register.wav")

        except sr.UnknownValueError:
            print("Oops! Didn't catch that")
        except sr.RequestError as e:
            print("Uh oh! Couldn't request results from Google Speech Recognition service; {0}".format(e))
except KeyboardInterrupt:
    pass