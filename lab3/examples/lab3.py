import os
import json

from lab3 import BuchiAutomaton
from lab3.base import Bipole, StrongIteration, Concatenation


def list_files(directory):
    """List all files in the given directory."""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            yield filename


def process_files(directory: str, filename1: str, filename2: str):
    print("Processing files: {} and {}".format(filename1, filename2))

    with open(os.path.join(directory, filename1), "r") as file1, open(
        os.path.join(directory, filename2), "r"
    ) as file2:
        data1 = json.load(file1)
        data2 = json.load(file2)
        automaton1 = BuchiAutomaton(
            states=set(data1["states"]),
            alphabet=set(data1["alphabet"]),
            transitions={
                state: {
                    symbol: set(next_states)
                    for symbol, next_states in symbol_dict.items()
                }
                for state, symbol_dict in data1["transitions"].items()
            },
            initial_state=data1["initial_state"],
            accepting_states=set(data1["accepting_states"]),
        )
        automaton2 = BuchiAutomaton(
            states=set(data2["states"]),
            alphabet=set(data2["alphabet"]),
            transitions={
                state: {
                    symbol: set(next_states)
                    for symbol, next_states in symbol_dict.items()
                }
                for state, symbol_dict in data2["transitions"].items()
            },
            initial_state=data2["initial_state"],
            accepting_states=set(data2["accepting_states"]),
        )

    print("Büchi Automaton 1: {}".format(automaton1.to_json()))
    automaton1.visualize("lab3/results/buchi-{}".format(os.path.splitext(filename1)[0]))

    print("Büchi Automaton 2: {}".format(automaton2.to_json()))
    automaton2.visualize("lab3/results/buchi-{}".format(os.path.splitext(filename2)[0]))


    bipole1 = Bipole(automaton1)
    bipole1.visualize("lab3/results/bipole-{}".format(os.path.splitext(filename1)[0]))

    bipole2 = Bipole(automaton2)
    bipole2.visualize("lab3/results/bipole-{}".format(os.path.splitext(filename2)[0]))

    strong_iteration = StrongIteration(bipole2)
    strong_iteration.visualize("lab3/results/strong-iteration-{}".format(os.path.splitext(filename2)[0]))

    concatenation = Concatenation(bipole1, strong_iteration)
    concatenated_automaton = concatenation.to_buchi_automaton()
    concatenated_automaton.visualize(
        "lab3/results/concatenated-buchi-{}-{}".format(
            os.path.splitext(filename1)[0], os.path.splitext(filename2)[0]
        )
    )

    print("Finished processing files: {} and {}".format(filename1, filename2))


def main():
    files = list(list_files("lab3/data"))
    for i in range(len(files) - 1):
        process_files("lab3/data", files[i], files[i + 1])
