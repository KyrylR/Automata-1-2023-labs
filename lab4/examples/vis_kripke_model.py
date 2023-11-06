import graphviz


# Function to visualize the Kripke model
def visualize_kripke_model(labelings, transitions):
    dot = graphviz.Digraph(comment="Kripke Model")

    # Add nodes to the graph
    for state, props in enumerate(labelings):
        props_label = ",".join(props) if props else "∅"
        dot.node(str(state), f"{state}\n{{{props_label}}}", shape="circle")

    # Add edges to the graph
    for state, next_states in transitions.items():
        for next_state in next_states:
            dot.edge(str(state), str(next_state))

    return dot


labelings = [{"r"}, {"p"}, {"p"}, {"q", "r"}, {"q", "r"}]
transitions = {0: {3}, 1: {3, 4}, 2: {4}, 3: set(), 4: {0, 1, 2}}


def main():
    # Visualize the Kripke model
    kripke_graph = visualize_kripke_model(labelings, transitions)
    kripke_graph.render("./lab4/results/kripke_model", format="png", cleanup=True)
