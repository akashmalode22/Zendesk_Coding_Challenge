from tabulate import tabulate
import textwrap


class Printer:
    @staticmethod
    def displayInitialMessage():
        print("\n\n***** Welcome to the Zendesk Ticket Viewer *****\n")

    @staticmethod
    def displayMainMenu():
        print()
        print("\tMain Menu:")
        print("\t--Press 1 to view all tickets")
        print("\t--Press 2 to view a selected ticket")
        print('\t--Press q or type "quit" to quit')
        print()

    @staticmethod
    def displayInvalidInput():
        print("\nInvalid option selected. Please select a valid menu option...\n")

    def displayResponseErrors(status_code):
        if status_code == 401:
            print(
                "\nUnauthorized user. Please check login credentials and re-run the program.\n"
            )

        elif status_code == 404:
            print(
                "\nInvalid request. Verify subdomain and credentials, and re-run the program.\n"
            )
        elif status_code == 500:
            print(
                "\nInternal Server Error. If problem persists, the service may be down.\n"
            )
        else:
            print("\nResponse is invalid.\n")
        exit()

    @staticmethod
    def displayNoNextPage():
        print("\nNext page doesn't exist... Go to a previous page.\n")

    @staticmethod
    def displayNoPreviousPage():
        print("\nPrevious page doesn't exist... Go to a next page.\n")

    @staticmethod
    def displayAllTicketsMessage():
        print("\nDisplaying all tickets. Please wait while we fetch them...\n")

    def displaySelectedTicketMessage(user_input):
        print("\nDisplaying ticket #" + user_input + "...\n")

    @staticmethod
    def displayInvalidType():
        print("\nPlease enter an integer...")

    @staticmethod
    def displayExitMessage():
        print("\n********************************************************")
        print("Thank you for using the Zendesk Ticket Viewer! Bye.")
        print("********************************************************\n")

    def displayTicketInfo(ticket):
        """Displays information of a single ticket.

        Relevant information of the ticket is extracted, and printed using
        the tabulate module. Shortens ticket description to 100 characters.

        Args:
            ticket (JSON object): ticket received from API

        Returns:
            no value
        """

        table = [
            ["Ticket ID", ticket["ticket"]["id"]],
            ["Subject", ticket["ticket"]["subject"]],
            ["Requested by", ticket["ticket"]["requester_id"]],
            ["Tags", ticket["ticket"]["tags"]],
            [
                "Description",
                textwrap.shorten(ticket["ticket"]["description"], width=100),
            ],
        ]

        print()
        print(tabulate(table, tablefmt="grid"))
        print()

    @staticmethod
    def displayOutOfRangeInput():
        print("\nTicket ID selected doesn't exist. Select another ticket ID...\n")

    def displayAllTicketsInfo(tickets, number_of_tickets, current_page, total_pages):
        """Displays information of all tickets.

        Relevant information of the ticket is extracted, and printed using
        the tabulate module. JSON object is different when only 1 ticket is
        retrieved from the API, hence the if condition.

        Args:
            tickets (JSON object): list of tickets in JSON format from API
            number_of_tickets (int): total number of tickets on the Zendesk account
            current_page (int): index of the page to be displayed
            total_pages (int): total number of pages that exist for all tickets

        Returns:
            no value
        """

        modified_tickets = []

        # JSON object attributes differ if it is a single ticket
        if number_of_tickets == 1:
            single_ticket = [
                tickets["id"],
                tickets["subject"],
                tickets["requester_id"],
                tickets["created_at"],
            ]

            modified_tickets.append(single_ticket)

        else:
            for i in range(0, number_of_tickets):

                single_ticket = [
                    tickets[i]["id"],
                    tickets[i]["subject"],
                    tickets[i]["requester_id"],
                    tickets[i]["created_at"],
                ]

                modified_tickets.append(single_ticket)

        print()
        print(tabulate(modified_tickets, headers=["ID", "Subject", "By", "Dated"]))
        print("Page [", current_page, "/", total_pages, "]")
        print()

    @staticmethod
    def displayPaginationMenu():
        print()
        print("\tPagination Menu:")
        print('\t--Press "n" to view next page')
        print('\t--Press "p" to view previous page')
        print('\t--Press "s" to view a selected ticket')
        print('\t--Press "m" to go to main menu')
        print('\t--Press "q" or type "quit" to quit')
        print()
