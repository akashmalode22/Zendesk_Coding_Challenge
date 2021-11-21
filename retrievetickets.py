import requests
from requests.auth import HTTPBasicAuth
import errormacros


class RetrieveTickets:
    def getTicketByID(self, ticket_id):

        url = "https://zccakashmalode.zendesk.com/api/v2/tickets/" + ticket_id + ".json"
        user = "amalode@purdue.edu/token"
        pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        return data
