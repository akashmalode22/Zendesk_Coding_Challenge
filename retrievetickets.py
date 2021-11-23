import requests
from requests.auth import HTTPBasicAuth
import errormacros
import modes
from printer import Printer


class RetrieveTickets:

    number_of_tickets = 0
    last_ticket_shown = 0

    start_id = 0
    end_id = 0

    def generateURL(self, url_sublink):
        return (
            "https://zccakashmalode.zendesk.com/api/v2/tickets" + url_sublink + ".json"
        )

    def getCredentials(self):
        user = "amalode@purdue.edu/token"
        pwd = "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1"

        return [user, pwd]

    def getResponseFromServer(self, url):
        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != 200:
            print(
                "Status Code:", response.status_code, "Unable to execute GET request."
            )
            exit()

        return response.json()

    def getNumberOfTickets(self):
        url = self.generateURL("/count")

        data = self.getResponseFromServer(url)

        self.number_of_tickets = data["count"]["value"]

    def getTicketByID(self, ticket_id):

        url = self.generateURL("/" + ticket_id)

        data = self.getResponseFromServer(url)

        return data

    def getAllTicketsNoPagination(self):

        url = self.generateURL("")

        data = self.getResponseFromServer(url)

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

        data = self.getResponseFromServer(url)

        if len(ids) == 1:
            return [data["ticket"], end_id - start_id + 1]
        else:
            return [data["tickets"], end_id - start_id + 1]

    def pageTickets(self, mode):

        while mode.CURRENT_MODE == modes.MODE_PAGINATION:

            Printer.displayPaginationMenu()

            # Get user input (menu selection)
            user_input = input("Select an option from the menu above: ")

            if mode.exit(user_input):
                Printer.displayExitMessage()
                exit()

            elif user_input == "s":

                # Get user input for ticket number
                user_input_ticket_number = input("Enter a ticket number: ")

                # Get ticket data from server, store in variable
                ticket = self.getTicketByID(user_input_ticket_number)

                # Display ticket information
                Printer.displayTicketInfo(ticket)

                continue

            elif user_input == "m":
                mode.changeMode(modes.MODE_MAIN_MENU)
                return

            elif user_input == "n":

                self.start_id = self.last_ticket_shown + 1
                self.end_id = min(self.last_ticket_shown + 25, self.number_of_tickets)

                [tickets, number_of_tickets] = self.getTicketsInRange(
                    self.start_id, self.end_id
                )
                self.last_ticket_shown = self.end_id

                Printer.displayAllTicketsInfo(tickets, number_of_tickets)

            elif user_input == "p":

                self.start_id = self.start_id - 25

                if self.end_id % 25 != 0:
                    offset = self.end_id % 25
                    self.end_id = self.end_id - offset
                else:
                    self.end_id = self.end_id - 25

                [tickets, number_of_tickets] = self.getTicketsInRange(
                    self.start_id, self.end_id
                )
                self.last_ticket_shown = self.end_id

                Printer.displayAllTicketsInfo(tickets, number_of_tickets)

            else:
                Printer.displayInvalidInput()
