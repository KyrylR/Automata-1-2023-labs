import unittest

from lab1 import Automata, ENFAToNFAConverter


class TestEnfaToNfaConversion(unittest.TestCase):
    def test_enfa_to_nfa_conversion(self):
        # Given ENFA
        A = {"0", "1", "2"}
        X = {"x", "y", "z"}
        f = {
            ("0", "x"): {"0"},
            ("1", "y"): {"1"},
            ("2", "z"): {"2"},
            ("0", "epsilon"): {"1"},
            ("1", "epsilon"): {"2"},
        }
        a0 = "0"
        F = {"2"}
        epsilon = "epsilon"

        automata = Automata(A, X, f, a0, F, epsilon)

        # Expected NFA
        expected_f_prime = {
            ("0", "x"): {"0", "1", "2"},
            ("0", "y"): {"1", "2"},
            ("0", "z"): {"2"},
            ("1", "y"): {"1", "2"},
            ("2", "z"): {"2"},
        }
        expected_a0_prime = "0"
        expected_F_prime = {"0", "2"}

        expected_automata = Automata(
            A, X, expected_f_prime, expected_a0_prime, expected_F_prime, epsilon
        )

        # Actual NFA
        actual_automata = ENFAToNFAConverter(automata).convert_to_nfa()

        # Assert that the actual NFA matches the expected NFA
        self.assertTrue(actual_automata == expected_automata)
