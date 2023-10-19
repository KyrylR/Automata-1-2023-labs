import json

from dataclasses import dataclass

from automata.fa.nfa import NFA

@dataclass
class Automata:
    A: set  # Set of states
    X: set  # Alphabet
    f: dict  # Transition function
    a0: str  # Start state
    F: set  # Set of final states
    epsilon: str = None  # Epsilon symbol (optional)

    @classmethod
    def from_json(cls, json_string):
        """Deserialize the JSON string to create an Automata instance."""
        data = json.loads(json_string)
        data["A"] = set(data["A"])
        data["X"] = set(data["X"])
        data["f"] = {tuple(eval(k)): set(v) for k, v in data["f"].items()}
        data["F"] = set(data["F"])
        return cls(**data)

    @classmethod
    def load_from_file(cls, filename: str):
        """Load an Automata instance from a file containing its JSON representation."""
        with open(filename, "r") as file:
            json_string = file.read()
            return cls.from_json(json_string)

    def __repr__(self):
        return (
            f"Automata(\n"
            f"States (A): {self.A}\n"
            f"Alphabet (X): {self.X}\n"
            f"Transition Function (f):\n{self._format_transition_table()}\n"
            f"Start State (a0): {self.a0}\n"
            f"Final States (F): {self.F}\n"
            f"Epsilon: {self.epsilon}\n"
            f")"
        )

    def visualize(self, filename: str = "automata.png"):
        """Generate a visual representation of the automaton and save it to a file."""
        # Convert the transition function to the format expected by visual-automata
        transitions = {}
        for (state, symbol), targets in self.f.items():
            if state not in transitions:
                transitions[state] = {}

            if symbol == self.epsilon:
                symbol = ''

            transitions[state][symbol] = targets

        automaton = NFA(
            states=self.A,
            input_symbols=self.X,
            transitions=transitions,
            initial_state=self.a0,
            final_states=self.F,
        )

        # Generate the graph and save it to a file
        graph = automaton.show_diagram()
        graph.draw(filename, prog='dot', format='png')

    def to_json(self):
        """Serialize the Automata instance to a JSON string."""
        return json.dumps(
            {
                "A": sorted(list(self.A)),
                "X": sorted(list(self.X)),
                "f": {str(k): sorted(list(v)) for k, v in self.f.items()},
                "a0": self.a0,
                "F": sorted(list(self.F)),
                "epsilon": self.epsilon,
            }
        )

    def save_to_file(self, filename: str):
        """Save the Automata instance to a file in JSON format."""
        with open(filename, "w") as file:
            file.write(self.to_json())

    def _format_transition_table(self):
        """Helper method to format the transition function as a table."""
        table = []

        # Header row
        header = ["State"] + sorted([str(x) for x in self.X])
        if self.epsilon:
            header.append(self.epsilon)
        table.append(header)

        # Transition rows
        for state in sorted(self.A, key=str):
            row = [state]
            for symbol in sorted(self.X, key=str):
                transition = self.f.get((state, symbol), "-")
                row.append(", ".join(map(str, transition)) if transition else "-")
            if self.epsilon:
                epsilon_transition = self.f.get((state, self.epsilon), "-")
                row.append(", ".join(map(str, epsilon_transition)) if epsilon_transition else "-")
            table.append(row)

        # Format table as string
        col_widths = [max(len(str(cell)) for cell in col) for col in zip(*table)]
        table_str = "\n".join(
            [
                "  ".join(
                    str(cell).ljust(width) for cell, width in zip(row, col_widths)
                )
                for row in table
            ]
        )
        return table_str
