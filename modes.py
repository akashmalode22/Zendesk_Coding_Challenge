from printer import Printer

MODE_MAIN_MENU = 0
MODE_ALL_TICKETS = 1
MODE_SELECTED_TICKET = 2
MODE_PAGINATION = 3
MODE_NO_PAGINATION = 4


class Modes:

    CURRENT_MODE = 0

    def validateModeSelection(self, user_input):
        if user_input == "q" or user_input == "quit":
            return True

        elif user_input == "0" or user_input == "1" or user_input == "2":
            return True

        return False

    def changeMode(self, user_input):
        Modes.CURRENT_MODE = user_input

    def exit(self, user_input):
        if user_input == "q" or user_input == "quit":
            return True
        return False

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

        return

    def handleAllTicketsMode(self, retriever):

        # Display all tickets message
        Printer.displayAllTicketsMessage()

        # Get the number of tickets
        retriever.getNumberOfTickets()

        # Determine if we need to page through tickets based
        # on the total number of tickets available
        if retriever.number_of_tickets < 25:
            self.changeMode(MODE_NO_PAGINATION)
        elif retriever.number_of_tickets >= 25:
            self.changeMode(MODE_PAGINATION)

        return
