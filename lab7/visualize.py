import graphviz

# Create a new directed graph
dot = graphviz.Digraph(comment='PDA Diagram')

# Define graph nodes for the states
dot.node('q0', 'q_start')
dot.node('q1', 'q_read')
dot.node('q2', 'q_build')
dot.node('q3', 'q_accept')

# Define edges with labels for transitions
# Format: (state_from, state_to, label)
transitions = [
    ('q0', 'q1', 'ε, ε → $σ'),
    ('q1', 'q1', 'a, σ → Aσ'),
    ('q1', 'q1', 'b, σ → B'),
    ('q1', 'q1', 'b, B → BB'),
    ('q1', 'q1', 'ε, A → ε'),
    ('q1', 'q1', 'ε, B → ε'),
    ('q1', 'q2', 'ε, σ → ε'),
    ('q2', 'q2', 'ε, A → ε'),
    ('q2', 'q2', 'ε, B → ε'),
    ('q2', 'q3', 'ε, $ → ε'),
]

# Add edges to the graph
for fr, to, label in transitions:
    dot.edge(fr, to, label=label)

# Render the graph to a file (PNG)
dot.render('/mnt/data/pda_automaton', format='png', view=True)
