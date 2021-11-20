from printer import printer
import modes


def displayInitialMessage():
    printer.display_initial_message()


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

    while True:

        # print("current mode: ", mode.CURRENT_MODE)
        # print("main menu mode: ", modes.MODE_MAIN_MENU)

        if mode.CURRENT_MODE == modes.MODE_MAIN_MENU:
            # Display main menu
            printer.display_main_menu()

            # Get user input (menu selection)
            user_input = input("Select an option from the menu above: ")

            # Validate user input is one of the options provided
            if !modes.validateModeSelection(user_input):
                printer.display_invalid_input()
                continue

            # Change mode based on user_input
            mode.changeMode(int(user_input))

            print(mode.CURRENT_MODE)
        
        elif mode.CURRENT_MODE == modes.MODE_ALL_TICKETS:
        
        elif mode.CURRENT_MODE == modes.MODE_SELECTED_TICKET:
            
        elif 


if __name__ == "__main__":
    displayInitialMessage()
    initializeTicketViewer()
