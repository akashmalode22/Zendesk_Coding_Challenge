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


 1. Install Python 3

	Run the following command to see if you already have python3 installed:
	```python3 --version```
	
	If the command responds with some version number of python3, then you can move to the next step. If not, continue to install python3.
	
	Head over to: https://www.python.org/downloads/
	
	Download and run the latest version of the python installer.

2. Install pip

	Run the following cURL command to download pip:
	```curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py```

	Execute the downloaded file using the command:
	```python3 get-pip.py```

3. Install the tabulate module using pip
	
	```pip3 install tabulate```

4. Install the requests module for python3
	
	```pip3 install requests```

5. Install Pytest
	
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
	**Be sure to run the program with `python3`. If you run it with just `python`, you may get an error saying 		`ImportError: No module named tabulate`**

## Running tests
1. Run all test files prefixed with `test_` using the following command(s):

	```python3 test_modes.py```
	```python3 test_retrievetickets.py```
	```python3 test_utils.py```


