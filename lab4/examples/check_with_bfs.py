from collections import deque


# Function to perform a breadth-first search on the product automaton to find a path from initial to accepting states
def bfs_search(product_transitions, product_initial_states, product_accepting_states):
    # Queue for BFS
    queue = deque(product_initial_states)
    # Set to keep track of visited states
    visited = set(product_initial_states)
    # Dictionary to store the path
    path = {
        state: None for state in product_initial_states
    }  # None indicates no predecessor

    # Perform BFS
    while queue:
        current_state = queue.popleft()

        # If the current state is an accepting state, construct the path back to the initial state
        if current_state in product_accepting_states:
            path_to_accepting = []
            while current_state is not None:
                path_to_accepting.append(current_state)
                current_state = path[current_state]
            return True, path_to_accepting[::-1]  # Return the reversed path

        # Get the next possible states from the current state
        next_states = product_transitions.get(current_state, set())
        for next_state in next_states:
            if next_state not in visited:
                visited.add(next_state)
                queue.append(next_state)
                path[
                    next_state
                ] = current_state  # Set the predecessor for the next state

    # If no accepting state is found, return False (the formula is not satisfied)
    return False, None


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
    # Perform the search for a path from initial to accepting states in the product automaton
    is_satisfied, path_to_accepting = bfs_search(
        product_transitions, product_initial_states, product_accepting_states
    )

    # Display the result of the check
    print(is_satisfied, path_to_accepting)
