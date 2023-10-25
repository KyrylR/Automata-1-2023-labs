import unittest

from lab2 import MealyAutomata
from lab2.tests.test_data import STATES, INPUT_ALPHABET, OUTPUT_ALPHABET, TRANSITIONS, INITIAL_STATE, OUTPUT_FUNCTION, FINAL_SYMBOLS


class TestConvertMealyToMoore(unittest.TestCase):
    def test_convert_mealy_to_moore(self):
        mealy_machine = MealyAutomata(STATES, INPUT_ALPHABET, OUTPUT_ALPHABET, TRANSITIONS, INITIAL_STATE,
                                      OUTPUT_FUNCTION)
        moore_machine = mealy_machine.to_moore(FINAL_SYMBOLS)

        assert (1, 'v') in moore_machine.states
        assert (4, 'u') in moore_machine.states
        assert (2, 'v') in moore_machine.states
        assert (3, 'u') in moore_machine.states
        assert (4, 'u') in moore_machine.final_states
        assert (3, 'u') in moore_machine.final_states
        assert (1, 'v') not in moore_machine.final_states
        assert (2, 'v') not in moore_machine.final_states

