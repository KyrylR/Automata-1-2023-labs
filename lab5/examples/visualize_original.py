import graphviz

from lab5.lab5.core import ClockRegion, State, transition_mapping, RegionAutomaton


def visualize_original_automaton_with_times(states, initial_states, transitions, name="Original Automaton with Times"):
    """
    Visualize the original automaton using Graphviz with clock times specified in transitions.
    """
    dot = graphviz.Digraph(name)
    dot.attr(rankdir='LR')

    # Add nodes (states) to the graph
    for state in states:
        state_label = f"State {state.state_id}"
        if state in initial_states:
            dot.node(state_label, state_label, shape='doublecircle')
        else:
            dot.node(state_label, state_label, shape='circle')

    # Add edges (transitions) to the graph
    for from_state, to_state, action, constraint in transitions:
        from_label = f"State {from_state.state_id}"
        to_label = f"State {to_state.state_id}"
        # Convert the constraint dictionary into a string representation
        constraint_str = " ".join(f"{key}{value}" for key, value in constraint.items())
        edge_label = f'{action} [{constraint_str}]'
        dot.edge(from_label, to_label, label=edge_label)

    return dot

# Define clock regions for each state based on the provided constraints
clock_region_0 = ClockRegion({'x': '=1', 'y': '<1'})
clock_region_1 = ClockRegion({'x': '<1', 'y': '=1'})
clock_region_2 = ClockRegion({'x': '=1', 'y': '=1'})

# Define states and associate them with the corresponding clock regions
state_0 = State(0, clock_region_0)
state_1 = State(1, clock_region_1)
state_2 = State(2, clock_region_2)

# Defining the states and initial states
states = [state_0, state_1, state_2]
initial_states = [state_0]

# Define the original transitions based on the automaton description
original_transitions = [
    (state_0, state_0, 'a', {'x=': 1}),  # From state 0, on reading 'a', stay in state 0 with x = 1
    (state_0, state_1, 'b', {'y<': 1}),  # From state 0, on reading 'b', move to state 1 with y < 1
    (state_1, state_0, 'a', {'x<': 1}),  # From state 1, on reading 'a', move to state 0 with x < 1
    (state_1, state_2, 'b', {'y=': 1}),  # From state 1, on reading 'b', move to state 2 with y = 1
    (state_2, state_0, 'a', {'x=': 1}),  # From state 2, on reading 'a', move to state 0 with x = 1
    (state_2, state_2, 'b', {'y=': 1}),  # From state 2, on reading 'b', stay in state 2 with y = 1
]


def main():
    # Visualizing the original automaton
    dot_original_automaton = visualize_original_automaton_with_times(states, initial_states, original_transitions,
                                                          "Original Automaton")
    dot_original_automaton.render('./lab5/results/original_region_automaton', format='png', cleanup=True)
