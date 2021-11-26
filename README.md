# Zendesk Coding Challenge

A CLI-based Ticket Viewing System using Zendesk's API. 

Written in Python (python3). The program retrieves ticket information from a Zendesk account using HTTP requests, and displays single ticket information or pages through them if many tickets are retrieved.

This is a requirement challenge for Zendesk's summer internship for 2022.


# Requirements
## Functional Requirements
- Connect to the Zendesk API
- Request all tickets for user's account
- Display them in a list
- Display individual ticket details
- Page through tickets when more than 25 are returned

## Non-functional requirements
- README with usage instructions
- Display some knowledge of application design
- Handle basic errors
	- API errors
	- Program errors
- Include unit tests
- UI is easy to use and readable

# Running the Ticket Viewer

## Installation prerequisites
Assumption: The program is being run on a system running MacOS (or some linux system)
The following steps have been tested on MacOS. Steps may be different for Windows machines.

You will require the following programs and packages:

- Python3
- pip
- tabulate (module)
- requests (module)
- pytest

If you have everything installed, you can skip to the next section. If you have any of these missing, please read the respective instructions:


 1. **Install Python 3**

	Run the following command to see if you already have python3 installed:
	```python3 --version```
	
	If the command responds with some version number of python3, then you can move to the next step. If not, continue to install python3.
	
	Head over to: https://www.python.org/downloads/
	
	Download and run the latest version of the python installer.

2. **Install pip**

	Run the following cURL command to download pip:
	
	```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

	Execute the downloaded file using the command:
	
	```python3 get-pip.py```

3. **Install the tabulate module using pip**
	
	```pip3 install tabulate```

4. **Install the requests module for python3**
	
	```pip3 install requests```

5. **Install Pytest**
	
	```pip3 install -U pytest```
	
## Running the program

1. Download the repository to your local machine (within some folder):

	```
	git clone https://github.com/akashmalode22/Zendesk_Coding_Challenge.git
	```

2. Open `credentials.txt` and change the subdomain, user, and token to test with your own Zendesk account. The file has my credentials saved with the tickets test data provided by Zendesk.
3. Run the program using the command
	```
	python3 main.py
	```
	**NOTE: Be sure to run the program with `python3`. If you run it with just `python`, you may get an error saying 		`ImportError: No module named tabulate`**

## Running tests
1. Run all test files prefixed with `test_` using the following command(s):

	```python3 test_modes.py```
	
	```python3 test_retrievetickets.py```
	
	```python3 test_utils.py```

## Design Choices

### Main Process

Considering the entire program runs based off of user input, I decided to revolve the entire execution of the program based on **modes**. These modes include `main menu`, `all tickets`, `selected ticket`, `pagination`, and `no pagination`. Every time the user selects an option, the mode context of the program switches to either one of these modes. This helps with interleaving modes without more complicated code.

For example, the user can choose to receive information of one ticket. This puts the program in the `selected ticket` mode. Next, the user wants to receive all tickets. This puts the program in `pagination` (or `no pagination`) mode, depending on the number of tickets. 
What if the user wants to select a ticket to view its details? Instead of repeating code, the program can just change the mode to `selected ticket` mode. 

This makes the code very modular and easy to replicate and reuse.

### Separation and Modularization

I decided to have 3 classes: `modes`, `retrievetickets`, and `printer`, each perform their own functions:

- `modes`: handles all the loops to validate user input, change modes of the program, and execute a selected mode.

- `retrievetickets`: handles all the GET requests from the Zendesk API by generating a URL, reading credentials, getting a single ticket, getting tickets in range by ID, etc.

- `printer`: handles all the print statements including printing details of tickets using the tabulate python module, displaying menu options, and printing error messages.

Separating functionality in this manner makes the code modular and very easy to read. It also makes the code easier to reuse and debug if the program were to get more complex.

### Fetching tickets only when needed

I fetch tickets from the API only when required, for the following reasons:

- **Minimize storage**: If the Zendesk account has a large set of tickets, requesting for all tickets would use a lot of local storage

- **Reduce requests time**: If the user just wants to view the details of one ticket, requesting for all tickets would take some time and would make the program appear slow and unresponsive

- **User prematurely quits program**: If the user asks for a few tickets and quits the program, requesting for all tickets seems excessive and a waste of both storage and time

- **User requests for all tickets**: If the user requests for all tickets, views the first page (of 25 tickets), and quits the program, requesting for all of the data would waste storage and time. Hence, I decided to request for the required number of tickets. If the user moves to the next page, I fetch the next 25 tickets and display them

- **Ticket information updates**: If some ticket information was updated while the program was already running, the prefetched data would be outdated. Hence, I decided to always fetch tickets fresh from the server as and when required. This ensures all data is up-to-date

- **No Caching**: I was unable to find some field analogous to `last_modified` on each ticket object. If something like that were to exist, I could implement a caching feature that checks if the ticket information on local storage matches the information on the server by comparing the `last_modified` field, and only retrieve the ticket when the local information is outdated

Therefore, I request for certain tickets only when they are requested as there is no caching implemented in the program. This ensures both storage and bandwidth is not wasted, and that all ticket information is up-to-date.


## Challenges


