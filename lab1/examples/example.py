import os

from lab1 import Automata, ENFAToNFAConverter


def list_files(directory):
    """List all files in the given directory."""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            yield filename


def process_file(directory: str, filename: str):
    print("Processing file: {}".format(filename))

    automata = Automata.load_from_file(os.path.join(directory, filename))

    print("e-NFA: {}".format(automata.to_json()))

    automata.visualize(
        "lab1/results/e-nfa-{}.png".format(os.path.splitext(filename)[0])
    )

    converter = ENFAToNFAConverter(automata)

    nfa = converter.convert_to_nfa()

    nfa.visualize("lab1/results/nfa-{}.png".format(os.path.splitext(filename)[0]))
    print("NFA: {}".format(nfa.to_json()))

    nfa.save_to_file(os.path.join("lab1/results", "nfa-{}".format(filename)))

    print("Finished processing file: {}".format(filename))


def main():
    for file in list_files("lab1/data"):
        process_file("lab1/data", file)
