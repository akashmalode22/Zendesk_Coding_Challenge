import requests
from requests.auth import HTTPBasicAuth
import errormacros


class RetrieveTickets:
    def generateURL(self, url_sublink):
        return (
            "https://zccakashmalode.zendesk.com/api/v2/tickets/" + url_sublink + ".json"
        )

    def getCredentials(self):
        user = "amalode@purdue.edu/token"
        pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

        return [user, pwd]

    # def getNumberOfTickets():

    def getTicketByID(self, ticket_id):

        url = self.generateURL(ticket_id)
        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        return data
