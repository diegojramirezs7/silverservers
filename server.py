from flask import Flask, render_template, request, make_response, redirect, url_for
app = Flask(__name__)
from playsound import playsound
from api_handler import AzureHandler, VoiceitHandler
import json
import speech_recognition as sr
from model import Model

r = sr.Recognizer()

_pkey = "704c3dd99d09405f962d9dfce5719f13"
_endpoint= 'voice-recog.cognitiveservices.azure.com'

azure = AzureHandler(_endpoint, _pkey)
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")
model = Model("localhost", 'root', 'Mysql_pw1?', 'silverservers')

@app.route("/", methods=['POST', 'GET'])
def index():
	if request.method == 'GET':
		return render_template("index.html")
	else:
		return ""

def start_registration():
	try:
		voiceit = start_voiceit_registration()
		azure_resp = start_azure_registration()

		values = {
			'voiceitUserId': voiceit['voiceitUserId'],
			'voiceitPhrases': voiceit['voiceitPhrases'],
			'azureIdentificationUserId': azure_resp['azureIdenProfileId'],
			'azureVerificationUserId': azure_resp['azureVerProfileId'],
			'azurePhrases': azure_resp['azurePhrases']
		}

		r = model.save_user(values.voiceitUserId, values.azureVerificationUserId ,values.azureIdentificationUserId)
		print(r)
	except Exception as e:
		return "the error is {0}".format(e)

def file_to_text(path):
	with sr.AudioFile(path) as source:
		audio = r.record(source)

	try:
		text = r.recognize_google(audio)
		return text
	except Exception as e:
		return str(e)

def remove_id(message):
	if 'usr_' in message:
		position = msg.index('usr_')
		uid = message[position: position + 36]
		st = message.replace(uid, "")
	elif 'grp_' in message:
		position = msg.index('grp_')
		gid = message[position: position + 36]
		st = message.replace(gid, "")
	else:
		st = message

	return st
		
#azure 
@app.route("/enroll", methods=['POST', 'GET'])
def enroll():
	if request.method == 'GET':
		return render_template("enroll.html", dic = "")
	elif request.method == 'POST':
		#d = request.form()
		command = request.form.get('command')
		fullname = request.form.get('fullname')
		empNo = request.form.get('employeeNo')

		if command == 'start_registration':
			voiceit_dic = start_voiceit_registration()
			resp_dic = {
				'fullname': fullname,
				'empNo': empNo,
				'voiceitUserId': voiceit_dic['voiceitUserId'],
				'voiceitPhrases': voiceit_dic['voiceitPhrases']
			}
			return render_template("registration.html", dic = resp_dic)
		elif command == 'file_sent':
			f = request.files['audio_data']
			uid = request.form.get('uid');
			path = "/Users/diego_ramirezs/documents/flaskapp/audio_files/{0}.wav".format(uid)
			f.save(path)
			phrase = file_to_text(path)
			print(uid)
			print(phrase)
			response = voiceit.enroll_user(uid, phrase, path)
			return response['message']

		return ""

@app.route("/users", methods = ['POST', 'GET'])
def get_users():
	pass


@app.route("/start_voiceit_registration", methods = ['POST', 'GET'])
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

		req = request.get_json()
		name = req.get('name')

		model.save_user(name = name, voiceit_id = voiceit_userId)
    	model.add_user_to_group(voiceit_userId, groupId = 1)

		return resp_dic
	except Exception as e:
		return "Error: {0}".format(e)


@app.route("/voiceit_enrollment", methods=['POST', 'GET'])
def voiceit_enrollment():
	try:
		if request.method == 'POST':
			phrase = request.headers.get('phrase')
			filename = request.headers.get('filename')
			uid = request.headers.get('userId')
			file_path = "/Users/diego_ramirezs/documents/flaskapp/audio_files/"+filename+".wav"
			
			f = request.files[filename]
			f.save(file_path)
			db_tuple = model.get_user(uid)
			name = db_tuple[1]
			
			res = voiceit.enroll_user(uid, phrase, file_path)
			if res['responseCode'] == 'SUCC':
				response_dic = {
					'responseCode': res['responseCode'],
					'message': 'Successfully enrolled user',
					'name': name
				}
			else:
				message = res['message']
				st = remove_id(message)

				response_dic = {
					'responseCode': res['responseCode'],
					'message': st
				}
			return response_dic
		else:
			return "Invalid HTTP method"
	except Exception as e:
		return str(e)

@app_route('/voiceit_identify', methods=['POST', 'GET'])
def voiceit_identify():
	try:
		if request.method == 'POST':
			phrase = request.headers.get('phrase')
			filename = request.headers.get('filename')
			groupId = request.headers.get('groupId')
			file_path = "/Users/diego_ramirezs/documents/flaskapp/audio_files/"+filename+".wav"

			f = request.files[filename]
			f.save(file_path)

			identification_response = voiceit.identify(groupId, phrase, file_path)
			responseCode = identification_response.get('responseCode')
			if responseCode == 'SUCC':
				userId = identification_response.get('userId')
				message = identification_response.get('message')
				clean_message = remove_id(messsage)
				confidence = identification_response.get('confidence')

				db_tuple = model.get_user(userId)
				if db_tuple:
					name = db_tuple[1]
				else:
					name = ''

				response_dic = {
					'responseCode': responseCode,
					'userId': userId,
					'message': clean_message,
					'username': name,
					'confidence': confidence
				}
				return response_dic
			else:
				message = identification_response.get('message')
				clean_message = remove_id(message)
				response_dic = {
					'responseCode': responseCode,
					'message': clean_message,
				}
				return response_dic
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)


@app.route("/voiceit_verify", methods=['POST', 'GET'])
def verify():
	try:
		if request.method == 'POST':
			phrase = request.headers.get('phrase')
			filename = request.headers.get('filename')
			userId = request.headers.get('userId')
			file_path = "/Users/diego_ramirezs/documents/flaskapp/audio_files/"+filename+".wav"

			f = request.files[filename]
			f.save(file_path)

			verification_response = voiceit.verify(userId, phrase, file_path)
			responseCode = verification_response.get('responseCode')
			if responseCode == 'SUCC':
				confidence = verification_response.get('confidence')
				message = verification_response.get('message')
				clean_message = remove_id(message)
				response_dic = {
					'responseCode': responseCode,
					'message': clean_message,
					'confidence': confidence,
				}
				return response_dic
			else:
				message = verification_response.get('message')
				clean_message = remove_id(message)
				response_dic = {
					'responseCode': responseCode,
					'message': clean_message,
				}
				return response_dic
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)


@app.route("/start_azure_registration", methods=['POST', 'GET'])
def start_azure_registration():
	try:
		azure_resp = azure.create_identification_profile()
		azure_resp = parse_results(azure_resp)	
		azureIdenProfileId = azure_resp['identificationProfileId']
		
		azure_resp = azure.create_verification_profile()
		azure_resp = parse_results(azure_resp)
		azureVerProfileId = azure_resp['verificationProfileId']
		
		azure_phrases_resp = azure.get_verification_phrases()
		azure_phrases_resp = parse_results(azure_phrases_resp)
		azure_phrases = [x['phrase'] for x in azure_phrases_resp]

		resp_dic = {
			'azureIdenProfileId': azureIdenProfileId,
			'azureVerProfileId': azureVerProfileId,
			'azurePhrases': azure_phrases
		}

		return resp_dic
	except Exception as e:
		return "Error: {0}".format(e)


## ############################### TODO #####################################################
@app.route("/azure_identification_enrollment", methods=['POST', 'GET'])
def azure_identification_enrollment():
	try:
		if request.method == 'POST':
			userId = request.headers.get('identificationId')
			filename = request.headers.get('filename')
			file_path = "/Users/diego_ramirezs/documents/flaskapp/audio_files/"+filename+".wav"
			
			f = request.files[filename]
			f.save(file_path)
			
			identification_response = azure.enroll_identification_user(file_path, userId)
			
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)

@app.route("/azure_verification_enrollment", methods=['POST', 'GET'])
def azure_verification_enrollment():
	try:
		if request.method == 'POST':
			pass
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)


@app.route("/azure_identification", methods=['POST', 'GET'])
def azure_identification():
	try:
		if request.method == 'POST':
			pass
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)


@app.route("/azure_verification", methods=['POST', 'GET'])
def azure_verification():
	try:
		if request.method == 'POST':
			pass
		else:
			return "Incorrect HTTP method"
	except Exception as e:
		print(str(e))
		return str(e)

def get_azure_operation(operationId):
	pass

def parse_results(resp):
	return json.loads(resp.decode("ascii"))

if __name__ == "__main__":
	app.run()
