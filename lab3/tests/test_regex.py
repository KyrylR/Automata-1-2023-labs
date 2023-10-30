import unittest

from lab3 import BuchiAutomaton


class GenerateRegexFromBuchiTest(unittest.TestCase):
    def test_approximate_regex_complex(self):
        # Define a Büchi automaton
        states = {"q0", "q1", "q2", "q3"}
        alphabet = {"a", "b", "c"}
        transitions = {
            "q0": {"a": {"q1"}, "b": {"q2"}},
            "q1": {"c": {"q3"}},
            "q2": {"c": {"q3"}},
            "q3": {"a": {"q3"}, "b": {"q2"}},
        }
        initial_state = "q0"
        accepting_states = {"q3"}
        automaton = BuchiAutomaton(
            states, alphabet, transitions, initial_state, accepting_states
        )

        # Generate an approximate regular expression from the automaton
        approximate_regex = automaton.to_approximate_regex()

        # Check the approximate regular expression
        self.assertEqual(approximate_regex, "(a)*|(bc)*")
