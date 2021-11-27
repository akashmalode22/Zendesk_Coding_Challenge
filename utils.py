import modes
import retrievetickets
import printer


def initializeClassObjects():
    """Instantiate Modes and RetrieveTickets class objects.

    Objects for Modes and RetrieveTickets classes are instantiated and returned

    Args:
        no value

    Returns:
        mode: Object of Modes class
        retriever: Object of RetrieveTickets class
    """

    mode = modes.Modes()
    retriever = retrievetickets.RetrieveTickets()

    return [mode, retriever]


def getDataFromFile(filename):
    """Reads data from filename and converts into dictionary

    Opens "filename" file. Reads contents line by line and separates
    into key:value pairs based on ':' symbol. Returns credentials
    structured as
    {
        subdomain:<subdomain>,
        user:<user>,
        token:<token>
    }

    Args:
        filename (string): File to extract authorization credentials from

    Returns:
        credentials (dictionary): key-value pairs of credentials
    """

    credentials = []
    try:
        file = open(filename)

    except Exception as e:
        print("Cannot open ", filename, ". Please check that it exists.")
        exit()

    for line in file:
        credentials.append(tuple(line.strip().split(":")))

    credentials = dict(credentials)

    file.close()

    return credentials


def getCredentialsFromFile(filename):
    """Extracts user and token from previously read file

    Extracts the "user" and "token" fields from dictionary
    which was read from filename. Returns the two fields

    Args:
        filename (string): File to extract authorization credentials from

    Returns:
        user (string): user extracted from filename
        token (string): token extracted from filename
    """

    credentials = getDataFromFile(filename)

    return [credentials["user"], credentials["token"]]


def getSubdomainFromFile(filename):
    """Extracts subdomain from previously read file

    Extracts the "subdomain" field from dictionary
    which was read from filename. Returns the subdomain.

    Args:
        filename (string): File to extract authorization credentials from

    Returns:
        subdomain (string): subdomain extracted from filename
    """
    credentials = getDataFromFile(filename)

    return credentials["subdomain"]


def populateListWithIDs(start_id, end_id):
    """Populates a list with numbers in range of start_id
    to end_id

    Populates a list with IDs from a start_id to end_id. Converts all
    values to strings. This list is used to retrieve certain tickets with
    IDs from the API.

    Args:
        start_id (integer): Starting index for range to populate list with
        end_id (integer): Ending index for range to populate list with
                          (inclusive)

    Returns:
        ids (list of strings): Requested ID numbers converted to strings
    """

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
    """Calculates the range of tickets required to display the next page
    of tickets

    Calculating the range of tickets for the next page depends on the
    last ticket shown and the total number of tickets. For the next page,
    the start index is just incremented, but the end index can either be
    itself added with page limit, or the total number of tickets.

    For example: Last ticket shown was 50, total tickets is 100.
                 The next indices should be 51 to 75
    For example: Last ticket shown was 100, total tickets is 101.
                 The next indices should be 101 to 101 (cannot go out of bounds)

    Args:
        last_ticket_shown (integer): ID of the last ticket displayed
        number_of_tickets (integer): total number of tickets on the
                                     Zendesk account

    Returns:
        start_id (integer): Ticket ID to start from for next page
        end_id (integer): Ticket ID to end at for next page
    """

    if not isinstance(last_ticket_shown, int) or not isinstance(number_of_tickets, int):
        raise TypeError("last_ticket_shown and number_of_tickets must be integers.")

    start_id = last_ticket_shown + 1
    end_id = min(last_ticket_shown + modes.TICKETS_PER_PAGE_LIMIT, number_of_tickets)

    return [start_id, end_id]


def calculatePreviousPageBounds(start_id, end_id):
    """Calculates the range of tickets required to display the previous
    page of tickets

    Calculating the range of tickets for the previous page depends on the
    start and end IDs of the current page being displayed. For the previous
    page, the start index is just decremented by the page limit,
    but the end index has to be a factor of the page limit.

    Args:
        start_id (integer): First ticket ID currently displayed
        end_id (integer): Last ticket ID currently displayed

    Returns:
        start_id (integer): Ticket ID to start from for prev page
        end_id (integer): Ticket ID to end at for prev page
    """

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
    """Calculates the total number of pages required to display
    all the tickets

    Divides total number of tickets with the page limit. If there
    still are remaining tickets not accounted for (modulo), add
    a page

    Args:
        number_of_tickets (integer): total number of tickets on the
                                     Zendesk account

    Returns:
        total_pages (integer): total pages to display all tickets
    """

    if not isinstance(number_of_tickets, int):
        raise TypeError("number_or_tickets should be an integer")

    total_pages = 0

    total_pages += number_of_tickets / modes.TICKETS_PER_PAGE_LIMIT

    if number_of_tickets % modes.TICKETS_PER_PAGE_LIMIT:
        total_pages += 1

    return int(total_pages)
