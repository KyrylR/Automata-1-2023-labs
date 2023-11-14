import graphviz

# Redefine the Kripke model according to the new design
kripke_labelings = [
    {"p", "r", "s"},  # State 0
    {"p", "q", "r"},  # State 1
    {"p", "r", "s"},  # State 2
    {"p", "q", "s"},  # State 3
    {"q", "r", "s"}   # State 4
]

kripke_transitions = {
    0: {1},
    1: {2, 4},
    2: {3},
    3: {3, 4},
    4: {4}
}

# Create a new graph for the Kripke model
dot = graphviz.Digraph(comment='New Kripke Model')

# Adding nodes (states) with labels
for i, labels in enumerate(kripke_labelings):
    dot.node(str(i), f'{i}: {", ".join(labels)}')

# Adding edges (transitions)
for state, transitions in kripke_transitions.items():
    for next_state in transitions:
        dot.edge(str(state), str(next_state))


def main():
    # Render the graph
    new_kripke_graph_path = './lab4/results/New_Kripke_Model.png'
    dot.render(new_kripke_graph_path, format='png', cleanup=True)

