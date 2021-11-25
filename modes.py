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
        """Validate the user's input according to the mode the program is in.

        The user's input is checked against the current mode's allowed inputs from the
        input list defined above as OPTIONS_*_*. The user's input is converted to an
        integer for validating if a selected ticket ID exists.

        Args:
            user_input (string): the user's input when prompted to enter a menu option
            number_of_tickets (integer) (optional): number of tickets that exist on the Zendesk account
            from_paging (boolean) (optional): check whether this function was invoked from paging mode

        Returns:
            boolean: True if the user's input is valid, False otherwise
        """

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
        """Validate whether a next page exists when paging through tickets.

        The last ticket shown is checked with the total number of tickets. If there are
        more tickets to be shown after the last ticket, a next page exists.

        Args:
            start_id (integer): start index of range of tickets that was previously displayed
            end_id (integer): end index of range of tickets that was previously displayed
            number_of_tickets (integer): number of tickets that exist on the Zendesk account

        Returns:
            boolean: True if next page exists, False otherwise.
        """

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
        """Validate whether a previous page exists when paging through tickets.

        If the first ticket ID in the range of tickets previously displayed is not yet zero,
        a previous page exists.

        Args:
            start_id (integer): start index of range of tickets that was previously displayed
            end_id (integer): end index of range of tickets that was previously displayed
            number_of_tickets (integer): number of tickets that exist on the Zendesk account

        Returns:
            boolean: True if previous page exists, False otherwise.
        """

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
        """Checks whether the user's requested ticket ID exists.

        The user's input is checked with the number of tickets that exist on the Zendesk
        account, and returns a boolean as a result.

        Args:
            user_input (integer): the user's input when prompted to enter a ticket ID
            number_of_tickets (integer): number of tickets that exist on the Zendesk account

        Returns:
            boolean: True if the user's input falls in range of number of existing
            tickets, False otherwise.
        """

        if not isinstance(user_input, int) or not isinstance(number_of_tickets, int):
            raise TypeError("user_input, number_of_tickets must be integers.")

        return user_input > 0 and user_input <= number_of_tickets

    def requireMultiplePages(self, number_of_tickets):
        """Determines whether multiple pages are required to show all tickets
        (25 tickets per page limit).

        The total number of tickets on the Zendesk account is compared with the
        tickets per page limit.

        Args:
            number_of_tickets (integer): number of tickets that exist on the Zendesk account

        Returns:
            boolean: True if number of tickets exceeds the tickets per page limit,
            False otherwise.
        """

        if not isinstance(number_of_tickets, int):
            raise TypeError("number_of_tickets must be integers.")

        return number_of_tickets > TICKETS_PER_PAGE_LIMIT

    def changeMode(self, user_input):
        """Changes the class variable to the required mode value.

        The class's variable is changed to the user's input mode. Validation was
        previously done, so it is safe to not validate here.

        Args:
            user_input (integer): the user's input when prompted to enter a menu option

        Returns:
            no value
        """

        if not isinstance(user_input, int):
            raise TypeError("mode must be integer.")

        if user_input > 4:
            raise IndexError("mode does not exist.")

        Modes.CURRENT_MODE = user_input

    def exit(self, user_input):
        """Checks whether the user asked to quit the program.

        The user's input is checked with the valid options to quit the program from
        the OPTIONS_QUIT list.

        Args:
            user_input (integer): the user's input when prompted to enter a menu option

        Returns:
            boolean: True if the user's input is a valid quit option, False otherwise.
        """

        if not isinstance(user_input, str):
            raise TypeError("user_input must be a string.")

        return user_input in OPTIONS_QUIT

    def handleMainMenuMode(self):
        """Executes main menu mode.

        Main menu options are displayed. The user is asked for a menu option which is
        validated. If user wishes to quit the program, the program exits. Otherwise,
        the program's mode is changed to the user's requested mode.

        Args:
            no value

        Returns:
            no value
        """

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
        """Executes display all tickets mode.

        The program gets the existing number of tickets on the Zendesk account.
        Program's mode is changed to the appropriate mode if multiple pages are
        required to display all tickets, or if a single page is sufficient.

        Args:
            retriever (RetrieveTickets object): a RetrieveTickets class object
                that stores total number of tickets

        Returns:
            no value
        """

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
        """Executes display a selected ticket mode.

        User is asked to enter a ticket ID, which is validated if the ticket ID
        exists. The retriever object requests for the ticket from the API, and the printer
        class displays the ticket's information. If the method was called from paging mode,
        the program stays in paging mode. If not, the mode is changed to main menu.

        Args:
            retriever (RetrieveTickets object): a RetrieveTickets class object
            from_paging (boolean) (optional): check whether this function was invoked
                from paging mode

        Returns:
            no value
        """

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
        """Executes display all tickets in a single page.

        API request is made to get all tickets. Details of all tickets are displayed.
        Mode is changed to main menu mode.

        Args:
            retriever (RetrieveTickets object): a RetrieveTickets class object

        Returns:
            no value
        """

        # We have fewer than 25 total tickets. Just display them all
        [tickets, number_of_tickets] = retriever.getAllTicketsNoPagination()

        Printer.displayAllTicketsInfo(tickets, number_of_tickets, 1, 1)

        self.changeMode(MODE_MAIN_MENU)

    def handleMultiplePagesMode(self, retriever):
        """Executes display all tickets in multiple pages.

        API request is made to get tickets in a range (25 tickets). Details
        of first 25 tickets are displayed. The program goes into a pagination mode until
        the user exits the mode. After user exits pagination mode, the range of
        tickets shown is reset.

        Args:
            retriever (RetrieveTickets object): a RetrieveTickets class object

        Returns:
            no value
        """

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
