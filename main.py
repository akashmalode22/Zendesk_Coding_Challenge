from printer import Printer
import modes
import retrievetickets
import utils


def initializeTicketViewer():

    [mode, retriever] = utils.initializeClassObjects()

    # Program just began. Should start with main menu mode
    mode.changeMode(modes.MODE_MAIN_MENU)

    Printer.displayInitialMessage()

    while True:

        if mode.CURRENT_MODE == modes.MODE_MAIN_MENU:

            mode.handleMainMenuMode()

        elif mode.CURRENT_MODE == modes.MODE_ALL_TICKETS:

            mode.handleAllTicketsMode(retriever)

        elif mode.CURRENT_MODE == modes.MODE_SELECTED_TICKET:

            mode.handleSelectedTicketMode(retriever)

        elif mode.CURRENT_MODE == modes.MODE_NO_PAGINATION:

            mode.handleSinglePageMode(retriever)

        elif mode.CURRENT_MODE == modes.MODE_PAGINATION:

            mode.handleMultiplePagesMode(retriever)


if __name__ == "__main__":
    initializeTicketViewer()
