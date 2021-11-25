import modes
import retrievetickets


def initializeClassObjects():

    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    return [mode, retriever]


def getDataFromFile(filename):
    credentials = []
    file = open(filename)
    for line in file:
        credentials.append(tuple(line.strip().split(":")))

    credentials = dict(credentials)

    file.close()

    return credentials


def getCredentialsFromFile(filename):

    credentials = getDataFromFile(filename)

    return [credentials["user"], credentials["token"]]


def getSubdomainFromFile(filename):
    credentials = getDataFromFile(filename)

    return credentials["subdomain"]


def populateListWithIDs(start_id, end_id):

    if start_id < 0 or end_id < 0 or end_id < start_id:
        raise IndexError("invalid start_id or end_id.")
    if not isinstance(start_id, int) or not isinstance(end_id, int):
        raise TypeError("start_id and end_id must be integers.")

    # Store required ticket IDs in an integer list
    ids = []
    for i in range(start_id, end_id + 1):
        ids.append(i)

    # Convert integer list to string list
    ids = [str(id) for id in ids]

    return ids


def calculateNextPageBounds(last_ticket_shown, number_of_tickets):

    if not isinstance(last_ticket_shown, int) or not isinstance(number_of_tickets, int):
        raise TypeError("last_ticket_shown and number_of_tickets must be integers.")

    start_id = last_ticket_shown + 1
    end_id = min(last_ticket_shown + modes.TICKETS_PER_PAGE_LIMIT, number_of_tickets)

    return [start_id, end_id]


def calculatePreviousPageBounds(start_id, end_id):

    if start_id < modes.TICKETS_PER_PAGE_LIMIT or end_id < start_id:
        raise IndexError("start_id is not in range.")

    if not isinstance(start_id, int) or not isinstance(end_id, int):
        raise TypeError("start_id and end_id must be integers.")

    start_id = start_id - modes.TICKETS_PER_PAGE_LIMIT

    if end_id % modes.TICKETS_PER_PAGE_LIMIT != 0:
        offset = end_id % modes.TICKETS_PER_PAGE_LIMIT
        end_id = end_id - offset
    else:
        end_id = end_id - modes.TICKETS_PER_PAGE_LIMIT

    return [start_id, end_id]


def calculateTotalPages(number_of_tickets):

    if not isinstance(number_of_tickets, int):
        raise TypeError("number_or_tickets should be an integer")

    total_pages = 0

    total_pages += number_of_tickets / modes.TICKETS_PER_PAGE_LIMIT

    if number_of_tickets % modes.TICKETS_PER_PAGE_LIMIT:
        total_pages += 1

    return int(total_pages)
