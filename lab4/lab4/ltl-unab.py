# Define the LTL formula components
ltl_formula = "box p and diamond not q"
atomic_props = {"p", "q"}
closure = set()

# Closure includes the formula itself
closure.add(ltl_formula)

# Add subformulas of the LTL formula to the closure
closure.add("p")  # From box p
closure.add("not q")  # From diamond not q
closure.add("true")  # Since box p can be seen as p U true
closure.add("false")  # As a fundamental part of any closure

# The Until subformulas are implicit in the box and diamond operators
closure.add("box p")  # box p is equivalent to p U true
closure.add("diamond not q")  # diamond not q is equivalent to true U not q

# The algorithm also requires negations of all subformulas for completeness
closure.add("not box p")
closure.add("not diamond not q")
closure.add("not p")
closure.add("not true")
closure.add("not false")

# Define the states (A0) for the automaton based on the initial subformulas
# Since box p is globally true, and diamond not q means that not q should eventually be true
# we create an initial state where both box p and diamond not q are true
initial_states = {frozenset({"box p", "diamond not q"})}

# Define the empty set of transitions and accepting states
transitions = set()
accepting_states = set()

# Convert the closure into an immutable form for processing
closure = frozenset(closure)

# The workset initially contains the initial states
workset = initial_states.copy()


# Function to check if s' satisfies the rules R1-R2 given s and the closure of the LTL formula
def satisfies_r1_r2(s, s_prime, closure):
    # Implementing the rules as per the LTL-UNAB algorithm
    for formula in closure:
        # Rule R1: If an atomic proposition is in s, it must be in s'.
        if formula in atomic_props and formula in s and formula not in s_prime:
            return False

        # Rule R2 for Until formulas
        # A U B in s implies B in s or (A in s and A U B in s')
        if " U " in formula:
            A, B = formula.split(" U ")
            if formula in s and not (B in s or (A in s and formula in s_prime)):
                return False

        # Handling the negation of Until formulas
        if "not " in formula and " U " in formula.split("not ")[1]:
            not_formula = formula.split("not ")[1]
            A, B = not_formula.split(" U ")
            if formula in s and (
                B in s_prime or (A not in s and not_formula not in s_prime)
            ):
                return False

    return True


# Function to get the propositions that are true based on the current state and the closure
def get_true_propositions(state, closure):
    return {prop for prop in closure if prop in state}


# Function to compute the next state based on the current state and the rules
def compute_next_state(state, closure):
    next_states = set()
    for prop in atomic_props:
        for negation in ["", "not "]:
            possible_next_state = set(state)  # Start with the current state
            if f"{negation}{prop}" in closure:
                if negation:
                    possible_next_state.discard(prop)
                else:
                    possible_next_state.add(prop)
                if satisfies_r1_r2(state, possible_next_state, closure):
                    next_states.add(frozenset(possible_next_state))
    return next_states


# Function to compute the closure of an LTL formula
def compute_closure(atomic_props):
    # Initial closure contains the atomic propositions and their negations
    closure = set(atomic_props) | set(f"not {p}" for p in atomic_props)

    # Adding the LTL formulas themselves
    closure.add("box p")
    closure.add("diamond not q")

    # Add the sub-formulas of the LTL formulas
    closure.add("p")
    closure.add("not q")
    closure.add("true")  # Helper for box and diamond
    closure.add("false")  # Helper for negations

    # Negations of the main formulas
    closure.add("not box p")
    closure.add("not diamond not q")

    # Return the closure as a frozen set so it's immutable
    return frozenset(closure)


# Compute the closure for the formula "box p and diamond not q"
closure = compute_closure(atomic_props)

# Initialize sets for the LTL-UNAB algorithm
A = set()  # Set of states
F = set()  # Set of accepting states
f = set()  # Transition relation

# Initial states (A0) are those where both 'box p' and 'diamond not q' could be true
A0 = {frozenset({"box p", "diamond not q"})}

# Workset (C) starts with the initial states
C = set(A0)

# Implement the LTL-UNAB algorithm
while C:
    s = C.pop()
    A.add(s)

    # For the accepting states (F), we consider 'box p' (p U true) and 'diamond not q' (true U not q)
    if "box p" in s or "diamond not q" in s:
        F.add(s)

    # Compute transitions (f) for s
    for s_prime in compute_next_state(s, closure):
        # Transition function is a relation between states and the propositions that hold
        f.add((s, s_prime, frozenset(get_true_propositions(s_prime, closure))))
        if s_prime not in A:
            C.add(s_prime)

# Define Büchi Automaton (A, B(AP),f,A0,F)
LTL_Buchi_Automaton = (A, atomic_props, f, A0, F)

# Display the components of the Büchi Automaton
print(LTL_Buchi_Automaton)
