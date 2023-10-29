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

    def test_compose(self):
        states1 = {"q0", "q1"}
        alphabet1 = {"a", "b"}
        transitions1 = {
            "q0": {"a": {"q1"}, "b": {"q0"}},
            "q1": {"a": {"q1"}, "b": {"q0"}},
        }
        initial_state1 = "q0"
        accepting_states1 = {"q1"}
        automaton1 = BuchiAutomaton(
            states1, alphabet1, transitions1, initial_state1, accepting_states1
        )

        states2 = {"p0", "p1"}
        alphabet2 = {"a", "b"}
        transitions2 = {
            "p0": {"a": {"p1"}, "b": {"p0"}},
            "p1": {"a": {"p1"}, "b": {"p0"}},
        }
        initial_state2 = "p0"
        accepting_states2 = {"p1"}
        automaton2 = BuchiAutomaton(
            states2, alphabet2, transitions2, initial_state2, accepting_states2
        )

        composed_automaton = automaton1.compose(automaton2)

        expected_states = {("q0", "p0"), ("q0", "p1"), ("q1", "p0"), ("q1", "p1")}
        expected_alphabet = {"a", "b"}
        expected_transitions = {
            ("q0", "p0"): {"a": {("q1", "p1")}, "b": {("q0", "p0")}},
            ("q0", "p1"): {"a": {("q1", "p1")}, "b": {("q0", "p0")}},
            ("q1", "p0"): {"a": {("q1", "p1")}, "b": {("q0", "p0")}},
            ("q1", "p1"): {"a": {("q1", "p1")}, "b": {("q0", "p0")}},
        }
        expected_initial_state = ("q0", "p0")
        expected_accepting_states = {("q1", "p1")}

        self.assertEqual(composed_automaton.states, expected_states)
        self.assertEqual(composed_automaton.alphabet, expected_alphabet)
        self.assertEqual(composed_automaton.transitions, expected_transitions)
        self.assertEqual(composed_automaton.initial_state, expected_initial_state)
        self.assertEqual(composed_automaton.accepting_states, expected_accepting_states)
