from printer import Printer

MODE_MAIN_MENU = 0
MODE_ALL_TICKETS = 1
MODE_SELECTED_TICKET = 2
MODE_PAGINATION = 3
MODE_NO_PAGINATION = 4

TICKETS_PER_PAGE_LIMIT = 25

OPTIONS_MAIN_MENU = ["1", "2", "q", "quit"]
OPTIONS_PAGE_MENU = ["n", "p", "s", "m", "q", "quit"]
OPTIONS_QUIT = ["q", "quit"]


class Modes:

    CURRENT_MODE = 0

    def validateModeSelection(self, user_input, number_of_tickets=0, from_paging=False):

        if not isinstance(user_input, str):
            raise TypeError("User input should be of string type.")

        if self.CURRENT_MODE == MODE_MAIN_MENU:
            if user_input in OPTIONS_MAIN_MENU:
                return True
            return False

        if self.CURRENT_MODE == MODE_PAGINATION:
            if user_input in OPTIONS_PAGE_MENU:
                return True
            if from_paging:
                user_input = int(user_input)
                if self.ticketExists(user_input, number_of_tickets):
                    return True

            return False

        if self.CURRENT_MODE == MODE_SELECTED_TICKET:
            user_input = int(user_input)

            if self.ticketExists(user_input, number_of_tickets):
                return True
            return False

        return False

    def validateNextPageExists(self, start_id, end_id, number_of_tickets):
        if (
            not isinstance(start_id, int)
            or not isinstance(end_id, int)
            or not isinstance(number_of_tickets, int)
        ):
            raise TypeError("start_id, end_id, number_of_tickets must all be integers.")

        if start_id < 0 or end_id > number_of_tickets:
            raise IndexError("start_id or end_id out of expected range.")

        return end_id + 1 <= number_of_tickets

    def validatePreviousPageExists(self, start_id, end_id, number_of_tickets):
        if (
            not isinstance(start_id, int)
            or not isinstance(end_id, int)
            or not isinstance(number_of_tickets, int)
        ):
            raise TypeError("start_id, end_id, number_of_tickets must all be integers.")

        if start_id < 0 or end_id > number_of_tickets:
            raise IndexError("start_id or end_id out of expected range.")

        return start_id - 1 > 0

    def ticketExists(self, user_input, number_of_tickets):
        if not isinstance(user_input, int) or not isinstance(number_of_tickets, int):
            raise TypeError("user_input, number_of_tickets must be integers.")

        return user_input > 0 and user_input <= number_of_tickets

    def requireMultiplePages(self, number_of_tickets):
        if not isinstance(number_of_tickets, int):
            raise TypeError("number_of_tickets must be integers.")

        return number_of_tickets > TICKETS_PER_PAGE_LIMIT

    def changeMode(self, user_input):
        if not isinstance(user_input, int):
            raise TypeError("mode must be integer.")

        if user_input > 4:
            raise IndexError("mode does not exist.")

        Modes.CURRENT_MODE = user_input

    def exit(self, user_input):
        if not isinstance(user_input, str):
            raise TypeError("user_input must be a string.")

        return user_input in OPTIONS_QUIT

    def handleMainMenuMode(self):

        # Display main menu
        Printer.displayMainMenu()

        # Get user input (menu selection)
        user_input = input("Select an option from the menu above: ")

        # Validate user input is one of the options provided
        if not self.validateModeSelection(user_input):
            Printer.displayInvalidInput()
            return

        if self.exit(user_input):
            Printer.displayExitMessage()
            exit()

        # Change mode based on user_input
        self.changeMode(int(user_input))

    def handleAllTicketsMode(self, retriever):

        # Display all tickets message
        Printer.displayAllTicketsMessage()

        # Get the number of tickets
        retriever.getNumberOfTickets()

        # Determine if we need to page through tickets based
        # on the total number of tickets available
        if self.requireMultiplePages(retriever.number_of_tickets):
            self.changeMode(MODE_PAGINATION)
        else:
            self.changeMode(MODE_NO_PAGINATION)

    def handleSelectedTicketMode(self, retriever, from_paging=False):

        # Get user input for ticket number
        user_input_ticket_number = input("Enter a ticket number: ")

        # Get number of tickets on Zendesk account
        retriever.getNumberOfTickets()

        # Validate whether user selected a valid ticket ID
        if not self.validateModeSelection(
            user_input_ticket_number, retriever.number_of_tickets, from_paging
        ):
            Printer.displayOutOfRangeInput()
            return

        # Get ticket data from server, store in variable
        ticket = retriever.getTicketByID(user_input_ticket_number)

        # Display ticket information
        Printer.displayTicketInfo(ticket)

        # If method was access from paging menu, leave as is. Just return.
        if from_paging:
            return

        # Switch back to main menu mode
        self.changeMode(MODE_MAIN_MENU)

    def handleSinglePageMode(self, retriever):

        # We have fewer than 25 total tickets. Just display them all
        [tickets, number_of_tickets] = retriever.getAllTicketsNoPagination()

        Printer.displayAllTicketsInfo(tickets, number_of_tickets, 1, 1)

        self.changeMode(MODE_MAIN_MENU)

    def handleMultiplePagesMode(self, retriever):

        # Retrieve the first 25 tickets
        [tickets, number_of_tickets] = retriever.getTicketsInRange(
            1, TICKETS_PER_PAGE_LIMIT
        )
        retriever.last_ticket_shown = TICKETS_PER_PAGE_LIMIT

        # Display the first 25 tickets
        Printer.displayAllTicketsInfo(
            tickets, number_of_tickets, 1, retriever.total_pages
        )

        # Start the pagination loop (for more pages)
        retriever.pageTickets(self)

        # Pagination is over. Reset last ticket shown for future pagination
        retriever.last_ticket_shown = 0
