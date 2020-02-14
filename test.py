import http.client, urllib.request, urllib.parse, urllib.error, base64

def test_request():
	headers = {
    	# Request headers
    	'Content-Type': 'application/json',
	}

	params = urllib.parse.urlencode({
	})

	body = '{"username":"diegojramirezs7", "pw": "mypassword"}'

	try:
		conn = http.client.HTTPConnection("localhost:5000")
		conn.request("POST", "/test", body, headers)
		response = conn.getresponse()
		data = response.read()
		print(data.decode("ascii"))
		conn.close()
		return data
	except Exception as e:
		print(e)


test_request()