## Components
#### Raspberry Pi Client
#### Web Client -- admin website
#### Server
#### MySQL DB 

## Azure Cognitive Services

#### 2 main services: Identification and verification
**accross all scripts, 2 common variables**
- endpoint: https://voice-recog-ss.cognitiveservices.azure.com
- subscription key: b30c8294acd244e2babe4e2d1451018c 

The key and endpoint depend on subscription to Azure and the name of the created resource in Azure. 

#### Identification
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

#### Verification
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



