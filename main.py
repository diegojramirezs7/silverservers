import azure.cognitiveservices.speech as speechsdk
import time
import wave
import record

# Creates an instance of a speech config with specified subscription key and service region.
# Replace with your own subscription key and service region (e.g., "westus").
speech_key, service_region = "b9744c52527a4a14b36783371ac678de", "westus"
speech_config = speechsdk.SpeechConfig(subscription=speech_key, region=service_region)

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
			speech_recognizer.stop_continuous_recognition()
			time.sleep(3)
			print(evt.result.text)
			record.record()
			speech_recognizer.start_continuous_recognition()
		elif evt.result.text.lower().strip(".") == "cup of wine":
			print(evt.result.text)
			print("executing the second command")
	elif evt.result.reason == speechsdk.ResultReason.NoMatch:
		print("No speech could be recognized, please try again")
	elif evt.result.reason == speechsdk.ResultReason.Canceled:
		print("Speech Recognition canceled: {}".format(cancellation_details.reason))

speech_recognizer.recognized.connect(handler)
speech_recognizer.start_continuous_recognition()
time.sleep(30)
speech_recognizer.stop_continuous_recognition()

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
