from typing import Set

from lab2 import MealyAutomata
from lab2.tests.test_data import (
    STATES,
    INPUT_ALPHABET,
    TRANSITIONS,
    OUTPUT_ALPHABET,
    INITIAL_STATE,
    OUTPUT_FUNCTION,
    FINAL_SYMBOLS,
)


def solve_linear_equations(equations):
    """
    Solve left linear equations of the form:
    Si = SjXj or SkXk or ...
    """

    # Deep copy the input equations to avoid modifying them in-place
    solved_equations = equations.copy()

    # Flag to check if we have made any updates in the current iteration
    updated = True

    while updated:
        updated = False

        # For each state in the equations
        for state, terms in solved_equations.items():
            new_terms = terms.copy()

            # For each term in the state's equation
            for term_state, term_symbols in terms.items():
                # If the term's state is not the current state and has its own equation
                if term_state != state and term_state in solved_equations:
                    for next_term_state, next_term_symbols in solved_equations[
                        term_state
                    ].items():
                        # Expand the term using its equation
                        if next_term_state not in new_terms:
                            new_terms[next_term_state] = []

                        for symbol in term_symbols:
                            for next_symbol in next_term_symbols:
                                # Check if expansion leads to infinite repetition
                                if (
                                    symbol + next_symbol
                                    not in new_terms[next_term_state]
                                ):
                                    new_terms[next_term_state].append(
                                        symbol + next_symbol
                                    )
                                    updated = True

            # Remove duplicates from the terms
            for term_state in new_terms:
                new_terms[term_state] = list(set(new_terms[term_state]))

            # Update the equation for the current state
            solved_equations[state] = new_terms

    # Return the solved equations
    return solved_equations


def solve_linear_equations_mealy(
    mealy_machine: MealyAutomata, final_symbols: Set[str]
) -> None:
    print("Mealy machine:")
    print(f"States: {mealy_machine.states}")
    print(f"Input alphabet: {mealy_machine.input_alphabet}")
    print(f"Output alphabet: {mealy_machine.output_alphabet}")
    print(f"Transitions: {mealy_machine.transitions}")
    print(f"Initial state: {mealy_machine.initial_state}")
    print(f"Output function: {mealy_machine.output_function}")

    # Build left linear equations Let's represent left linear equations as a list of mappings, where in mapping key
    # is a state and value is tuple. First element of tuple is a state from which we can get to the key state Second
    # element of tuple is a list of symbols which are used to get to the key state from the first element of tuple
    left_linear_equations = dict()
    for transition in mealy_machine.transitions:
        value = mealy_machine.transitions[transition]

        for symbol in value:
            key = value[symbol][0]
            equation = left_linear_equations.get(key, None)

            if equation is None:
                left_linear_equations[key] = dict()
                left_linear_equations[key][transition] = [symbol]
            else:
                nested_eq = left_linear_equations[key].get(transition, None)

                if nested_eq is None:
                    left_linear_equations[key][transition] = [symbol]
                else:
                    left_linear_equations[key][transition].append(symbol)

    print("Left linear equations:")
    print(left_linear_equations)

    # After solving left linear equations let's build SM.
    sm_equation = dict()
    for transition in mealy_machine.transitions:
        value = mealy_machine.transitions[transition]

        for symbol in value:
            output_symbol = value[symbol][1]

            if output_symbol not in final_symbols:
                continue

            print(
                f"Transition: {transition}, symbol: {symbol}, output symbol: {output_symbol}. State: {value[symbol][0]}"
            )

            state = value[symbol][0]
            equation = sm_equation.get(state, None)

            if equation is None:
                sm_equation[state] = dict()
                sm_equation[state][transition] = [symbol]
            else:
                nested_eq = sm_equation[state].get(transition, None)

                if nested_eq is None:
                    sm_equation[state][transition] = [symbol]
                else:
                    sm_equation[state][transition].append(symbol)

    print("SM equation:")
    print(sm_equation)


if __name__ == "__main__":
    # Create a Mealy machine from the test data
    mealy_machine = MealyAutomata(
        states=STATES,
        input_alphabet=INPUT_ALPHABET,
        output_alphabet=OUTPUT_ALPHABET,
        transitions=TRANSITIONS,
        initial_state=INITIAL_STATE,
        output_function=OUTPUT_FUNCTION,
    )

    # Debug the analysis problem for the Mealy machine
    solve_linear_equations_mealy(mealy_machine, FINAL_SYMBOLS)
