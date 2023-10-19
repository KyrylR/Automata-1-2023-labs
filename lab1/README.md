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
