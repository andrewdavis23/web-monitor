# source: https://www.geeksforgeeks.org/send-sms-with-rest-using-python/

import requests

url = "https://www.fast2sms.com/dev/bulkV2"

querystring = {
	"authorization": "API_KEY_OF_YOURS",
	"message": "This is test Message sent from \
		Python Script using REST API.",
	"language": "english",
	"route": "q",
	"numbers": "XXXXXXXX98, YYYYYYYY89"}

headers = {
	'cache-control': "no-cache"
}
try:
	response = requests.request("GET", url,
								headers = headers,
								params = querystring)
	
	print("SMS Successfully Sent")
except:
	print("Oops! Something wrong")
