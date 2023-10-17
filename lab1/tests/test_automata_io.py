import unittest

from automata import Automata


class TestAutomataFileOperations(unittest.TestCase):
    def setUp(self):
        # Example Automata for testing
        self.example_automata = Automata(
            A={"0", "1", "2"},
            X={"x", "y", "z"},
            f={
                ("0", "x"): {"0", "1", "2"},
                ("0", "y"): {"1", "2"},
                ("0", "z"): {"2"},
                ("1", "y"): {"1", "2"},
                ("2", "z"): {"2"},
            },
            a0="0",
            F={"2"},
            epsilon="epsilon",
        )
        # Test filename
        self.filename = ".pytest_cache/temp_automata.json"

    def test_save_to_file(self):
        # Save the automata to a file
        self.example_automata.save_to_file(self.filename)

        # Check if file exists and if it has content
        with open(self.filename, "r") as file:
            content = file.read()
            self.assertTrue(content)  # Assert that the file has content

    def test_load_from_file(self):
        # Save the automata to a file
        self.example_automata.save_to_file(self.filename)

        # Load the automata from the file
        loaded_automata = Automata.load_from_file(self.filename)

        # Assert that the loaded Automata matches the original example Automata
        self.assertEqual(loaded_automata, self.example_automata)
