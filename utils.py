import modes
import retrievetickets


def initializeClassObjects():

    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    return [mode, retriever]


def populateListWithIDs(start_id, end_id):

    # Store required ticket IDs in an integer list
    ids = []
    for i in range(start_id, end_id + 1):
        ids.append(i)

    # Convert integer list to string list
    ids = [str(id) for id in ids]

    return ids
