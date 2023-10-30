import json
from typing import Set, Dict, List

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
            state_str = str(state)  # Convert state to string
            if state in self.accepting_states:
                dot.node(state_str, shape="doublecircle")
            else:
                dot.node(state_str)

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(str(state), str(next_state), label=symbol)

        # Add initial state arrow
        dot.node("start", shape="plaintext")
        dot.edge("start", str(self.initial_state))

        # Render the graph to a file in PNG format
        dot.render(filename, format="png")

    def to_json(self) -> str:
        data = {
            "states": list(map(str, self.states)),
            "alphabet": list(self.alphabet),
            "transitions": {
                str(state): {
                    symbol: list(map(str, next_states))
                    for symbol, next_states in transitions.items()
                }
                for state, transitions in self.transitions.items()
            },
            "initial_state": str(self.initial_state),
            "accepting_states": list(map(str, self.accepting_states)),
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

    def concatenate(self, other: "BuchiAutomaton") -> "BuchiAutomaton":
        # Step 1: Construct bipoles B and C
        bipole_b = Bipole(self)
        bipole_c = Bipole(other)

        # Step 2: Apply the strong iteration operation to C
        strong_iteration_c = StrongIteration(bipole_c)

        # Step 3: Apply the concatenation operation to B and C'
        concatenation = Concatenation(bipole_b, strong_iteration_c)

        # Step 4: Return the new automaton A'
        return concatenation.to_buchi_automaton()

    def to_approximate_regex(self, max_length: int = 5) -> str:
        regexes = []
        for accepting_state in self.accepting_states:
            path = self.find_path(self.initial_state, accepting_state, max_length)
            if path:
                regex = self.path_to_regex(path)
                regexes.append(regex)
        approximate_regex = "|".join(regexes)
        return approximate_regex

    def find_path(self, start_state: str, end_state: str, max_length: int) -> List[str]:
        visited = set()
        queue = [(start_state, [])]
        while queue:
            state, path = queue.pop(0)
            if state in visited:
                continue
            visited.add(state)
            new_path = path + [state]
            if state == end_state and len(new_path) <= max_length:
                return new_path
            if len(new_path) < max_length:
                for symbol, next_states in self.transitions.get(state, {}).items():
                    for next_state in next_states:
                        if next_state not in visited:
                            queue.append((next_state, new_path))
        return []

    def path_to_regex(self, path: List[str]) -> str:
        regex = ""
        for i in range(len(path) - 1):
            state = path[i]
            next_state = path[i + 1]
            for symbol, transitions in self.transitions.get(state, {}).items():
                if next_state in transitions:
                    regex += symbol
                    break
        return regex


class Bipole:
    def __init__(self, automaton: BuchiAutomaton):
        self.automaton = automaton
        self.entry_states = set()
        self.exit_states = set()
        self.construct_bipole()

    def construct_bipole(self):
        # Entry states are the initial states of the automaton
        self.entry_states.add(self.initial_state)

        # Exit states are the accepting states of the automaton
        self.exit_states = self.accepting_states.copy()

    def __repr__(self):
        return (
            f"Bipole(\nAutomaton: {self.automaton},\n"
            f"Entry States: {self.entry_states},\n"
            f"Exit States: {self.exit_states}\n)"
        )

    @property
    def states(self):
        return self.automaton.states

    @property
    def alphabet(self):
        return self.automaton.alphabet

    @property
    def transitions(self):
        return self.automaton.transitions

    @property
    def initial_state(self):
        return self.automaton.initial_state

    @property
    def accepting_states(self):
        return self.automaton.accepting_states


class StrongIteration:
    def __init__(self, bipole: Bipole):
        self.bipole = bipole
        self.transitions = self.bipole.transitions.copy()
        self.accepting_states = self.bipole.accepting_states.copy()  # Added this line
        self.construct_strong_iteration()

    def construct_strong_iteration(self):
        for exit_state in self.exit_states:
            for entry_state in self.entry_states:
                if exit_state != entry_state:
                    self.add_transition(exit_state, entry_state)

    def add_transition(self, from_state, to_state):
        existing_symbols = self.transitions.get(from_state, {}).keys()
        if existing_symbols:
            symbol = next(iter(existing_symbols))  # take any existing symbol
        else:
            symbol = next(iter(self.alphabet))  # take any symbol from the alphabet
        if from_state not in self.transitions:
            self.transitions[from_state] = {}
        if symbol not in self.transitions[from_state]:
            self.transitions[from_state][symbol] = set()
        self.transitions[from_state][symbol].add(to_state)

    def __repr__(self):
        return f"StrongIteration(\nBipole: {self.bipole}\n)"

    @property
    def states(self):
        return self.bipole.states

    @property
    def alphabet(self):
        return self.bipole.alphabet

    @property
    def entry_states(self):
        return self.bipole.entry_states

    @property
    def exit_states(self):
        return self.bipole.exit_states


class Concatenation:
    def __init__(self, bipole_b: Bipole, strong_iteration_c: StrongIteration):
        self.bipole_b = bipole_b
        self.strong_iteration_c = strong_iteration_c
        self.states = set()
        self.alphabet = set()
        self.transitions = dict()
        self.initial_state = None
        self.accepting_states = set()
        self.construct_concatenation()

    def construct_concatenation(self):
        # Step 2: Create the new automaton A
        self.states = self.bipole_b.states | self.strong_iteration_c.states
        self.alphabet = self.bipole_b.alphabet & self.strong_iteration_c.alphabet
        self.initial_state = self.bipole_b.initial_state
        self.accepting_states = self.strong_iteration_c.accepting_states

        # Step 3: Define the transition function
        for state_b in self.bipole_b.states:
            for state_c in self.strong_iteration_c.states:
                state_a = (state_b, state_c)
                self.transitions[state_a] = dict()
                for symbol in self.alphabet:
                    next_states_b = self.bipole_b.transitions.get(state_b, {}).get(
                        symbol, set()
                    )
                    next_states_c = self.strong_iteration_c.transitions.get(
                        state_c, {}
                    ).get(symbol, set())
                    self.transitions[state_a][symbol] = set()
                    if state_b in self.bipole_b.accepting_states:
                        for next_state_c in next_states_c:
                            self.transitions[state_a][symbol].add(
                                (state_b, next_state_c)
                            )
                    else:
                        for next_state_b in next_states_b:
                            for next_state_c in next_states_c:
                                self.transitions[state_a][symbol].add(
                                    (next_state_b, next_state_c)
                                )

    def to_buchi_automaton(self) -> BuchiAutomaton:
        return BuchiAutomaton(
            self.states,
            self.alphabet,
            self.transitions,
            self.initial_state,
            self.accepting_states,
        )

    def __repr__(self):
        return f"Concatenation(\nBipole B: {self.bipole_b}\nStrong Iteration C: {self.strong_iteration_c}\n)"
