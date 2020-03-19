from pi_model import Model
from speak import speak
from api_handler import AzureHandler, VoiceitHandler
import record
import speech_recognition as sr
from request_handler import general_request, file_request

model = Model("localhost", 'root', 'Mysql_pw1?', 'silverservers')
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")
r = sr.Recognizer()
m = sr.Microphone()

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

def start_voiceit_registration():
    try:
        askname_filename = 'askname'
        audio_length = 5
        
        # ask for name and convert speech input to text
        tts("please say your name", askname_filename)
        askname_cmd = 'mpg321 ttsfiles/{}.mp3'.format(askname_filename)
        os.system(askname_cmd)
        record.record(audio_length, "name.wav")
        name = file_to_text("name.wav")

        # send request to local server 
        path = '/start_voiceit_registration'
        method = 'POST'
        body = "{'name':'{0}',}".format(name)
        response = general_request(path, method, body)
        return response
    except Exception as e:
        return str(e)

def voiceit_enrollment(uid, phrases):
    try:
        iterations = 3
        audio_length = 5
        enrollment_filename = 'enrollment.wav'
        response_filename = 'voiceit_enrollment_response'
        
        print("supported phrases: \n", pretty_list(phrases))

        count = 1
        path = '/voiceit_enrollment'
        filename = enrollment_filename
        method = 'POST'
        
        # 3 enrollments required for this API, keep trying until 3 successful enrollments are made
        while count <= iterations:
            os.system("mpg321 ttsfiles/countdown.mp3")
            record.record(audio_length, enrollment_filename)
            phrase = file_to_text(enrollment_filename)
            params = {
                'phrase': phrase,
                'filename': filename,
                'userId': uid
            }
            
            #send request to local server (middleware)
            enrollment_response = file_request("/voiceit_enrollment", filename, params = params)
            enrollment_response_code = enrollment_response.get('responseCode')
            
            # if enrollment attempt is successful, provide user feedback and increment count
            if enrollment_response_code == 'SUCC':
                count += 1
                text = "attempt {0} of enrollment successful".format(count)
                tts(text, response_filename)
            else:
                tts(r['message'], response_filename)

            enrollment_cmd = 'mpg321 ttsfiles/{}.mp3'.format(response_filename)
            os.system(enrollment_cmd)

        os.system("mpg321 ttsfiles/EnrollmentSuccess.mp3")
        return enrollment_response
    except Exception as e:
        print(str(e))
        return str(e)

def voiceit_verification(groupId):
    try:
        # identification process 
        verification_filename = 'verify.wav'
        identification_response_filename = 'identification_response'
        audio_length = 5
        verification_response_filename = 'verification_response'

        os.system("mpg321 ttsfiles/startedVerification.mp3")
        os.system("mpg321 ttsfiles/countdown.mp3")
        record.record(audio_length, verification_filename)
        phrase = file_to_text(verification_filename)
        params = {
            'phrase': phrase,
            'filename': verification_filename,
            'groupId': groupId
        }

        identification_response = file_request('/voiceit_identification', verification_filename, params)
        responseCode = res.get('responseCode')
        
        # if identification is successful proceed to verification using the recorded file
        # and the userId returned in the response to identification
        if responseCode == 'SUCC':
            print(res)
            uid = res.get('userId')
            name = res.get('username')
            
            # if the name of the user is available, use that name. Otherwise, just say user
            if name:
                s = "First step completed, {0} was successfully identified. Please wait for the complete verification".format(name)
            else:
                s = "First step completed, user was successfully identified. Please wait for the complete verification"
            
            tts(s, identification_response_filename)
            identification_cmd = 'mpg321 ttsfiles/{}.mp3'.format(identification_response_filename)
            os.system(identification_cmd)
            
            params = {
                'phrase': phrase,
                'filename': verification_filename, 
                'userId': uid
            }

            verification_response = file_request('/voiceit_verification', verification_filename, params)
            verification_response_code = verification_response.get('responseCode')
            if verification_response_code == 'SUCC':
                confidence = verification_response.get('confidence')
                st = "successfully verified user with confidence: {0}".format(confidence) 
            else:
                st = verification_response.get('message')
            
            print(verification_response)
            tts(st, verification_response_filename)
            verification_cmd = 'mpg321 ttsfiles/{}.mp3'.format(verification_response_filename) 
            os.system(verification_cmd)
            return verification_response
        else:
            st = identification_response.get("message")
            tts(st, identification_response_filename)
            identification_cmd = 'mpg321 ttsfiles/{}.mp3'.format(identification_response_filename)
            os.system(identification_cmd)
            return identification_response
    except Exception as e:
        print(str(e))
        return str(e)

def start_azure_registration():
    pass

def azure_enrollment():
    pass

def azure_verification():
    pass

