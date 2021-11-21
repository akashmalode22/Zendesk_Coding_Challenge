class Printer:
    def displayInitialMessage():
        print("\n\n***** Welcome to the Zendesk Ticket Viewer *****\n")

    def displayMainMenu():
        print("\tMain Menu:")
        print("\t--Press 1 to view all tickets")
        print("\t--Press 2 to view a selected ticket")
        print('\t--Press q or type "quit" to quit')
        print()

    def displayInvalidInput():
        print("Invalid option selected. Ignoring user input...\n")

    def displayAllTicketsMessage():
        print("Displaying all tickets ...\n")

    def displaySelectedTicketMessage(user_input):
        print("Displaying ticket #" + user_input + "...\n")

    def displayExitMessage():
        print("\n********************************************************")
        print("Thank you for using the Zendesk Ticket Viewer! Bye.")
        print("********************************************************\n")
