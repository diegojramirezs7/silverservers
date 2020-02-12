import verification
import identification
import record

req_handler = identification.RequestHandler("voice-recog-ss.cognitiveservices.azure.com", 'b30c8294acd244e2babe4e2d1451018c')

def enroll():
	data = req_handler.create_profile()
	data_dictionary = req_handler.parse_results(data)
	uid = data_dictionary['identificationProfileId']
	record.record(30, "enroll.wav")
	enrollment_resp = req_handler.enroll_user("enroll.wav", uid)
	oid = get_oid(enrollment_resp)
	enrollment_operation = req_handler.get_operation(oid)
	print(enrollment_operation)
	return uid

def identify(uid):
	record.record(30, "identify.wav")
	idetify_resp = req_handler.identify("identify.wav", uid)
	oid = get_oid(identify_resp)
	identify_operation = req_handler.get_opertion(oid)
	print(identify_operation)
	
def get_oid(resp):
	operation_url = resp.getheader('Operation-Location')
	index = operation_url.index("operations/")
	oid = operation_url[index + len("operations/"):]
	return oid