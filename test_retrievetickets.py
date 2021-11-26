import unittest
from unittest import mock
from unittest.mock import patch
import modes
import retrievetickets
import utils


class TestRetrieveTickets(unittest.TestCase):
    def setUp(self):
        self.retriever = retrievetickets.RetrieveTickets()

    def tearDown(self):
        del self.retriever

    def test_getRawResponseFromServer(self):
        with patch("retrievetickets.requests.get") as mock_get:
            mock_get.return_value.status_code = 200
            response = self.retriever.getRawResponseFromServer("")

        self.assertEqual(response.status_code, 200)

    def test_generateURL(self):
        subdomain = utils.getSubdomainFromFile("credentials.txt")
        self.assertEqual(
            self.retriever.generateURL("/1"),
            "https://" + subdomain + ".zendesk.com/api/v2/tickets/1.json",
        )

        with self.assertRaises(TypeError):
            self.retriever.generateURL(123)

    def test_getCredentials(self):
        with mock.patch(
            "utils.getCredentialsFromFile",
            return_value=[
                "amalode@purdue.edu",
                "KCghGkIuanNLONrTjn6UuoCNr79VhqUR7koXjrG1",
            ],
        ):
            [user, pwd] = self.retriever.getCredentials()

        expected_user = "amalode@purdue.edu/token"
        self.assertIn(expected_user, [user, pwd])

    def test_getNumberOfTickets(self):
        url = self.retriever.generateURL("/count")
        data = self.retriever.getResponseFromServer(url)
        self.retriever.number_of_tickets = data["count"]["value"]

        self.assertEqual(self.retriever.number_of_tickets, data["count"]["value"])


if __name__ == "__main__":
    unittest.main()
