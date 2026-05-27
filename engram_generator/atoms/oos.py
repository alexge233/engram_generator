"""Knowledge atoms for out-of-set held-out evaluation tasks.

These atoms are sourced from Wikipedia and provide the theoretical
grounding for OOS generators. They are never used during training.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

register_atom(Atom(
    atom_type="definition",
    name="propositional_logic",
    content="""Propositional calculus is a branch of logic. It is also called
propositional logic, statement logic, sentential calculus, sentential logic,
or sometimes zeroth-order logic. It deals with propositions (which can be
true or false) and relations between propositions, including the construction
of arguments based on them. Compound propositions are formed by connecting
propositions by logical connectives representing the truth functions of
conjunction, disjunction, implication, biconditional, and negation. Some
sources include other connectives as well.

Modus ponens: if P implies Q, and P is true, then Q is true.
Modus tollens: if P implies Q, and Q is false, then P is false.
Conjunction introduction: if P is true and Q is true, then P AND Q is true.
Disjunction introduction: if P is true, then P OR Q is true.
Disjunction elimination: if P OR Q is true, and P is false, then Q is true.

A formal system of propositional logic consists of a set of axioms and
inference rules that allow deriving new true propositions from existing ones.
The completeness theorem states that every tautology is provable.""",
    tier=99,
    domain="logic",
    source="Wikipedia, 'Propositional calculus'",
    source_url="https://en.wikipedia.org/wiki/Propositional_calculus",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="unit_conversion",
    content="""Conversion of units is the conversion of the unit of measurement
in which a quantity is expressed, typically through a multiplicative conversion
factor that changes the unit without changing the quantity. This is also often
loosely taken to include replacement of a quantity with a corresponding quantity
that describes the same physical property.

Unit conversion is achieved by using conversion factors:
  Length: 1 km = 1000 m, 1 m = 100 cm, 1 cm = 10 mm
  Mass: 1 kg = 1000 g, 1 g = 1000 mg
  Time: 1 hr = 60 min, 1 min = 60 sec
  Imperial: 1 mi = 1760 yd, 1 yd = 3 ft, 1 ft = 12 in
  Digital: 1 TB = 1024 GB, 1 GB = 1024 MB, 1 MB = 1024 KB

Multi-step conversions chain these factors: to convert km to mm, multiply
by 1000 (km to m), then by 100 (m to cm), then by 10 (cm to mm).
Dimensional analysis ensures correctness by tracking unit cancellation.""",
    tier=99,
    domain="measurement",
    source="Wikipedia, 'Conversion of units'",
    source_url="https://en.wikipedia.org/wiki/Conversion_of_units",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="finite_state_machine",
    content="""A finite-state machine (FSM) or finite-state automaton (FSA,
plural: automata), finite automaton, or simply a state machine, is a
mathematical model of computation. It is an abstract machine that can be in
exactly one of a finite number of states at any given time. The FSM can
change from one state to another in response to some inputs; the change from
one state to another is called a transition. An FSM is defined by a list of
its states, its initial state, and the inputs that trigger each transition.

Formally, a deterministic finite automaton (DFA) is a 5-tuple
(Q, Sigma, delta, q0, F) where:
  Q is a finite set of states
  Sigma is a finite set of input symbols (the alphabet)
  delta: Q x Sigma -> Q is the transition function
  q0 in Q is the initial state
  F subset Q is the set of accepting states

The machine processes an input string one symbol at a time, transitioning
between states according to the transition function delta. The final state
after processing all input determines whether the string is accepted.""",
    tier=99,
    domain="computation",
    source="Wikipedia, 'Finite-state machine'",
    source_url="https://en.wikipedia.org/wiki/Finite-state_machine",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="program_tracing",
    content="""In software engineering, tracing involves a specialised use of
logging to record information about a program's execution. Program tracing
involves mentally or mechanically executing a program step by step, tracking
the values of variables at each point.

For imperative programs, tracing follows the sequential execution model:
  1. Assignment: x = expr evaluates expr and stores the result in x
  2. Conditional: if condition is true, execute the if-branch; otherwise
     execute the else-branch
  3. Loop: repeat the body while the condition holds
  4. Function call: evaluate arguments, bind to parameters, execute body

Variable state is tracked as a mapping from variable names to current values.
Each statement potentially updates this mapping. The output of a program
trace is the sequence of variable states and the final return value.

Tracing is fundamental to debugging and program verification. It requires
maintaining a mental model of the machine state across sequential operations,
which is structurally similar to maintaining memory across iterations.""",
    tier=99,
    domain="computation",
    source="Wikipedia, 'Tracing (software)'",
    source_url="https://en.wikipedia.org/wiki/Tracing_(software)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="musical_interval",
    content="""In music theory, an interval is a difference in pitch between
two sounds. An interval may be described as horizontal, linear, or melodic
if it refers to successively sounding tones, such as two adjacent pitches in
a melody, and vertical or harmonic if it pertains to simultaneously sounding
tones, such as in a chord.

In Western music, intervals are most commonly differences between notes of a
diatonic scale. Intervals between successive notes of a scale are also known
as scale steps.

The chromatic scale divides the octave into 12 equal semitones:
  C, C#, D, D#, E, F, F#, G, G#, A, A#, B

Common intervals in semitones:
  Unison: 0, Minor 2nd: 1, Major 2nd: 2, Minor 3rd: 3,
  Major 3rd: 4, Perfect 4th: 5, Tritone: 6, Perfect 5th: 7,
  Minor 6th: 8, Major 6th: 9, Minor 7th: 10, Major 7th: 11,
  Octave: 12

Interval arithmetic is modular: moving up 7 semitones from G# gives
(8 + 7) mod 12 = 3, which is D#. This is structurally identical to
modular arithmetic in base 12.""",
    tier=99,
    domain="music_theory",
    source="Wikipedia, 'Interval (music)'",
    source_url="https://en.wikipedia.org/wiki/Interval_(music)",
    prerequisites=[],
))
