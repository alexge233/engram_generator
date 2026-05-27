"""Atoms for automata."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


register_atom(Atom(atom_type="algorithm", name="dfa_accept",
    content="A deterministic finite automaton (DFA) has states, a start state, accept states, "
    "and a transition function delta(state, symbol) -> state. To check if a string is accepted: "
    "start at the initial state, follow transitions for each symbol, accept if the final state "
    "is an accept state.",
    tier=3, domain="automata",
    source="Wikipedia contributors, 'Deterministic finite automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Deterministic_finite_automaton"))

register_atom(Atom(atom_type="algorithm", name="nfa_simulate",
    content="A nondeterministic finite automaton (NFA) can be in multiple states simultaneously. "
    "To simulate: maintain a set of current states, for each symbol expand to all reachable states "
    "(including epsilon transitions). Accept if any final state is an accept state.",
    tier=4, domain="automata",
    source="Wikipedia contributors, 'Nondeterministic finite automaton', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Nondeterministic_finite_automaton",
    prerequisites=["dfa_accept"]))

register_atom(Atom(atom_type="algorithm", name="turing_machine_step",
    content="A Turing machine has a tape, a head, states, and transition rules: "
    "(state, symbol) -> (new_state, write_symbol, move_direction). "
    "Execute one step: read symbol under head, apply the matching rule, write, move, change state.",
    tier=4, domain="automata",
    source="Wikipedia contributors, 'Turing machine', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Turing_machine",
    prerequisites=["dfa_accept"]))
