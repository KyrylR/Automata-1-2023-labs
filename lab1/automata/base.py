import json

from dataclasses import dataclass


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
        header = ["State"] + sorted(list(self.X))
        if self.epsilon:
            header.append(self.epsilon)
        table.append(header)

        # Transition rows
        for state in sorted(self.A):
            row = [state]
            for symbol in sorted(self.X):
                transition = self.f.get((state, symbol), "-")
                row.append(", ".join(transition) if transition else "-")
            if self.epsilon:
                epsilon_transition = self.f.get((state, self.epsilon), "-")
                row.append(", ".join(epsilon_transition) if epsilon_transition else "-")
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
