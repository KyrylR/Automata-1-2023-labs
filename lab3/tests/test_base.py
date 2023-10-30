import unittest

from lab3 import BuchiAutomaton


class TestBuchiAutomataBaseClass(unittest.TestCase):
    def test_json(self):
        states = {"q0", "q1"}
        alphabet = {"a", "b"}
        transitions = {
            "q0": {"a": {"q1"}, "b": {"q0"}},
            "q1": {"a": {"q1"}, "b": {"q0"}},
        }
        initial_state = "q0"
        accepting_states = {"q1"}
        automaton = BuchiAutomaton(
            states, alphabet, transitions, initial_state, accepting_states
        )
        json_str = automaton.to_json()
        automaton2 = BuchiAutomaton.from_json(json_str)
        self.assertEqual(automaton.states, automaton2.states)
        self.assertEqual(automaton.alphabet, automaton2.alphabet)
        self.assertEqual(automaton.transitions, automaton2.transitions)
        self.assertEqual(automaton.initial_state, automaton2.initial_state)
        self.assertEqual(automaton.accepting_states, automaton2.accepting_states)

    def test_empty_automaton(self):
        states = set()
        alphabet = set()
        transitions = dict()
        initial_state = ""
        accepting_states = set()
        automaton = BuchiAutomaton(
            states, alphabet, transitions, initial_state, accepting_states
        )
        self.assertEqual(automaton.states, set())
        self.assertEqual(automaton.alphabet, set())
        self.assertEqual(automaton.transitions, dict())
        self.assertEqual(automaton.initial_state, "")
        self.assertEqual(automaton.accepting_states, set())

    def test_invalid_initial_state(self):
        states = {"q0", "q1"}
        alphabet = {"a", "b"}
        transitions = {
            "q0": {"a": {"q1"}, "b": {"q0"}},
            "q1": {"a": {"q1"}, "b": {"q0"}},
        }
        initial_state = "q2"
        accepting_states = {"q1"}
        with self.assertRaises(ValueError):
            BuchiAutomaton(
                states, alphabet, transitions, initial_state, accepting_states
            )

    def test_invalid_accepting_state(self):
        states = {"q0", "q1"}
        alphabet = {"a", "b"}
        transitions = {
            "q0": {"a": {"q1"}, "b": {"q0"}},
            "q1": {"a": {"q1"}, "b": {"q0"}},
        }
        initial_state = "q0"
        accepting_states = {"q2"}
        with self.assertRaises(ValueError):
            BuchiAutomaton(
                states, alphabet, transitions, initial_state, accepting_states
            )
