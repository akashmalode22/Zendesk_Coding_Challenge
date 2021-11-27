import requests
from requests.auth import HTTPBasicAuth
import errormacros
import modes
from printer import Printer
import utils


class RetrieveTickets:

    number_of_tickets = 0
    last_ticket_shown = 0
    total_pages = 0
    current_page = 1

    start_id = 0
    end_id = 0

    def generateURL(self, url_sublink):
        """Constructs the URL link to send a GET request to

        Combines the subdomain extracted from the credentials file
        and the url_sublink to generate a URL. The URL is returned.

        Args:
            url_sublink (string): sub path for the URL

        Returns:
            url (string): Ticket ID to start from for prev page
        """

        if not isinstance(url_sublink, str):
            raise TypeError("url_sublink must be a string.")

        subdomain = utils.getSubdomainFromFile("credentials.txt")
        return (
            "https://"
            + subdomain
            + ".zendesk.com/api/v2/tickets"
            + url_sublink
            + ".json"
        )

    def getCredentials(self):
        """Retrieves credentials from credentials.txt

        Retrieves credentials from credentials.txt. Appends
        "/token" to user string.

        Args:
            no value

        Returns:
            user (string): user email with "/token" appended
            pwd (string): user's API token
        """

        [user, pwd] = utils.getCredentialsFromFile("credentials.txt")
        user += "/token"

        return [user, pwd]

    def getRawResponseFromServer(self, url):
        """Does a GET request using url specified

        Retrieves user and password for authentication. Does
        a GET request at the specified url. Returns the JSON
        converted response data.

        Args:
            url (string): url to call GET request at

        Returns:
            response (JSON object): response from API in
                                    its raw format
        """

        [user, pwd] = self.getCredentials()

        response = requests.get(url, auth=(user, pwd))

        if response.status_code != errormacros.GET_SUCCESS_CODE:
            Printer.displayResponseErrors(response.status_code)

        return response

    def getResponseFromServer(self, url):
        """Converts server response to JSON

        Args:
            url (string): url to call GET request at

        Returns:
            response (JSON object): response from API at
                                    specified URL in JSON
                                    format
        """

        response = self.getRawResponseFromServer(url)

        return response.json()

    def getNumberOfTickets(self):
        """Retrieves total number of tickets on the Zendesk account

        Calls a GET request with "/count" sublink. Extracts the
        count and value fields. Sets the class's variable to the
        count

        Args:
            no value

        Returns:
            no value
        """

        url = self.generateURL("/count")

        data = self.getResponseFromServer(url)

        self.number_of_tickets = data["count"]["value"]

        self.total_pages = utils.calculateTotalPages(self.number_of_tickets)

    def getTicketByID(self, ticket_id):
        """Does a GET request for ticket with specific ID

        Generates appropriate URL with ticket ID and performs
        a GET request. Returns the response.

        Args:
            ticket_id (string): ID of the ticket requested

        Returns:
            data (JSON object): Ticket information requested by ID
        """

        url = self.generateURL("/" + ticket_id)

        print("\nFetching ticket #", ticket_id, ". Please wait...\n")

        data = self.getResponseFromServer(url)

        return data

    def getAllTicketsNoPagination(self):
        """Does a GET request to get all tickets

        Get request is performed at the default URL to retrieve
        all tickets on the Zendesk account. Returns a JSON object
        of tickets, and the number of tickets.

        Args:
            no value

        Returns:
            data (JSON object): Information of all tickets
            number_of_tickets (int): total number of tickets
                                     on the account
        """

        url = self.generateURL("")

        data = self.getResponseFromServer(url)

        return [data["tickets"], self.number_of_tickets]

    def getTicketsInRange(self, start_id, end_id):
        """Does a GET request to get certain tickets in a range

        Get request is performed with certain ticket IDs to
        retrieve tickets on the Zendesk account. Returns a JSON object
        of tickets, and the number of tickets retrieved (not all
        tickets).

        Args:
            start_id (integer): starting index for ticket ID requested
            end_id (integer): ending index for ticket ID requested

        Returns:
            data (JSON object): Information of all tickets
            number_of_tickets (int): total number of tickets
                                     retrieved
        """

        self.getNumberOfTickets()

        ids = utils.populateListWithIDs(start_id, end_id)

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
        """Handles paging through ticket pages

        Stays in a loop until user changes the mode of the program.
        User is prompted to select a menu option, with the option
        to go to the next or previous page of tickets.

        Args:
            mode (Modes object): Modes object

        Returns:
            no value
        """

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
                self.current_page = 1
                mode.changeMode(modes.MODE_MAIN_MENU)
                return

            elif user_input == "n" or user_input == "p":

                if user_input == "n":

                    if not mode.validateNextPageExists(
                        self.start_id, self.end_id, self.number_of_tickets
                    ):
                        Printer.displayNoNextPage()
                        continue

                    self.current_page += 1

                    [self.start_id, self.end_id] = utils.calculateNextPageBounds(
                        self.last_ticket_shown, self.number_of_tickets
                    )

                elif user_input == "p":

                    if not mode.validatePreviousPageExists(
                        self.start_id, self.end_id, self.number_of_tickets
                    ):
                        Printer.displayNoPreviousPage()
                        continue

                    self.current_page -= 1

                    [self.start_id, self.end_id] = utils.calculatePreviousPageBounds(
                        self.start_id, self.end_id
                    )

                [tickets, number_of_tickets] = self.getTicketsInRange(
                    self.start_id, self.end_id
                )
                self.last_ticket_shown = self.end_id

                Printer.displayAllTicketsInfo(
                    tickets, number_of_tickets, self.current_page, self.total_pages
                )

            else:
                # Invalid input. Display message.
                Printer.displayInvalidInput()
