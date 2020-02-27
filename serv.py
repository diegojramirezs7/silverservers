from flask import Flask, render_template, request, make_response, redirect
app = Flask(__name__)
from playsound import playsound
from api_handler import AzureHandler, VoiceitHandler
import json

_pkey = "704c3dd99d09405f962d9dfce5719f13"
_endpoint= 'https://voice-recog.cognitiveservices.azure.com/spid/v1.0'

azure = AzureHandler(_endpoint, _pkey)
voiceit = VoiceitHandler("key_d79251d085214874b7479cdf67cd40b8", "tok_3f628df367944320a359510086825836")

@app.route("/")
def index():
	return render_template("index.html")

def start_registration():
	try:
		voiceit = start_voiceit_registration()
		azure_resp = start_azure_registration()

		response_dict = {
			'voiceitUserId': voiceit,
			'voiceitPhrases': voiceit_phrases,
			'azureIdentificationUserId': azureIdenProfileId,
			'azureVerificationUserId': azureVerProfileId,
			'azurePhrases': azure_phrases
		}
		if request.method == 'GET':
			return json.dumps(response_dict)
		else:
			return redirect("enroll", code = 302, Response = response_dict)
	except Exception as e:
		return "the error is {0}".format(e)

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

		return "some string"
	

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


@app.route("/enroll_verification", methods=['POST', 'GET'])
def enroll_verification():
	return render_template("enroll_verification.html")

@app.route("/test", methods=['POST', 'GET'])
def test():
	return "aqui tamos"

def parse_results(resp):
	return json.loads(resp.decode("ascii"))

if __name__ == "__main__":
	app.run()
