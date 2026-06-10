# Engram Generator -- Coverage Gap Analysis

Current: 385 generators across ~15 domains.
Target: comprehensive coverage of human scientific knowledge for reasoning AI training.

## What we have (385 generators)

| Domain | Count | Assessment |
|---|---|---|
| Arithmetic/Algebra | ~25 | Solid foundation |
| Number Theory | ~22 | Good, + open problems |
| Calculus/Analysis | ~30 | Good basics, missing advanced |
| Linear Algebra | ~16 | Good basics |
| Geometry | ~20 | Euclidean covered, missing differential/projective |
| Trigonometry | ~9 | Basic only |
| Probability/Statistics | ~32 | Decent |
| Physics | ~20 | Classical + astro basics |
| Quantum | ~7 | Very thin |
| Chemistry | ~5 | Minimal |
| AI/ML | ~24 | Good |
| Logic | ~10 | Propositional only |
| Meta-reasoning | ~44 | Strong (tiers 7-10) |
| CS/Data Structures | ~30 | Moderate |
| Open Problems | ~12 | Just added |
| Other (strings, economics, etc.) | ~99 | Mixed |

## What we're missing entirely

### Mathematics (~150 generators needed)
- **Abstract Algebra**: group axioms, subgroups, cosets, Lagrange's theorem, ring homomorphisms, field extensions, Galois groups, symmetric groups, quotient groups
- **Real Analysis**: epsilon-delta proofs, Cauchy sequences, completeness, uniform convergence, Lebesgue measure, Lp spaces
- **Complex Analysis**: Cauchy-Riemann equations, contour integrals, residue theorem, conformal maps, analytic continuation
- **Topology**: open/closed sets, continuity, compactness, connectedness, fundamental group, Euler characteristic, fixed-point theorems
- **Differential Geometry**: curvature, geodesics, Christoffel symbols, parallel transport, Riemannian metrics
- **Algebraic Geometry**: polynomial ideals, Bezout's theorem, elliptic curves, projective coordinates
- **Measure Theory**: sigma-algebras, measurable functions, dominated convergence, Fubini's theorem
- **Functional Analysis**: Banach spaces, Hilbert spaces, spectral theorem, compact operators
- **Category Theory**: functors, natural transformations, adjunctions, limits/colimits
- **Representation Theory**: character tables, irreducible representations
- **Optimization**: linear programming (simplex), convex optimization, KKT conditions, duality

### Physics (~100 generators needed)
- **Electromagnetism**: Coulomb's law, electric fields, Gauss's law, Faraday's law, Maxwell's equations, Lorentz force, RLC circuits, impedance
- **Thermodynamics**: first/second/third law, entropy, Carnot cycle, heat engines, free energy, phase transitions
- **Statistical Mechanics**: partition functions, Boltzmann distribution, Fermi-Dirac, Bose-Einstein, Ising model
- **Special Relativity**: Lorentz transforms, time dilation, length contraction, relativistic energy, spacetime intervals, four-vectors
- **General Relativity**: metric tensor, Einstein field equations (simplified), Schwarzschild solution, gravitational waves
- **Optics**: Snell's law, thin lenses, diffraction, interference, polarisation
- **Fluid Mechanics**: Bernoulli's equation, Reynolds number, Navier-Stokes (simplified), viscosity
- **Nuclear Physics**: binding energy, mass defect, radioactive decay chains, half-life, nuclear reactions
- **Solid State**: crystal structures, band theory, semiconductors, Bragg diffraction
- **Acoustics**: wave equation, standing waves, resonance, Doppler effect

### Quantum Mechanics (~30 generators needed)
- **Formalism**: Schrodinger equation, operators, commutators, Heisenberg uncertainty
- **Angular Momentum**: L^2 operator, spherical harmonics, spin-orbit coupling, Clebsch-Gordan
- **Many-body**: Slater determinant, Hartree-Fock, second quantisation
- **Quantum Information**: entanglement measures, Bell inequalities, quantum teleportation, error correction codes
- **Quantum Computing**: circuit synthesis, Grover's algorithm steps, Shor's algorithm (modular exponentiation part), quantum Fourier transform

### Chemistry (~50 generators needed)
- **General Chemistry**: electron configuration, periodic trends, Lewis structures, VSEPR, hybridisation
- **Physical Chemistry**: rate laws, Arrhenius equation, equilibrium constants, Nernst equation, thermochemistry (Hess's law)
- **Organic Chemistry**: functional groups, nomenclature, reaction mechanisms (SN1/SN2/E1/E2), stereochemistry
- **Biochemistry**: amino acid properties, peptide bonds, enzyme kinetics (Michaelis-Menten), DNA base pairing
- **Electrochemistry**: cell potential, Faraday's law of electrolysis, galvanic cells

### Biology (~40 generators needed)
- **Genetics**: Mendelian inheritance, Punnett squares, Hardy-Weinberg equilibrium, DNA replication steps
- **Ecology**: population growth (logistic), Lotka-Volterra, carrying capacity, food web energy flow
- **Evolution**: phylogenetic trees, fitness calculations, genetic drift, natural selection models
- **Molecular Biology**: codon table lookup, transcription/translation, gel electrophoresis interpretation
- **Neuroscience**: Hodgkin-Huxley (simplified), membrane potential, synaptic transmission

### Computer Science (~80 generators needed)
- **Cryptography**: RSA keygen, Diffie-Hellman, elliptic curve point addition, AES steps, hash collision resistance, digital signatures
- **Automata/Languages**: NFA to DFA, regular expression matching, context-free grammars, pushdown automata, Turing machine simulation
- **Compilers**: tokenisation, recursive descent parsing, type checking, register allocation
- **Information Theory**: channel capacity, Huffman coding, Hamming distance, error correction, Kolmogorov complexity bounds
- **Distributed Systems**: consensus (simplified Paxos), vector clocks, consistent hashing
- **Databases**: relational algebra, normalisation (1NF-BCNF), SQL query equivalence
- **Networking**: subnet calculation, routing tables, TCP window, DNS resolution
- **Operating Systems**: scheduling (FIFO, SJF, Round Robin), page replacement (LRU, FIFO), deadlock detection

### Engineering (~40 generators needed)
- **Signal Processing**: DFT computation, FIR/IIR filters, sampling theorem, convolution theorem, z-transform
- **Control Theory**: transfer functions, PID tuning, Bode plots, stability (Routh-Hurwitz), state space
- **Electrical Engineering**: AC circuits, impedance, power factor, transformer ratios
- **Materials Science**: stress-strain, Young's modulus, crystal Miller indices

### Earth/Space Sciences (~20 generators needed)
- **Astronomy**: stellar classification (HR diagram), magnitude system, parallax distance, orbital mechanics
- **Geology**: mineral hardness, seismic wave velocity, radiometric dating
- **Climate**: radiative forcing, albedo, greenhouse effect calculations

### Social Sciences (~20 generators needed)
- **Linguistics**: formal grammars (Chomsky hierarchy), phonetic transcription, morphological analysis
- **Economics**: expanded supply/demand, Nash equilibrium computation, auction theory, Cobb-Douglas
- **Decision Theory**: expected utility, risk aversion, prospect theory

## Summary

| Category | Current | Estimated Gap | Target |
|---|---|---|---|
| Mathematics | ~140 | ~150 | ~290 |
| Physics | ~20 | ~100 | ~120 |
| Chemistry | ~5 | ~50 | ~55 |
| Biology | 0 | ~40 | ~40 |
| Computer Science | ~60 | ~80 | ~140 |
| Quantum | ~7 | ~30 | ~37 |
| Engineering | ~5 | ~40 | ~45 |
| Earth/Space | ~5 | ~20 | ~25 |
| Social Sciences | ~10 | ~20 | ~30 |
| AI/ML | ~24 | ~10 | ~34 |
| Meta-reasoning | ~44 | ~10 | ~54 |
| Open Problems | ~12 | ~5 | ~17 |
| **Total** | **~385** | **~555** | **~940** |

We need roughly 2.5x what we currently have to achieve broad coverage.
True depth (graduate+ level) would push it past 1500.
