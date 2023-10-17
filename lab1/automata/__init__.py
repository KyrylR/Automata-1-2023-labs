"""
The automata package contains modules and classes related to different types
of automata, including deterministic (DFA), nondeterministic (NFA), and
epsilon-nondeterministic (ENFA) finite automata. This package provides
the foundational representations for automata and their basic operations.
"""

from automata.base import Automata

from automata.converters import ENFAToNFAConverter
