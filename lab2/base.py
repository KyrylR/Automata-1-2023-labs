from collections import defaultdict
from dataclasses import dataclass, field


@dataclass
class MooreAutomata:
    states: set
    input_alphabet: set
    output_alphabet: set
    transitions: dict
    initial_state: tuple
    final_states: set


@dataclass
class MealyAutomata:
    states: set
    input_alphabet: set
    output_alphabet: set
    transitions: dict
    initial_state: int
    output_function: callable = field(default=None)
    current_state: int = field(init=False)

    def __post_init__(self):
        self.current_state = self.initial_state

    def reset(self):
        self.current_state = self.initial_state

    def step(self, input_symbol):
        if input_symbol not in self.input_alphabet:
            raise ValueError("Input symbol not in input alphabet")
        if self.current_state not in self.states:
            raise ValueError("Current state not in list of states")

        next_state, output_symbol = self.transitions[self.current_state][input_symbol]
        self.current_state = next_state
        return output_symbol

    def to_moore(self, final_symbols):
        # Create an empty set for the states of the Moore machine.
        states = set()

        # Get the input and output alphabets from the Mealy machine.
        input_alphabet = self.input_alphabet
        output_alphabet = self.output_alphabet

        # Create a default dictionary for the transitions of the Moore machine.
        transitions = defaultdict(dict)

        # Create an empty set for the final states of the Moore machine.
        final_states = set()

        # Iterate through each state in the Mealy machine.
        for state in self.states:
            # Iterate through each input symbol in the Mealy machine.
            for input_symbol in self.input_alphabet:
                # Get the next state and output symbol for the current state and input symbol.
                next_state, output_symbol = self.transitions[state][input_symbol]

                # Create a new state for the Moore machine by combining the state and output symbol.
                new_state = (state, output_symbol)

                # Add the new state to the set of states.
                states.add(new_state)

                # Add a transition for the new state and input symbol.
                transitions[new_state][input_symbol] = (next_state, output_symbol)

                # If the output symbol is in the set of final symbols, add the new state to the set of final states.
                if output_symbol in final_symbols:
                    final_states.add(new_state)

        # Get the initial state for the Moore machine by combining the initial state of the Mealy machine with the
        # output function.
        initial_state = (self.initial_state, self.output_function[self.initial_state])

        # Create a Moore machine with the states, input alphabet, output alphabet, transitions, initial state,
        # and final states.
        moore_machine = MooreAutomata(
            states,
            input_alphabet,
            output_alphabet,
            transitions,
            initial_state,
            final_states,
        )

        # Return the Moore machine.
        return moore_machine
