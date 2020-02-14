## Components
### Raspberry Pi Client
#### main services
1. **Speech-To-Text** 
Constantly listening for audio through USB microphone. Python script running in "daemon" mode, converting detected audio to text. Certain commands would trigger actions like "register, identify, verify". This script should only run the speech-to-text method and have some if statements to detect if certain commands are detected. The main python script running on the RPi. 
It calls method on the record.py file and methods on requesthandler.py
2. **Record and Save Audio File**
Python script to rercord a wav file and save it to the local directory. Should be customizable to different durations and filename. This script can be a simple method or a method within a file.
3. **Web Client that sends HTTP requests to Server**
Python script that sends requests to the server running on silverservers for verification and identification. Each request would would contain the recorded .wav file, the keywords spoken and the command (identify, verify, enroll?)

### Web Client -- admin website
#### main services
1. Create, View, Update & Delete users
Only through website forms. 
2. Create, View, Update (add/remove users) & Delete groups
Only through website forms.
3. Enroll users for identification
Website form + wav file ()
4. Enroll users for verification

### Server

#### Python application that implements Flask (web framework)
This application is the main script attached to the server. It listens for the HTTP requests coming from the Raspberry Pi and the Website. It will act as the controller in the MVC architecture. Depending on the requests received from the client it will do the appropriate API calls and DB queries. Then, it will return the necessary information back to the client, depending on the type of UI. 

#### Azure Cognitive Services
**2 main services: Identification and verification**
**accross all scripts, 2 common variables**
- endpoint: https://voice-recog-ss.cognitiveservices.azure.com
- subscription key: b30c8294acd244e2babe4e2d1451018c 

The key and endpoint depend on subscription to Azure and the name of the created resource in Azure. 

##### Identification
1. Create Identification Profile: 
- path after endpoint: /spid/v1.0/identificationProfiles
- HTTP method: POST
- body content-type: application/json
- body content: {"locale":"en-us",}
- response format: json
- response: 
```json
{"identificationProfileId": "49a36324-fc4b-4387-aa06-090cfbf0064f"}
```
2. Create Enrollment
- path after endpoint: /spid/v1.0/identificationProfiles/identificationProfileId/enroll
- HTTP method: POST
- body content-type: binary -- multipart/form-data
- body content: binary represenation of file.wav, only 1 file of 30+ seconds
- response format: empty body, data is in HTTP headers. 
- response: the operation location gives the url where a subsequent HTTP request has to be made
```http
Content-Length: 0
Operation-Location: https://voice-recog-ss.cognitiveservices.azure.com/spid/v1.0/operations/d3ffd28f-751a-4b41-9def-3ba7eab43e7a
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: object-src 'none'; form-action 'self'; frame-ancestors 'none'
apim-request-id: 86cf8006-08fc-4efc-bccd-9a8acaa0b2fa
Date: Thu, 30 Jan 2020 23:12:50 GMT
```

3. Get Profile
- path after endpoint: /spid/v1.0/identificationProfiles/{identificationProfileId}?{params}
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
{"identificationProfileId":"7bd2514a-a19d-4404-95e1-a4488681245e","enrollmentSpeechTime":193.34,"remainingEnrollmentSpeechTime":0.0,"locale":"en-us","createdDateTime":"2020-01-29T22:48:17.007Z","lastActionDateTime":"2020-01-30T23:12:55.818Z","enrollmentStatus":"Enrolled"}
```

4. Get All Profiles
- path after endpoint: /spid/v1.0/identificationProfiles?{params}
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
[{"identificationProfileId":"7bd2514a-a19d-4404-95e1-a4488681245e","enrollmentSpeechTime":193.34,"remainingEnrollmentSpeechTime":0.0,"locale":"en-us","createdDateTime":"2020-01-29T22:48:17.007Z","lastActionDateTime":"2020-01-30T23:12:55.818Z","enrollmentStatus":"Enrolled"},{"identificationProfileId":"88b2c68b-f469-483f-adbe-275ebb5157ed","enrollmentSpeechTime":193.34,"remainingEnrollmentSpeechTime":0.0,"locale":"en-us","createdDateTime":"2020-01-29T20:27:00.265Z","lastActionDateTime":"2020-01-29T22:19:48.788Z","enrollmentStatus":"Enrolled"},{"identificationProfileId":"922028b2-1624-4aac-b7df-851e47b162f2","enrollmentSpeechTime":0.0,"remainingEnrollmentSpeechTime":30.0,"locale":"en-us","createdDateTime":"2020-01-29T22:34:27.423Z","lastActionDateTime":"2020-01-29T22:34:27.423Z","enrollmentStatus":"Enrolling"}]
```

5. Identify User
- path after endpoint: "/spid/v1.0/identify?identificationProfileIds={listOfProfileIds}&{params}"
- HTTP method: POST
- body content-type: binary -- multipart/form-data
- body content: binary represenation of file.wav, only 1 file of 30+ seconds
- response format: empty body, data is in HTTP headers. 
- response: the operation location gives the url where a subsequent HTTP request has to be made
```http
Content-Length: 0
Operation-Location: https://voice-recog-ss.cognitiveservices.azure.com/spid/v1.0/operations/e9048234-126e-4f1e-8918-67732e563b8a
X-Frame-Options: DENY
X-XSS-Protection: 1; mode=block
X-Content-Type-Options: nosniff
Strict-Transport-Security: max-age=31536000; includeSubDomains; preload
Referrer-Policy: strict-origin-when-cross-origin
Content-Security-Policy: object-src 'none'; form-action 'self'; frame-ancestors 'none'
apim-request-id: f1e617ad-2c77-4969-872b-2d41a571ce3c
Date: Thu, 30 Jan 2020 23:47:59 GMT
```

6. Get Operation Results (from Enroll and Identify)
- path after endpoint: /spid/v1.0/operations/{operationId}?{params}
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
{"status":"succeeded","createdDateTime":"2020-01-30T23:47:59.8780883Z","lastActionDateTime":"2020-01-30T23:48:01.9999543Z","processingResult":{"confidence":"High","identifiedProfileId":"7bd2514a-a19d-4404-95e1-a4488681245e"}}
```

##### Verification
1. Create Verification Profile: 
- path after endpoint: /spid/v1.0/verificationProfiles
- HTTP method: POST
- body content-type: application/json
- body content: {"locale":"en-us",}
- response format: json
- response: 
```json
{"verificationProfileId":"d7c62d70-632d-4e3d-af8b-8e5485f56dad"}
```

2. Create Enrollment
- path after endpoint: /spid/v1.0/verificationProfiles/{verificationProfileId}/enroll?{params}
- HTTP method: POST
- body content-type: binary -- multipart/form-data
- body content: binary represenation of file.wav, 15+ seconds. Send request 3 times. 
- response format: empty body, data is in HTTP headers. 
- response: the operation location gives the url where a subsequent HTTP request has to be made
```json
{"enrollmentStatus":"Enrolling","enrollmentsCount":1,"remainingEnrollments":2,"phrase":"be yourself everyone else is already taken"}
```

3. Get Profile
- path after endpoint: /spid/v1.0/verificationProfiles/{verificationProfileId}?{params}
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
{"verificationProfileId":"d7c62d70-632d-4e3d-af8b-8e5485f56dad","enrollmentsCount":3,"remainingEnrollmentsCount":0,"locale":"en-us","createdDateTime":"2020-01-31T00:12:36.560Z","lastActionDateTime":"2020-01-31T18:29:40.565Z","enrollmentStatus":"Enrolled"}
```

4. Get All Profiles
- path after endpoint: /spid/v1.0/verificationProfiles?{params}
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
[{"verificationProfileId":"d7c62d70-632d-4e3d-af8b-8e5485f56dad","enrollmentsCount":3,"remainingEnrollmentsCount":0,"locale":"en-us","createdDateTime":"2020-01-31T00:12:36.560Z","lastActionDateTime":"2020-01-31T18:29:40.565Z","enrollmentStatus":"Enrolled"}]
```

5. verify User
- path after endpoint: /spid/v1.0/identify?identificationProfileIds={listOfProfileIds}&{params}
- HTTP method: POST
- body content-type: binary -- multipart/form-data
- body content: binary represenation of file.wav, only 1 file of 30+ seconds
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
{"confidence":"High","result":"Accept","phrase":"be yourself everyone else is already taken"}
```

6. Get All Supported Phrases
- path after endpoint: /spid/v1.0/verificationPhrases?locale=en-us
- HTTP method: GET
- body content-type: empty
- body content: empty
- response format: json
- response: need to convert to ascii/utf first and then to json object
```json
[{"phrase":"i am going to make him an offer he cannot refuse"},{"phrase":"houston we have had a problem"},{"phrase":"my voice is my passport verify me"},{"phrase":"apple juice tastes funny after toothpaste"},{"phrase":"you can get in without your password"},{"phrase":"you can activate security system now"},{"phrase":"my voice is stronger than passwords"},{"phrase":"my password is not your business"},{"phrase":"my name is unknown to you"},{"phrase":"be yourself everyone else is already taken"}]
```

#### VoiceIt
**2 main services: Identification and verification**
**accross all scripts, 2 common variables**
- subscription key: "key_d79251d085214874b7479cdf67cd40b8"
- token: "tok_3f628df367944320a359510086825836" 
- need to create a VoiceIt2 object to which the key and token as passed as initialization arguments
- all responses are in json format

##### Common methods
1. Create Profile
- method: vi2.create_user()
- specifications: this profile can be used for both identification and authentication
- sample response: 
```json
{"createdAt": 1581662117000, "timeTaken": 0.016, "message": "Created user with userId : usr_e10fcfd25d3c43879a827495d4653293", "userId": "usr_e10fcfd25d3c43879a827495d4653293", "responseCode": "SUCC", "status": 201}
```

2. Get supported phrases
- method: vi2.get_phrases("en-US")
- specifications: one of the returned phrases has to be used for enrollment, verification and identification. Phrases can be added in the voiceit.io website
- sample response:
```json
{"message": "Successfully got all en-CA phrases for account", "phrases": [{"text": "Never forget tomorrow is a new day", "contentLanguage": "en-CA"}, {"text": "Zoos are filled with large and small animals", "contentLanguage": "en-CA"}, {"text": "Remember to wash your hands before eating", "contentLanguage": "en-CA"}, {"text": "Today is a nice day to go for a walk", "contentLanguage": "en-CA"}], "count": 4, "responseCode": "SUCC", "timeTaken": "0.018s", "status": 200} 
```

3. Create Enrollment
- method: vi2.create_voice_enrollment("userid", "en-US", "phrase", "absolute filepath")
- specifications: record the user saying the phrase 3 times and send 3 different requests with their corresponding file. The file has to be fixed length of 5 seconds (wav format)
- sample response:
```json
{"textConfidence": 71.88, "createdAt": 1581663308000, "timeTaken": "1.298s", "contentLanguage": "en-US", "text": "Never forget tomorrow is a new day", "id": 453931, "message": "Successfully enrolled voice for user with userId : usr_e10fcfd25d3c43879a827495d4653293", "responseCode": "SUCC", "status": 201}
```

##### Identification
Identify individual from a group of registered users
1. Create Group
- method: vi2.create_group("description")
- specifications: groups are used to have different types of users
- sample response: 
```json
{"createdAt": 1581665189000, "timeTaken": "0.025s", "groupId": "grp_450e14a5ff3748d0844246aac940de35", "description": "employees", "message": "Created group with groupId : grp_450e14a5ff3748d0844246aac940de35", "responseCode": "SUCC", "status": 201}
```

2. Add user to Group
- method: vi2.add_user_to_group(groupId, userId)
- specifications: can get group and user ids with _get_all_groups()_ _get_all_users()_
- sample_response: 
```json
{"message": "Successfully added user with userId : usr_e10fcfd25d3c43879a827495d4653293 to group with groupId : grp_450e14a5ff3748d0844246aac940de35", "timeTaken": "0.041s", "responseCode": "SUCC", "status": 200}
```

3. Identify
- method: vi2.voice_identification("groupId", "contentLanguage", "phrase", "absolute filepath")
- specifications: there needs to be at least 2 users with 3 enrollments each using the same phrase. 
- sample response:
```json
{"timeTaken": "1.439s", "message": "Failed to identify voice for user in group with groupId : grp_450e14a5ff3748d0844246aac940de35, group does not have enough users with three (3) or more enrollments of the phrase 'Today is a nice day to go for a walk", "responseCode": "PNTE", "status": 400}
```

##### Verification
1. verify
- method: vi2.voice_verification("userId", "en-US", "phrase", "absolute filepath")
- specifications: file has to be fixed length of 5 seconds
- sample response:
```json
{"textConfidence": 59.85, "timeTaken": "2.977s", "confidence": 97.84, "text": "Never forget tomorrow is a new day", "message": "Successfully verified voice for user with userId : usr_e10fcfd25d3c43879a827495d4653293", "responseCode": "SUCC", "status": 200}
```

#### MySQL DB
1. Tables
- user(azure_verification_id, azure_identification_id, voiceit_id)






