import http.client, urllib.request, urllib.parse, urllib.error, base64

_endpoint = "voice-recog-ss.cognitiveservices.azure.com"
_pkey = 'b30c8294acd244e2babe4e2d1451018c'

class RequestHandler:
    def __init__(self, subkey, endpoint):
        self.subkey = subkey
        self.endpoint = endpoint

    def create_profile(self):
        headers = {
            # Request headers
            'Content-Type': 'application/json',
            'Ocp-Apim-Subscription-Key': self.subkey,
        }

        body = '{"locale":"en-us",}'

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection(self.endpoint)
            conn.request("POST", "/spid/v1.0/verificationProfiles?{}".format(params), body, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return response
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def enroll_user(self, profileId):
        """needs to be done 3 times with predefined phrase"""
        headers = {
            # Request headers
            'Content-Type': 'multipart/form-data',
            'Ocp-Apim-Subscription-Key': self.subkey,
        }

        params = urllib.parse.urlencode({
        })

        with open("test.wav", "rb") as f:
            b = f.read()

        try:
            conn = http.client.HTTPSConnection(self.endpoint)
            conn.request("POST", "/spid/v1.0/verificationProfiles/{0}/enroll?{1}".format(profileId, params), b, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return response
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def get_profile(self, profileId):

        headers = {
            # Request headers
            'Ocp-Apim-Subscription-Key': self.subkey,
        }

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection(self.endpoint)
            conn.request("GET", "/spid/v1.0/verificationProfiles/{0}?{1}s".format(profileId, params) , "", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return response
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
            conn.request("GET", "/spid/v1.0/verificationProfiles?{0}".format(params), "", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))

    def validate(self, profileId):
        """needs to send profileId of individual user 
        request returns accept/reject, confidence level and detected phrase
        """
        headers = {
            # Request headers
            'Content-Type': 'application/octet-stream',
            'Ocp-Apim-Subscription-Key': self.subkey,
        }

        params = urllib.parse.urlencode({
        })

        with open("test.wav", "rb") as f:
            b = f.read()

        try:
            conn = http.client.HTTPSConnection(self.endpoint)
            conn.request("POST", "/spid/v1.0/verify?verificationProfileId={0}&{1}".format(profileId, params), b, headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return response
        except Exception as e:
            print("[Errno {0}] {1}".format(e.errno, e.strerror))


    def get_supported_phrases(self):
        headers = {
            'Ocp-Apim-Subscription-Key': self.subkey,
        }   

        params = urllib.parse.urlencode({
        })

        try:
            conn = http.client.HTTPSConnection(self.endpoint)
            conn.request("GET", "/spid/v1.0/verificationPhrases?locale=en-us", "", headers)
            response = conn.getresponse()
            data = response.read()
            print(data)
            conn.close()
            return response
        except Exception as e:
            print(e)


handler = RequestHandler(endpoint=_endpoint, subkey = _pkey)
prid = "d7c62d70-632d-4e3d-af8b-8e5485f56dad"
res = handler.get_supported_phrases()
print(res.msg)





