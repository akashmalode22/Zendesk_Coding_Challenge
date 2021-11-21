import requests
from requests.auth import HTTPBasicAuth
import errormacros
import modes
from printer import Printer


class RetrieveTickets:

    number_of_tickets = 0
    last_ticket_shown = 0

    def generateURL(self, url_sublink):
        return (
            "https://zccakashmalode.zendesk.com/api/v2/tickets" + url_sublink + ".json"
        )

    def getCredentials(self):
        user = "amalode@purdue.edu/token"
        pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

        return [user, pwd]

    def getNumberOfTickets(self):
        url = self.generateURL("/count")
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

        url = self.generateURL("/" + ticket_id)
        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        return data

    def getAllTicketsNoPagination(self):

        url = self.generateURL("")
        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        return [data["tickets"], self.number_of_tickets]

    def getTicketsInRange(self, start_id, end_id):

        self.getNumberOfTickets()

        # Store required ticket IDs in an integer list
        ids = []
        for i in range(start_id, end_id + 1):
            ids.append(i)

        # Convert integer list to string list
        ids = [str(id) for id in ids]

        url = ""
        if len(ids) == 1:
            url = self.generateURL("/" + ids[0])
        else:
            url = self.generateURL("/show_many?ids=" + ",".join(ids))

        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        data = response.json()

        if len(ids) == 1:
            return [data["ticket"], end_id - start_id + 1]
        else:
            return [data["tickets"], end_id - start_id + 1]

    def pageTickets(self, mode):

        Printer.displayPaginationMenu()

        # Get user input (menu selection)
        user_input = input("Select an option from the menu above: ")

        if mode.exit(user_input):
            Printer.displayExitMessage()
            exit()

        if user_input == "s":
            mode.changeMode(modes.MODE_SELECTED_TICKET)
            return

        if user_input == "m":
            mode.changeMode(modes.MODE_MAIN_MENU)
            return

        if user_input == "n":

            while mode.CURRENT_MODE == modes.MODE_PAGINATION:

                start_id = self.last_ticket_shown + 1
                end_id = min(self.last_ticket_shown + 25, self.number_of_tickets)

                self.last_ticket_shown = end_id
                [tickets, number_of_tickets] = self.getTicketsInRange(start_id, end_id)
                self.last_ticket_shown = end_id

                Printer.displayAllTicketsInfo(tickets, number_of_tickets)

                Printer.displayPaginationMenu()

                # Get user input (menu selection)
                user_input = input("Select an option from the menu above: ")
