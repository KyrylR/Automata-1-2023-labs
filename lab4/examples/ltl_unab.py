import graphviz

# Initialize the components of the Büchi automaton for the LTL formula using LTL-UNAB algorithm

# Initial States (A0)
initial_state = frozenset({"square p", "diamond not q"})

# All States (A), Transition Function (f), Valid States (F)
states = set([initial_state])
transitions = {}
valid_states = set()  # States where "diamond not q" is eventually met

# Working Set (C)
working_set = set([initial_state])

# Rules R1 and R2
while working_set:
    current_state = working_set.pop()

    # Determine the next states based on the current state
    # Applying R1 and R2
    next_states = set()

    if "square p" in current_state and "diamond not q" in current_state:
        next_states.add(frozenset({"p", "square p", "not q", "diamond not q"}))
        next_states.add(
            frozenset({"p", "square p", "diamond not q"})
        )  # Case where q is true
        valid_states.add(frozenset({"p", "square p", "not q", "diamond not q"}))

    # Considering the empty symbol
    next_states.add(current_state)  # Self-loop for the empty symbol

    # Add the next states to the working set if they are not already explored
    for state in next_states:
        if state not in states:
            working_set.add(state)
            states.add(state)

    # Update the transition function
    transitions[current_state] = next_states

# Enhancing the graph with more details and making it more balanced

# Reinitialize the graph
dot = graphviz.Digraph(comment="Enhanced Büchi Automaton for LTL Formula")
dot.attr(rankdir="LR")  # Left to Right graph for a more balanced look

# Adding states to the graph with more details
for state in states:
    # Create a readable label for each state
    state_label = ", ".join(state)
    if state in valid_states:
        # Valid states with double circles
        dot.node(
            str(state),
            f"{state_label}\n(Valid)",
            shape="doublecircle",
            style="filled",
            color="lightgreen",
        )
    else:
        # Other states
        dot.node(str(state), state_label)

# Adding transitions to the graph
for state, next_states in transitions.items():
    for next_state in next_states:
        # Label each transition with the relevant atomic propositions
        transition_label = "p" if "p" in next_state else ""
        transition_label += (
            ", ¬q"
            if "not q" in next_state
            else ", q"
            if transition_label != ""
            else "q"
        )
        if next_state == state:
            # Label for the empty symbol specifying 'p' and 'q' remain unchanged
            transition_label += ", ε"
        dot.edge(str(state), str(next_state), label=transition_label)


def main():
    # Render the graph
    enhanced_buchi_graph_path = (
        "./lab4/results/Enhanced_Buchi_Automaton_LTL_Formula_Box_p_and_Diamond_not_q"
    )
    dot.render(enhanced_buchi_graph_path, format="png", cleanup=True)
