import unittest
from unittest.mock import patch
import modes
import retrievetickets
import utils


class TestUtils(unittest.TestCase):
    def setUp(self):
        self.mode = modes.Modes()
        self.retriever = retrievetickets.RetrieveTickets()

    def tearDown(self):
        del self.mode

    def test_initializeClassObjects(self):
        [mode, retriever] = utils.initializeClassObjects()
        self.assertEqual(type(mode), type(self.mode))
        self.assertEqual(type(retriever), type(self.retriever))

    def test_getDataFromFile(self):
        file = open("test_credentials.txt", "w")
        file.write("subdomain:testdomain\nuser:test@email.com\ntoken:123token456\n")
        file.close()
        credentials = utils.getDataFromFile("test_credentials.txt")

        self.assertEqual(credentials["user"], "test@email.com")
        self.assertEqual(credentials["subdomain"], "testdomain")
        self.assertEqual(credentials["token"], "123token456")

    def test_populateListWithIDs(self):
        self.assertEqual(utils.populateListWithIDs(1, 5), ["1", "2", "3", "4", "5"])
        self.assertEqual(utils.populateListWithIDs(1, 1), ["1"])

        with self.assertRaises(IndexError):
            utils.populateListWithIDs(5, 2)
            utils.populateListWithIDs(0, 2)
            utils.populateListWithIDs(-1, -1)

        with self.assertRaises(TypeError):
            utils.populateListWithIDs(5, "2")
            utils.populateListWithIDs("0", 2)
            utils.populateListWithIDs(None, 10)

    def test_calculateNextPageBounds(self):
        self.assertEqual(utils.calculateNextPageBounds(25, 101), [26, 50])
        self.assertEqual(utils.calculateNextPageBounds(50, 101), [51, 75])
        self.assertEqual(utils.calculateNextPageBounds(100, 101), [101, 101])

        with self.assertRaises(TypeError):
            utils.calculateNextPageBounds(5, "2")
            utils.calculateNextPageBounds("0", 2)
            utils.calculateNextPageBounds(None, 10)

    def test_calculatePreviousPageBounds(self):
        self.assertEqual(utils.calculatePreviousPageBounds(26, 50), [1, 25])
        self.assertEqual(utils.calculatePreviousPageBounds(101, 101), [76, 100])

        with self.assertRaises(IndexError):
            utils.calculatePreviousPageBounds(1, 25)

        with self.assertRaises(TypeError):
            utils.calculateNextPageBounds(5, "2")
            utils.calculateNextPageBounds("0", 2)
            utils.calculateNextPageBounds(None, 10)

    def test_calculateTotalPages(self):

        self.assertEqual(utils.calculateTotalPages(101), 5)
        self.assertEqual(utils.calculateTotalPages(100), 4)
        self.assertEqual(utils.calculateTotalPages(25), 1)
        self.assertEqual(utils.calculateTotalPages(10), 1)
        self.assertEqual(utils.calculateTotalPages(0), 0)

        with self.assertRaises(TypeError):
            utils.calculateTotalPages("2")
            utils.calculateTotalPages(None)
            utils.calculateTotalPages(True)


if __name__ == "__main__":
    unittest.main()
