# Global variables for test data
STATES = {1, 2, 3, 4}
INPUT_ALPHABET = {"x", "y"}
OUTPUT_ALPHABET = {"u", "v"}
TRANSITIONS = {
    1: {
        "x": (1, "v"),
        "y": (4, "u"),
    },
    2: {
        "x": (1, "v"),
        "y": (1, "v"),
    },
    3: {
        "x": (1, "u"),
        "y": (1, "u"),
    },
    4: {
        "x": (2, "u"),
        "y": (3, "v"),
    },
}
INITIAL_STATE = 1
OUTPUT_FUNCTION = None
FINAL_SYMBOLS = {"u"}
