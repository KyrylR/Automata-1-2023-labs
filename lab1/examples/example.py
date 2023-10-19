import os

from core import Automata

from core import ENFAToNFAConverter


def list_files(directory):
    """List all files in the given directory."""
    for filename in os.listdir(directory):
        if os.path.isfile(os.path.join(directory, filename)):
            yield filename


def process_file(directory: str, filename: str):
    print("Processing file: {}".format(filename))

    automata = Automata.load_from_file(os.path.join(directory, filename))

    print("e-NFA: {}".format(automata.to_json()))

    automata.visualize('results/e-nfa-{}.png'.format(filename))

    converter = ENFAToNFAConverter(automata)

    converter.convert_to_nfa().visualize("results/nfa-{}.png".format(filename))

    print("NFA: {}".format(converter.convert_to_nfa().to_json()))
    print("Finished processing file: {}".format(filename))


def main():
    for file in list_files("data"):
        process_file("data", file)
