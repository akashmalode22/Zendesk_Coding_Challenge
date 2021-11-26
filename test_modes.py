import unittest
from unittest.mock import patch
import modes


class TestModes(unittest.TestCase):
    def setUp(self):
        self.mode = modes.Modes()

    def tearDown(self):
        del self.mode

    def test_validateModeSelection(self):

        self.mode.CURRENT_MODE = modes.MODE_MAIN_MENU
        self.assertEqual(self.mode.validateModeSelection("1"), True)
        self.assertEqual(self.mode.validateModeSelection("2"), True)
        self.assertEqual(self.mode.validateModeSelection("q"), True)
        self.assertEqual(self.mode.validateModeSelection("quit"), True)
        self.assertEqual(self.mode.validateModeSelection("3"), False)
        self.assertEqual(self.mode.validateModeSelection("abc"), False)
        with self.assertRaises(TypeError):
            self.mode.validateModeSelection(None)
            self.mode.validateModeSelection(1)

        self.mode.CURRENT_MODE = modes.MODE_PAGINATION
        self.assertEqual(self.mode.validateModeSelection("n"), True)
        self.assertEqual(self.mode.validateModeSelection("p"), True)
        self.assertEqual(self.mode.validateModeSelection("s"), True)
        self.assertEqual(self.mode.validateModeSelection("m"), True)
        self.assertEqual(self.mode.validateModeSelection("q"), True)
        self.assertEqual(self.mode.validateModeSelection("quit"), True)
        self.assertEqual(self.mode.validateModeSelection("a"), False)
        with self.assertRaises(TypeError):
            self.mode.validateModeSelection(None)
            self.mode.validateModeSelection(1)
            self.mode.validateModeSelection(-10)

        self.assertEqual(
            self.mode.validateModeSelection(
                "1", number_of_tickets=10, from_paging=True
            ),
            True,
        )

        self.assertEqual(
            self.mode.validateModeSelection(
                "-10", number_of_tickets=10, from_paging=True
            ),
            False,
        )

        self.mode.CURRENT_MODE = modes.MODE_SELECTED_TICKET
        self.assertEqual(
            self.mode.validateModeSelection(
                "1", number_of_tickets=10, from_paging=True
            ),
            True,
        )

        self.assertEqual(
            self.mode.validateModeSelection(
                "-10", number_of_tickets=10, from_paging=True
            ),
            False,
        )

        self.mode.CURRENT_MODE = 6
        self.assertEqual(self.mode.validateModeSelection("1"), False)

    def test_validateNextPageExists(self):
        self.assertEqual(self.mode.validateNextPageExists(1, 50, 100), True)
        self.assertEqual(self.mode.validateNextPageExists(75, 100, 101), True)
        self.assertEqual(self.mode.validateNextPageExists(101, 101, 101), False)

        with self.assertRaises(TypeError):
            self.mode.validateNextPageExists(None, 25, 100)

        with self.assertRaises(IndexError):
            self.mode.validateNextPageExists(1, 50, 25)

    def test_validatePreviousPageExists(self):
        self.assertEqual(self.mode.validatePreviousPageExists(1, 50, 100), False)
        self.assertEqual(self.mode.validatePreviousPageExists(25, 50, 101), True)

        with self.assertRaises(TypeError):
            self.mode.validatePreviousPageExists(None, "25", 100)

        with self.assertRaises(IndexError):
            self.mode.validatePreviousPageExists(1, 50, 25)

    def test_ticketExists(self):
        self.assertEqual(self.mode.ticketExists(30, 100), True)
        self.assertEqual(self.mode.ticketExists(-1, 100), False)
        self.assertEqual(self.mode.ticketExists(101, 100), False)
        self.assertEqual(self.mode.ticketExists(101, 101), True)

        with self.assertRaises(TypeError):
            self.mode.validateNextPageExists("25", 100)
            self.mode.validateNextPageExists(25, None)

    def test_requireMultiplePages(self):
        self.assertEqual(self.mode.requireMultiplePages(100), True)
        self.assertEqual(self.mode.requireMultiplePages(45), True)
        self.assertEqual(self.mode.requireMultiplePages(15), False)

        with self.assertRaises(TypeError):
            self.mode.validateNextPageExists("10")
            self.mode.validateNextPageExists(None)

    def test_changeMode(self):
        self.mode.changeMode(2)
        self.assertEqual(self.mode.CURRENT_MODE, 2)

        self.mode.changeMode(0)
        self.assertEqual(self.mode.CURRENT_MODE, 0)

        with self.assertRaises(TypeError):
            self.mode.changeMode("2")

        with self.assertRaises(IndexError):
            self.mode.changeMode(5)
            self.mode.changeMode(-1)

    def test_exit(self):
        self.assertEqual(self.mode.exit("q"), True)
        self.assertEqual(self.mode.exit("quit"), True)
        self.assertEqual(self.mode.exit("a"), False)

        with self.assertRaises(TypeError):
            self.mode.exit(10)
            self.mode.exit(None)


if __name__ == "__main__":
    unittest.main()
