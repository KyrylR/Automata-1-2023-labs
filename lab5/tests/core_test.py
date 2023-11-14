import unittest

from lab5.lab5.core import satisfies_constraint, ClockRegion, State, RegionAutomaton, transition_mapping, time_successors


class RegionAutomatonTest(unittest.TestCase):
    def setUp(self):
        # Setup common test data
        self.clock_region_0 = ClockRegion({'x': '=1', 'y': '<1'})
        self.clock_region_1 = ClockRegion({'x': '<1', 'y': '=1'})
        self.clock_region_2 = ClockRegion({'x': '=1', 'y': '=1'})

        self.state_0 = State(0, self.clock_region_0)
        self.state_1 = State(1, self.clock_region_1)
        self.state_2 = State(2, self.clock_region_2)

        self.states = [self.state_0, self.state_1, self.state_2]
        self.initial_states = [self.state_0]

        self.original_transitions = [
            (self.state_0, self.state_1, 'a', {'x': 1}),
            (self.state_1, self.state_2, 'b', {'y': 2}),
        ]

        region_transitions = transition_mapping(self.original_transitions, self.states)
        self.region_automaton = RegionAutomaton(self.states, self.initial_states, region_transitions)

    def test_initial_states(self):
        # Test if the initial states of the region automaton match the expected initial states
        self.assertEqual(set(self.region_automaton.initial_states), set(self.initial_states))

    def test_state_transitions(self):
        # Test if the region automaton correctly represents the transitions from the original automaton
        for from_state, to_state, action, _ in self.original_transitions:
            found = any(
                from_state.state_id == ra_from_state.state_id and
                to_state.state_id == ra_to_state.state_id and
                action == ra_action
                for ra_from_state, ra_to_state, ra_action, _ in self.region_automaton.transitions
            )
            self.assertTrue(found)

    def test_clock_constraints(self):
        # Test if the clock constraints are correctly applied in the region automaton transitions
        for from_state, to_state, action, constraint in self.original_transitions:
            for ra_from_state, ra_to_state, ra_action, ra_clock_region in self.region_automaton.transitions:
                if (from_state.state_id == ra_from_state.state_id and
                        to_state.state_id == ra_to_state.state_id and
                        action == ra_action):
                    self.assertTrue(satisfies_constraint(ra_clock_region, constraint))

    def test_completeness(self):
        # Test if every state and transition in the original automaton is represented in the region automaton
        original_state_ids = {state.state_id for state in self.states}
        region_automaton_state_ids = {state.state_id for state in self.region_automaton.states}
        self.assertEqual(original_state_ids, region_automaton_state_ids)
