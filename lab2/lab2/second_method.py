class Automaton:
    def __init__(self, states, alphabet, transitions, initial_state, final_states):
        self.states = states
        self.alphabet = alphabet
        self.transitions = transitions
        self.initial_state = initial_state
        self.final_states = final_states

    def eliminate_state(self, state):
        """
        Eliminate the given state from the automaton and update the transitions accordingly.
        """
        for i in self.states:
            if i == state or i == self.initial_state and state in self.final_states:
                continue
            for j in self.states:
                if j == state or j in self.final_states and state == self.initial_state:
                    continue
                re_i_s = self.reach(i, state)
                re_s_s = self.reach(state, state)
                re_s_j = self.reach(state, j)
                new_re = self.combine_re(re_i_s, re_s_s, re_s_j)
                if new_re:
                    self.add_transition(i, j, new_re)

        # Remove the state and its transitions
        self.states.remove(state)
        for (s, _) in list(self.transitions.keys()):
            if s == state:
                del self.transitions[(s, _)]

    def reach(self, start, end):
        """
        Find the regular expression for the paths from start state to end state.
        """
        re = set()
        for symbol in self.alphabet:
            if (start, symbol) in self.transitions and end in self.transitions[(start, symbol)]:
                re.add(symbol)
        return '|'.join(re)

    def add_transition(self, start, end, re):
        """
        Add a new transition with the given regular expression.
        """
        if (start, re) in self.transitions:
            if end not in self.transitions[(start, re)]:
                self.transitions[(start, re)].append(end)
        else:
            self.transitions[(start, re)] = [end]

    @staticmethod
    def combine_re(re1, re2, re3):
        """
        Combine three regular expressions with concatenation and Kleene star.
        """
        if re2:
            re2 = f'({re2})*'
        return f'{re1}{re2}{re3}'

    def to_regular_expression(self):
        """
        Convert the automaton to a regular expression using the state elimination algorithm.
        """
        # Step 1: Eliminate intermediate states
        for state in self.states[:]:
            if state != self.initial_state and state not in self.final_states:
                self.eliminate_state(state)

        # Step 2: Reduce to a two-state automaton and find regular expression
        res = []
        for final_state in self.final_states:
            if final_state == self.initial_state:
                re = self.reach(self.initial_state, self.initial_state)
                if re:
                    re = f'({re})*'
            else:
                re = self.reach(self.initial_state, self.initial_state)
                if re:
                    re = f'({re})*'
                re2 = self.reach(self.initial_state, final_state)
                if re2:
                    re += re2
                re3 = self.reach(final_state, final_state)
                if re3:
                    re += f'({re3})*'
            if re:
                res.append(re)

        # Step 4: Find the union of all regular expressions obtained
        return '|'.join(res).replace('||', '|').replace('()', '')
