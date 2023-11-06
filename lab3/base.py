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

    def to_approximate_regex(self) -> str:
        """
        Generate an approximate regular expression that represents the language
        accepted by the Büchi automaton.
        """
        sccs = self._find_strongly_connected_components()
        accepting_sccs = [
            scc for scc in sccs if any(state in self.accepting_states for state in scc)
        ]
        regexes = [self._scc_to_regex(scc) for scc in accepting_sccs]
        approximate_regex = "|".join(regexes)
        return approximate_regex

    def _find_strongly_connected_components(self) -> List[Set[str]]:
        """
        Find the strongly connected components (SCCs) of the automaton using Tarjan's algorithm.
        """
        index_counter = [0]
        stack = []
        lowlinks = {}
        index = {}
        result = []

        def strongconnect(node):
            index[node] = index_counter[0]
            lowlinks[node] = index_counter[0]
            index_counter[0] += 1
            stack.append(node)

            successors = set()
            for symbol, next_states in self.transitions.get(node, {}).items():
                successors.update(next_states)
            for successor in successors:
                if successor not in index:
                    strongconnect(successor)
                    lowlinks[node] = min(lowlinks[node], lowlinks[successor])
                elif successor in stack:
                    lowlinks[node] = min(lowlinks[node], index[successor])

            if lowlinks[node] == index[node]:
                connected_component = set()
                while True:
                    successor = stack.pop()
                    connected_component.add(successor)
                    if successor == node:
                        break
                component = tuple(connected_component)
                result.append(component)

        for node in self.states:
            if node not in index:
                strongconnect(node)

        return result

    def _scc_to_regex(self, scc: Set[str]) -> str:
        """
        Convert a strongly connected component (SCC) into a regular expression.
        """
        cycles = self._find_cycles_in_scc(scc)
        cycle_regexes = [self._cycle_to_regex(cycle) for cycle in cycles]
        scc_regex = "|".join(cycle_regexes)
        return scc_regex

    def _find_cycles_in_scc(self, scc: Set[str]) -> List[List[str]]:
        """
        Find cycles in the SCC using a depth-first search (DFS) algorithm.
        """
        cycles = []

        def dfs(node, visited, stack):
            visited.add(node)
            stack.append(node)

            for symbol, next_states in self.transitions.get(node, {}).items():
                for next_state in next_states:
                    if next_state in scc:
                        if next_state not in visited:
                            dfs(next_state, visited, stack)
                        else:
                            cycle_start_index = stack.index(next_state)
                            cycle = stack[cycle_start_index:]
                            cycles.append(cycle)

            stack.pop()

        visited = set()
        for state in scc:
            if state not in visited:
                dfs(state, visited, [])

        return cycles

    def _cycle_to_regex(self, cycle: List[str]) -> str:
        """
        Convert a cycle into a regular expression.
        """
        regex = ""
        for i in range(len(cycle)):
            state = cycle[i]
            next_state = cycle[(i + 1) % len(cycle)]
            for symbol, next_states in self.transitions.get(state, {}).items():
                if next_state in next_states:
                    regex += symbol
        cycle_regex = f"({regex})*"
        return cycle_regex


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

    def visualize(self, filename="bipole"):
        dot = Digraph(comment="Bipole")

        # Add states
        for state in self.states:
            state_str = str(state)
            if state in self.accepting_states:
                dot.node(state_str, shape="doublecircle")
            else:
                dot.node(state_str)

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(str(state), str(next_state), label=symbol)

        # Add entry states
        for entry_state in self.entry_states:
            dot.node(str(entry_state), style="filled", fillcolor="green")

        # Add exit states
        for exit_state in self.exit_states:
            dot.node(str(exit_state), style="filled", fillcolor="red")

        # Render the graph to a file in PNG format
        dot.render(filename, format="png")

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

    def visualize(self, filename="strong_iteration"):
        dot = Digraph(comment="StrongIteration")

        # Add states
        for state in self.states:
            state_str = str(state)
            if state in self.accepting_states:
                dot.node(state_str, shape="doublecircle")
            else:
                dot.node(state_str)

        # Add transitions
        for state, transitions in self.transitions.items():
            for symbol, next_states in transitions.items():
                for next_state in next_states:
                    dot.edge(str(state), str(next_state), label=symbol)

        # Add entry states with a green fill
        for entry_state in self.entry_states:
            dot.node(str(entry_state), style="filled", fillcolor="green")

        # Add exit states with a blue fill
        for exit_state in self.exit_states:
            dot.node(str(exit_state), style="filled", fillcolor="blue")

        # Render the graph to a file in PNG format
        dot.render(filename, format="png")

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
        self.states = {
            (state_b, state_c)
            for state_b in self.bipole_b.states
            for state_c in self.strong_iteration_c.states
        }
        self.alphabet = self.bipole_b.alphabet & self.strong_iteration_c.alphabet
        self.initial_state = (
            self.bipole_b.initial_state,
            next(iter(self.strong_iteration_c.entry_states)),
        )
        self.accepting_states = {
            (state_b, state_c)
            for state_b in self.bipole_b.states
            for state_c in self.strong_iteration_c.accepting_states
        }

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
