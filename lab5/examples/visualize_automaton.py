import graphviz

from lab5.lab5.core import ClockRegion, State, transition_mapping, RegionAutomaton


def visualize_region_automaton(automaton, name="Region Automaton"):
    """
    Visualize the region automaton using Graphviz, with states broken down by clock regions.
    """
    dot = graphviz.Digraph(name)
    dot.attr(rankdir="LR")

    # Create a unique label for each state-region pair
    def create_state_label(state, clock_region):
        region_label = ", ".join(f"{k}{v}" for k, v in clock_region.constraints.items())
        return f"State {state.state_id}\n[{region_label}]"

    # Add nodes (states) to the graph
    for state in automaton.states:
        state_label = create_state_label(state, state.clock_region)
        if (
            str(state.state_id) in automaton.initial_states
            and str(state.state_id) in automaton.final_states
        ):
            dot.node(
                state_label,
                state_label,
                shape="doubleoctagon",
                style="filled",
                color="lightblue",
            )
        elif str(state.state_id) in automaton.initial_states:
            dot.node(
                state_label,
                state_label,
                shape="octagon",
                style="filled",
                color="lightgrey",
            )
        elif str(state.state_id) in automaton.final_states:
            dot.node(
                state_label,
                state_label,
                shape="doublecircle",
                style="filled",
                color="lightgreen",
            )
        else:
            dot.node(state_label, state_label, shape="circle")

    # Add edges (transitions) to the graph
    for from_state, to_state, action, clock_region in automaton.transitions:
        from_label = create_state_label(from_state, from_state.clock_region)
        to_label = create_state_label(to_state, clock_region)
        edge_label = f"{action}"
        dot.edge(from_label, to_label, label=edge_label)

    return dot


def format_clock_region(clock_region):
    return ", ".join(f"{k} {v}" for k, v in clock_region.constraints.items())


# Based on the given timed automaton, we first define the clock regions for each state and action
clock_regions = {
    "0_a": ClockRegion({"x": "=1"}),
    "0_b": ClockRegion({"y": "<1"}),
    "1_a": ClockRegion({"x": "<1"}),
    "1_b": ClockRegion({"y": "=1"}),
    "2_a": ClockRegion({"x": "=1"}),
    "2_b": ClockRegion({"y": "=1"}),
}

# Define the states with their respective clock regions
states = [
    State("0", clock_regions["0_a"]),
    State("0", clock_regions["0_b"]),
    State("1", clock_regions["1_a"]),
    State("1", clock_regions["1_b"]),
    State("2", clock_regions["2_a"]),
    State("2", clock_regions["2_b"]),
]

# Define the transitions based on the timed automaton
transitions = [
    ("0", "0", "a", {"x": 1}),  # From state 0 on reading 'a', x=1
    ("0", "1", "b", {"y": "<1"}),  # From state 0 on reading 'b', y<1
    ("1", "0", "a", {"x": "<1"}),  # From state 1 on reading 'a', x<1
    ("1", "2", "b", {"y": 1}),  # From state 1 on reading 'b', y=1
    ("2", "0", "a", {"x": 1}),  # From state 2 on reading 'a', x=1
    ("2", "2", "b", {"y": 1}),  # From state 2 on reading 'b', y=1
]

# Map the original transitions to the region automaton transitions
region_automaton_transitions = transition_mapping(transitions, states)

# Create the Region Automaton
region_automaton = RegionAutomaton(states, ["0"], ["1"], region_automaton_transitions)


def main():
    # print(region_automaton)
    dot_original = visualize_region_automaton(region_automaton, "Region Automaton")
    dot_original.render("./lab5/results/region_automaton", format="png", cleanup=True)
