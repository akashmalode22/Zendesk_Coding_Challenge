MODE_MAIN_MENU = 0
MODE_ALL_TICKETS = 1
MODE_SELECTED_TICKET = 2


class Modes:

    CURRENT_MODE = 0

    def validateModeSelection(self, user_input):
        if user_input == "q" or user_input == "quit":
            return True

        user_option = int(user_input)

        if user_input == 1 or user_input == 2:
            return True

        return False

    def changeMode(self, user_input):
        Modes.CURRENT_MODE = user_input
