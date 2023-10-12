# This code sample uses the 'requests' library:
# http://docs.python-requests.org
import requests
from requests.auth import HTTPBasicAuth
import json

url = "https://fyi.atlassian.net/rest/api/3/mypermissions"

auth = HTTPBasicAuth("fyiqaintern@gmail.com", "PHgDUqOBMz7IZKm6WCyPyNmKLEmCBebSi4VIIQZU>")

headers = {
  "Accept": "application/json"
}

query = {
  'permissions': 'BROWSE_PROJECTS,EDIT_ISSUES'
}

response = requests.request(
   "GET",
   url,
   headers=headers,
   params=query,
   auth=auth
)

print(json.dumps(json.loads(response.text), sort_keys=True, indent=4, separators=(",", ": ")))