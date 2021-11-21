from tabulate import tabulate


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

    def displayTicketInfo(ticket):
        print("Displaying ticket #", ticket["ticket"]["id"], "...\n")
        print(
            "------------------------------------------------------------------------"
        )
        print("Ticket ID:", ticket["ticket"]["id"])
        print("Subject: " + ticket["ticket"]["subject"])
        print("Description: " + ticket["ticket"]["description"])
        print("Requested by:", ticket["ticket"]["requester_id"])
        print("Tags:", ticket["ticket"]["tags"])
        print(
            "------------------------------------------------------------------------\n"
        )

    def displayAllTicketsInfo(tickets, number_of_tickets):
        modified_tickets = []

        for i in range(0, 25):

            single_ticket = [
                tickets[i]["id"],
                tickets[i]["subject"],
                tickets[i]["requester_id"],
                tickets[i]["created_at"],
            ]

            modified_tickets.append(single_ticket)

        print(tabulate(modified_tickets, headers=["ID", "Subject", "By", "Dated"]))
