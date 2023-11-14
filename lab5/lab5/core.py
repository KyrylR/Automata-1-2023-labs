class RegionAutomaton:
    """
    Represents a region automaton, constructed from a timed automaton.
    """

    def __init__(self, states, initial_states, transitions):
        """
        Initializes a RegionAutomaton.
        :param states: A list of State instances.
        :param initial_states: A list of initial State instances.
        :param transitions: A list of transitions in the form (from_state, to_state, action, clock_region).
        """
        self.states = states
        self.initial_states = initial_states
        self.transitions = transitions

    def __repr__(self):
        return f"RegionAutomaton(States: {self.states}, Initial States: {self.initial_states}, Transitions: {self.transitions})"


class ClockRegion:
    """
    Represents a clock region with constraints on clock values.
    """

    def __init__(self, constraints):
        """
        Initializes a ClockRegion with given constraints.
        :param constraints: Dict representing clock constraints, e.g., {'x': '=1', 'y': '<1'}
        """
        self.constraints = constraints

    def __repr__(self):
        return f"ClockRegion({self.constraints})"


class State:
    """
    Represents a state in the automaton, associated with a clock region.
    """

    def __init__(self, state_id, clock_region):
        """
        Initializes a State with an ID and a corresponding clock region.
        :param state_id: ID of the state.
        :param clock_region: ClockRegion associated with this state.
        """
        self.state_id = state_id
        self.clock_region = clock_region

    def __repr__(self):
        return f"State({self.state_id}, {self.clock_region})"


def time_successors(clock_region):
    """
    Function to calculate the time-successors of a given clock region.
    """
    successors = []

    for clock, constraint in clock_region.constraints.items():
        if constraint.startswith('='):
            # For an exact value, the time-successor can either exceed this value or stay the same
            value = int(constraint[1:])
            successors.append(ClockRegion({clock: f'>{value}'}))  # Exceeding value
            successors.append(ClockRegion({clock: f'={value}'}))  # Staying the same
        elif constraint.startswith('<'):
            # For a less than constraint, consider reaching the value and exceeding it
            value = int(constraint[1:])
            successors.append(ClockRegion({clock: f'={value}'}))  # Reaching value
            successors.append(ClockRegion({clock: f'>{value}'}))  # Exceeding value
        elif constraint.startswith('>'):
            # For a greater than constraint, consider only exceeding the value
            value = int(constraint[1:])
            successors.append(ClockRegion({clock: f'>{value}'}))  # Exceeding value

    return successors


def satisfies_constraint(clock_region, transition_constraint):
    """
    Adjusted method to check if a given clock region satisfies a specific clock constraint.
    Handles different types of constraints.
    """
    for clock, region_constraint in clock_region.constraints.items():
        if clock in transition_constraint:
            if region_constraint.startswith('='):
                region_value = int(region_constraint[1:])
                if isinstance(transition_constraint[clock], int):
                    if region_value != transition_constraint[clock]:
                        return False
                elif isinstance(transition_constraint[clock], str):
                    # If constraint is a string, parse and compare values
                    transition_value = int(transition_constraint[clock][1:])
                    if transition_constraint[clock].startswith('<') and region_value >= transition_value:
                        return False
                    elif transition_constraint[clock].startswith('>') and region_value <= transition_value:
                        return False
            elif region_constraint.startswith('>'):
                region_value = int(region_constraint[1:])
                if isinstance(transition_constraint[clock], int):
                    if region_value <= transition_constraint[clock]:
                        return False
                elif isinstance(transition_constraint[clock], str):
                    transition_value = int(transition_constraint[clock][1:])
                    if transition_constraint[clock].startswith('<') and region_value >= transition_value:
                        return False
                    elif transition_constraint[clock].startswith('=') and region_value != transition_value:
                        return False
            elif region_constraint.startswith('<'):
                region_value = int(region_constraint[1:])
                if isinstance(transition_constraint[clock], int):
                    if region_value >= transition_constraint[clock]:
                        return False
                elif isinstance(transition_constraint[clock], str):
                    transition_value = int(transition_constraint[clock][1:])
                    if transition_constraint[clock].startswith('>') and region_value <= transition_value:
                        return False
                    elif transition_constraint[clock].startswith('=') and region_value != transition_value:
                        return False
    return True


def transition_mapping(original_transitions, states):
    """
    Function to create a transition mapping for the region automaton, adjusted to work with state IDs.
    """
    region_automaton_transitions = []

    for from_state_id, to_state_id, action, constraint in original_transitions:
        ra_from_states = [s for s in states if s.state_id == from_state_id]

        for ra_from_state in ra_from_states:
            successors = time_successors(ra_from_state.clock_region)

            for successor in successors:
                if satisfies_constraint(successor, constraint):
                    ra_to_states = [s for s in states if s.state_id == to_state_id]

                    for ra_to_state in ra_to_states:
                        region_transition = (ra_from_state, ra_to_state, action, successor)
                        region_automaton_transitions.append(region_transition)

    return region_automaton_transitions
