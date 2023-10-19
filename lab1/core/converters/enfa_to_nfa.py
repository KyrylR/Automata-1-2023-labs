from core import Automata


class ENFAToNFAConverter:
    """
    Converter from Epsilon-Nondeterministic Finite Automata (ENFA) to
    Nondeterministic Finite Automata (NFA).

    Algorithm:
    ----------
    1. Initialize the starting state, transition function, and final states of the NFA.
    2. Begin with transitions from the starting state of the ENFA.
    3. Process each transition:
       - For non-epsilon transitions, handle direct transitions and transitions resulting from epsilon moves.
       - For epsilon transitions, handle direct epsilon transitions and transitions resulting from other epsilon moves.
    4. Return the resulting NFA.

    Pseudocode ENFA to NFA:

    Input: ENFA A = (A, X, f, a0, F)
    Output: NFA B = (A', X, f', a0', F')

    Method:
    a0' := a0;
    A' := {a0'}; f' := {}; F' := F intersection {a0};
    f'' := {}; W := {(a0, alpha, a') in f};
        while W != {} do
      choose (a1, alpha, a2) from W;
      if alpha != epsilon then
        add a2 to A'; add (a1, alpha, a2) to f'; if a2 in F then add a2 to F';
        for all a3 in f(a2, epsilon) do
          if (a1, alpha, a3) not in f' then add (a1, alpha, a3) to W;
        od
        for all x in X and a3 in f(a2, x) do
          if (a2, x, a3) not in f' then add (a2, x, a3) to W;
        od
      else /* alpha = epsilon */
        add (a1, alpha, a2) to f''; if a2 in F then add a0 to F';
        for all beta in X union {epsilon} and a3 in f(a2, beta) do
          if (a1, beta, a3) not in f' union f'' then add (a1, beta, a3) to W;
        od
    od
    """

    def __init__(self, enfa: Automata):
        self.enfa = enfa

    def convert_to_nfa(self) -> "Automata":
        """Convert the ENFA to an NFA."""
        # Initialize the starting state of the NFA.
        a0_prime = self.enfa.a0
        A_prime = {a0_prime}

        # Initialize the transition function of the NFA.
        f_prime = set()

        # Initialize the final states of the NFA.
        # Include the starting state if it's a final state in the ENFA.
        F_prime = self.enfa.F.intersection({self.enfa.a0})

        # Initialize the set of epsilon transitions.
        f_double_prime = set()

        # Begin with transitions from the starting state.
        W = {
            (a, alpha, a_prime)
            for (a, alpha), states in self.enfa.f.items()
            for a_prime in states
            if a == self.enfa.a0
        }

        # Process transitions until no new ones are added.
        while W:
            (a1, alpha, a2) = W.pop()

            # Handle non-epsilon transitions.
            if alpha != self.enfa.epsilon:
                A_prime.add(a2)
                f_prime.add((a1, alpha, a2))
                if a2 in self.enfa.F:
                    F_prime.add(a2)

                # Add transitions resulting from epsilon moves after the transition.
                for a3 in self.enfa.f.get((a2, self.enfa.epsilon), set()):
                    if (a1, alpha, a3) not in f_prime:
                        W.add((a1, alpha, a3))

                # Handle other transitions.
                for x in self.enfa.X:
                    for a3 in self.enfa.f.get((a2, x), set()):
                        if (a2, x, a3) not in f_prime:
                            W.add((a2, x, a3))
            else:  # Handle epsilon transitions.
                f_double_prime.add((a1, alpha, a2))

                # If the target of an epsilon transition is a final state,
                # the source state becomes a final state.
                if a2 in self.enfa.F:
                    F_prime.add(self.enfa.a0)

                # Add transitions resulting from epsilon moves.
                for beta in self.enfa.X.union({self.enfa.epsilon}):
                    for a3 in self.enfa.f.get((a2, beta), set()):
                        if (a1, beta, a3) not in f_prime.union(f_double_prime):
                            W.add((a1, beta, a3))

        # Convert the transition function set to a dictionary
        f_prime_dict = {}
        for a, x, b in f_prime:
            f_prime_dict.setdefault((a, x), set()).add(b)

        return Automata(
            A_prime, self.enfa.X, f_prime_dict, a0_prime, F_prime, self.enfa.epsilon
        )
