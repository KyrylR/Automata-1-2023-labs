import graphviz


# Function to visualize the LTL automaton
def visualize_ltl_automaton(ltl_states, ltl_transitions, ltl_accepting_states):
    dot = graphviz.Digraph(comment="LTL Automaton")

    # Add nodes to the graph
    for state in ltl_states:
        shape = "doublecircle" if state in ltl_accepting_states else "circle"
        dot.node(str(state), f"{state}", shape=shape)

    # Add edges to the graph
    for state, transitions in ltl_transitions.items():
        for inputs, next_state in transitions.items():
            label = ",".join(inputs) if inputs else "∅"
            dot.edge(str(state), str(next_state), label=label)

    return dot


ltl_states = {
    ("box_p", "diamond_q"),
    ("box_p", "not_diamond_q"),
    ("not_box_p", "diamond_q"),
    ("not_box_p", "not_diamond_q"),
}
ltl_transitions = {
    ("box_p", "not_diamond_q"): {
        ("p", "q"): ("box_p", "diamond_q"),
        ("p",): ("box_p", "not_diamond_q"),
        ("q",): ("box_p", "diamond_q"),
        (): ("not_box_p", "not_diamond_q"),
    },
    ("box_p", "diamond_q"): {
        ("p", "q"): ("box_p", "diamond_q"),
        ("p",): ("box_p", "diamond_q"),
        ("q",): ("box_p", "diamond_q"),
        (): ("not_box_p", "diamond_q"),
    },
    ("not_box_p", "diamond_q"): {
        ("p", "q"): ("not_box_p", "diamond_q"),
        ("p",): ("not_box_p", "diamond_q"),
        ("q",): ("not_box_p", "diamond_q"),
        (): ("not_box_p", "diamond_q"),
    },
    ("not_box_p", "not_diamond_q"): {
        ("p", "q"): ("not_box_p", "diamond_q"),
        ("p",): ("not_box_p", "not_diamond_q"),
        ("q",): ("not_box_p", "diamond_q"),
        (): ("not_box_p", "not_diamond_q"),
    },
}
ltl_accepting_states = {
    ("box_p", "diamond_q"),
    ("box_p", "not_diamond_q"),
    ("not_box_p", "diamond_q"),
}


def main():
    # Visualize the LTL automaton
    ltl_graph = visualize_ltl_automaton(
        ltl_states, ltl_transitions, ltl_accepting_states
    )
    ltl_graph.render("./lab4/results/ltl_automaton", format="png", cleanup=True)
