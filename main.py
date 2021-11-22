from printer import Printer
import modes
import retrievetickets


def initializeTicketViewer():

    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    # Program just began. Should start with main menu mode
    mode.changeMode(modes.MODE_MAIN_MENU)

    Printer.displayInitialMessage()

    while True:

        if mode.CURRENT_MODE == modes.MODE_MAIN_MENU:

            mode.handleMainMenuMode()

        elif mode.CURRENT_MODE == modes.MODE_ALL_TICKETS:

            mode.handleAllTicketsMode(retriever)

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

            mode.changeMode(modes.MODE_MAIN_MENU)

        elif mode.CURRENT_MODE == modes.MODE_PAGINATION:

            # Get 25 tickets at a time
            [tickets, number_of_tickets] = retriever.getTicketsInRange(1, 25)
            retriever.last_ticket_shown = 25

            Printer.displayAllTicketsInfo(tickets, number_of_tickets)

            retriever.pageTickets(mode)


if __name__ == "__main__":
    initializeTicketViewer()
