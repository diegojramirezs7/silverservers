import azure.cognitiveservices.speech as speechsdk
import time
import wave
import record
import identification

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "b9744c52527a4a14b36783371ac678de", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)


_endpoint = "voice-recog-ss.cognitiveservices.azure.com"
_subkey = 'b30c8294acd244e2babe4e2d1451018c'

req_handler = identification.RequestHandler(_endpoint, _subkey)

# Creates a recognizer with the given settings
speech_recognizer = speechsdk.SpeechRecognizer(speech_config=speech_config)

print("Say something...")
# Starts speech recognition, and returns after a single utterance is recognized. The end of a
# single utterance is determined by listening for silence at the end or until a maximum of 15
# seconds of audio is processed.  The task returns the recognition text as result. 
# Note: Since recognize_once() returns only a single utterance, it is suitable only for single
# shot recognition like command or query. 
# For long-running multi-utterance recognition, use start_continuous_recognition() instead.

def handler(evt):
	if evt.result.reason == speechsdk.ResultReason.RecognizedSpeech:
		result = evt.result.text.lower().strip(".")
		print(result)
		if result == "register":
			print(evt.result.text)
		elif evt.result.text.lower().strip(".") == "identify":
			print(evt.result.text)

	elif evt.result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized, please try again")
	elif evt.result.reason == speechsdk.ResultReason.Canceled:
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))

speech_recognizer.recognized.connect(handler)
speech_recognizer.start_continuous_recognition()
time.sleep(400)
speech_recognizer.stop_continuous_recognition()

def enroll():
	data = req_handler.create_profile()
	data_dictionary = req_handler.parse_results(data)
	uid = resp_dictionary['identificationProfileId']
	enrollment_resp = req_handler.enroll_user("enroll.wav",uid)
	oid = get_oid(enrollment_resp)
	enrollment_operation = req_handler.get_opertion(oid)
	print(enrollment_operation)
	return uid

def identify(uid):
	try:
		print("enter identify function")
		idetify_resp = req_handler.identify("identify.wav", uid)
		oid = get_oid(identify_resp)
		identify_operation = req_handler.get_opertion(oid)
		print(identify_operation)
	except:
		print("error identifying")

def get_oid(resp):
	operation_url = resp.getheader('Operation-Location')
	index = operation_url.index("operations/")
	oid = operation_url[index + len("operations/"):]
	return oid

#result = speech_recognizer.recognize_once()

# Checks result.
# if result.reason == speechsdk.ResultReason.RecognizedSpeech:
#     print("Recognized: {}".format(result.text))
# elif result.reason == speechsdk.ResultReason.NoMatch:
#     print("No speech could be recognized: {}".format(result.no_match_details))
# elif result.reason == speechsdk.ResultReason.Canceled:
#     cancellation_details = result.cancellation_details
#     print("Speech Recognition canceled: {}".format(cancellation_details.reason))
#     if cancellation_details.reason == speechsdk.CancellationReason.Error:
#         print("Error details: {}".format(cancellation_details.error_details))
