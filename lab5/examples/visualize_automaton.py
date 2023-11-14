import graphviz

from lab5.lab5.core import ClockRegion, State, transition_mapping, RegionAutomaton


def visualize_region_automaton(automaton, name="Region Automaton"):
    """
    Visualize the region automaton using Graphviz, with states broken down by clock regions.
    """
    dot = graphviz.Digraph(name)
    dot.attr(rankdir='LR')

    # Create a unique label for each state-region pair
    def create_state_label(state, clock_region):
        region_label = ", ".join(f"{k}{v}" for k, v in clock_region.constraints.items())
        return f"State {state.state_id}\n[{region_label}]"

    # Add nodes (states) to the graph
    for state in automaton.states:
        state_label = create_state_label(state, state.clock_region)
        if state in automaton.initial_states:
            dot.node(state_label, state_label, shape='doublecircle')
        else:
            dot.node(state_label, state_label, shape='circle')

    # Add edges (transitions) to the graph
    for from_state, to_state, action, clock_region in automaton.transitions:
        from_label = create_state_label(from_state, from_state.clock_region)
        to_label = create_state_label(to_state, clock_region)
        edge_label = f'{action}'
        dot.edge(from_label, to_label, label=edge_label)

    return dot


def format_clock_region(clock_region):
    return ", ".join(f"{k} {v}" for k, v in clock_region.constraints.items())


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
    (state_0, state_0, 'a', {'x': 1}),  # From state 0, on reading 'a', stay in state 0 with x = 1
    (state_0, state_1, 'b', {'y': 0}),  # From state 0, on reading 'b', move to state 1 with y < 1
    (state_1, state_0, 'a', {'x': 0}),  # From state 1, on reading 'a', move to state 0 with x < 1
    (state_1, state_2, 'b', {'y': 1}),  # From state 1, on reading 'b', move to state 2 with y = 1
    (state_2, state_0, 'a', {'x': 1}),  # From state 2, on reading 'a', move to state 0 with x = 1
    (state_2, state_2, 'b', {'y': 1}),  # From state 2, on reading 'b', stay in state 2 with y = 1
]

# Constructing the region automaton transitions
region_transitions = transition_mapping(original_transitions, states)

# Constructing the Region Automaton with defined states, initial states, and transitions
region_automaton = RegionAutomaton(states, initial_states, region_transitions)


def main():
    dot_original = visualize_region_automaton(region_automaton, "Region Automaton")
    dot_original.render('./lab5/results/region_automaton', format='png', cleanup=True)
