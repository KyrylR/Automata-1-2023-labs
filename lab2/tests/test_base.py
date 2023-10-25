import unittest

from lab2 import MealyAutomata
from lab2.tests.test_data import STATES, INPUT_ALPHABET, OUTPUT_ALPHABET, TRANSITIONS, INITIAL_STATE, OUTPUT_FUNCTION


class TestMealyAutomataBaseClass(unittest.TestCase):
    def test_mealy_automata(self):
        # Create the Mealy machine
        machine = MealyAutomata(STATES, INPUT_ALPHABET, OUTPUT_ALPHABET, TRANSITIONS, INITIAL_STATE, OUTPUT_FUNCTION)

        # Test the machine with the given input sequence
        input_sequence = ['x', 'y', 'x', 'y']
        expected_output_sequence = ['v', 'u', 'u', 'v']
        actual_output_sequence = [machine.step(input_symbol) for input_symbol in input_sequence]

        # Assert that the expected output matches the actual output
        self.assertTrue(actual_output_sequence == expected_output_sequence)
