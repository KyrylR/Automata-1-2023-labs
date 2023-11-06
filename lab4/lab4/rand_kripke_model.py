import random
from itertools import product

# Define the number of states and the atomic propositions
num_states = 5
atomic_props = {"p", "q", "r"}


# Function to generate a random Kripke model
def generate_random_kripke_model(num_states, atomic_props):
    # Generate a random set of propositions for each state
    labelings = [
        {prop for prop in atomic_props if random.choice([True, False])}
        for _ in range(num_states)
    ]
    # Generate random transitions (for simplicity each state will have at least one transition to another state)
    transitions = {
        i: {j for j in range(num_states) if i != j and random.choice([True, False])}
        for i in range(num_states)
    }
    return labelings, transitions


def main():
    # Generate the Kripke model
    labelings, transitions = generate_random_kripke_model(num_states, atomic_props)

    # Display the generated Kripke model
    print(labelings, transitions)
