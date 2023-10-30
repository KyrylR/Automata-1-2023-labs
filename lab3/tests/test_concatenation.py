import unittest

from lab3 import BuchiAutomaton


class TestBuchiAutomataConcatenationClass(unittest.TestCase):
    def test_concatenation(self):
        # Define the first automaton A
        states_a = {"q0", "q1"}
        alphabet_a = {"a", "b"}
        transitions_a = {
            "q0": {"a": {"q1"}},
            "q1": {"b": {"q0"}},
        }
        initial_state_a = "q0"
        accepting_states_a = {"q1"}
        automaton_a = BuchiAutomaton(
            states_a, alphabet_a, transitions_a, initial_state_a, accepting_states_a
        )

        # Define the second automaton A1
        states_a1 = {"s0", "s1"}
        alphabet_a1 = {"a", "b"}
        transitions_a1 = {
            "s0": {"a": {"s1"}},
            "s1": {"b": {"s0"}},
        }
        initial_state_a1 = "s0"
        accepting_states_a1 = {"s1"}
        automaton_a1 = BuchiAutomaton(
            states_a1,
            alphabet_a1,
            transitions_a1,
            initial_state_a1,
            accepting_states_a1,
        )

        # Concatenate the two automata
        concatenated_automaton = automaton_a.concatenate(automaton_a1)

        # Check the properties of the concatenated automaton
        self.assertEqual(
            concatenated_automaton.initial_state, automaton_a.initial_state
        )
        self.assertEqual(
            concatenated_automaton.accepting_states, automaton_a1.accepting_states
        )
        self.assertEqual(
            concatenated_automaton.alphabet,
            automaton_a.alphabet & automaton_a1.alphabet,
        )

        # Check the transitions of the concatenated automaton
        for state_a, transitions_a in concatenated_automaton.transitions.items():
            state_b, state_c = state_a
            for symbol, next_states_a in transitions_a.items():
                if state_b in automaton_a.accepting_states:
                    next_states_c = automaton_a1.transitions.get(state_c, {}).get(
                        symbol, set()
                    )
                    for next_state_c in next_states_c:
                        self.assertIn((state_b, next_state_c), next_states_a)
                else:
                    next_states_b = automaton_a.transitions.get(state_b, {}).get(
                        symbol, set()
                    )
                    next_states_c = automaton_a1.transitions.get(state_c, {}).get(
                        symbol, set()
                    )
                    for next_state_b in next_states_b:
                        for next_state_c in next_states_c:
                            self.assertIn((next_state_b, next_state_c), next_states_a)
