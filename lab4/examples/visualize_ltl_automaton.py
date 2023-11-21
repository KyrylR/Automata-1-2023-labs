import graphviz

# Create a Digraph object
dot = graphviz.Digraph(comment="Büchi Automaton for LTL Formula")

# Adding nodes (states)
dot.node("S0", "S0\n(Initial)", shape="circle")
dot.node("S1", "S1\n(p is false at least once)", shape="doublecircle")
dot.node("S2", "S2\n(q is true at least once)", shape="circle")

# Adding edges (transitions)
# Transitions from S0
dot.edge("S0", "S1", label="¬p ∧ ¬q / ¬p ∧ q")
dot.edge("S0", "S2", label="p ∧ q")
dot.edge("S0", "S0", label="p ∧ ¬q")

# Transitions from S1
dot.edge("S1", "S1", label="p ∧ q / p ∧ ¬q / ¬p ∧ q / ¬p ∧ ¬q")

# Transitions from S2
dot.edge("S2", "S2", label="p ∧ q / p ∧ ¬q / ¬p ∧ q / ¬p ∧ ¬q")


def main():
    dot.render("./lab4/results/Buchi_Automaton_LTL_Formula", format="png", cleanup=True)
