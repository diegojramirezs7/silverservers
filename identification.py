import http.client, urllib.request, urllib.parse, urllib.error, base64
import io
import json

_endpoint = "voice-recog-ss.cognitiveservices.azure.com"
_pkey = 'b30c8294acd244e2babe4e2d1451018c'

class RequestHandler:
	def __init__(self, endpoint, subkey):
		self.endpoint = endpoint
		self.subkey = subkey

	def create_profile(self):
		headers = {
    		# Request headers
    		'Content-Type': 'application/json',
    		'Ocp-Apim-Subscription-Key': self.subkey,
		}

		params = urllib.parse.urlencode({
		})

		body = '{"locale":"en-us",}'

		try:
			conn = http.client.HTTPSConnection(self.endpoint)
			conn.request("POST", "/spid/v1.0/identificationProfiles?%s" % params, body, headers)
			response = conn.getresponse()
			data = response.read()
			print(data)
			conn.close()
			return data
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	def enroll_user(self, filename, profileId):
		headers = {
		    # Request headers
		    'Content-Type': 'multipart/form-data',
		    'Ocp-Apim-Subscription-Key': self.subkey,
		}

		try:
			with open(filename, "rb") as f:
				b = f.read()
			
			conn = http.client.HTTPSConnection(self.endpoint)
			conn.request("POST", "/spid/v1.0/identificationProfiles/{0}/enroll".format(profileId), b, headers)
			response = conn.getresponse()
			data = response.read()
			print(data)
			conn.close()
			return response
		except Exception as e:
			print(e)

	def get_profile(self, profileId):
		headers = {
		    # Request headers
		    'Ocp-Apim-Subscription-Key': self.subkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(self.endpoint)
		    conn.request("GET", "/spid/v1.0/identificationProfiles/{0}?{1}s".format(profileId, params), "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		    return data
		except Exception as e:
		    print("[Errno {0}] {1}".format(e.errno, e.strerror))

	def get_all_profiles(self):
		headers = {
	    	# Request headers
	    	'Ocp-Apim-Subscription-Key': self.subkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(self.endpoint)
		    conn.request("GET", "/spid/v1.0/identificationProfiles?{0}".format(params), "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    #print(data)
		    conn.close()
		    return data
		except Exception as e:
		    print("Error getting all profiles")

	def identify(self, filename, pids):
		"""returns URL with operationId, 
		a subsequent HTTP GET request has to be made to that url with that operationId
		to get the results of any given identify operations
		a list of profileIds has to be send as params and the chosen one will be returned or None
		"""
		headers = {
		    # Request headers
		    'Content-Type': 'application/octet-stream',
		    'Ocp-Apim-Subscription-Key': self.subkey,
		}

		params = urllib.parse.urlencode({
			"shortAudio": True
		})

		with open(filename, "rb") as f:
			b = f.read()

		try:
		    conn = http.client.HTTPSConnection(self.endpoint)
		    conn.request("POST", "/spid/v1.0/identify?identificationProfileIds={0}&{1}".format(pids, params), b, headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		    return response
		except Exception as e:
		    print("error identifying user")


	def get_operation(self, operationId):
		"""returns cofidence level and profileId of user in json format for identify operations
		returns confidence level for preselected user in json format. 
		"""
		headers = {
		    # Request headers
		    'Ocp-Apim-Subscription-Key': self.subkey,
		}

		params = urllib.parse.urlencode({
		})

		try:
		    conn = http.client.HTTPSConnection(self.endpoint)
		    conn.request("GET", "/spid/v1.0/operations/{0}?{1}".format(operationId,params), "", headers)
		    response = conn.getresponse()
		    data = response.read()
		    print(data)
		    conn.close()
		    return data
		except Exception as e:
		    print("error getting operation")

	def parse_results(self, data):
		return json.loads(data.decode("ascii"))

#handler = RequestHandler(endpoint=_endpoint, subkey = _pkey)

# oid = "e9048234-126e-4f1e-8918-67732e563b8a"
# filename = "output.wav"

# handler.get_operation(oid)

# class User:
# 	def __init__(self, profileId, enrollmentSpeechTime = None, 
# 			locale="en-us", created=None, lastAction=None, enrollmentStatus = None)
# 		self.profileId = profileId
# 		self.enrollmentSpeechTime = enrollmentSpeechTime
# 		self.locale = locale
# 		self.created = created
# 		self.lastAction = lastAction
# 		self.enrollmentStatus = enrollmentStatus

#https://voice-recog-ss.cognitiveservices.azure.com/spid/v1.0/operations/057922d5-3341-44b0-84e0-b8c8ff898db9



