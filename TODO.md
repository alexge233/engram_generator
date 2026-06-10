# Engram Generator -- Coverage Expansion TODO

Goal: comprehensive coverage of human scientific knowledge for reasoning AI training.
Current: 385 generators. Target: ~940+ generators.

Each task below is one generator file (or addition to existing file). Each generator must:
- Subclass `StepGenerator`, implement all abstract methods
- Use `@register` decorator
- Have Google-style docstrings
- Respect tier constraints (prerequisites must be same tier or lower)
- Keep targets under 512 characters
- Use `self._rng` for all randomness
- Include a matching `Atom` with Wikipedia/authoritative source
- Update hardcoded count in `tests/test_structural.py` and `tests/test_skill_tree_full.py`

---

## Phase 1: Mathematics Foundation (~80 generators)

### 1.1 Abstract Algebra (file: `generators/abstract_algebra.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | group_axiom_check | Verify closure/associativity/identity/inverse on a Cayley table | 5 | group_table |
| 2 | subgroup_test | Check if subset is a subgroup (closure + inverse) | 5 | group_axiom_check |
| 3 | coset_enumerate | List left cosets of H in G | 5 | subgroup_test |
| 4 | lagrange_verify | Verify |H| divides |G| for given subgroup | 5 | coset_enumerate |
| 5 | cyclic_group_gen | Find generator of cyclic group Z_n | 5 | group_order |
| 6 | normal_subgroup | Check if subgroup is normal (gHg^-1 = H) | 6 | coset_enumerate |
| 7 | quotient_group | Compute multiplication table of G/N | 6 | normal_subgroup |
| 8 | kernel_compute | Find kernel of a group homomorphism | 6 | group_homomorphism |
| 9 | isomorphism_check | Determine if two small groups are isomorphic | 6 | group_table |
| 10 | ring_ideal_check | Verify if subset is an ideal of a ring | 6 | ring_arithmetic |
| 11 | field_extension | Compute minimal polynomial over Q | 6 | polynomial_division |
| 12 | symmetric_group | Compose permutations in S_n notation | 5 | permutation |

### 1.2 Real Analysis (file: `generators/real_analysis.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | epsilon_delta | Prove limit using epsilon-delta: find delta for given epsilon | 6 | limit |
| 2 | cauchy_sequence | Check if a sequence is Cauchy (|a_m - a_n| < eps) | 6 | limit |
| 3 | sequence_convergence | Determine if sequence converges and find limit | 5 | limit |
| 4 | supremum_infimum | Find sup and inf of a bounded set | 5 | comparison |
| 5 | uniform_convergence | Test uniform convergence of function sequence | 6 | epsilon_delta |
| 6 | pointwise_vs_uniform | Distinguish pointwise from uniform convergence | 6 | uniform_convergence |
| 7 | ratio_test | Apply ratio test to determine series convergence | 5 | series_convergence |
| 8 | root_test | Apply root test to determine series convergence | 5 | series_convergence |
| 9 | comparison_test | Apply direct/limit comparison test | 5 | series_convergence |
| 10 | alternating_series | Apply Leibniz test to alternating series | 5 | series_convergence |
| 11 | power_series_radius | Find radius of convergence of power series | 6 | ratio_test |
| 12 | intermediate_value | Apply IVT to show existence of root in interval | 6 | sequence_convergence |

### 1.3 Complex Analysis (file: `generators/complex_analysis.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | cauchy_riemann | Verify Cauchy-Riemann equations for f(z) | 6 | partial_derivative, complex_arithmetic |
| 2 | complex_power_series | Find Taylor series of complex function about z_0 | 6 | taylor_series, complex_arithmetic |
| 3 | residue_compute | Compute residue of f(z) at a pole | 6 | complex_power_series |
| 4 | contour_integral | Evaluate integral using residue theorem | 7 | residue_compute |
| 5 | analytic_check | Determine if function is analytic on domain | 6 | cauchy_riemann |
| 6 | mobius_transform | Apply Mobius transformation (az+b)/(cz+d) | 6 | complex_division |
| 7 | laurent_series | Find Laurent series at isolated singularity | 7 | complex_power_series |
| 8 | poles_classify | Classify singularity (removable, pole, essential) | 7 | laurent_series |

### 1.4 Topology (file: `generators/topology.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | open_closed_sets | Determine if subset is open, closed, both, or neither | 6 | set_membership |
| 2 | closure_interior | Compute closure and interior of a set | 6 | open_closed_sets |
| 3 | continuity_topological | Verify if map is continuous (preimage of open is open) | 6 | open_closed_sets |
| 4 | homeomorphism_check | Check if bijection is a homeomorphism | 7 | continuity_topological |
| 5 | euler_characteristic | Compute V - E + F for polyhedra/graphs | 5 | addition, subtraction |
| 6 | connected_check | Determine if topological space is connected | 6 | open_closed_sets |
| 7 | compactness_check | Determine if subset of R^n is compact (closed + bounded) | 6 | open_closed_sets |
| 8 | fixed_point | Apply Brouwer fixed-point theorem to find fixed point | 7 | continuity_topological |

### 1.5 Differential Geometry (file: `generators/differential_geometry.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | curvature_2d | Compute curvature kappa for parametric curve | 6 | derivative, chain_rule |
| 2 | arc_length_param | Compute arc length of parametric curve | 6 | definite_integral |
| 3 | tangent_normal | Find unit tangent and normal vectors | 6 | gradient, vector_norm |
| 4 | christoffel_symbol | Compute Christoffel symbols for 2D metric | 7 | partial_derivative, matrix_inverse |
| 5 | geodesic_equation | Write geodesic equation for simple surface | 7 | christoffel_symbol |
| 6 | gaussian_curvature | Compute Gaussian curvature of surface | 7 | christoffel_symbol |

### 1.6 Optimization (file: `generators/optimization.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | linear_program | Solve 2-variable LP graphically (vertex enumeration) | 5 | system_equations |
| 2 | simplex_step | Perform one simplex pivot step | 6 | linear_program |
| 3 | dual_lp | Write the dual of a linear program | 6 | linear_program |
| 4 | convex_check | Verify if function is convex (Hessian positive semidefinite) | 6 | eigenvalue |
| 5 | kkt_conditions | Write KKT conditions for constrained optimization | 6 | lagrange_multiplier |
| 6 | gradient_descent_step | Compute one GD step with exact line search | 5 | gradient_descent |

### 1.7 Number Theory Extensions (file: `generators/number_theory_ext.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | quadratic_reciprocity | Apply quadratic reciprocity law | 6 | quadratic_residue |
| 2 | primitive_root | Find primitive root mod p | 6 | totient |
| 3 | sum_of_squares | Express n as sum of two squares (Fermat) | 5 | primality |
| 4 | mobius_function | Compute mu(n) from prime factorisation | 6 | factorisation |
| 5 | divisor_function | Compute sigma_k(n) (sum of k-th powers of divisors) | 5 | factorisation |
| 6 | jacobi_symbol | Compute Jacobi symbol (a/n) | 6 | quadratic_reciprocity |
| 7 | pell_equation | Find fundamental solution to x^2 - Dy^2 = 1 | 6 | continued_fraction |
| 8 | order_element | Find multiplicative order of a mod n | 6 | mod_pow |

---

## Phase 2: Physics & Engineering (~100 generators)

### 2.1 Electromagnetism (file: `generators/electromagnetism.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | coulombs_law | Compute force between point charges | 4 | multiplication, division |
| 2 | electric_field | Compute E field at point from charge(s) | 5 | coulombs_law |
| 3 | gauss_law | Apply Gauss's law to symmetric charge distributions | 5 | electric_field |
| 4 | electric_potential | Compute V from point charges (superposition) | 5 | coulombs_law |
| 5 | capacitance | Compute C for parallel plate / series / parallel | 4 | division, multiplication |
| 6 | rc_circuit | Compute time constant and voltage in RC circuit | 5 | ohms_law, capacitance |
| 7 | magnetic_force | Compute F = qv x B on moving charge | 5 | cross_product |
| 8 | faraday_law | Compute induced EMF from changing flux | 6 | derivative |
| 9 | rlc_impedance | Compute impedance of RLC circuit | 6 | complex_arithmetic |
| 10 | ac_power | Compute real/reactive/apparent power in AC circuit | 6 | rlc_impedance |
| 11 | maxwell_displacement | Compute displacement current from changing E field | 6 | faraday_law |
| 12 | electromagnetic_wave | Relate E, B, c in plane wave | 5 | wave_equation |

### 2.2 Thermodynamics (file: `generators/thermodynamics.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | first_law | Apply dU = Q - W for thermodynamic process | 4 | addition, subtraction |
| 2 | work_pv | Compute W = integral P dV for process | 5 | definite_integral |
| 3 | heat_capacity | Compute Q = mc*dT or Q = nC*dT | 4 | multiplication |
| 4 | carnot_efficiency | Compute efficiency eta = 1 - T_cold/T_hot | 4 | division |
| 5 | entropy_change | Compute dS = Q_rev/T for reversible process | 5 | division, logarithm |
| 6 | free_energy | Compute Gibbs/Helmholtz free energy change | 5 | first_law, entropy_change |
| 7 | clausius_inequality | Verify Clausius inequality for cycle | 6 | entropy_change |
| 8 | phase_transition | Compute latent heat and Clausius-Clapeyron | 6 | derivative |
| 9 | adiabatic_process | Compute PV^gamma relations | 5 | exponentiation |
| 10 | heat_engine_cycle | Analyze multi-step thermodynamic cycle | 6 | work_pv |

### 2.3 Special Relativity (file: `generators/relativity.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | lorentz_factor | Compute gamma = 1/sqrt(1 - v^2/c^2) | 5 | square_root |
| 2 | time_dilation | Compute dilated time dt' = gamma * dt | 5 | lorentz_factor |
| 3 | length_contraction | Compute contracted length L' = L/gamma | 5 | lorentz_factor |
| 4 | relativistic_energy | Compute E = gamma*mc^2, KE = (gamma-1)mc^2 | 5 | lorentz_factor |
| 5 | spacetime_interval | Compute ds^2 = -c^2*dt^2 + dx^2 + dy^2 + dz^2 | 5 | exponentiation |
| 6 | lorentz_transform | Apply Lorentz boost to (t,x) coordinates | 6 | lorentz_factor |
| 7 | velocity_addition | Relativistic velocity addition u' = (u+v)/(1+uv/c^2) | 5 | division |
| 8 | four_momentum | Compute four-momentum components | 6 | relativistic_energy |

### 2.4 Optics (file: `generators/optics.py`, tier 4-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | snells_law | Apply n1*sin(t1) = n2*sin(t2) | 4 | sin_cos_eval |
| 2 | thin_lens | Apply 1/f = 1/do + 1/di for thin lens | 4 | division |
| 3 | magnification | Compute magnification M = -di/do | 4 | division |
| 4 | double_slit | Compute fringe spacing in double-slit experiment | 5 | sin_cos_eval |
| 5 | brewster_angle | Compute Brewster angle tan(tB) = n2/n1 | 5 | snells_law |
| 6 | diffraction_grating | Compute d*sin(theta) = m*lambda | 5 | snells_law |

### 2.5 Fluid Mechanics (file: `generators/fluid_mechanics.py`, tier 4-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | bernoulli | Apply P + 0.5*rho*v^2 + rho*g*h = const | 4 | multiplication |
| 2 | reynolds_number | Compute Re = rho*v*L/mu, classify flow | 4 | multiplication, division |
| 3 | continuity_eq | Apply A1*v1 = A2*v2 for incompressible flow | 4 | division |
| 4 | drag_force | Compute F_d = 0.5*C_d*rho*A*v^2 | 5 | multiplication |
| 5 | buoyancy | Compute buoyant force F_b = rho*g*V | 4 | multiplication |
| 6 | viscous_flow | Hagen-Poiseuille flow rate Q = pi*r^4*dP/(8*mu*L) | 5 | multiplication |

### 2.6 Nuclear Physics (file: `generators/nuclear_physics.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | mass_defect | Compute mass defect dm and binding energy E=dm*c^2 | 5 | subtraction, multiplication |
| 2 | binding_energy_per_nucleon | Compute BE/A from mass defect | 5 | mass_defect |
| 3 | radioactive_decay | N(t) = N_0 * e^(-lambda*t), compute remaining | 5 | exponentiation |
| 4 | half_life | Compute half-life from decay constant | 5 | logarithm |
| 5 | decay_chain | Follow decay chain (alpha/beta) track Z, A | 5 | subtraction |
| 6 | nuclear_reaction | Balance nuclear reaction, compute Q value | 6 | mass_defect |

### 2.7 Signal Processing (file: `generators/signal_processing.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | dft_compute | Compute DFT of small signal (N=4 or 8) | 6 | complex_arithmetic, summation |
| 2 | sampling_theorem | Determine Nyquist rate, check aliasing | 5 | multiplication |
| 3 | fir_filter | Apply FIR filter coefficients to signal | 5 | convolution |
| 4 | z_transform | Compute Z-transform of finite sequence | 6 | exponentiation, summation |
| 5 | transfer_function | Compute H(z) = Y(z)/X(z) for LTI system | 6 | z_transform |
| 6 | frequency_response | Evaluate H(e^jw) at given frequencies | 6 | transfer_function |

### 2.8 Control Theory (file: `generators/control_theory.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | transfer_function_sys | Compute transfer function from ODE | 5 | laplace_transform |
| 2 | pid_response | Compute PID controller output for error signal | 5 | derivative, integral |
| 3 | stability_routh | Apply Routh-Hurwitz criterion | 6 | polynomial_eval |
| 4 | bode_magnitude | Compute magnitude in dB at given frequency | 5 | logarithm |
| 5 | state_space | Convert transfer function to state space | 6 | matrix_multiply |
| 6 | feedback_gain | Compute closed-loop transfer function | 5 | division |

---

## Phase 3: Chemistry & Biology (~70 generators)

### 3.1 General Chemistry (file: `generators/general_chemistry.py`, tier 3-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | electron_config | Write electron configuration for element | 3 | counting |
| 2 | periodic_trend | Compare ionization energy/electronegativity/radius | 3 | comparison |
| 3 | lewis_structure | Draw Lewis structure (count bonds + lone pairs) | 4 | electron_config |
| 4 | vsepr_geometry | Predict molecular geometry from electron groups | 4 | lewis_structure |
| 5 | hybridisation | Determine hybridisation (sp, sp2, sp3) | 4 | vsepr_geometry |
| 6 | oxidation_state | Assign oxidation states in compound | 4 | balancing_equation |
| 7 | electronegativity_bond | Classify bond as ionic/polar/nonpolar | 3 | periodic_trend |
| 8 | ideal_gas_stoich | Gas stoichiometry with PV=nRT | 5 | ideal_gas, stoichiometry |

### 3.2 Physical Chemistry (file: `generators/physical_chemistry.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | rate_law | Determine rate from rate law expression | 5 | exponentiation, multiplication |
| 2 | arrhenius | Compute k from Arrhenius equation | 5 | exponentiation, logarithm |
| 3 | equilibrium_constant | Compute K from concentrations | 5 | multiplication, division |
| 4 | le_chatelier | Predict equilibrium shift from perturbation | 5 | equilibrium_constant |
| 5 | hess_law | Calculate enthalpy change using Hess's law | 5 | addition |
| 6 | nernst_equation | Compute cell potential under non-standard conditions | 6 | logarithm |
| 7 | gibbs_spontaneity | Determine spontaneity from dG = dH - TdS | 5 | multiplication, subtraction |
| 8 | reaction_order | Determine reaction order from data (method of initial rates) | 5 | logarithm, linear_regression |

### 3.3 Organic Chemistry (file: `generators/organic_chemistry.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | iupac_naming | Name simple organic molecule (alkane/alkene/alkyne) | 4 | counting |
| 2 | functional_group | Identify functional group from structure | 4 | iupac_naming |
| 3 | degree_unsaturation | Compute degrees of unsaturation from formula | 4 | division |
| 4 | stereocenter_count | Count R/S stereocenters in molecule | 5 | functional_group |
| 5 | sn1_vs_sn2 | Predict substitution mechanism from substrate/nucleophile | 5 | functional_group |
| 6 | reaction_product | Predict major product of organic reaction | 6 | sn1_vs_sn2 |
| 7 | polymer_unit | Identify monomer and repeat unit | 5 | functional_group |
| 8 | isomer_count | Count structural isomers for given formula | 5 | degree_unsaturation |

### 3.4 Biochemistry (file: `generators/biochemistry.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | amino_acid_property | Identify properties (polar/nonpolar/charge) at given pH | 4 | ph_calculation |
| 2 | peptide_bond_count | Count peptide bonds in polypeptide | 3 | subtraction |
| 3 | michaelis_menten | Compute reaction rate V = Vmax*[S]/(Km+[S]) | 5 | division |
| 4 | lineweaver_burk | Compute 1/V vs 1/[S] intercepts for Km, Vmax | 5 | linear_regression |
| 5 | dna_complement | Write complementary DNA strand (A-T, G-C) | 3 | string_reverse |
| 6 | codon_translate | Translate mRNA codons to amino acid sequence | 4 | dna_complement |
| 7 | protein_mass | Estimate protein molecular weight from sequence | 4 | multiplication, addition |
| 8 | enzyme_inhibition | Classify inhibitor type from kinetic data | 6 | michaelis_menten |

### 3.5 Genetics (file: `generators/genetics.py`, tier 3-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | punnett_square | Complete Punnett square for monohybrid cross | 3 | basic_prob |
| 2 | dihybrid_cross | Compute phenotype ratios for dihybrid cross | 4 | punnett_square |
| 3 | hardy_weinberg | Compute allele/genotype frequencies from p+q=1 | 4 | quadratic |
| 4 | chi_square_genetics | Chi-square test for Mendelian ratio | 5 | hypothesis_test |
| 5 | linked_genes | Compute recombination frequency from test cross | 4 | division |
| 6 | blood_type | Determine possible blood types from parental genotypes | 3 | punnett_square |

### 3.6 Ecology (file: `generators/ecology.py`, tier 4-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | logistic_growth | Compute N(t) with carrying capacity K | 4 | exponentiation |
| 2 | lotka_volterra | One step of predator-prey dynamics | 5 | system_equations |
| 3 | population_doubling | Compute doubling time from growth rate | 4 | logarithm |
| 4 | trophic_efficiency | Compute energy transfer between trophic levels (10% rule) | 4 | multiplication |
| 5 | species_diversity | Compute Shannon diversity index H' | 5 | info_entropy |
| 6 | carrying_capacity | Estimate K from population data | 5 | logistic_growth |

---

## Phase 4: Computer Science (~60 generators)

### 4.1 Cryptography (file: `generators/cryptography.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | rsa_keygen | Generate RSA keys from two primes (compute n, phi, e, d) | 6 | totient, mod_inv |
| 2 | rsa_encrypt | Encrypt message m^e mod n | 6 | mod_pow |
| 3 | rsa_decrypt | Decrypt ciphertext c^d mod n | 6 | mod_pow |
| 4 | diffie_hellman | Compute shared secret from DH key exchange | 6 | mod_pow |
| 5 | elliptic_curve_add | Point addition on elliptic curve y^2 = x^3 + ax + b | 6 | mod_inv |
| 6 | hash_collision | Find collision in simple hash function | 5 | modular |
| 7 | digital_signature | Verify signature using public key | 6 | rsa_encrypt |
| 8 | otp_encrypt | Apply one-time pad (XOR) encryption | 4 | binary_arithmetic |
| 9 | feistel_round | Compute one round of Feistel cipher | 5 | binary_arithmetic |
| 10 | aes_mixcolumn | Compute one AES MixColumns step in GF(2^8) | 6 | polynomial_multiply |

### 4.2 Automata & Languages (file: `generators/formal_languages.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | nfa_to_dfa | Convert NFA to DFA via subset construction | 5 | nfa_simulate |
| 2 | regex_to_nfa | Convert simple regex to NFA (Thompson's) | 5 | regex_match |
| 3 | cfg_derivation | Derive string from context-free grammar | 5 | regex_match |
| 4 | cfg_ambiguity | Determine if grammar is ambiguous (find two parse trees) | 6 | cfg_derivation |
| 5 | pushdown_simulate | Simulate pushdown automaton on input string | 5 | stack_operations, dfa_accept |
| 6 | pumping_lemma | Apply pumping lemma to show language is not regular | 6 | proof_by_contradiction |
| 7 | chomsky_normal | Convert grammar to Chomsky normal form | 6 | cfg_derivation |
| 8 | language_classify | Classify language in Chomsky hierarchy | 6 | chomsky_normal |

### 4.3 Information Theory (file: `generators/information_theory.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | channel_capacity | Compute capacity C = max I(X;Y) for binary channel | 6 | mutual_information |
| 2 | huffman_coding | Build Huffman tree and compute codewords | 5 | info_entropy |
| 3 | hamming_encode | Encode data word with Hamming(7,4) code | 5 | binary_arithmetic |
| 4 | hamming_decode | Detect and correct single-bit error | 5 | hamming_encode |
| 5 | source_coding | Compute expected code length, check Kraft inequality | 5 | info_entropy |
| 6 | error_rate | Compute bit error rate for given channel | 5 | basic_prob |

### 4.4 Databases & Systems (file: `generators/systems.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | relational_algebra | Evaluate select/project/join on small tables | 4 | set_operations |
| 2 | normalisation | Identify functional dependencies, normalize to 3NF | 5 | relational_algebra |
| 3 | sql_equivalence | Determine if two SQL queries are equivalent | 5 | relational_algebra |
| 4 | scheduling_algorithm | Simulate FIFO/SJF/Round-Robin CPU scheduling | 4 | sorting |
| 5 | page_replacement | Simulate LRU/FIFO page replacement, count faults | 4 | queue_operations |
| 6 | subnet_calculate | Compute network/broadcast/host range from CIDR | 4 | binary_arithmetic |
| 7 | consistent_hashing | Determine key placement on hash ring | 5 | hash_table_ops |
| 8 | vector_clock | Update vector clocks for distributed events | 5 | comparison |

### 4.5 Compiler/PL Theory (file: `generators/compilers.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | tokenize | Tokenize simple expression into token stream | 4 | regex_match |
| 2 | recursive_descent | Parse expression with recursive descent | 5 | tokenize |
| 3 | first_follow_set | Compute FIRST and FOLLOW sets for grammar | 5 | cfg_derivation |
| 4 | ll1_parse_table | Build LL(1) parse table from FIRST/FOLLOW | 6 | first_follow_set |
| 5 | type_check | Type-check simple expressions (int, float, bool) | 5 | recursive_descent |
| 6 | lambda_reduce | Perform beta reduction on lambda calculus term | 6 | expression_simplify |

---

## Phase 5: Quantum (~20 generators)

### 5.1 Quantum Mechanics (file: `generators/quantum_mechanics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | schrodinger_1d | Solve 1D particle-in-box energies E_n = n^2*h^2/(8mL^2) | 5 | exponentiation |
| 2 | uncertainty_compute | Compute dx*dp >= hbar/2 for given state | 5 | std_dev |
| 3 | commutator | Compute [A,B] = AB - BA for simple operators | 6 | matrix_multiply |
| 4 | angular_momentum | Compute L^2 and L_z eigenvalues from quantum numbers | 5 | exponentiation |
| 5 | spin_addition | Add angular momenta j1 + j2 -> j values | 6 | angular_momentum |
| 6 | hydrogen_energy | Compute hydrogen energy levels E_n = -13.6/n^2 eV | 5 | division |

### 5.2 Quantum Information (file: `generators/quantum_info.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | bell_state | Construct Bell states from CNOT + Hadamard | 6 | quantum_gate |
| 2 | entanglement_measure | Compute concurrence or entropy of entanglement | 7 | eigenvalue |
| 3 | quantum_teleportation | Step through teleportation protocol | 7 | bell_state |
| 4 | grover_step | Compute one Grover iteration (oracle + diffusion) | 6 | quantum_gate |
| 5 | qft_compute | Compute 2-qubit quantum Fourier transform | 7 | quantum_gate, dft_compute |
| 6 | error_syndrome | Compute syndrome for 3-qubit bit-flip code | 6 | quantum_gate |
| 7 | density_matrix | Compute density matrix for mixed state | 6 | matrix_multiply |
| 8 | no_cloning | Prove no-cloning theorem for specific states | 7 | quantum_gate |

---

## Phase 6: Earth/Space/Social Sciences (~30 generators)

### 6.1 Astronomy (file: `generators/astronomy.py`, tier 4-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | parallax_distance | Compute distance from parallax angle | 4 | division |
| 2 | hr_diagram | Classify star from temperature and luminosity | 4 | comparison |
| 3 | absolute_magnitude | Compute M from m and distance | 5 | logarithm |
| 4 | doppler_velocity | Compute radial velocity from spectral shift | 4 | redshift |
| 5 | tidal_force | Compute tidal acceleration from mass and distance | 5 | gravitational_force |
| 6 | drake_equation | Estimate N from Drake equation factors | 4 | multiplication |

### 6.2 Geology (file: `generators/geology.py`, tier 4-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | radiometric_dating | Compute age from parent/daughter ratio | 5 | half_life |
| 2 | seismic_velocity | Compute distance from P-S wave time difference | 4 | multiplication |
| 3 | mohs_hardness | Rank minerals by hardness, predict scratching | 3 | comparison |
| 4 | richter_magnitude | Compute Richter magnitude from amplitude ratio | 4 | logarithm |

### 6.3 Linguistics (file: `generators/linguistics.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | chomsky_classify | Classify grammar in Chomsky hierarchy | 5 | cfg_derivation |
| 2 | morpheme_parse | Count morphemes in word (prefix + root + suffix) | 3 | counting |
| 3 | syntax_tree | Build parse tree for simple sentence | 4 | recursive_descent |
| 4 | phonetic_features | Identify distinctive features of phoneme | 4 | set_membership |
| 5 | regular_language_check | Determine if language is regular from description | 5 | pumping_lemma |

### 6.4 Advanced Economics (file: `generators/advanced_economics.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | cobb_douglas | Compute output Y = A*K^alpha*L^(1-alpha) | 5 | exponentiation |
| 2 | elasticity | Compute price elasticity of demand | 4 | derivative |
| 3 | auction_revenue | Compute expected revenue in second-price auction | 5 | expected_value |
| 4 | supply_demand | Find equilibrium price and quantity | 4 | system_equations |
| 5 | comparative_advantage | Determine comparative advantage from opportunity costs | 4 | division |
| 6 | utility_maximise | Maximize utility subject to budget constraint | 5 | lagrange_multiplier |

---

## Phase 7: Expanded AI/ML & Meta-reasoning (~20 generators)

### 7.1 Advanced ML (file: `generators/advanced_ml.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | attention_multihead | Compute multi-head attention output | 6 | attention_score |
| 2 | layer_norm | Compute layer normalization | 5 | arithmetic_mean, std_dev |
| 3 | positional_encoding | Compute sinusoidal positional encoding | 5 | sin_cos_eval |
| 4 | beam_search_step | Compute one step of beam search decoding | 5 | softmax_eval |
| 5 | contrastive_loss | Compute InfoNCE / contrastive loss | 6 | cross_entropy |
| 6 | transformer_flops | Estimate FLOPs for transformer forward pass | 6 | multiplication |
| 7 | lr_schedule | Compute learning rate at step t (warmup + cosine) | 5 | sin_cos_eval |
| 8 | weight_init | Compute Xavier/He initialization variance | 5 | division, square_root |

### 7.2 Meta-reasoning Extensions (file: `generators/meta_reasoning_ext2.py`, tier 7-10)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | proof_strategy | Select appropriate proof strategy for given statement | 7 | verify_proof |
| 2 | dimensional_check | Verify dimensional consistency of physics equation | 7 | dimensional_analysis |
| 3 | approximation_bound | Bound error of numerical approximation | 7 | taylor_series |
| 4 | research_methodology | Design experiment to test mathematical conjecture | 9 | hypothesis_design |
| 5 | theorem_dependency | Identify which theorems are needed for a proof | 8 | verify_proof |

---

## Execution Plan

### Priority order (by impact on reasoning coverage)
1. **Phase 2.1-2.2** (EM + Thermo) -- fundamental physics, high prerequisite demand
2. **Phase 1.1-1.2** (Abstract Algebra + Real Analysis) -- mathematical maturity
3. **Phase 4.1** (Cryptography) -- applied number theory, high depth
4. **Phase 3.1-3.2** (General + Physical Chemistry) -- fills biggest domain gap
5. **Phase 2.3** (Special Relativity) -- conceptually rich
6. **Phase 3.5** (Genetics) -- accessible, strong prerequisite structure
7. **Phase 1.3-1.4** (Complex Analysis + Topology) -- graduate mathematics
8. **Phase 4.2-4.3** (Formal Languages + Info Theory) -- CS foundations
9. **Phase 5** (Quantum expanded) -- builds on existing quantum base
10. **Phase 3.3-3.4** (Organic + Biochemistry) -- domain depth
11. **Phase 2.4-2.6** (Optics, Fluids, Nuclear) -- physics breadth
12. **Phase 6** (Earth/Space/Social) -- breadth coverage
13. **Phase 2.7-2.8** (Signal Processing, Control) -- engineering
14. **Phase 1.5-1.7** (DiffGeo, Optimization, NT extensions) -- mathematical depth
15. **Phase 4.4-4.5** (Systems, Compilers) -- CS depth
16. **Phase 7** (Advanced ML, Meta-reasoning) -- AI training relevance

### Per-phase deliverables
- [ ] Generator file with all generators in the table
- [ ] Atoms file with Wikipedia-sourced atoms for each task
- [ ] `_EXTRA_PREREQUISITES` entries in `curriculum/registry.py` as needed
- [ ] Import in `generators/__init__.py`
- [ ] Update hardcoded count in `test_structural.py` and `test_skill_tree_full.py`
- [ ] Run `python -m pytest tests/ -q` -- all pass
- [ ] Run `engram-validate --all --samples 5` -- no crashes
- [ ] Commit with summary of generators added

---

## Phase 8: Graduate Mathematics (~100 generators)

### 8.1 Measure Theory (file: `generators/measure_theory.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | sigma_algebra | Verify if collection is a sigma-algebra | 6 | set_operations |
| 2 | measurable_function | Check if function is measurable | 6 | sigma_algebra |
| 3 | lebesgue_measure | Compute Lebesgue measure of set in R | 6 | supremum_infimum |
| 4 | simple_function_integral | Integrate simple function (sum of indicators) | 6 | lebesgue_measure |
| 5 | dominated_convergence | Apply DCT to exchange limit and integral | 7 | uniform_convergence |
| 6 | monotone_convergence | Apply MCT to increasing function sequence | 7 | sequence_convergence |
| 7 | fubini_compute | Apply Fubini's theorem to iterated integral | 7 | definite_integral |
| 8 | borel_set | Identify Borel set from construction | 6 | open_closed_sets |

### 8.2 Functional Analysis (file: `generators/functional_analysis.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | norm_compute | Compute L1, L2, L_inf norms | 5 | vector_norm |
| 2 | banach_space_check | Verify completeness for given norm | 6 | cauchy_sequence |
| 3 | inner_product | Compute inner product, verify axioms | 5 | dot_product |
| 4 | orthogonal_projection | Project vector onto subspace | 6 | inner_product |
| 5 | adjoint_operator | Compute adjoint of linear operator | 6 | matrix_transpose |
| 6 | spectral_decomposition | Decompose symmetric matrix via eigenvalues | 6 | eigenvalue |
| 7 | compact_operator | Verify if operator is compact on finite-dim space | 7 | spectral_decomposition |
| 8 | dual_space | Compute dual basis for finite-dim space | 6 | matrix_inverse |
| 9 | hahn_banach | Apply Hahn-Banach to extend functional | 7 | dual_space |
| 10 | riesz_representation | Identify representing element for functional | 7 | inner_product |

### 8.3 Algebraic Geometry (file: `generators/algebraic_geometry.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | variety_points | Find points on algebraic variety V(f) over F_p | 6 | modular, polynomial_eval |
| 2 | ideal_membership | Test if polynomial is in ideal using Groebner basis | 7 | polynomial_division |
| 3 | bezout_intersection | Count intersection points of two curves (Bezout's theorem) | 6 | system_equations |
| 4 | elliptic_curve_group | Compute point addition on elliptic curve | 6 | mod_inv |
| 5 | projective_coords | Convert affine to projective coordinates | 6 | gcd |
| 6 | genus_compute | Compute genus of algebraic curve | 7 | bezout_intersection |
| 7 | rational_points | Find rational points on conic section | 6 | quadratic |
| 8 | tangent_line_variety | Compute tangent line to curve at point | 6 | partial_derivative |

### 8.4 Category Theory (file: `generators/category_theory.py`, tier 7-8)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | morphism_compose | Compose morphisms in small category | 7 | group_table |
| 2 | functor_apply | Apply functor between categories | 7 | morphism_compose |
| 3 | natural_transform | Verify naturality square commutes | 7 | functor_apply |
| 4 | product_category | Construct product in category | 7 | morphism_compose |
| 5 | coproduct_category | Construct coproduct in category | 7 | product_category |
| 6 | adjunction_check | Verify adjunction between functors | 8 | natural_transform |
| 7 | yoneda_apply | Apply Yoneda lemma to representable functor | 8 | natural_transform |
| 8 | limit_compute | Compute limit of diagram in Set | 7 | product_category |

### 8.5 Representation Theory (file: `generators/representation_theory.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | character_compute | Compute character of representation (trace) | 6 | matrix_trace |
| 2 | character_table | Build character table for small group | 7 | character_compute |
| 3 | irreducible_check | Check if representation is irreducible | 7 | character_table |
| 4 | decompose_rep | Decompose representation into irreducibles | 7 | irreducible_check |
| 5 | tensor_rep | Compute tensor product of representations | 7 | tensor_product |
| 6 | schur_lemma | Apply Schur's lemma to morphism between irreps | 7 | irreducible_check |

### 8.6 Stochastic Processes (file: `generators/stochastic.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | random_walk | Compute probability of reaching state in random walk | 5 | basic_prob |
| 2 | markov_stationary | Find stationary distribution of Markov chain | 5 | markov_chain |
| 3 | markov_absorption | Compute absorption probabilities | 6 | markov_stationary |
| 4 | birth_death | Compute steady-state of birth-death chain | 6 | markov_stationary |
| 5 | poisson_process | Compute inter-arrival and counting probabilities | 5 | poisson_dist |
| 6 | brownian_motion | Compute properties of Brownian motion (E[B_t], Var) | 6 | std_dev |
| 7 | martingale_check | Verify if process is a martingale (E[X_{n+1}|F_n] = X_n) | 7 | expected_value |
| 8 | renewal_theory | Compute renewal function for given distribution | 7 | poisson_process |

### 8.7 Partial Differential Equations (file: `generators/pde.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | classify_pde | Classify PDE as elliptic/parabolic/hyperbolic | 6 | partial_derivative |
| 2 | heat_equation | Solve 1D heat equation by separation of variables | 6 | separation_of_variables, fourier_coefficient |
| 3 | wave_equation_1d | Solve 1D wave equation (d'Alembert) | 6 | separation_of_variables |
| 4 | laplace_equation | Solve Laplace equation on rectangle | 7 | heat_equation |
| 5 | method_of_characteristics | Solve first-order PDE by characteristics | 7 | diff_equation |
| 6 | greens_function | Compute Green's function for simple operator | 7 | laplace_equation |
| 7 | fourier_transform_pde | Solve PDE using Fourier transform | 7 | dft_compute |
| 8 | finite_difference | Discretise PDE using finite differences | 6 | numerical_derivative |

### 8.8 Tensor Analysis (file: `generators/tensor_analysis.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | tensor_contraction | Contract indices of rank-2 tensor | 6 | matrix_trace |
| 2 | covariant_derivative | Compute covariant derivative with Christoffel symbols | 7 | christoffel_symbol |
| 3 | metric_tensor | Compute metric tensor for coordinate system | 6 | partial_derivative |
| 4 | ricci_tensor | Compute Ricci tensor from Christoffel symbols | 7 | covariant_derivative |
| 5 | levi_civita | Evaluate Levi-Civita symbol permutations | 5 | permutation |
| 6 | index_gymnastics | Raise/lower indices using metric tensor | 6 | metric_tensor |

### 8.9 Discrete Mathematics Extensions (file: `generators/discrete_ext.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | generating_function | Find generating function for sequence | 6 | power_series_radius |
| 2 | ramsey_number | Compute R(s,t) for small s,t | 5 | pigeonhole |
| 3 | burnside_counting | Count distinct colorings under group action | 6 | group_order |
| 4 | hall_marriage | Verify Hall's condition for bipartite matching | 5 | bipartite_check |
| 5 | matroid_check | Verify matroid axioms for given independent sets | 6 | set_operations |
| 6 | chromatic_polynomial | Compute chromatic polynomial of small graph | 6 | graph_coloring |
| 7 | flow_network | Compute max flow via Ford-Fulkerson on small network | 5 | bfs_order |
| 8 | planar_check | Check if graph is planar (Euler's formula / K_{3,3}) | 5 | euler_characteristic |
| 9 | lattice_operations | Compute meet and join in finite lattice | 5 | set_operations |
| 10 | partition_function | Count integer partitions of n | 5 | catalan |

---

## Phase 9: Advanced Physics (~80 generators)

### 9.1 Classical Mechanics (Analytical) (file: `generators/analytical_mechanics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | lagrangian | Write Lagrangian L = T - V for simple system | 5 | kinetic_energy, potential_energy |
| 2 | euler_lagrange_mech | Derive equation of motion from Lagrangian | 6 | euler_lagrange |
| 3 | hamiltonian | Compute Hamiltonian H from Legendre transform | 6 | lagrangian |
| 4 | hamilton_equations | Write Hamilton's equations for given H | 6 | hamiltonian |
| 5 | noether_theorem | Identify conserved quantity from symmetry | 7 | lagrangian |
| 6 | phase_space | Sketch phase portrait for 1D system | 6 | hamilton_equations |
| 7 | normal_modes | Find normal modes of coupled oscillators | 6 | eigenvalue |
| 8 | canonical_transform | Verify canonicity of transformation | 7 | hamilton_equations |

### 9.2 Statistical Mechanics (file: `generators/statistical_mechanics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | partition_function_stat | Compute Z = sum exp(-E_i/kT) for discrete system | 5 | exponentiation |
| 2 | boltzmann_probability | Compute P_i = exp(-E_i/kT)/Z | 5 | partition_function_stat |
| 3 | average_energy | Compute <E> = -d(ln Z)/d(beta) | 6 | partition_function_stat |
| 4 | fermi_dirac | Compute Fermi-Dirac occupation f(E) | 5 | exponentiation |
| 5 | bose_einstein | Compute Bose-Einstein distribution n(E) | 5 | exponentiation |
| 6 | ising_model | Compute energy and magnetization of 1D Ising chain | 6 | summation |
| 7 | entropy_stat_mech | Compute S = k_B ln(Omega) for microcanonical ensemble | 5 | logarithm |
| 8 | equipartition | Apply equipartition theorem (E = f/2 * kT) | 5 | multiplication |
| 9 | specific_heat | Compute C_V from partition function | 6 | average_energy |
| 10 | grand_canonical | Compute grand partition function with chemical potential | 7 | partition_function_stat |

### 9.3 General Relativity (file: `generators/general_relativity.py`, tier 6-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | schwarzschild_metric | Write Schwarzschild metric components | 6 | metric_tensor |
| 2 | gravitational_redshift | Compute frequency shift in gravitational field | 6 | schwarzschild_radius |
| 3 | geodesic_schwarzschild | Compute geodesic in Schwarzschild spacetime | 7 | geodesic_equation |
| 4 | einstein_tensor | Compute Einstein tensor G_mn for simple metric | 7 | ricci_tensor |
| 5 | cosmological_expansion | Friedmann equation: compute scale factor evolution | 7 | diff_equation |
| 6 | gravitational_wave_strain | Compute GW strain h from source parameters | 6 | gravitational_lensing |
| 7 | perihelion_precession | Compute precession angle for orbit | 7 | geodesic_schwarzschild |
| 8 | cosmic_distance | Compute comoving/luminosity/angular diameter distance | 6 | definite_integral |

### 9.4 Particle Physics (file: `generators/particle_physics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | conservation_laws | Check conservation of charge/baryon/lepton number | 5 | addition |
| 2 | quark_content | Determine quark composition of hadron | 5 | conservation_laws |
| 3 | feynman_vertex | Identify allowed/forbidden vertices from SM rules | 6 | conservation_laws |
| 4 | cross_section | Compute cross-section from matrix element (toy) | 7 | definite_integral |
| 5 | decay_width | Compute partial decay width from coupling | 6 | multiplication |
| 6 | invariant_mass | Compute invariant mass from 4-momenta | 6 | four_momentum |
| 7 | cms_energy | Compute center-of-mass energy from beam energies | 5 | relativistic_energy |
| 8 | symmetry_group | Identify symmetry group of particle interaction | 7 | group_table |

### 9.5 Nonlinear Dynamics (file: `generators/nonlinear_dynamics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | fixed_point_classify | Find and classify fixed points (stable/unstable/saddle) | 5 | eigenvalue |
| 2 | bifurcation_detect | Identify bifurcation type as parameter varies | 6 | fixed_point_classify |
| 3 | lyapunov_exponent | Compute Lyapunov exponent for 1D map | 6 | logarithm |
| 4 | logistic_map | Iterate logistic map x_{n+1} = r*x_n*(1-x_n) | 5 | multiplication |
| 5 | limit_cycle | Determine if system has limit cycle (Poincare-Bendixson) | 7 | phase_space |
| 6 | strange_attractor | Iterate Henon map, classify orbit | 6 | logistic_map |
| 7 | fractal_dimension | Compute box-counting dimension | 6 | logarithm |
| 8 | chaos_sensitivity | Measure sensitivity to initial conditions | 6 | lyapunov_exponent |

### 9.6 Solid State Physics (file: `generators/solid_state.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | bragg_diffraction | Compute diffraction angle from Bragg's law | 5 | sin_cos_eval |
| 2 | miller_indices | Convert crystal planes to Miller indices | 4 | gcd |
| 3 | reciprocal_lattice | Compute reciprocal lattice vectors | 6 | cross_product |
| 4 | band_gap | Compute conduction properties from band gap | 5 | comparison |
| 5 | fermi_level | Compute Fermi level for semiconductor | 6 | fermi_dirac |
| 6 | phonon_dispersion | Compute phonon frequency for 1D chain | 6 | sin_cos_eval |
| 7 | hall_effect | Compute Hall coefficient and carrier type | 5 | division |
| 8 | debye_model | Compute specific heat from Debye model | 6 | definite_integral |

---

## Phase 10: Advanced CS & Engineering (~80 generators)

### 10.1 Algorithm Design Patterns (file: `generators/algorithm_patterns.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | divide_conquer_recurrence | Solve recurrence T(n) = aT(n/b) + f(n) (Master theorem) | 5 | recurrence_solve |
| 2 | amortised_analysis | Compute amortised cost (aggregate/accounting) | 6 | summation |
| 3 | greedy_proof | Prove greedy choice property for problem | 7 | proof_by_contradiction |
| 4 | dp_optimal_substructure | Identify optimal substructure for DP problem | 6 | memoisation |
| 5 | np_reduction | Reduce problem A to problem B (polynomial) | 7 | sat_verify |
| 6 | approximation_ratio | Compute approximation ratio for greedy algorithm | 6 | division |
| 7 | randomised_algorithm | Analyze expected runtime of randomised algorithm | 6 | expected_value |
| 8 | online_algorithm | Compute competitive ratio for online problem | 7 | approximation_ratio |

### 10.2 Machine Learning Theory (file: `generators/ml_theory.py`, tier 6-8)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | vc_dimension | Compute VC dimension for hypothesis class | 7 | learning_bound |
| 2 | pac_bound | Compute PAC sample complexity bound | 7 | vc_dimension |
| 3 | rademacher_complexity | Bound Rademacher complexity for function class | 7 | supremum_infimum |
| 4 | kernel_trick | Compute kernel function K(x,y) = phi(x).phi(y) | 6 | dot_product |
| 5 | regularisation_path | Trace L1/L2 regularisation effect on weights | 6 | gradient_descent |
| 6 | bias_variance_decompose | Decompose expected loss into bias^2 + variance + noise | 6 | bias_variance |
| 7 | cross_validation | Compute k-fold cross-validation estimate | 5 | arithmetic_mean |
| 8 | information_gain | Compute information gain for decision tree split | 5 | info_entropy |
| 9 | gradient_flow | Trace gradient flow through computation graph | 6 | backprop_simple |
| 10 | attention_complexity | Analyze time/space complexity of attention mechanisms | 7 | big_o |

### 10.3 Distributed Systems (file: `generators/distributed.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | lamport_clock | Update Lamport timestamps for events | 5 | comparison |
| 2 | vector_clock_update | Update vector clocks for send/receive events | 5 | vector_clock |
| 3 | consensus_round | Simulate one round of consensus protocol | 6 | vector_clock_update |
| 4 | cap_theorem | Identify which CAP property is sacrificed | 5 | comparison |
| 5 | consistent_hash | Compute key placement and rebalancing | 5 | hash_table_ops |
| 6 | two_phase_commit | Trace 2PC protocol with coordinator/participants | 6 | consensus_round |
| 7 | raft_election | Simulate Raft leader election round | 6 | consensus_round |
| 8 | crdt_merge | Compute CRDT merge for G-counter/PN-counter | 5 | addition |

### 10.4 Computer Graphics (file: `generators/computer_graphics.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | matrix_transform_3d | Apply rotation/scaling/translation matrix in 3D | 5 | matrix_multiply |
| 2 | perspective_projection | Project 3D point to 2D screen coordinates | 5 | matrix_transform_3d |
| 3 | ray_sphere_intersect | Compute ray-sphere intersection point | 5 | quadratic |
| 4 | barycentric_coords | Compute barycentric coordinates of point in triangle | 5 | system_equations |
| 5 | bezier_curve | Evaluate point on Bezier curve (de Casteljau) | 5 | polynomial_eval |
| 6 | phong_shading | Compute Phong illumination at surface point | 5 | dot_product, vector_norm |
| 7 | frustum_culling | Determine if point is inside view frustum | 5 | dot_product |
| 8 | quaternion_rotate | Apply quaternion rotation to 3D vector | 6 | complex_arithmetic |

### 10.5 Telecommunications (file: `generators/telecom.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | shannon_limit | Compute channel capacity C = B*log2(1 + SNR) | 5 | logarithm |
| 2 | modulation_bpsk | Compute BER for BPSK modulation | 5 | basic_prob |
| 3 | link_budget | Compute received power from Friis equation | 5 | logarithm |
| 4 | antenna_gain | Compute antenna gain from aperture | 5 | division |
| 5 | ofdm_subcarrier | Compute OFDM subcarrier frequencies | 5 | dft_compute |
| 6 | spread_spectrum | Compute processing gain for DSSS | 5 | logarithm |

### 10.6 Robotics & Planning (file: `generators/robotics.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | forward_kinematics | Compute end-effector position from joint angles | 5 | matrix_transform_3d |
| 2 | inverse_kinematics | Solve for joint angles given target position | 6 | system_equations |
| 3 | path_planning | Find path using A* on grid with obstacles | 5 | shortest_path |
| 4 | pid_control_robot | Compute PID output for robot joint control | 5 | pid_response |
| 5 | kalman_update | Compute one Kalman filter update step | 6 | matrix_multiply |
| 6 | mdp_policy | Compute optimal policy for small MDP | 6 | bellman_equation |

---

## Phase 11: Advanced Chemistry & Life Sciences (~60 generators)

### 11.1 Inorganic Chemistry (file: `generators/inorganic_chemistry.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | crystal_field | Determine d-orbital splitting in octahedral/tetrahedral field | 5 | electron_config |
| 2 | coordination_number | Determine coordination number and geometry | 4 | lewis_structure |
| 3 | isomer_coordination | Count geometric/optical isomers of complex | 5 | coordination_number |
| 4 | spectrochemical | Order ligands by spectrochemical series | 5 | crystal_field |
| 5 | magnetic_moment | Compute spin-only magnetic moment | 5 | crystal_field |
| 6 | solubility_product | Compute Ksp and predict precipitation | 5 | equilibrium_constant |

### 11.2 Spectroscopy (file: `generators/spectroscopy.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | beer_lambert | Apply A = epsilon*l*c for absorbance | 5 | logarithm |
| 2 | wavelength_energy | Convert between wavelength and photon energy | 5 | division |
| 3 | nmr_splitting | Predict NMR splitting pattern (n+1 rule) | 5 | functional_group |
| 4 | mass_spec_fragment | Identify fragment from m/z ratio | 5 | subtraction |
| 5 | ir_functional_group | Identify functional group from IR absorption frequency | 5 | functional_group |
| 6 | emission_spectrum | Compute emission wavelength from energy levels | 5 | hydrogen_energy |

### 11.3 Cell Biology (file: `generators/cell_biology.py`, tier 3-5)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | mitosis_phase | Identify mitosis phase from description | 3 | counting |
| 2 | meiosis_gametes | Compute number of unique gametes (2^n) | 4 | exponentiation |
| 3 | membrane_transport | Classify transport type (passive/active/vesicular) | 3 | comparison |
| 4 | atp_yield | Compute ATP yield from glucose metabolism | 4 | multiplication |
| 5 | cell_cycle_duration | Compute cell count after n divisions | 4 | exponentiation |
| 6 | osmolarity | Compute osmotic pressure from concentration | 4 | multiplication |

### 11.4 Bioinformatics (file: `generators/bioinformatics.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | sequence_alignment | Compute pairwise alignment score (Needleman-Wunsch) | 6 | edit_distance |
| 2 | blast_evalue | Compute E-value from bit score | 5 | exponentiation |
| 3 | phylo_distance | Compute evolutionary distance from substitution matrix | 5 | logarithm |
| 4 | gc_content | Compute GC content percentage of DNA sequence | 4 | division |
| 5 | open_reading_frame | Find longest ORF in DNA sequence | 5 | codon_translate |
| 6 | restriction_digest | Predict fragment sizes from restriction enzyme cut sites | 4 | subtraction |

### 11.5 Epidemiology (file: `generators/epidemiology.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | sir_model | Compute one step of SIR model dynamics | 5 | multiplication |
| 2 | basic_reproduction | Compute R_0 from SIR parameters | 5 | sir_model |
| 3 | incidence_rate | Compute incidence/prevalence from population data | 4 | division |
| 4 | relative_risk | Compute relative risk and odds ratio | 4 | division |
| 5 | herd_immunity | Compute herd immunity threshold 1 - 1/R_0 | 4 | basic_reproduction |
| 6 | life_table | Compute life expectancy from mortality data | 5 | summation |

### 11.6 Pharmacology (file: `generators/pharmacology.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | half_life_drug | Compute drug concentration after n half-lives | 5 | radioactive_decay |
| 2 | dose_response | Compute EC50 from Hill equation | 5 | michaelis_menten |
| 3 | bioavailability | Compute bioavailability from AUC comparison | 5 | area_under_curve |
| 4 | clearance_rate | Compute renal/hepatic clearance | 5 | division |
| 5 | steady_state | Compute steady-state concentration from dosing interval | 5 | geometric_sequence |
| 6 | therapeutic_index | Compute therapeutic index TD50/ED50 | 4 | division |

---

## Phase 12: Cognitive & Decision Sciences (~40 generators)

### 12.1 Decision Theory (file: `generators/decision_theory.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | expected_utility | Compute EU for lottery under risk aversion | 5 | expected_value |
| 2 | risk_dominance | Determine if strategy risk-dominates another | 5 | nash_equilibrium |
| 3 | bayesian_updating | Update beliefs from evidence (full Bayesian) | 5 | bayes_theorem |
| 4 | value_of_information | Compute VoI for decision under uncertainty | 6 | bayesian_updating |
| 5 | multi_criteria | Apply weighted scoring for multi-criteria decision | 5 | weighted_sum |
| 6 | prospect_theory | Compute value under prospect theory (loss aversion) | 6 | expected_utility |
| 7 | sequential_decision | Solve sequential decision via backward induction | 6 | minimax |
| 8 | mechanism_design | Design incentive-compatible mechanism (VCG) | 7 | auction_revenue |

### 12.2 Network Science (file: `generators/network_science.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | degree_distribution | Compute degree distribution of graph | 5 | connected_components |
| 2 | clustering_coefficient | Compute local/global clustering coefficient | 5 | connected_components |
| 3 | betweenness_centrality | Compute betweenness centrality for node | 6 | shortest_path |
| 4 | pagerank | Compute one iteration of PageRank | 5 | markov_chain |
| 5 | small_world | Check small-world property (high clustering + low diameter) | 5 | clustering_coefficient |
| 6 | community_detect | Apply modularity-based community detection | 6 | pagerank |

### 12.3 Cognitive Science (file: `generators/cognitive_science.py`, tier 5-7)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | signal_detection | Compute d-prime from hit/false alarm rates | 5 | z_score |
| 2 | memory_decay | Compute forgetting curve (Ebbinghaus) | 5 | exponentiation |
| 3 | reaction_time | Compute Hick's law RT = a + b*log2(n) | 4 | logarithm |
| 4 | weber_fraction | Compute Weber fraction dI/I | 4 | division |
| 5 | information_processing | Compute channel capacity of human observer | 5 | channel_capacity |
| 6 | reinforcement_learning_model | Compute Rescorla-Wagner learning update | 5 | multiplication |

---

## Phase 13: Mathematical Logic & Foundations (~30 generators)

### 13.1 Model Theory (file: `generators/model_theory.py`, tier 7-8)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | structure_check | Verify if structure is a model of theory | 7 | quantifier_eval |
| 2 | elementary_equivalence | Check if two structures satisfy same sentences | 7 | structure_check |
| 3 | compactness_apply | Apply compactness theorem to derive consequence | 8 | structure_check |
| 4 | ultraproduct | Construct ultraproduct of finite structures | 8 | compactness_apply |
| 5 | definability | Check if set is definable by first-order formula | 7 | quantifier_eval |

### 13.2 Computability Theory (file: `generators/computability.py`, tier 6-8)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | halting_problem | Argue undecidability via diagonalization | 7 | proof_by_contradiction |
| 2 | reduction_computability | Reduce language A to language B | 7 | turing_machine_step |
| 3 | rice_theorem | Apply Rice's theorem to show undecidability | 7 | halting_problem |
| 4 | recursive_enumerable | Classify language as recursive/RE/co-RE | 7 | halting_problem |
| 5 | kolmogorov_complexity | Bound Kolmogorov complexity K(x) | 7 | info_entropy |
| 6 | godel_number | Compute Godel number for formula | 6 | prime_factorisation |

### 13.3 Proof Theory (file: `generators/proof_theory.py`, tier 7-8)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | natural_deduction | Derive conclusion using natural deduction rules | 7 | deduction_chain |
| 2 | sequent_calculus | Apply cut-elimination to sequent proof | 8 | natural_deduction |
| 3 | resolution_refutation | Prove unsatisfiability by resolution | 6 | sat_verify |
| 4 | horn_clause | Evaluate Horn clause program (Prolog-style) | 6 | deduction_chain |
| 5 | modal_logic | Evaluate formula in Kripke model | 7 | propositional_eval |
| 6 | intuitionistic_logic | Identify which classical theorems fail intuitionistically | 7 | natural_deduction |

---

## Phase 14: Materials, Aerospace & Power (~30 generators)

### 14.1 Materials Science (file: `generators/materials_science.py`, tier 4-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | stress_strain | Compute stress/strain from force and dimensions | 4 | division |
| 2 | youngs_modulus | Compute Young's modulus from stress-strain data | 4 | linear_regression |
| 3 | thermal_expansion | Compute dimensional change from temperature | 4 | multiplication |
| 4 | crystal_structure | Compute atomic packing factor for FCC/BCC/HCP | 5 | volume_sphere |
| 5 | diffusion_fick | Compute diffusion flux from Fick's first law | 5 | derivative |
| 6 | phase_diagram | Read binary phase diagram (eutectic, lever rule) | 5 | linear_equation |

### 14.2 Aerospace (file: `generators/aerospace.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | thrust_equation | Compute rocket thrust F = dm/dt * v_e | 5 | multiplication |
| 2 | tsiolkovsky | Apply Tsiolkovsky rocket equation dv = v_e * ln(m0/mf) | 5 | logarithm |
| 3 | orbital_velocity | Compute circular orbital velocity v = sqrt(GM/r) | 5 | escape_velocity |
| 4 | hohmann_transfer | Compute delta-v for Hohmann transfer orbit | 6 | orbital_velocity |
| 5 | drag_coefficient | Compute drag force in atmospheric flight | 5 | drag_force |
| 6 | lift_equation | Compute lift L = 0.5*rho*v^2*S*C_L | 5 | multiplication |

### 14.3 Power Systems (file: `generators/power_systems.py`, tier 5-6)

| # | task_name | Description | Tier | Prerequisites |
|---|---|---|---|---|
| 1 | three_phase_power | Compute 3-phase power P = sqrt(3)*V*I*cos(phi) | 5 | ac_power |
| 2 | transformer_ratio | Compute voltage/current ratio from turns ratio | 4 | division |
| 3 | power_factor_correction | Compute capacitance for power factor correction | 5 | rlc_impedance |
| 4 | transmission_loss | Compute I^2*R losses in transmission line | 4 | ohms_law |
| 5 | generator_frequency | Compute frequency from speed and pole pairs | 4 | division |
| 6 | load_flow | Solve simple 2-bus load flow | 6 | system_equations |

---

## Estimated total when complete

| Domain | Current | Ph 1-7 | Ph 8-14 | Total |
|---|---|---|---|---|
| Mathematics | ~140 | +80 | +100 | **~320** |
| Physics/Engineering | ~25 | +76 | +110 | **~211** |
| Chemistry/Biology | ~5 | +54 | +60 | **~119** |
| Computer Science | ~60 | +52 | +80 | **~192** |
| Quantum | ~7 | +20 | +0 | **~27** |
| Earth/Space/Social | ~15 | +27 | +40 | **~82** |
| AI/ML + Meta | ~68 | +13 | +0 | **~81** |
| Open Problems | ~12 | +0 | +0 | **~12** |
| Logic/Foundations | ~10 | +0 | +30 | **~40** |
| Life Sciences | ~0 | +0 | +30 | **~30** |
| Decision/Cognitive | ~0 | +0 | +20 | **~20** |
| Materials/Aerospace | ~0 | +0 | +18 | **~18** |
| **Total** | **~385** | **+322** | **+488** | **~1195** |

After Phase 1-14: **~1195 generators**. With depth expansions within each phase (10-15% additional from subtopics discovered during implementation): target **~1350-1500 generators**.

Phase 15+ (future): research-frontier depth -- quantum field theory, algebraic K-theory, homological algebra, advanced condensed matter, systems biology, computational neuroscience. Pushes past 1500.
