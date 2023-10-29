import json
from typing import Set, Dict

from graphviz import Digraph


class BuchiAutomaton:
    def __init__(
        self,
        states: Set[str],
        alphabet: Set[str],
        transitions: Dict[str, Dict[str, Set[str]]],
        initial_state: str,
        accepting_states: Set[str],
    ):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.accepting_states = accepting_states

        if states and (initial_state not in states):
            raise ValueError("Initial state must be in the set of states")

        if states and (not accepting_states.issubset(states)):
            raise ValueError("Accepting states must be a subset of states")

    def visualize(self, filename="buchi_automaton"):
        dot = Digraph(comment="Büchi Automaton")

        # Add states
        for state in self.states:
            if state in self.accepting_states:
                dot.node(state, shape="doublecircle")
            else:
                dot.node(state)

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(state, next_state, label=symbol)

        # Add initial state arrow
        dot.node("start", shape="plaintext")
        dot.edge("start", self.initial_state)

        dot.render(filename, view=True)

    def to_json(self) -> str:
        data = {
            "states": list(self.states),
            "alphabet": list(self.alphabet),
            "transitions": {
                state: {
                    symbol: list(next_states)
                    for symbol, next_states in symbol_dict.items()
                }
                for state, symbol_dict in self.transitions.items()
            },
            "initial_state": self.initial_state,
            "accepting_states": list(self.accepting_states),
        }
        return json.dumps(data, indent=4)

    @classmethod
    def from_json(cls, json_str: str):
        data = json.loads(json_str)
        return cls(
            states=set(data["states"]),
            alphabet=set(data["alphabet"]),
            transitions={
                state: {
                    symbol: set(next_states)
                    for symbol, next_states in symbol_dict.items()
                }
                for state, symbol_dict in data["transitions"].items()
            },
            initial_state=data["initial_state"],
            accepting_states=set(data["accepting_states"]),
        )

    def compose(self, other: 'BuchiAutomaton') -> 'BuchiAutomaton':
        # Create the set of states for the composed automaton
        composed_states = {(s1, s2) for s1 in self.states for s2 in other.states}

        # Create the alphabet for the composed automaton
        composed_alphabet = self.alphabet.intersection(other.alphabet)

        # Create the transitions for the composed automaton
        composed_transitions = dict()
        for (s1, s2) in composed_states:
            composed_transitions[(s1, s2)] = dict()
            for symbol in composed_alphabet:
                next_states1 = self.transitions.get(s1, {}).get(symbol, set())
                next_states2 = other.transitions.get(s2, {}).get(symbol, set())
                composed_transitions[(s1, s2)][symbol] = {(n1, n2) for n1 in next_states1 for n2 in next_states2}

        # Create the initial state for the composed automaton
        composed_initial_state = (self.initial_state, other.initial_state)

        # Create the set of accepting states for the composed automaton
        composed_accepting_states = {(s1, s2) for s1 in self.accepting_states for s2 in other.accepting_states}

        return BuchiAutomaton(
            composed_states,
            composed_alphabet,
            composed_transitions,
            composed_initial_state,
            composed_accepting_states
        )
