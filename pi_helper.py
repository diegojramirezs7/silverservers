from pi_model import Model
#from speak import speak
from api_handler import AzureHandler, VoiceitHandler
import record
import speech_recognition as sr
from text_to_speech import tts
import os

model = Model("localhost", 'root', 'Mysql_pw1?', 'silverservers')
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")
r = sr.Recognizer()
m = sr.Microphone()

talkback = {
    'countdown': "Please say the selected phrase, starting recording in 3 ... 2 ... 1. ... Go. ",
    'startedRegistration': "Started registration process",
    'startedVerification': "started verification process"
}

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


def voiceit_enrollment(uid, phrases):
    iterations = 3
    audio_length = 5
    tts("please say your name", 'name')
    os.system("mpg321 ttsfiles/name.mp3")
    record.record(audio_length, "name.wav")
    name = file_to_text("name.wav")
    print(name)
    model.save_user(name = name, voiceit_id = uid)
    model.add_user_to_group(uid, groupId = 1)
    voiceit.add_user_to_group("grp_bc595294f94341568dc66dd7a09790bc", uid)
    print("user id: ", uid)
    print("supported phrases: \n", pretty_list(phrases))
    count = 1
    while count <= iterations:
        #speak("Please say the selected phrase, starting recording in 3 ... 2 ... 1. ... Go. ")
        os.system("mpg321 ttsfiles/countdown.mp3")
        record.record(audio_length, "test.wav")
        phrase = file_to_text("test.wav")
        res = voiceit.enroll_user(uid, phrase, "test.wav")
        print("response message: ",res['message'])
        print(phrase)
        print("")
        if res['responseCode'] == 'SUCC':
            st = "attempt {0} of enrollment successful".format(count)
            tts(st, 'response')
            count += 1
        else:
            msg = res['message']
            if 'grp_' in msg:
                position = msg.index("grp_")
                gid = msg[position: position+36]
                st = msg.replace(gid, "")
            else:
                st = msg
            tts(st, 'response')
        os.system("mpg321 ttsfiles/response.mp3")

    os.system("mpg321 ttsfiles/EnrollmentSuccess.mp3")


def voiceit_verification(groupId):
    audio_length = 5
    try:
        tts('started verification process', 'startedVerification')
        os.system('mpg321 ttsfiles/startedVerification')
        os.system("mpg321 ttsfiles/countdown.mp3")
        
        record.record(audio_length, "verify.wav")
        phrase = file_to_text("verify.wav")
        identification_response = voiceit.identify(groupId, phrase, 'verify.wav')
        if identification_response['responseCode'] == 'SUCC':
            print(identification_response)
            uid = identification_response['userId']
            db_response = model.get_user(uid)
            if len(db_response) > 1:
                name = db_response[1]
                s = "First step completed, {0} was successfully identified. Please wait for the complete verification".format(name)
            else:
                s = "First step completed, user was successfully identified. Please wait for the complete verification"
            
            tts(s, 'response')
            os.system('mpg321 ttsfiles/response.mp3')
            verification_response = voiceit.verify(uid, phrase, 'verify.wav')
            if verification_response['responseCode'] == 'SUCC':
                print(reverification_responsesp)
                confidence = verification_response['confidence']
                st = "successfully verified user with confidence: {0}".format(confidence) 
                tts(st, 'response')
            else:
                st = reverification_responsesp['message']

            os.system('mpg321 ttsfiles/response.mp3')
        else:
            s = identification_response['message']
            tts()
    except Exception as e:
        return str(e)


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