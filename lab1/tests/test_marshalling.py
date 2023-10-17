import json
import unittest

from automata import Automata


class TestAutomataSerializationMethods(unittest.TestCase):
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
        # Serialized version of the example automata
        self.serialized_example = json.dumps(
            {
                "A": ["0", "1", "2"],
                "X": ["x", "y", "z"],
                "f": {
                    "('0', 'x')": ["0", "1", "2"],
                    "('0', 'y')": ["1", "2"],
                    "('0', 'z')": ["2"],
                    "('1', 'y')": ["1", "2"],
                    "('2', 'z')": ["2"],
                },
                "a0": "0",
                "F": ["2"],
                "epsilon": "epsilon",
            }
        )

    def test_to_json(self):
        print(self.example_automata.to_json())
        print(self.serialized_example)
        serialized = self.example_automata.to_json()
        self.assertEqual(str(serialized), str(self.serialized_example))

    def test_from_json(self):
        deserialized = Automata.from_json(self.serialized_example)
        self.assertEqual(deserialized, self.example_automata)

    def test_round_trip_serialization(self):
        serialized = self.example_automata.to_json()
        deserialized = Automata.from_json(serialized)
        self.assertEqual(deserialized, self.example_automata)
