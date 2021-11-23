import requests
from requests.auth import HTTPBasicAuth
import errormacros
import modes
from printer import Printer
import utils


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

        ids = utils.populateListWithIDs(start_id, end_id)

        # url = "" TODO: Do I need this?
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
                mode.handleSelectedTicketMode(self, True)
                continue

            elif user_input == "m":
                mode.changeMode(modes.MODE_MAIN_MENU)
                return

            elif user_input == "n" or user_input == "p":

                if user_input == "n":
                    [self.start_id, self.end_id] = utils.calculateNextPageBounds(
                        self.last_ticket_shown, self.number_of_tickets
                    )

                elif user_input == "p":
                    [self.start_id, self.end_id] = utils.calculatePreviousPageBounds(
                        self.start_id, self.end_id
                    )

                [tickets, number_of_tickets] = self.getTicketsInRange(
                    self.start_id, self.end_id
                )
                self.last_ticket_shown = self.end_id

                Printer.displayAllTicketsInfo(tickets, number_of_tickets)

            else:
                # Invalid input. Display message.
                Printer.displayInvalidInput()
