# Function to create an automaton for the LTL formula (box p or diamond q)
def create_ltl_automaton():
    # States of the automaton
    # We track two conditions: 'p' always true (box_p), and 'q' eventually true (diamond_q)
    # Initial state assumes both 'p' is always true and 'q' has not yet been seen
    states = {
        (
            "box_p",
            "not_diamond_q",
        ),  # Initial state: 'p' always true up to now, 'q' not seen
        ("box_p", "diamond_q"),  # 'p' always true, 'q' seen
        ("not_box_p", "diamond_q"),  # 'p' not always true, 'q' seen
        ("not_box_p", "not_diamond_q"),  # 'p' not always true, 'q' not seen
    }

    # Transitions for the automaton based on the presence of 'p' and 'q'
    # If 'p' is not seen, we move to a state where box_p is violated
    # If 'q' is seen, we move to a state where diamond_q is satisfied
    transitions = {
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
        ("not_box_p", "diamond_q"): {  # Once in these states, we stay there
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

    # Accepting states are those where 'q' is eventually true or 'p' is always true
    accepting_states = {
        ("box_p", "not_diamond_q"),
        ("box_p", "diamond_q"),
        ("not_box_p", "diamond_q"),
    }

    return states, transitions, accepting_states


def main():
    # Create the automaton for the LTL formula
    ltl_states, ltl_transitions, ltl_accepting_states = create_ltl_automaton()

    # Display the LTL automaton
    print(ltl_states, ltl_transitions, ltl_accepting_states)
