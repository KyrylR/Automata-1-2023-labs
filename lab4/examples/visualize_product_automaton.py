import graphviz

# Redefine the Kripke model according to the new design
kripke_labelings = [
    {"p", "r", "s"},  # State 0
    {"p", "q", "r"},  # State 1
    {"p", "r", "s"},  # State 2
    {"p", "q", "s"},  # State 3
    {"q", "r", "s"},  # State 4
]

kripke_transitions = {0: {1}, 1: {2, 4}, 2: {3}, 3: {3, 4}, 4: {4}}


# Define the Büchi automaton states and transitions
buchi_states = ["S0", "S1", "S2"]


# Function to determine the next Büchi state based on current Büchi state and Kripke state labeling
def buchi_transition(buchi_state, kripke_label):
    if buchi_state == "S0":
        if "p" not in kripke_label:
            return "S1"
        elif "q" in kripke_label:
            return "S2"
        else:
            return "S0"
    elif buchi_state == "S1":
        return "S1"
    elif buchi_state == "S2":
        return "S2"
    else:
        raise ValueError("Invalid Büchi state")


# Constructing the product states and transitions
product_states = []
product_transitions = {}

for k_state in range(len(kripke_labelings)):
    for b_state in buchi_states:
        product_state = (k_state, b_state)
        product_states.append(product_state)

        # Compute transitions for each product state
        product_transitions[product_state] = set()
        for next_k_state in kripke_transitions[k_state]:
            next_b_state = buchi_transition(b_state, kripke_labelings[next_k_state])
            product_transitions[product_state].add((next_k_state, next_b_state))


def main():
    # Enhancing the graph with more details, highlighting initial and accepting states

    # Redefining the graph
    dot = graphviz.Digraph(
        comment="Enhanced Direct Product of Kripke Model and Büchi Automaton"
    )
    dot.attr(rankdir="LR")  # Left to Right graph

    # Adding nodes (product states) with specific attributes for initial and accepting states
    for state in product_states:
        # Check if it's an initial or accepting state
        is_initial = state[1] == "S0"
        is_accepting = state[1] == "S1" and "q" not in kripke_labelings[state[0]]

        # Define node attributes based on state type
        if is_initial and is_accepting:
            dot.node(
                str(state),
                f"{state}\n(Initial, Accepting)",
                shape="doubleoctagon",
                style="filled",
                color="lightblue",
            )
        elif is_initial:
            dot.node(
                str(state),
                f"{state}\n(Initial)",
                shape="octagon",
                style="filled",
                color="lightgrey",
            )
        elif is_accepting:
            dot.node(
                str(state),
                f"{state}\n(Accepting)",
                shape="doublecircle",
                style="filled",
                color="lightgreen",
            )
        else:
            dot.node(str(state), f"{state}")

    # Adding edges (product transitions)
    for state, transitions in product_transitions.items():
        for next_state in transitions:
            # Label for the transition
            label = (
                f"Kripke: {state[0]}→{next_state[0]}\nBüchi: {state[1]}→{next_state[1]}"
            )
            dot.edge(str(state), str(next_state), label=label)

    # Render the graph with enhanced details
    enhanced_graph_path = "./lab4/results/Enhanced_Product_Kripke_Buchi.png"
    dot.render(enhanced_graph_path, format="png", cleanup=True)
