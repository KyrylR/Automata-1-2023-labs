"""
The core package contains modules and classes related to different types
of core, including deterministic (DFA), nondeterministic (NFA), and
epsilon-nondeterministic (ENFA) finite core. This package provides
the foundational representations for core and their basic operations.
"""

from core.base import Automata

from core.converters import ENFAToNFAConverter
