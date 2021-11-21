from printer import Printer
import modes
import retrievetickets


def initializeTicketViewer():

    # Display initial welcome message
    # Display outer menu
    # 1 --> View all tickets
    # 2 --> View individual ticket

    # If inside some menu
    # If inside "individual ticket"
    # nothing extra
    # If inside "view all tickets"
    # If number of tickets > 25
    # menu should be "next page", "prev page", "main menu"

    # Program just began. Should start with main menu mode
    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    Printer.displayInitialMessage()

    while True:

        # print("current mode: ", mode.CURRENT_MODE)
        # print("main menu mode: ", modes.MODE_MAIN_MENU)

        if mode.CURRENT_MODE == modes.MODE_MAIN_MENU:
            # Display main menu
            Printer.displayMainMenu()

            # Get user input (menu selection)
            user_input = input("Select an option from the menu above: ")

            # Validate user input is one of the options provided
            if not mode.validateModeSelection(user_input):
                Printer.displayInvalidInput()
                continue

            if mode.exit(user_input):
                Printer.displayExitMessage()
                break

            # Change mode based on user_input
            mode.changeMode(int(user_input))

        elif mode.CURRENT_MODE == modes.MODE_ALL_TICKETS:
            # Display all tickets message
            Printer.displayAllTicketsMessage()

            # Get the number of tickets
            retriever.getNumberOfTickets()

            if retriever.number_of_tickets < 25:
                mode.changeMode(modes.MODE_NO_PAGINATION)
            elif retriever.number_of_tickets >= 25:
                mode.changeMode(modes.MODE_NO_PAGINATION)

        elif mode.CURRENT_MODE == modes.MODE_SELECTED_TICKET:

            # Get user input for ticket number
            user_input_ticket_number = input("Enter a ticket number: ")

            # Get ticket data from server, store in variable
            ticket = retriever.getTicketByID(user_input_ticket_number)

            # Display ticket information
            Printer.displayTicketInfo(ticket)

            # Switch back to main menu mode
            mode.changeMode(modes.MODE_MAIN_MENU)

        elif mode.CURRENT_MODE == modes.MODE_NO_PAGINATION:

            # We have fewer than 25 total tickets. Just display them all
            [tickets, number_of_tickets] = retriever.getAllTicketsNoPagination()

            Printer.displayAllTicketsInfo(tickets, number_of_tickets)

            exit()


if __name__ == "__main__":
    initializeTicketViewer()
