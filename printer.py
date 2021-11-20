class printer:
    def display_initial_message():
        print("\n\n***** Welcome to the Zendesk Ticket Viewer *****\n")

    def display_main_menu():
        print("\tMain Menu:")
        print("\t--Press 1 to view all tickets")
        print("\t--Press 2 to view a selected ticket")
        print('\t--Press q or type "quit" to quit')
        print()

    def display_invalid_input():
        print("Invalid option selected. Ignoring user input...\n")
