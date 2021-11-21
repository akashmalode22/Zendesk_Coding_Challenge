import requests
from requests.auth import HTTPBasicAuth

import errormacros


url = "https://zccakashmalode.zendesk.com/api/v2/tickets/2.json"

user = "amalode@purdue.edu/token"
pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

response = requests.get(url, auth=(user, pwd))

if response.status_code != errormacros.GET_SUCCESS_CODE:
    print("Status Code:", response.status_code, "Unable to execute GET request.")
    exit()

data = response.json()

print(data["ticket"]["subject"])
