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


def calculateNextPageBounds(last_ticket_shown, number_of_tickets):
    start_id = last_ticket_shown + 1
    end_id = min(last_ticket_shown + modes.TICKETS_PER_PAGE_LIMIT, number_of_tickets)

    return [start_id, end_id]


def calculatePreviousPageBounds(start_id, end_id):
    start_id = start_id - modes.TICKETS_PER_PAGE_LIMIT

    if end_id % modes.TICKETS_PER_PAGE_LIMIT != 0:
        offset = end_id % modes.TICKETS_PER_PAGE_LIMIT
        end_id = end_id - offset
    else:
        end_id = end_id - modes.TICKETS_PER_PAGE_LIMIT

    return [start_id, end_id]
