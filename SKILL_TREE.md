# Engram Curriculum -- Skill Tree

373 tasks across 11 tiers. Nesting shows same-tier prerequisite chains.
Arrows (`<-`) show cross-tier dependencies.

Run `engram-validate --skill-tree` for the rich interactive version.

## Tier 0 -- Basic arithmetic (20 tasks)

```
├── addition
│   └── perimeter_rectangle
├── boolean_eval
├── character_count
├── comparison
├── counting
├── digit_root
├── negation
├── rounding
├── set_intersection
├── set_membership
├── set_union
├── sorting
├── string_reverse
│   └── palindrome_check
├── subtraction
├── truth_table
├── unit_conversion_length
├── unit_conversion_mass
└── unit_conversion_temp
```

## Tier 1 -- Operations (36 tasks)

```
├── absolute_value <- subtraction
├── anagram_check <- character_count
├── caesar <- addition
├── division <- subtraction
│   ├── floor_ceil
│   └── roi <- subtraction
├── expression_simplify <- addition, subtraction
├── fibonacci <- addition
├── implication <- boolean_eval
│   ├── biconditional
│   └── syllogism
├── linear_equation <- addition, subtraction
├── multiplication <- addition
│   ├── angle_conversion
│   ├── area_circle
│   ├── area_rectangle
│   │   ├── area_triangle
│   │   └── volume_box
│   ├── arithmetic_sequence <- addition
│   ├── circumference
│   ├── fraction_arithmetic <- addition
│   ├── percentage
│   ├── pythagorean <- addition
│   ├── scientific_notation
│   ├── simple_interest
│   └── sin_cos_eval
│       └── tan_eval
├── pattern_continue <- addition
├── run_length <- counting
├── sequence_next <- addition
├── set_cardinality <- set_union, set_intersection
├── set_difference <- set_membership
├── set_subset <- set_membership
├── significant_figures <- counting
├── substring_find <- character_count
└── time_arithmetic <- addition
```

## Tier 2 -- Intermediate (46 tasks)

```
├── angle_sum_triangle <- subtraction
│   └── law_of_sines <- sin_cos_eval
├── arithmetic_mean <- addition, division
├── balancing_equation <- multiplication
├── basic_prob <- division
├── binomial <- multiplication, division
├── bounding_box <- subtraction
├── break_even <- division
├── cartesian_product <- set_cardinality
├── combination_count <- multiplication, division
├── contrapositive <- implication, negation
├── depreciation <- subtraction, division
├── distance_2d <- pythagorean
├── exponentiation <- multiplication
│   ├── compound_interest <- simple_interest
│   ├── geometric_sequence <- multiplication
│   └── polynomial_eval <- multiplication
│       └── derivative
├── graph_reach <- boolean_eval
├── hamming_distance <- character_count
├── law_of_cosines <- sin_cos_eval, pythagorean
├── mean <- addition, division
├── median <- sorting
├── midpoint <- addition, division
├── mode <- sorting
├── modular <- division
│   └── gcd
├── molar_mass <- multiplication, addition
├── permutation_with_rep <- multiplication
├── pigeonhole <- division
├── power_set <- set_subset
├── prime_factorisation <- division
├── propositional_eval <- boolean_eval, implication
│   └── logical_equivalence
├── quadratic <- multiplication, subtraction
├── queue_operations <- sorting
├── recursive_trace <- multiplication
│   └── base_case_identify
├── sequence_sum <- arithmetic_sequence
├── similar_triangles <- division, multiplication
├── slope <- subtraction, division
├── square_root <- multiplication
├── stack_operations <- sorting
├── string_encode_decode <- character_count
├── venn_diagram_count <- set_cardinality
└── weighted_sum <- multiplication, addition
```

## Tier 3 -- Advanced (59 tasks)

```
├── base_conversion <- division, modular
│   └── binary_arithmetic <- addition
├── bfs_order <- graph_reach
│   └── connected_components
├── binary_tree_traversal <- stack_operations
├── bisection_method <- division
├── boolean_algebra <- boolean_eval
├── call_stack_depth <- recursive_trace
├── circle_arc_length <- circumference
├── collatz <- division, multiplication
├── conditional_prob <- basic_prob, division
├── convergent_series <- geometric_sequence
├── cycle_detect <- graph_reach
├── deduction_chain <- propositional_eval, contrapositive
│   └── direct_proof <- implication
├── determinant <- multiplication, subtraction
├── dfa_accept <- boolean_eval
├── dfs_order <- graph_reach
├── dot_product <- multiplication, addition
├── expected_value <- multiplication, addition
├── hash_table_ops <- modular
├── heap_operations <- sorting
├── inclusion_exclusion <- combination_count, venn_diagram_count
├── independence_test <- basic_prob, multiplication
├── integral <- derivative
├── lcm <- gcd, multiplication
├── line_intersection <- slope, linear_equation
│   └── point_in_polygon
├── logic_gate_eval <- boolean_eval
├── matrix_add <- addition
├── matrix_scalar <- multiplication
├── memoisation <- recursive_trace, fibonacci
├── mod_inv <- gcd
├── mod_pow <- exponentiation, modular
├── molarity <- molar_mass, division
├── numerical_derivative <- derivative
├── payoff_matrix <- addition
│   └── dominant_strategy
├── permutation <- multiplication
├── polygon_area <- area_triangle, multiplication
├── prefix_scan <- addition, multiplication
├── present_value <- compound_interest
├── product_notation <- multiplication
├── quantifier_eval <- boolean_eval
├── recurrence_linear <- arithmetic_sequence
├── regex_match <- pattern_continue, boolean_eval
├── rpn <- addition, subtraction, multiplication
├── second_derivative <- derivative
├── sector_area <- area_circle
├── set_operations <- addition, subtraction
├── stars_and_bars <- combination_count
├── stoichiometry <- molar_mass, multiplication
├── summation <- addition, exponentiation
├── system_equations <- linear_equation, multiplication
├── trapezoidal_rule <- area_rectangle
├── trig_identity <- sin_cos_eval, tan_eval
└── variance <- mean, exponentiation
    └── std_dev
        └── z_score <- mean
```

## Tier 4 -- Applied (57 tasks)

```
├── big_o <- multiplication
├── binomial_dist <- binomial, exponentiation
├── bipartite_check <- bfs_order
├── coin_change <- addition
├── complex_arithmetic <- multiplication, addition
│   └── complex_modulus <- exponentiation
├── conditional_independence <- conditional_prob, independence_test
├── confusion_matrix <- division
├── conv_output_size <- division, addition
├── convex_hull_check <- polygon_area
├── coordinate_rotation <- distance_2d
├── correlation <- std_dev, mean
├── cross_product <- multiplication, subtraction
├── derivative_eval <- derivative, polynomial_eval
│   └── gradient_descent
├── edit_distance <- addition
├── eigenvalue <- quadratic, determinant
├── euler_method_ode <- derivative
├── graph_coloring <- graph_reach
├── group_table <- modular
├── ideal_gas <- multiplication, division
├── kinematics_displacement <- multiplication, exponentiation
├── kinematics_velocity <- multiplication, addition
├── kinetic_energy <- multiplication, exponentiation
│   └── conservation_energy
├── knights_knaves <- deduction_chain
├── linear_regression <- mean, multiplication
├── logical_puzzle <- deduction_chain
├── lr_decay <- exponentiation, multiplication
├── matrix_inverse <- determinant
├── matrix_multiply <- multiplication, addition
├── matrix_trace <- addition
├── matrix_transpose <- matrix_add
├── minimax <- payoff_matrix
├── minimum_spanning_tree <- connected_components, sorting
├── momentum <- multiplication, system_equations
├── mse_loss <- mean, exponentiation
├── nash_equilibrium <- dominant_strategy
├── nfa_simulate <- dfa_accept, set_union
├── number_base_arithmetic <- addition, base_conversion
├── ohms_law <- linear_equation
├── partial_derivative <- derivative
├── pendulum_period <- division, multiplication
├── potential_energy <- multiplication
├── proof_by_cases <- direct_proof
├── proof_by_contradiction <- direct_proof, negation
├── reflection_2d <- distance_2d
├── separation_of_variables <- integral, derivative
├── shortest_path <- graph_reach, addition
├── total_probability <- conditional_prob, addition
├── turing_machine_step <- dfa_accept
├── twos_complement <- binary_arithmetic
├── variance_dist <- expected_value, exponentiation
├── vector_norm <- exponentiation, addition
├── volume_cylinder <- area_circle
├── volume_sphere <- area_circle
└── wave_equation <- multiplication, division
```

## Tier 5 -- Expert (55 tasks)

```
├── attention_score <- matrix_multiply, division
├── backprop_simple <- derivative_eval
├── batch_norm <- mean, variance
├── bias_variance <- mse_loss, variance
├── chain_rule <- derivative
│   ├── implicit_diff <- derivative
│   ├── integrating_factor <- separation_of_variables
│   └── related_rates <- derivative
├── characteristic_equation <- quadratic, separation_of_variables
├── complex_division <- complex_arithmetic
├── confidence_interval <- mean, std_dev, z_score
├── convolution <- multiplication, addition
├── cross_entropy <- multiplication, addition
│   └── bce_loss
├── definite_integral <- integral, subtraction
│   └── area_under_curve
├── discounted_return <- exponentiation, prefix_scan
├── divergence <- partial_derivative, addition
├── dropout_compute <- multiplication, division
├── euler_formula <- complex_arithmetic, exponentiation
├── gaussian_elimination <- matrix_multiply, division
├── gradient <- partial_derivative
├── gravitational_force <- multiplication, exponentiation, division
│   └── escape_velocity
├── hubble_law <- multiplication
├── hypothesis_test <- mean, std_dev
├── info_entropy <- multiplication, addition
│   ├── kl_divergence
│   │   └── kl_from_distributions
│   └── mutual_information
├── joint_distribution <- conditional_independence, expected_value
├── kirchhoff <- system_equations, ohms_law
├── laplace_transform <- integral
├── limit <- derivative, division
├── logarithm <- exponentiation
│   └── ph_calculation
├── markov_chain <- matrix_multiply, expected_value
│   └── markov_reward <- expected_value
├── momentum_sgd <- gradient_descent
│   └── adam_step
├── newton_raphson <- derivative, division
├── poisson_dist <- exponentiation, division
├── polynomial_division <- polynomial_eval, multiplication
├── polynomial_hash <- mod_pow, addition
├── product_rule <- derivative, multiplication
├── qubit_measure <- complex_modulus
├── quotient_rule <- derivative, multiplication
├── recurrence_solve <- multiplication, addition
├── redshift <- subtraction, division
├── ring_arithmetic <- group_table, mod_inv
├── roc_auc <- sorting, confusion_matrix
├── sigmoid_eval <- exponentiation, division
├── softmax_eval <- exponentiation, division, addition
├── taylor_series <- derivative, permutation
└── vigenere <- caesar
```

## Tier 6 -- Graduate (42 tasks)

```
├── bayes_theorem <- multiplication, division
│   └── bayes_chain <- conditional_prob
├── bellman_equation <- expected_value, multiplication
│   └── q_value_update
├── bloch_coords <- complex_modulus, euler_formula
├── catalan <- binomial
├── continued_fraction <- division, modular
├── conv_2d <- matrix_multiply, convolution
├── crt <- mod_inv, modular
├── de_moivre <- complex_modulus, exponentiation
├── derangement <- permutation, subtraction
├── diff_equation <- integral, division
│   └── system_ode <- system_equations
├── diophantine <- gcd, mod_inv
├── fourier_coefficient <- definite_integral
├── gravitational_lensing <- gravitational_force
├── group_order <- modular, multiplication
│   └── group_homomorphism <- group_table
├── integration_by_parts <- integral, product_rule
├── knapsack <- addition
├── lagrange_multiplier <- gradient, system_equations
├── lcs <- edit_distance
├── lis <- sorting
├── magnitude_distance <- division, multiplication
├── matrix_power <- matrix_multiply
├── neural_forward <- matrix_multiply, sigmoid_eval
├── orbital_period <- gravitational_force, exponentiation
├── partial_deriv_multi <- partial_derivative, product_rule
├── pauli_product <- matrix_multiply
├── policy_gradient <- backprop_simple
├── polynomial_multiply <- polynomial_eval, multiplication
├── primality <- division, modular
│   └── factorisation <- division
│       ├── partial_fractions <- system_equations
│       └── totient <- multiplication
├── quadratic_residue <- mod_pow
├── quantum_gate <- qubit_measure, matrix_multiply
├── schwarzschild_radius <- gravitational_force
├── series_convergence <- limit, division
├── stellar_luminosity <- exponentiation, multiplication
├── tensor_product <- matrix_multiply
└── topo_sort <- graph_reach
```

## Tier 7 -- Meta-reasoning (18 tasks)

```
├── constraint_optimisation <- lagrange_multiplier
├── construct_polynomial <- polynomial_eval, quadratic
│   └── problem_construction
├── counterexample <- primality, exponentiation
├── derive_formula <- quadratic, polynomial_multiply
│   └── derive_identity
├── dimensional_analysis <- multiplication, division
├── error_detection <- derivative, addition
│   └── error_correction
├── estimate_magnitude <- exponentiation, multiplication
├── generalise_sequence <- polynomial_eval
├── inverse_problem <- derivative, integral
├── method_selection <- quadratic, system_equations
├── proof_by_induction <- addition, multiplication
│   ├── strong_induction
│   └── verify_proof
├── sufficiency_analysis <- linear_equation
└── symmetry_detection <- polynomial_eval
```

## Tier 8 -- Creative (13 tasks)

```
├── analogy_completion <- generalise_sequence
├── complexity_reduction <- method_selection, derive_formula
│   └── solution_elegance
├── conjecture_generation <- generalise_sequence
├── cross_domain_transfer <- generalise_sequence, derive_formula
├── equation_construction <- polynomial_multiply, quadratic
├── isomorphism_detection <- method_selection, generalise_sequence
│   └── abstraction_level
├── minimal_axioms <- derive_formula
├── novel_problem <- problem_construction
├── problem_transformation <- quadratic, method_selection
│   └── dual_problem
└── self_evaluation <- error_detection, estimate_magnitude
```

## Tier 9 -- Research (14 tasks)

```
├── algorithm_design <- method_selection, sorting
│   ├── algorithm_improvement
│   ├── complexity_analysis
│   ├── complexity_comparison
│   │   ├── information_bottleneck <- info_entropy
│   │   └── representation_choice <- method_selection
│   ├── impossibility_proof <- binomial
│   └── reduction
├── failure_analysis <- error_detection
├── hypothesis_design <- method_selection
├── invariant_discovery <- determinant, generalise_sequence
│   └── convergence_proof
├── learning_bound <- binomial_dist, info_entropy
└── meta_pattern <- error_detection, generalise_sequence
```

## Tier 10 -- Self-architecture (13 tasks)

```
├── architecture_analysis <- matrix_multiply, multiplication
│   ├── efficiency_analysis
│   │   └── bottleneck_identification
│   └── successor_design <- algorithm_improvement
├── capacity_bound <- info_entropy, exponentiation
├── failure_mode_classification <- error_detection
├── gradient_analysis <- chain_rule, derivative_eval
├── loss_design <- cross_entropy
│   └── regularisation_design
└── scaling_prediction <- exponentiation, polynomial_eval
    ├── emergent_capability
    └── training_diagnosis
        └── data_prescription
```
