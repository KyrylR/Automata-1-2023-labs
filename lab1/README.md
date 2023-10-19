# Lab1

## Overview
This project offers tools and utilities to work with various types of automata, including deterministic (DFA), 
nondeterministic (NFA), and epsilon-nondeterministic (ENFA) finite automata. A core feature is the ability to convert 
between these types, starting with a transformation from ENFA to NFA.

## Getting Started

### Prerequisites
- Python 3.x
(Add any other requirements or dependencies here)

## Running the Project

### Installation and Setup
1. **Install Poetry**: If you don't have Poetry installed, you can get it using the following command:

```bash
curl -sSL https://install.python-poetry.org | python3 -
```

Alternatively, for Windows users, you can use:

```bash
(Invoke-WebRequest -Uri https://install.python-poetry.org -UseBasicParsing).Content | python -
```

2. **Clone the Repository**:

```bash
git clone [repository-url]
cd [repository-name]
```

3. **Install Dependencies**: 

```bash
poetry install
```

### Running Tests
To run tests using Poetry, simply use:

```bash
poetry run pytest
```

Here is how you can insert the new section into your README file:

## Running Examples

To run examples, use the following command:

```bash
poetry run example
```

This command will execute the `example` file, which performs the following actions:

1. **List Files in the Data Directory**: The script will list all files in the `data` directory, which should contain e-NFA automata in JSON format.

2. **Load Automata and Visualize**: For each file in the `data` directory, the script will:
    - Load the e-NFA automata from the file.
    - Visualize the e-NFA and save the image to the `results` directory with the filename `e-nfa-[filename].png`.

3. **Convert e-NFA to NFA and Visualize**: The script will then:
    - Convert the e-NFA to NFA using the `ENFAToNFAConverter` class.
    - Visualize the NFA and save the image to the `results` directory with the filename `nfa-[filename].png`.
    - Save the NFA to a JSON file in the `results` directory with the filename `nfa-[filename].json`.

4. **Output JSON Representations**: Finally, the script will print out the JSON representations of both the e-NFA and the converted NFA to the console.

This example runner provides a convenient way to see the transformation of e-NFA to NFA and visualize the automata for 
better understanding. It also helps to ensure that the conversion process is working correctly by comparing the images and JSON outputs.

## Usage

### Creating an Automata

```python
from core import Automata

automata_instance = Automata(
    A={"0", "1", "2"},
    X={"x", "y", "z"},
    f={
        ("0", "x"): {"0"},
        # ... other transitions ...
    },
    a0="0",
    F={"2"},
    epsilon="epsilon"
)
```

### Converting an ENFA to NFA

```python
from core import Automata, ENFAToNFAConverter

enfa_instance = Automata(...)
converter = ENFAToNFAConverter(enfa_instance)
nfa_instance = converter.convert_to_nfa()
```

### Serialization and Deserialization

Serialize an Automata instance to a JSON string:

```python
json_str = automata_instance.to_json()
```

Deserialize from a JSON string:

```python
automata_instance = Automata.from_json(json_str)
```

### File Operations

To save an Automata instance to a file:

```python
automata_instance.save_to_file("filename.json")
```

To load an Automata instance from a file:

```python
loaded_automata = Automata.load_from_file("filename.json")
```

## Project Structure
```
├── automata
│   ├── base.py (Foundational representations for automata)
│   ├── converters
│   │   ├── enfa_to_nfa.py (ENFA to NFA converter utility)
│   │   └── __init__.py
│   └── __init__.py
```

## License
This project is licensed under the MIT License.
