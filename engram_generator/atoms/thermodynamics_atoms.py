"""Knowledge atoms for thermodynamics generators.

Registers formula and law atoms covering the laws of thermodynamics,
heat engines, entropy, free energy, and phase transitions. Each atom
includes a worked example with known input and solution for
verification.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ---------------------------------------------------------------------------
# Tier 4
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="first_law_thermo",
    content=(
        "The first law of thermodynamics is a formulation of the law of "
        "conservation of energy in the context of thermodynamic processes. "
        "It states that the internal energy of an isolated system is "
        "constant. For a closed system undergoing a process, the change "
        "in internal energy equals the heat added to the system minus the "
        "work done by the system: dU = Q - W, where dU is the change in "
        "internal energy, Q is the heat added to the system, and W is the "
        "work done by the system on its surroundings."
    ),
    example=(
        "Given Q = 500 J (heat added) and W = 200 J (work done by system): "
        "dU = Q - W = 500 - 200 = 300 J. "
        "The internal energy increases by 300 J."
    ),
    tier=4,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'First law of thermodynamics', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/First_law_of_thermodynamics",
    prerequisites=["addition", "subtraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_capacity",
    content=(
        "Heat capacity (C) is the amount of heat required to change the "
        "temperature of a body by one degree. The specific heat capacity "
        "(c) is the heat capacity per unit mass. The relationship between "
        "heat transferred, mass, specific heat, and temperature change is: "
        "Q = m * c * dT, where Q is the heat transferred (in joules), "
        "m is the mass (in kg), c is the specific heat capacity "
        "(in J/(kg*K)), and dT is the change in temperature (in K or C). "
        "For water, c = 4186 J/(kg*K)."
    ),
    example=(
        "Given m = 2 kg of water (c = 4186 J/(kg*K)), heated from "
        "20 C to 80 C: dT = 60 K. "
        "Q = m * c * dT = 2 * 4186 * 60 = 502320 J = 502.32 kJ."
    ),
    tier=4,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Heat capacity', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Heat_capacity",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="carnot_efficiency",
    content=(
        "The Carnot efficiency is the maximum possible efficiency of a "
        "heat engine operating between two thermal reservoirs. It is "
        "determined solely by the temperatures of the hot and cold "
        "reservoirs: eta = 1 - T_cold / T_hot, where eta is the "
        "efficiency (dimensionless, between 0 and 1), T_cold is the "
        "absolute temperature of the cold reservoir (in kelvin), and "
        "T_hot is the absolute temperature of the hot reservoir (in "
        "kelvin). No real engine can exceed the Carnot efficiency. "
        "This result was derived by Sadi Carnot in 1824."
    ),
    example=(
        "Given T_hot = 600 K and T_cold = 300 K: "
        "eta = 1 - T_cold / T_hot = 1 - 300 / 600 = 1 - 0.5 = 0.5. "
        "Maximum efficiency is 50%."
    ),
    tier=4,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Carnot's theorem (thermodynamics)', "
        "Wikipedia, The Free Encyclopedia."
    ),
    source_url=(
        "https://en.wikipedia.org/wiki/"
        "Carnot%27s_theorem_(thermodynamics)"
    ),
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Tier 5
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="work_pv",
    content=(
        "In thermodynamics, pressure-volume work (or PV work) is the work "
        "done by or on a system when it expands or contracts against an "
        "external pressure. For an isobaric (constant pressure) process: "
        "W = P * dV, where W is the work (in joules), P is the constant "
        "pressure (in pascals), and dV is the change in volume (in cubic "
        "metres). For a general quasi-static process, the work is the "
        "integral W = integral(P dV) from V_initial to V_final. Work is "
        "positive when the system expands (dV > 0) and negative when it "
        "is compressed."
    ),
    example=(
        "Given P = 101325 Pa (1 atm) and expansion from "
        "V1 = 0.01 m^3 to V2 = 0.03 m^3: "
        "dV = 0.02 m^3. "
        "W = P * dV = 101325 * 0.02 = 2026.5 J."
    ),
    tier=5,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Work (thermodynamics)', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Work_(thermodynamics)",
    prerequisites=["multiplication", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="entropy_change",
    content=(
        "In thermodynamics, entropy is a measure of the number of "
        "microscopic configurations that correspond to a thermodynamic "
        "system's macroscopic state. For a reversible process at constant "
        "temperature: dS = Q_rev / T, where dS is the change in entropy "
        "(in J/K), Q_rev is the heat transferred reversibly (in joules), "
        "and T is the absolute temperature (in kelvin). For an "
        "irreversible process, dS > Q / T. The total entropy of an "
        "isolated system can only increase or remain constant (second "
        "law of thermodynamics)."
    ),
    example=(
        "Given Q_rev = 1000 J absorbed reversibly at T = 400 K: "
        "dS = Q_rev / T = 1000 / 400 = 2.5 J/K. "
        "Entropy increases by 2.5 J/K."
    ),
    tier=5,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Entropy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Entropy",
    prerequisites=["division", "first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula",
    name="free_energy",
    content=(
        "The Gibbs free energy (G) is a thermodynamic potential that "
        "measures the maximum amount of non-expansion work obtainable "
        "from a closed system at constant temperature and pressure. It "
        "is defined as: G = H - T * S, where H is the enthalpy, T is "
        "the absolute temperature, and S is the entropy. The change in "
        "Gibbs free energy for a process is: dG = dH - T * dS. A process "
        "is spontaneous at constant T and P when dG < 0. At equilibrium, "
        "dG = 0."
    ),
    example=(
        "Given dH = -100 kJ/mol (exothermic) and dS = 0.2 kJ/(mol*K) "
        "at T = 298 K: "
        "dG = dH - T * dS = -100 - 298 * 0.2 = -100 - 59.6 = -159.6 kJ/mol. "
        "Since dG < 0, the reaction is spontaneous."
    ),
    tier=5,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Gibbs free energy', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Gibbs_free_energy",
    prerequisites=["multiplication", "entropy_change"],
))

register_atom(Atom(
    atom_type="formula",
    name="adiabatic_process",
    content=(
        "An adiabatic process is a thermodynamic process in which no "
        "heat is transferred to or from the working fluid. For a "
        "reversible adiabatic (isentropic) process of an ideal gas: "
        "P * V^gamma = constant, and T * V^(gamma-1) = constant, where "
        "P is pressure, V is volume, T is absolute temperature, and "
        "gamma (the heat capacity ratio) = C_p / C_v. For a monatomic "
        "ideal gas, gamma = 5/3; for a diatomic ideal gas, gamma = 7/5. "
        "The work done in an adiabatic process is: "
        "W = (P1*V1 - P2*V2) / (gamma - 1)."
    ),
    example=(
        "Given a diatomic ideal gas (gamma = 1.4) compressed from "
        "V1 = 0.01 m^3 at P1 = 100000 Pa to V2 = 0.005 m^3: "
        "P2 = P1 * (V1/V2)^gamma = 100000 * 2^1.4 = 100000 * 2.6390 "
        "= 263900 Pa. "
        "W = (P1*V1 - P2*V2) / (gamma - 1) = "
        "(100000*0.01 - 263900*0.005) / 0.4 = (1000 - 1319.5) / 0.4 "
        "= -798.75 J (negative: work done ON gas)."
    ),
    tier=5,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Adiabatic process', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Adiabatic_process",
    prerequisites=["exponentiation", "first_law_thermo"],
))

# ---------------------------------------------------------------------------
# Tier 6
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="law",
    name="clausius_inequality",
    content=(
        "The Clausius inequality is a consequence of the second law of "
        "thermodynamics. It states that for any thermodynamic cycle, "
        "the cyclic integral of dQ/T is less than or equal to zero: "
        "oint(dQ / T) <= 0, where dQ is the infinitesimal heat transfer "
        "and T is the absolute temperature at the boundary where the "
        "heat transfer occurs. Equality holds for a reversible cycle. "
        "For an irreversible cycle, the integral is strictly negative. "
        "This inequality establishes that entropy is a state function "
        "and that the entropy of an isolated system never decreases."
    ),
    example=(
        "Given a cycle absorbing Q_hot = 800 J at T_hot = 400 K and "
        "rejecting Q_cold = 500 J at T_cold = 200 K: "
        "sum(Q/T) = 800/400 + (-500)/200 = 2.0 - 2.5 = -0.5 < 0. "
        "The Clausius inequality is satisfied (irreversible cycle)."
    ),
    tier=6,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Clausius theorem', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Clausius_theorem",
    prerequisites=["entropy_change", "definite_integral"],
))

register_atom(Atom(
    atom_type="formula",
    name="phase_transition",
    content=(
        "A phase transition is the transformation of a thermodynamic "
        "system from one phase of matter to another. During a first-order "
        "phase transition (such as melting, boiling, or sublimation), the "
        "system absorbs or releases a fixed amount of energy per unit "
        "mass called the latent heat (L). The heat required is: "
        "Q = m * L, where Q is the heat (in joules), m is the mass "
        "(in kg), and L is the specific latent heat (in J/kg). For water: "
        "L_fusion = 334000 J/kg, L_vaporisation = 2260000 J/kg. "
        "The Clausius-Clapeyron equation relates the slope of the phase "
        "boundary to the latent heat: dP/dT = L / (T * dV)."
    ),
    example=(
        "Given m = 0.5 kg of ice at 0 C melting to water "
        "(L_fusion = 334000 J/kg): "
        "Q = m * L = 0.5 * 334000 = 167000 J = 167 kJ."
    ),
    tier=6,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Phase transition', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Phase_transition",
    prerequisites=["multiplication", "heat_capacity"],
))

register_atom(Atom(
    atom_type="formula",
    name="heat_engine_cycle",
    content=(
        "A heat engine is a thermodynamic system that converts heat into "
        "mechanical work by exploiting the temperature difference between "
        "a hot source and a cold sink. The thermal efficiency of any heat "
        "engine is: eta = W / Q_hot = (Q_hot - Q_cold) / Q_hot = "
        "1 - Q_cold / Q_hot, where W is the net work output, Q_hot is "
        "the heat absorbed from the hot reservoir, and Q_cold is the heat "
        "rejected to the cold reservoir. Common idealised cycles include "
        "the Carnot cycle (maximum efficiency), the Otto cycle (petrol "
        "engines), and the Diesel cycle."
    ),
    example=(
        "Given Q_hot = 1000 J and Q_cold = 400 J: "
        "W = Q_hot - Q_cold = 1000 - 400 = 600 J. "
        "eta = W / Q_hot = 600 / 1000 = 0.6 (60% efficiency)."
    ),
    tier=6,
    domain="thermodynamics",
    source=(
        "Wikipedia contributors, 'Heat engine', Wikipedia, "
        "The Free Encyclopedia."
    ),
    source_url="https://en.wikipedia.org/wiki/Heat_engine",
    prerequisites=["carnot_efficiency", "first_law_thermo"],
))
