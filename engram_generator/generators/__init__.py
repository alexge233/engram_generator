"""Task generators organised by domain.

Each module registers its generators via the @register decorator.
Importing this package triggers all registrations.

Module naming convention:
- Domain modules: named after the subject domain (geometry, logic, etc.)
- Meta-reasoning modules: split by tier (meta_reasoning_t7, t8, t9, t10)
- Core modules: fundamental operations (arithmetic_core, arithmetic_ops)
"""
# Core arithmetic and operations
from engram_generator.generators import arithmetic_core  # noqa: F401
from engram_generator.generators import arithmetic_ops  # noqa: F401

# Mathematical domains by complexity
from engram_generator.generators import intermediate_math  # noqa: F401
from engram_generator.generators import advanced_ops  # noqa: F401
from engram_generator.generators import applied_math  # noqa: F401
from engram_generator.generators import expert_analysis  # noqa: F401
from engram_generator.generators import graduate_foundations  # noqa: F401
from engram_generator.generators import expanded_core  # noqa: F401
from engram_generator.generators import pure_math  # noqa: F401
from engram_generator.generators import advanced_analysis  # noqa: F401
from engram_generator.generators import real_analysis  # noqa: F401
from engram_generator.generators import complex_analysis  # noqa: F401
from engram_generator.generators import differential_geometry  # noqa: F401
from engram_generator.generators import measure_theory  # noqa: F401
from engram_generator.generators import functional_analysis  # noqa: F401

# Applied science and CS
from engram_generator.generators import applied_science  # noqa: F401
from engram_generator.generators import cs_foundations  # noqa: F401

# Meta-reasoning (tiers 7-10)
from engram_generator.generators import meta_reasoning_t7  # noqa: F401
from engram_generator.generators import meta_reasoning_t8  # noqa: F401
from engram_generator.generators import meta_reasoning_t9  # noqa: F401
from engram_generator.generators import meta_reasoning_t10  # noqa: F401
from engram_generator.generators import meta_reasoning_ext  # noqa: F401
from engram_generator.generators import meta_reasoning_ext2  # noqa: F401
from engram_generator.generators import meta_reasoning_upper  # noqa: F401
from engram_generator.generators import meta_reasoning_higher  # noqa: F401

# Domain-specific modules (new, properly structured)
from engram_generator.generators import geometry  # noqa: F401
from engram_generator.generators import logic  # noqa: F401
from engram_generator.generators import set_theory  # noqa: F401
from engram_generator.generators import strings  # noqa: F401
from engram_generator.generators import trigonometry  # noqa: F401
from engram_generator.generators import measurement  # noqa: F401
from engram_generator.generators import sequences  # noqa: F401
from engram_generator.generators import combinatorics  # noqa: F401
from engram_generator.generators import chemistry  # noqa: F401
from engram_generator.generators import general_chemistry  # noqa: F401
from engram_generator.generators import physical_chemistry  # noqa: F401
from engram_generator.generators import genetics  # noqa: F401
from engram_generator.generators import biochemistry  # noqa: F401
from engram_generator.generators import organic_chemistry  # noqa: F401
from engram_generator.generators import inorganic_chemistry  # noqa: F401
from engram_generator.generators import spectroscopy  # noqa: F401
from engram_generator.generators import cell_biology  # noqa: F401
from engram_generator.generators import bioinformatics  # noqa: F401
from engram_generator.generators import ecology  # noqa: F401
from engram_generator.generators import epidemiology  # noqa: F401
from engram_generator.generators import economics  # noqa: F401
from engram_generator.generators import advanced_economics  # noqa: F401
from engram_generator.generators import game_theory  # noqa: F401
from engram_generator.generators import automata  # noqa: F401
from engram_generator.generators import formal_languages  # noqa: F401
from engram_generator.generators import linguistics  # noqa: F401
from engram_generator.generators import spatial  # noqa: F401
from engram_generator.generators import numerical  # noqa: F401
from engram_generator.generators import graphs  # noqa: F401
from engram_generator.generators import data_structures  # noqa: F401
from engram_generator.generators import recursion  # noqa: F401
from engram_generator.generators import bridge_deep  # noqa: F401
from engram_generator.generators import cryptography  # noqa: F401
from engram_generator.generators import information_theory  # noqa: F401

from engram_generator.generators import pharmacology  # noqa: F401

# Original domain modules
from engram_generator.generators import physics  # noqa: F401
from engram_generator.generators import relativity  # noqa: F401
from engram_generator.generators import electromagnetism  # noqa: F401
from engram_generator.generators import thermodynamics  # noqa: F401
from engram_generator.generators import statistics  # noqa: F401
from engram_generator.generators import advanced_probability  # noqa: F401
from engram_generator.generators import quantum  # noqa: F401
from engram_generator.generators import quantum_mechanics  # noqa: F401
from engram_generator.generators import quantum_info  # noqa: F401
from engram_generator.generators import ai_ml  # noqa: F401
from engram_generator.generators import advanced_ml  # noqa: F401
from engram_generator.generators import optics  # noqa: F401
from engram_generator.generators import fluid_mechanics  # noqa: F401
from engram_generator.generators import nuclear_physics  # noqa: F401
from engram_generator.generators import oos  # noqa: F401

# Topology
from engram_generator.generators import topology  # noqa: F401

# Abstract algebra and representation theory
from engram_generator.generators import abstract_algebra  # noqa: F401
from engram_generator.generators import representation_theory  # noqa: F401

# Open problems in mathematics
from engram_generator.generators import open_problems  # noqa: F401

# Optimization
from engram_generator.generators import optimization  # noqa: F401

# Number theory extensions
from engram_generator.generators import number_theory_ext  # noqa: F401

# Earth and space sciences
from engram_generator.generators import astronomy  # noqa: F401
from engram_generator.generators import geology  # noqa: F401

# Signal processing and control theory
from engram_generator.generators import signal_processing  # noqa: F401
from engram_generator.generators import control_theory  # noqa: F401

# Systems and compilers
from engram_generator.generators import systems  # noqa: F401
from engram_generator.generators import compilers  # noqa: F401

# Algorithm patterns, ML theory, distributed systems
from engram_generator.generators import algorithm_patterns  # noqa: F401
from engram_generator.generators import ml_theory  # noqa: F401
from engram_generator.generators import distributed  # noqa: F401

# Extended discrete mathematics
from engram_generator.generators import discrete_ext  # noqa: F401

# Stochastic processes and stochastic calculus
from engram_generator.generators import stochastic  # noqa: F401
from engram_generator.generators import stochastic_calculus  # noqa: F401

# Climate science
from engram_generator.generators import climate_science  # noqa: F401

# Biostatistics
from engram_generator.generators import biostatistics  # noqa: F401

# Algebraic geometry and category theory
from engram_generator.generators import algebraic_geometry  # noqa: F401
from engram_generator.generators import category_theory  # noqa: F401

# Partial differential equations and tensor analysis
from engram_generator.generators import pde  # noqa: F401
from engram_generator.generators import tensor_analysis  # noqa: F401

# Particle physics, nonlinear dynamics, and solid state physics
from engram_generator.generators import particle_physics  # noqa: F401
from engram_generator.generators import nonlinear_dynamics  # noqa: F401
from engram_generator.generators import solid_state  # noqa: F401

# Analytical mechanics, statistical mechanics, and general relativity
from engram_generator.generators import analytical_mechanics  # noqa: F401
from engram_generator.generators import statistical_mechanics  # noqa: F401
from engram_generator.generators import general_relativity  # noqa: F401

# Decision theory, network science, and cognitive science
from engram_generator.generators import decision_theory  # noqa: F401
from engram_generator.generators import network_science  # noqa: F401
from engram_generator.generators import cognitive_science  # noqa: F401

# Model theory, computability, and proof theory
from engram_generator.generators import model_theory  # noqa: F401
from engram_generator.generators import computability  # noqa: F401
from engram_generator.generators import proof_theory  # noqa: F401

# Materials science, aerospace, and power systems
from engram_generator.generators import materials_science  # noqa: F401
from engram_generator.generators import aerospace  # noqa: F401
from engram_generator.generators import power_systems  # noqa: F401

# Extended numerical methods and combinatorial optimisation
from engram_generator.generators import numerical_methods_ext  # noqa: F401
from engram_generator.generators import combinatorial_optimization  # noqa: F401

# Quantum field theory basics and algebraic number theory
from engram_generator.generators import qft_basics  # noqa: F401
from engram_generator.generators import algebraic_number_theory  # noqa: F401

# Computer graphics, telecommunications, and robotics
from engram_generator.generators import computer_graphics  # noqa: F401
from engram_generator.generators import telecom  # noqa: F401
from engram_generator.generators import robotics  # noqa: F401

# Advanced graph theory and mathematical physics
from engram_generator.generators import advanced_graph_theory  # noqa: F401
from engram_generator.generators import mathematical_physics  # noqa: F401

# Homological algebra, harmonic analysis, and mathematical logic extensions
from engram_generator.generators import homological_algebra  # noqa: F401
from engram_generator.generators import harmonic_analysis  # noqa: F401
from engram_generator.generators import mathematical_logic_ext  # noqa: F401

# Oceanography, geophysics, and continuum mechanics
from engram_generator.generators import oceanography  # noqa: F401
from engram_generator.generators import geophysics  # noqa: F401
from engram_generator.generators import continuum_mechanics  # noqa: F401

# Financial mathematics, formal verification, and music theory
from engram_generator.generators import financial_mathematics  # noqa: F401
from engram_generator.generators import formal_verification  # noqa: F401
from engram_generator.generators import music_theory  # noqa: F401

# Neuroscience, systems biology, and plasma physics
from engram_generator.generators import neuroscience  # noqa: F401
from engram_generator.generators import systems_biology  # noqa: F401
from engram_generator.generators import plasma_physics  # noqa: F401

# Convex optimization, quantum error correction, persistent homology
from engram_generator.generators import convex_optimization  # noqa: F401
from engram_generator.generators import quantum_error_correction  # noqa: F401
from engram_generator.generators import persistent_homology  # noqa: F401

# Extended domain modules
from engram_generator.generators import game_theory_ext  # noqa: F401
from engram_generator.generators import spatial_ext  # noqa: F401
from engram_generator.generators import automata_ext  # noqa: F401

# Extended topology, differential equations, and trigonometry
from engram_generator.generators import topology_ext  # noqa: F401
from engram_generator.generators import diffeq_ext  # noqa: F401
from engram_generator.generators import trigonometry_ext  # noqa: F401

# Actuarial science and medical imaging
from engram_generator.generators import actuarial  # noqa: F401
from engram_generator.generators import medical_imaging  # noqa: F401

# Extended upper-tier meta-reasoning (tiers 8-10)
from engram_generator.generators import meta_reasoning_t10_ext  # noqa: F401
from engram_generator.generators import meta_reasoning_t9_ext  # noqa: F401
from engram_generator.generators import meta_reasoning_t10_ext2  # noqa: F401

# Extended differential geometry and measure theory
from engram_generator.generators import diffgeo_ext  # noqa: F401
from engram_generator.generators import measure_ext  # noqa: F401

# Operations research, photonics, and semiconductor physics
from engram_generator.generators import operations_research  # noqa: F401
from engram_generator.generators import photonics  # noqa: F401
from engram_generator.generators import semiconductor  # noqa: F401

# Antenna theory, tribology, and polymer science
from engram_generator.generators import antenna_theory  # noqa: F401
from engram_generator.generators import tribology  # noqa: F401
from engram_generator.generators import polymer_science  # noqa: F401

# Extended queuing theory, Bayesian statistics, and causal inference
from engram_generator.generators import queuing_ext  # noqa: F401
from engram_generator.generators import bayesian_statistics  # noqa: F401
from engram_generator.generators import causal_inference  # noqa: F401

# Algebraic topology, coding theory, and wavelet theory
from engram_generator.generators import algebraic_topology  # noqa: F401
from engram_generator.generators import coding_theory  # noqa: F401
from engram_generator.generators import wavelet_theory  # noqa: F401

# Reinforcement learning extensions, environmental engineering, cryptanalysis
from engram_generator.generators import rl_ext  # noqa: F401
from engram_generator.generators import environmental_engineering  # noqa: F401
from engram_generator.generators import cryptanalysis  # noqa: F401

# Computer architecture, networking, and NLP computation
from engram_generator.generators import computer_architecture  # noqa: F401
from engram_generator.generators import networking  # noqa: F401
from engram_generator.generators import nlp_computation  # noqa: F401

# Time series, nonparametric stats, dimensionality reduction, communication systems
from engram_generator.generators import time_series  # noqa: F401
from engram_generator.generators import nonparametric_stats  # noqa: F401
from engram_generator.generators import dimensionality_reduction  # noqa: F401
from engram_generator.generators import communication_systems  # noqa: F401

# Numerical linear algebra, information geometry, fuzzy logic, compressed sensing
from engram_generator.generators import numerical_linalg  # noqa: F401
from engram_generator.generators import information_geometry  # noqa: F401
from engram_generator.generators import fuzzy_logic  # noqa: F401
from engram_generator.generators import compressed_sensing  # noqa: F401

# Digital electronics, structural engineering, and heat transfer
from engram_generator.generators import digital_electronics  # noqa: F401
from engram_generator.generators import structural_engineering  # noqa: F401
from engram_generator.generators import heat_transfer  # noqa: F401

# Extended domain deepening: linear algebra, algorithms, organic chemistry
from engram_generator.generators import linear_algebra_ext  # noqa: F401
from engram_generator.generators import algorithms_ext  # noqa: F401
from engram_generator.generators import organic_chemistry_ext  # noqa: F401

# Extended physics domains (classical mechanics, electromagnetism, quantum)
from engram_generator.generators import classical_mechanics_ext  # noqa: F401
from engram_generator.generators import electromagnetism_ext  # noqa: F401
from engram_generator.generators import quantum_ext  # noqa: F401

# Extended biology domains (ecology, genetics, biochemistry, cell biology)
from engram_generator.generators import ecology_ext  # noqa: F401
from engram_generator.generators import genetics_ext  # noqa: F401
from engram_generator.generators import biochemistry_ext  # noqa: F401
from engram_generator.generators import cell_biology_ext  # noqa: F401

# Extended data structures, graphs, sequences, and combinatorics
from engram_generator.generators import data_structures_ext  # noqa: F401
from engram_generator.generators import graphs_ext  # noqa: F401
from engram_generator.generators import sequences_ext  # noqa: F401
from engram_generator.generators import combinatorics_ext  # noqa: F401

# Extended domain deepening: geology, measurement, economics, linguistics
from engram_generator.generators import geology_ext  # noqa: F401
from engram_generator.generators import measurement_ext  # noqa: F401
from engram_generator.generators import economics_ext  # noqa: F401
from engram_generator.generators import linguistics_ext  # noqa: F401

# Deep probability, statistics, and number theory extensions
from engram_generator.generators import probability_ext  # noqa: F401
from engram_generator.generators import statistics_ext  # noqa: F401
from engram_generator.generators import number_theory_deep  # noqa: F401

# Extended abstract algebra, deep topology, and extended logic
from engram_generator.generators import abstract_algebra_ext  # noqa: F401
from engram_generator.generators import topology_deep  # noqa: F401
from engram_generator.generators import logic_ext  # noqa: F401

# Extended CS theory, cryptography, information theory, and networking
from engram_generator.generators import cs_theory_ext  # noqa: F401
from engram_generator.generators import crypto_ext  # noqa: F401
from engram_generator.generators import info_theory_ext  # noqa: F401
from engram_generator.generators import networking_ext  # noqa: F401

# Extended calculus, analysis, and PDE generators
from engram_generator.generators import calculus_ext  # noqa: F401
from engram_generator.generators import analysis_ext  # noqa: F401
from engram_generator.generators import pde_ext  # noqa: F401

# Extended chemistry domains (physical, inorganic, general)
from engram_generator.generators import physical_chemistry_ext  # noqa: F401
from engram_generator.generators import inorganic_chemistry_ext  # noqa: F401
from engram_generator.generators import general_chemistry_ext  # noqa: F401

# Extended physics deepening: thermodynamics, optics, nuclear, fluid
from engram_generator.generators import thermodynamics_ext  # noqa: F401
from engram_generator.generators import optics_ext  # noqa: F401
from engram_generator.generators import nuclear_ext  # noqa: F401
from engram_generator.generators import fluid_ext  # noqa: F401

# Deep ML, extended robotics, and extended signal processing
from engram_generator.generators import ml_deep  # noqa: F401
from engram_generator.generators import robotics_ext  # noqa: F401
from engram_generator.generators import signal_ext  # noqa: F401

# Deep domain extensions: recursion, spatial, automata, numerical, chemistry
from engram_generator.generators import recursion_ext  # noqa: F401
from engram_generator.generators import spatial_deep  # noqa: F401
from engram_generator.generators import automata_deep  # noqa: F401
from engram_generator.generators import numerical_ext2  # noqa: F401
from engram_generator.generators import chemistry_ext  # noqa: F401

# Extended domain deepening: solid state, quantum info, astronomy, materials
from engram_generator.generators import solid_state_ext  # noqa: F401
from engram_generator.generators import quantum_info_ext  # noqa: F401
from engram_generator.generators import astronomy_ext  # noqa: F401
from engram_generator.generators import materials_ext  # noqa: F401

# Extended geometry, relativity, control theory, and deep game theory
from engram_generator.generators import geometry_ext  # noqa: F401
from engram_generator.generators import relativity_ext  # noqa: F401
from engram_generator.generators import control_ext  # noqa: F401
from engram_generator.generators import game_theory_deep  # noqa: F401

# Deep algebra, algorithms, and biology
from engram_generator.generators import algebra_deep  # noqa: F401
from engram_generator.generators import algorithms_deep  # noqa: F401
from engram_generator.generators import biology_deep  # noqa: F401

# Deep math/stats extensions: calculus, statistics, probability
from engram_generator.generators import calculus_deep  # noqa: F401
from engram_generator.generators import statistics_deep  # noqa: F401
from engram_generator.generators import probability_deep  # noqa: F401

# Deep physics domain extensions: EM, optics, thermodynamics, fluids
from engram_generator.generators import em_deep  # noqa: F401
from engram_generator.generators import optics_deep  # noqa: F401
from engram_generator.generators import thermo_deep  # noqa: F401
from engram_generator.generators import fluid_deep  # noqa: F401

# Deep domain extensions: number theory, combinatorics, logic
from engram_generator.generators import number_theory_deep2  # noqa: F401
from engram_generator.generators import combinatorics_deep  # noqa: F401
from engram_generator.generators import logic_deep  # noqa: F401

# Deep CS domain extensions: OS, distributed, compilers, networks
from engram_generator.generators import os_deep  # noqa: F401
from engram_generator.generators import distributed_deep  # noqa: F401
from engram_generator.generators import compilers_deep  # noqa: F401
from engram_generator.generators import networks_deep  # noqa: F401

# Deep domain generators: quantum, engineering, economics
from engram_generator.generators import quantum_deep  # noqa: F401
from engram_generator.generators import engineering_deep  # noqa: F401
from engram_generator.generators import economics_deep  # noqa: F401

# Deep chemistry, spectroscopy, and pharmacology
from engram_generator.generators import chemistry_deep  # noqa: F401
from engram_generator.generators import spectroscopy_deep  # noqa: F401
from engram_generator.generators import pharmacology_deep  # noqa: F401

# Deep ML optimisation, deep cryptography, deep information theory
from engram_generator.generators import ml_deep2  # noqa: F401
from engram_generator.generators import crypto_deep  # noqa: F401
from engram_generator.generators import info_theory_deep  # noqa: F401

# Deep topology, PDE, functional analysis, and category theory extensions
from engram_generator.generators import topology_deep2  # noqa: F401
from engram_generator.generators import pde_deep  # noqa: F401
from engram_generator.generators import functional_analysis_ext  # noqa: F401
from engram_generator.generators import category_ext  # noqa: F401

# Scenario pool expansions (must load AFTER generators)
from engram_generator.generators import scenario_expansions  # noqa: F401
