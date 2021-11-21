import requests
from requests.auth import HTTPBasicAuth
import errormacros


class RetrieveTickets:

    number_of_tickets = 0

    def generateURL(self, url_sublink):
        return (
            "https://zccakashmalode.zendesk.com/api/v2/tickets/" + url_sublink + ".json"
        )

    def getCredentials(self):
        user = "amalode@purdue.edu/token"
        pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

        return [user, pwd]

    def getNumberOfTickets(self):
        url = self.generateURL("count")
        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        self.number_of_tickets = data["count"]["value"]

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
