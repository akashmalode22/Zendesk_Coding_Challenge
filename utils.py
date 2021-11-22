import modes
import retrievetickets


def initializeClassObjects():

    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    return [mode, retriever]
