import graphviz


# Function to visualize the direct product
def visualize_direct_product(
    product_states,
    product_transitions,
    product_initial_states,
    product_accepting_states,
):
    dot = graphviz.Digraph(comment="Direct Product Automaton")

    # Add all states to the graph
    for state in product_states:
        if state in product_accepting_states:
            # Accepting states are doublecircles
            dot.node(str(state), shape="doublecircle")
        else:
            # Non-accepting states are circles
            dot.node(str(state), shape="circle")

    # Highlight initial states with a different color
    for init_state in product_initial_states:
        dot.node(str(init_state), str(init_state), color="green")

    # Add transitions to the graph
    for from_state, to_states in product_transitions.items():
        for to_state in to_states:
            dot.edge(str(from_state), str(to_state))

    return dot


product_states = {
    (0, ("box_p", "diamond_q")),
    (0, ("box_p", "not_diamond_q")),
    (0, ("not_box_p", "diamond_q")),
    (0, ("not_box_p", "not_diamond_q")),
    (1, ("box_p", "diamond_q")),
    (1, ("box_p", "not_diamond_q")),
    (1, ("not_box_p", "diamond_q")),
    (1, ("not_box_p", "not_diamond_q")),
    (2, ("box_p", "diamond_q")),
    (2, ("box_p", "not_diamond_q")),
    (2, ("not_box_p", "diamond_q")),
    (2, ("not_box_p", "not_diamond_q")),
    (3, ("box_p", "diamond_q")),
    (3, ("box_p", "not_diamond_q")),
    (3, ("not_box_p", "diamond_q")),
    (3, ("not_box_p", "not_diamond_q")),
    (4, ("box_p", "diamond_q")),
    (4, ("box_p", "not_diamond_q")),
    (4, ("not_box_p", "diamond_q")),
    (4, ("not_box_p", "not_diamond_q")),
}
product_transitions = {
    (4, ("box_p", "not_diamond_q")): {
        (0, ("not_box_p", "not_diamond_q")),
        (1, ("box_p", "not_diamond_q")),
        (1, ("not_box_p", "not_diamond_q")),
        (2, ("box_p", "not_diamond_q")),
        (2, ("not_box_p", "not_diamond_q")),
    },
    (4, ("box_p", "diamond_q")): {
        (0, ("not_box_p", "diamond_q")),
        (1, ("box_p", "diamond_q")),
        (1, ("not_box_p", "diamond_q")),
        (2, ("box_p", "diamond_q")),
        (2, ("not_box_p", "diamond_q")),
    },
    (0, ("not_box_p", "not_diamond_q")): {
        (3, ("not_box_p", "diamond_q")),
        (3, ("not_box_p", "not_diamond_q")),
    },
    (2, ("not_box_p", "not_diamond_q")): {
        (4, ("not_box_p", "diamond_q")),
        (4, ("not_box_p", "not_diamond_q")),
    },
    (1, ("box_p", "not_diamond_q")): {
        (3, ("box_p", "diamond_q")),
        (3, ("not_box_p", "not_diamond_q")),
        (4, ("box_p", "diamond_q")),
        (4, ("not_box_p", "not_diamond_q")),
    },
    (1, ("box_p", "diamond_q")): {
        (3, ("box_p", "diamond_q")),
        (3, ("not_box_p", "diamond_q")),
        (4, ("box_p", "diamond_q")),
        (4, ("not_box_p", "diamond_q")),
    },
    (0, ("not_box_p", "diamond_q")): {(3, ("not_box_p", "diamond_q"))},
    (2, ("not_box_p", "diamond_q")): {(4, ("not_box_p", "diamond_q"))},
    (3, ("box_p", "not_diamond_q")): set(),
    (3, ("box_p", "diamond_q")): set(),
    (4, ("not_box_p", "not_diamond_q")): {
        (0, ("not_box_p", "not_diamond_q")),
        (1, ("not_box_p", "not_diamond_q")),
        (2, ("not_box_p", "not_diamond_q")),
    },
    (4, ("not_box_p", "diamond_q")): {
        (0, ("not_box_p", "diamond_q")),
        (1, ("not_box_p", "diamond_q")),
        (2, ("not_box_p", "diamond_q")),
    },
    (1, ("not_box_p", "not_diamond_q")): {
        (3, ("not_box_p", "diamond_q")),
        (3, ("not_box_p", "not_diamond_q")),
        (4, ("not_box_p", "diamond_q")),
        (4, ("not_box_p", "not_diamond_q")),
    },
    (1, ("not_box_p", "diamond_q")): {
        (3, ("not_box_p", "diamond_q")),
        (4, ("not_box_p", "diamond_q")),
    },
    (3, ("not_box_p", "not_diamond_q")): set(),
    (3, ("not_box_p", "diamond_q")): set(),
    (0, ("box_p", "not_diamond_q")): {
        (3, ("box_p", "diamond_q")),
        (3, ("not_box_p", "not_diamond_q")),
    },
    (0, ("box_p", "diamond_q")): {
        (3, ("box_p", "diamond_q")),
        (3, ("not_box_p", "diamond_q")),
    },
    (2, ("box_p", "not_diamond_q")): {
        (4, ("box_p", "diamond_q")),
        (4, ("not_box_p", "not_diamond_q")),
    },
    (2, ("box_p", "diamond_q")): {
        (4, ("box_p", "diamond_q")),
        (4, ("not_box_p", "diamond_q")),
    },
}
product_initial_states = {
    (0, ("box_p", "diamond_q")),
    (0, ("box_p", "not_diamond_q")),
    (1, ("box_p", "diamond_q")),
    (1, ("box_p", "not_diamond_q")),
    (2, ("box_p", "diamond_q")),
    (2, ("box_p", "not_diamond_q")),
    (3, ("box_p", "diamond_q")),
    (3, ("box_p", "not_diamond_q")),
    (4, ("box_p", "diamond_q")),
    (4, ("box_p", "not_diamond_q")),
}
product_accepting_states = {
    (0, ("not_box_p", "diamond_q")),
    (1, ("box_p", "diamond_q")),
    (1, ("box_p", "not_diamond_q")),
    (1, ("not_box_p", "diamond_q")),
    (2, ("box_p", "diamond_q")),
    (2, ("box_p", "not_diamond_q")),
    (2, ("not_box_p", "diamond_q")),
    (3, ("box_p", "diamond_q")),
    (3, ("not_box_p", "diamond_q")),
    (4, ("box_p", "diamond_q")),
    (4, ("not_box_p", "diamond_q")),
}


def main():
    # Visualize the product automaton
    # Create a visualization of the direct product
    dot = visualize_direct_product(
        product_states,
        product_transitions,
        product_initial_states,
        product_accepting_states,
    )

    # Render the visualization
    dot.render("./lab4/results/product_automaton", format="png", cleanup=True)
