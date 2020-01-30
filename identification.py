import http.client, urllib.request, urllib.parse, urllib.error, base64
import io
import json

endpoint = "voice-recog-ss.cognitiveservices.azure.com"
pkey = 'b30c8294acd244e2babe4e2d1451018c'

class RequestHandler:
	def __init__(self, endpoint, subkey):
		self.endpoint = endpoint
		self.subkey = subkey

	def enroll_user(self):
		headers = {
		    # Request headers
		    'Content-Type': 'multipart/form-data',
		    'Ocp-Apim-Subscription-Key': pkey,
		}

		try:
			with open("output.wav", "rb") as f:
				b = f.read()
			
			conn = http.client.HTTPSConnection(endpoint)
			conn.request("POST", "/spid/v1.0/identificationProfiles/7bd2514a-a19d-4404-95e1-a4488681245e/enroll", b, headers)
			response = conn.getresponse()
			data = response.read()
			print(response.msg)
			conn.close()
		except Exception as e:
			#print("[Errno {0}] {1}".format(e.errno, e.strerror))
			print("some error")

	def get_profile(self):
		headers = {
		    # Request headers
		    'Ocp-Apim-Subscription-Key': pkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(endpoint)
		    conn.request("GET", "/spid/v1.0/identificationProfiles/7bd2514a-a19d-4404-95e1-a4488681245e?%s" % params, "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	def get_all_profiles(self):
		headers = {
	    	# Request headers
	    	'Ocp-Apim-Subscription-Key': pkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(endpoint)
		    conn.request("GET", "/spid/v1.0/identificationProfiles?%s" % params, "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    #print(data)
		    conn.close()
		    return data
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	def identify(self):
		"""returns URL with operationId, 
		a subsequent HTTP GET request has to be made to that url with that operationId
		to get the results of any given identify operations
		a list of profileIds has to be send as params and the chosen one will be returned or None
		"""
		headers = {
		    # Request headers
		    'Content-Type': 'multipart/form-data',
		    'Ocp-Apim-Subscription-Key': pkey,
		}

		params = urllib.parse.urlencode({
		})

		with open("output.wav", "rb") as f:
			b = f.read()

		try:
		    conn = http.client.HTTPSConnection(endpoint)
		    conn.request("POST", "/spid/v1.0/identify?identificationProfileIds=7bd2514a-a19d-4404-95e1-a4488681245e&%s" % params, b, headers)
		    response = conn.getresponse()
		    print(response.msg)
		    #data = response.read()
		    #print(data)
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	def validate(self):
		"""needs to send profileId of individual user 
		request returns accept/reject, confidence level and detected phrase
		"""
		headers = {
    		# Request headers
    		'Content-Type': 'multipart/form-data',
    		'Ocp-Apim-Subscription-Key': pkey,
		}

		params = urllib.parse.urlencode({
		})

		with open("output.wav", "rb") as f:
			b = f.read()

		try:
		    conn = http.client.HTTPSConnection(endpoint)
		    conn.request("POST", "/spid/v1.0/verify?verificationProfileId={verificationProfileId}&%s" % params, b , headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))


	def get_status(self):
		"""returns cofidence level and profileId of user in json format for identify operations
		returns confidence level for preselected user in json format. 
		"""
		headers = {
		    # Request headers
		    'Ocp-Apim-Subscription-Key': pkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(endpoint)
		    conn.request("GET", "/spid/v1.0/operations/fb1214f6-bfc2-4428-8afc-6d12cb56ee31?%s" % params, "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))


	def parse_results(self):
		res = get_all_profiles().decode("ascii")
		o = json.loads(res)
		for item in o:
			print(item)

class User:
	def __init__(self, profileId, enrollmentSpeechTime = None, 
		locale="en-us", created=None, lastAction=None, enrollmentStatus = None)
		self.profileId = profileId
		self.enrollmentSpeechTime = enrollmentSpeechTime
		self.locale = locale
		self.created = created
		self.lastAction = lastAction
		self.enrollmentStatus = enrollmentStatus



#https://voice-recog-ss.cognitiveservices.azure.com/spid/v1.0/operations/057922d5-3341-44b0-84e0-b8c8ff898db9



