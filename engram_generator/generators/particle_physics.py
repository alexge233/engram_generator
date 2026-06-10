"""Particle physics generators -- conservation laws through symmetry groups.

Covers conservation law checks, quark content, Feynman vertex validation,
toy cross-sections, partial decay widths, invariant mass from 4-momenta,
centre-of-mass energy, and symmetry group identification.  All tiers are
5-7 (intermediate to advanced).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# Helper utilities
# ---------------------------------------------------------------------------

def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ---------------------------------------------------------------------------
# Particle data tables
# ---------------------------------------------------------------------------

# (name, charge, baryon_number, lepton_number)
_PARTICLES = {
    "e-":     (-1,  0,  1),
    "e+":     ( 1,  0, -1),
    "nu_e":   ( 0,  0,  1),
    "nu_e~":  ( 0,  0, -1),
    "mu-":    (-1,  0,  1),
    "mu+":    ( 1,  0, -1),
    "nu_mu":  ( 0,  0,  1),
    "nu_mu~": ( 0,  0, -1),
    "p":      ( 1,  1,  0),
    "p~":     (-1, -1,  0),
    "n":      ( 0,  1,  0),
    "n~":     ( 0, -1,  0),
    "pi+":    ( 1,  0,  0),
    "pi-":    (-1,  0,  0),
    "pi0":    ( 0,  0,  0),
    "gamma":  ( 0,  0,  0),
    "K+":     ( 1,  0,  0),
    "K-":     (-1,  0,  0),
}

# Known hadrons: (name, quark_content, charge)
_HADRONS = [
    ("proton",  "uud",      1),
    ("neutron", "udd",      0),
    ("pi+",     "u d_bar",  1),
    ("pi-",     "d u_bar", -1),
    ("pi0",     "u u_bar",  0),
    ("K+",      "u s_bar",  1),
    ("K-",      "s u_bar", -1),
    ("Lambda",  "uds",      0),
    ("Sigma+",  "uus",      1),
    ("Sigma-",  "dds",     -1),
    ("Xi0",     "uss",      0),
    ("Xi-",     "dss",     -1),
    ("Omega-",  "sss",     -1),
]

# Quark charges
_QUARK_CHARGE = {
    "u":  2 / 3,
    "d": -1 / 3,
    "s": -1 / 3,
    "c":  2 / 3,
    "b": -1 / 3,
    "t":  2 / 3,
    "u_bar": -2 / 3,
    "d_bar":  1 / 3,
    "s_bar":  1 / 3,
    "c_bar": -2 / 3,
    "b_bar":  1 / 3,
    "t_bar": -2 / 3,
}


# ---------------------------------------------------------------------------
# Predefined reactions for conservation law checks
# ---------------------------------------------------------------------------

_REACTIONS = [
    # (reactants, products, allowed)
    (["p", "p~"], ["pi+", "pi-", "pi0"], True),
    (["n"], ["p", "e-", "nu_e~"], True),
    (["p", "pi-"], ["n", "pi0"], True),
    (["mu-"], ["e-", "nu_mu", "nu_e~"], True),
    (["p", "p"], ["p", "p", "pi0"], True),
    (["p", "e-"], ["n", "nu_e"], True),
    # Forbidden reactions
    (["p"], ["e+", "pi0"], False),
    (["n"], ["p", "e-"], False),
    (["p", "p"], ["p", "pi+"], False),
    (["mu-"], ["e-", "gamma"], False),
]


# ===================================================================
# 1. Conservation laws  (tier 5)
# ===================================================================

@register
class ConservationLawsGenerator(StepGenerator):
    """Check conservation of charge, baryon number, lepton number.

    Given a particle reaction, verify whether charge, baryon number,
    and lepton number are each conserved.

    Difficulty scaling:
        Difficulty 1-3: 2-body reactions, simple particles.
        Difficulty 4-6: 3-body final states.
        Difficulty 7-8: 4+ body, includes forbidden reactions.

    Prerequisites:
        addition.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "conservation_laws"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check conservation laws in particle reaction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a particle reaction and check conservation laws.

        Args:
            difficulty: Controls reaction complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = _REACTIONS[:4]
        elif difficulty <= 6:
            pool = _REACTIONS[:7]
        else:
            pool = _REACTIONS

        reactants, products, allowed = self._rng.choice(pool)

        q_in = sum(_PARTICLES[p][0] for p in reactants)
        q_out = sum(_PARTICLES[p][0] for p in products)
        b_in = sum(_PARTICLES[p][1] for p in reactants)
        b_out = sum(_PARTICLES[p][1] for p in products)
        l_in = sum(_PARTICLES[p][2] for p in reactants)
        l_out = sum(_PARTICLES[p][2] for p in products)

        react_str = " + ".join(reactants)
        prod_str = " + ".join(products)

        return f"{react_str} \\to {prod_str}", {
            "reactants": reactants, "products": products,
            "Q_in": q_in, "Q_out": q_out,
            "B_in": b_in, "B_out": b_out,
            "L_in": l_in, "L_out": l_out,
            "Q_conserved": q_in == q_out,
            "B_conserved": b_in == b_out,
            "L_conserved": l_in == l_out,
            "allowed": allowed,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate conservation law verification steps.

        Args:
            data: Solution data with quantum numbers.

        Returns:
            List of step strings.
        """
        return [
            f"Q: {data['Q_in']} -> {data['Q_out']}"
            f" ({'conserved' if data['Q_conserved'] else 'violated'})",
            f"B: {data['B_in']} -> {data['B_out']}"
            f" ({'conserved' if data['B_conserved'] else 'violated'})",
            f"L: {data['L_in']} -> {data['L_out']}"
            f" ({'conserved' if data['L_conserved'] else 'violated'})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether the reaction is allowed.

        Args:
            data: Solution data.

        Returns:
            String indicating allowed or forbidden.
        """
        return "allowed" if data["allowed"] else "forbidden"


# ===================================================================
# 2. Quark content  (tier 5)
# ===================================================================

@register
class QuarkContentGenerator(StepGenerator):
    """Determine quark composition and verify charge from quarks.

    Given a hadron name, identify its quark content and compute the
    total charge by summing quark charges.

    Difficulty scaling:
        Difficulty 1-3: proton, neutron, pions.
        Difficulty 4-6: kaons and Lambda.
        Difficulty 7-8: Sigma, Xi, Omega baryons.

    Prerequisites:
        conservation_laws.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "quark_content"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conservation_laws"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine quark content and verify charge"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hadron quark content problem.

        Args:
            difficulty: Controls hadron complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = _HADRONS[:5]
        elif difficulty <= 6:
            pool = _HADRONS[:8]
        else:
            pool = _HADRONS

        name, quarks_str, expected_charge = self._rng.choice(pool)
        quark_list = quarks_str.split()

        charge_sum = round(sum(_QUARK_CHARGE[q] for q in quark_list), 4)

        return f"\\text{{{name}}} = {quarks_str}", {
            "name": name, "quarks": quark_list,
            "quarks_str": quarks_str,
            "charge_per_quark": [round(_QUARK_CHARGE[q], 4) for q in quark_list],
            "total_charge": charge_sum,
            "expected_charge": expected_charge,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate quark content verification steps.

        Args:
            data: Solution data with quarks and charges.

        Returns:
            List of step strings.
        """
        charge_parts = " + ".join(
            f"{q}({_fmt(c)})" for q, c in zip(data["quarks"], data["charge_per_quark"])
        )
        return [
            f"{data['name']} = {data['quarks_str']}",
            f"charges: {charge_parts}",
            f"total = {_fmt(data['total_charge'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the quark content and total charge.

        Args:
            data: Solution data.

        Returns:
            String with quarks and charge.
        """
        return (
            f"{data['name']} = {data['quarks_str']}, "
            f"Q = {_fmt(data['total_charge'])}"
        )


# ===================================================================
# 3. Feynman vertex  (tier 6)
# ===================================================================

@register
class FeynmanVertexGenerator(StepGenerator):
    """Identify if a Feynman vertex is allowed by SM rules.

    Check charge conservation, lepton number, and baryon number
    at a single interaction vertex.

    Difficulty scaling:
        Difficulty 1-3: QED vertices (e-/e+/gamma).
        Difficulty 4-6: weak vertices with neutrinos.
        Difficulty 7-8: mixed vertices including forbidden ones.

    Prerequisites:
        conservation_laws.
    """

    _VERTICES = [
        # (particles_in, particles_out, vertex_type, allowed)
        (["e-"], ["e-", "gamma"], "QED", True),
        (["e-", "e+"], ["gamma"], "QED", True),
        (["mu-"], ["mu-", "gamma"], "QED", True),
        (["e-", "nu_e~"], ["pi-"], "weak", True),
        (["n"], ["p", "e-", "nu_e~"], "weak", True),
        (["mu-"], ["e-", "nu_mu", "nu_e~"], "weak", True),
        # Forbidden vertices
        (["e-"], ["mu-", "gamma"], "forbidden", False),
        (["e-", "e+"], ["p", "p~"], "forbidden_at_vertex", False),
        (["p"], ["n", "e+"], "forbidden", False),
        (["e-"], ["e-", "e-"], "forbidden", False),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "feynman_vertex"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["conservation_laws"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "check if Feynman vertex is allowed by SM rules"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vertex and check conservation laws.

        Args:
            difficulty: Controls vertex complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = self._VERTICES[:3]
        elif difficulty <= 6:
            pool = self._VERTICES[:6]
        else:
            pool = self._VERTICES

        p_in, p_out, vtype, allowed = self._rng.choice(pool)

        q_in = sum(_PARTICLES[p][0] for p in p_in)
        q_out = sum(_PARTICLES[p][0] for p in p_out)
        b_in = sum(_PARTICLES[p][1] for p in p_in)
        b_out = sum(_PARTICLES[p][1] for p in p_out)
        l_in = sum(_PARTICLES[p][2] for p in p_in)
        l_out = sum(_PARTICLES[p][2] for p in p_out)

        in_str = " + ".join(p_in)
        out_str = " + ".join(p_out)

        return f"{in_str} \\to {out_str}", {
            "in": p_in, "out": p_out,
            "vertex_type": vtype, "allowed": allowed,
            "Q_in": q_in, "Q_out": q_out,
            "B_in": b_in, "B_out": b_out,
            "L_in": l_in, "L_out": l_out,
            "Q_ok": q_in == q_out,
            "B_ok": b_in == b_out,
            "L_ok": l_in == l_out,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate vertex validation steps.

        Args:
            data: Solution data with quantum numbers.

        Returns:
            List of step strings.
        """
        return [
            f"Q: {data['Q_in']} -> {data['Q_out']}"
            f" ({'ok' if data['Q_ok'] else 'violated'})",
            f"B: {data['B_in']} -> {data['B_out']}"
            f" ({'ok' if data['B_ok'] else 'violated'})",
            f"L: {data['L_in']} -> {data['L_out']}"
            f" ({'ok' if data['L_ok'] else 'violated'})",
            f"type: {data['vertex_type']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether the vertex is allowed.

        Args:
            data: Solution data.

        Returns:
            String indicating allowed or forbidden with vertex type.
        """
        status = "allowed" if data["allowed"] else "forbidden"
        return f"{status} ({data['vertex_type']})"


# ===================================================================
# 4. Cross section  (tier 7)
# ===================================================================

@register
class CrossSectionGenerator(StepGenerator):
    """Compute toy cross-section for isotropic scattering.

    For isotropic |M|^2, sigma = 4*pi*|M|^2.  The matrix element
    squared is sampled randomly.

    Difficulty scaling:
        Difficulty 1-3: integer |M|^2 values.
        Difficulty 4-6: decimal |M|^2, compute in natural units.
        Difficulty 7-8: add flux factor F, sigma = 4*pi*|M|^2 / F.

    Prerequisites:
        definite_integral.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cross_section"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["definite_integral"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute scattering cross-section"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate cross-section computation.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m_sq = float(self._rng.randint(1, 10))
        else:
            m_sq = round(self._rng.uniform(0.1, 10.0), 4)

        sigma_base = round(4.0 * math.pi * m_sq, 4)

        if difficulty >= 7:
            flux = round(self._rng.uniform(1.0, 10.0), 4)
            sigma = round(sigma_base / flux, 4)
            return "\\sigma = \\frac{4\\pi |M|^2}{F}", {
                "M_sq": m_sq, "sigma_base": sigma_base,
                "flux": flux, "sigma": sigma,
                "has_flux": True,
            }

        return "\\sigma = 4\\pi |M|^2", {
            "M_sq": m_sq, "sigma_base": sigma_base,
            "sigma": sigma_base, "has_flux": False,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate cross-section computation steps.

        Args:
            data: Solution data with |M|^2 and sigma.

        Returns:
            List of step strings.
        """
        steps = [
            f"|M|^2 = {_fmt(data['M_sq'])}",
            f"4*pi*|M|^2 = 4*{_fmt(round(math.pi, 4))}*{_fmt(data['M_sq'])}"
            f" = {_fmt(data['sigma_base'])}",
        ]
        if data["has_flux"]:
            steps.append(
                f"sigma = {_fmt(data['sigma_base'])}/{_fmt(data['flux'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the cross-section.

        Args:
            data: Solution data.

        Returns:
            String with sigma value.
        """
        return f"sigma = {_fmt(data['sigma'])}"


# ===================================================================
# 5. Decay width  (tier 6)
# ===================================================================

@register
class DecayWidthGenerator(StepGenerator):
    """Compute partial and total decay widths.

    Gamma_i = g^2 * p_f / (8*pi*m^2).  Total width is sum of partials.
    Branching ratio BR_i = Gamma_i / Gamma_total.

    Difficulty scaling:
        Difficulty 1-3: single channel decay.
        Difficulty 4-6: two channels, compute total and BR.
        Difficulty 7-8: three channels, compute lifetime tau = 1/Gamma.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "decay_width"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute decay width and branching ratio"

    def _sample_channel(self) -> dict:
        """Sample parameters for a single decay channel.

        Returns:
            Dict with coupling g, final momentum p_f.
        """
        g = round(self._rng.uniform(0.1, 2.0), 4)
        p_f = round(self._rng.uniform(0.5, 5.0), 4)
        return {"g": g, "p_f": p_f}

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate decay width problem.

        Args:
            difficulty: Controls number of channels.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        m = round(self._rng.uniform(1.0, 10.0), 4)

        if difficulty <= 3:
            n_channels = 1
        elif difficulty <= 6:
            n_channels = 2
        else:
            n_channels = 3

        channels = [self._sample_channel() for _ in range(n_channels)]
        widths = []
        for ch in channels:
            gamma_i = round(
                ch["g"] ** 2 * ch["p_f"] / (8.0 * math.pi * m ** 2), 4
            )
            widths.append(gamma_i)

        gamma_total = round(sum(widths), 4)
        branching = [round(w / gamma_total, 4) for w in widths]
        lifetime = round(1.0 / gamma_total, 4) if gamma_total > 0 else 0.0

        return "\\Gamma_i = \\frac{g^2 p_f}{8\\pi m^2}", {
            "m": m, "channels": channels, "widths": widths,
            "gamma_total": gamma_total, "branching": branching,
            "lifetime": lifetime, "n_channels": n_channels,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate decay width computation steps.

        Args:
            data: Solution data with channels and widths.

        Returns:
            List of step strings.
        """
        steps = [f"m = {_fmt(data['m'])}"]
        for i, (ch, w) in enumerate(zip(data["channels"], data["widths"])):
            steps.append(
                f"Gamma_{i + 1} = {_fmt(ch['g'])}^2*{_fmt(ch['p_f'])}"
                f"/(8*pi*{_fmt(data['m'])}^2) = {_fmt(w)}"
            )
        steps.append(f"Gamma_total = {_fmt(data['gamma_total'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return total width and branching ratios.

        Args:
            data: Solution data.

        Returns:
            String with Gamma_total and BR values.
        """
        br_str = ", ".join(f"BR_{i + 1}={_fmt(b)}" for i, b in enumerate(data["branching"]))
        return f"Gamma = {_fmt(data['gamma_total'])}, {br_str}"


# ===================================================================
# 6. Invariant mass  (tier 6)
# ===================================================================

@register
class InvariantMassGenerator(StepGenerator):
    """Compute invariant mass from 4-momenta of decay products.

    M^2 = (E1+E2)^2 - (p1+p2)^2 for two-body decay products.
    Momenta are along x-axis for simplicity.

    Difficulty scaling:
        Difficulty 1-3: collinear momenta (same direction).
        Difficulty 4-6: opposite momenta (back-to-back).
        Difficulty 7-8: three-body invariant mass.

    Prerequisites:
        four_momentum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "invariant_mass"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["four_momentum"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute invariant mass from decay products"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate 4-momenta and compute invariant mass.

        Args:
            difficulty: Controls number of particles.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 6:
            n_particles = 2
        else:
            n_particles = 3

        energies = []
        momenta = []
        for i in range(n_particles):
            e = round(self._rng.uniform(1.0, 20.0), 4)
            if difficulty <= 3:
                p = round(self._rng.uniform(0.5, e - 0.1), 4)
            elif difficulty <= 6 and i == 1:
                p = -round(self._rng.uniform(0.5, e - 0.1), 4)
            else:
                sign = self._rng.choice([-1, 1])
                p = sign * round(self._rng.uniform(0.5, e - 0.1), 4)
            energies.append(e)
            momenta.append(p)

        e_total = round(sum(energies), 4)
        p_total = round(sum(momenta), 4)
        m_sq = round(e_total ** 2 - p_total ** 2, 4)
        m_inv = round(math.sqrt(max(m_sq, 0.0)), 4)

        return "M^2 = (\\sum E_i)^2 - (\\sum p_i)^2", {
            "energies": energies, "momenta": momenta,
            "E_total": e_total, "p_total": p_total,
            "M_sq": m_sq, "M_inv": m_inv,
            "n_particles": n_particles,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate invariant mass computation steps.

        Args:
            data: Solution data with energies and momenta.

        Returns:
            List of step strings.
        """
        e_parts = " + ".join(_fmt(e) for e in data["energies"])
        p_parts = " + ".join(
            f"({_fmt(p)})" if p < 0 else _fmt(p) for p in data["momenta"]
        )
        return [
            f"E_total = {e_parts} = {_fmt(data['E_total'])} GeV",
            f"p_total = {p_parts} = {_fmt(data['p_total'])} GeV/c",
            f"M^2 = {_fmt(data['E_total'])}^2 - {_fmt(data['p_total'])}^2"
            f" = {_fmt(data['M_sq'])}",
            f"M = sqrt({_fmt(data['M_sq'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the invariant mass.

        Args:
            data: Solution data.

        Returns:
            String with invariant mass.
        """
        return f"M = {_fmt(data['M_inv'])} GeV/c^2"


# ===================================================================
# 7. Centre-of-mass energy  (tier 5)
# ===================================================================

@register
class CMSEnergyGenerator(StepGenerator):
    """Compute centre-of-mass energy sqrt(s).

    Collider: sqrt(s) = sqrt((E1+E2)^2 - (p1+p2)^2).
    Fixed-target: sqrt(s) = sqrt(2*m*E_beam + 2*m^2).
    Uses GeV natural units.

    Difficulty scaling:
        Difficulty 1-3: equal energy collider (p1 = -p2).
        Difficulty 4-6: asymmetric collider.
        Difficulty 7-8: fixed-target experiment.

    Prerequisites:
        relativistic_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cms_energy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["relativistic_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute centre-of-mass energy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate CMS energy calculation.

        Args:
            difficulty: Controls experiment type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Equal energy collider
            e = round(self._rng.uniform(5.0, 100.0), 4)
            m = round(self._rng.uniform(0.1, 1.0), 4)
            p = round(math.sqrt(max(e ** 2 - m ** 2, 0.0)), 4)
            e_total = round(2 * e, 4)
            p_total = 0.0
            s = round(e_total ** 2, 4)
            sqrt_s = round(math.sqrt(s), 4)
            mode = "symmetric_collider"
            return "\\sqrt{s} = 2E", {
                "E1": e, "E2": e, "p1": p, "p2": -p,
                "E_total": e_total, "p_total": p_total,
                "s": s, "sqrt_s": sqrt_s, "m": m, "mode": mode,
            }

        if difficulty <= 6:
            # Asymmetric collider
            e1 = round(self._rng.uniform(5.0, 50.0), 4)
            e2 = round(self._rng.uniform(5.0, 50.0), 4)
            m = round(self._rng.uniform(0.1, 1.0), 4)
            p1 = round(math.sqrt(max(e1 ** 2 - m ** 2, 0.0)), 4)
            p2 = -round(math.sqrt(max(e2 ** 2 - m ** 2, 0.0)), 4)
            e_total = round(e1 + e2, 4)
            p_total = round(p1 + p2, 4)
            s = round(e_total ** 2 - p_total ** 2, 4)
            sqrt_s = round(math.sqrt(max(s, 0.0)), 4)
            mode = "asymmetric_collider"
            return "\\sqrt{s} = \\sqrt{(E_1+E_2)^2 - (p_1+p_2)^2}", {
                "E1": e1, "E2": e2, "p1": p1, "p2": p2,
                "E_total": e_total, "p_total": p_total,
                "s": s, "sqrt_s": sqrt_s, "m": m, "mode": mode,
            }

        # Fixed-target
        m = round(self._rng.uniform(0.1, 1.0), 4)
        e_beam = round(self._rng.uniform(10.0, 500.0), 4)
        s = round(2.0 * m * e_beam + 2.0 * m ** 2, 4)
        sqrt_s = round(math.sqrt(max(s, 0.0)), 4)
        mode = "fixed_target"
        return "\\sqrt{s} = \\sqrt{2 m E_{beam} + 2 m^2}", {
            "m": m, "E_beam": e_beam,
            "s": s, "sqrt_s": sqrt_s, "mode": mode,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CMS energy computation steps.

        Args:
            data: Solution data with energies and momenta.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "symmetric_collider":
            return [
                f"E1 = E2 = {_fmt(data['E1'])} GeV",
                f"E_total = 2*{_fmt(data['E1'])} = {_fmt(data['E_total'])} GeV",
                f"p_total = 0 (head-on)",
                f"sqrt(s) = {_fmt(data['E_total'])}",
            ]
        if mode == "asymmetric_collider":
            return [
                f"E1={_fmt(data['E1'])}, E2={_fmt(data['E2'])} GeV",
                f"p1={_fmt(data['p1'])}, p2={_fmt(data['p2'])} GeV/c",
                f"s = {_fmt(data['E_total'])}^2 - {_fmt(data['p_total'])}^2"
                f" = {_fmt(data['s'])}",
                f"sqrt(s) = sqrt({_fmt(data['s'])})",
            ]
        # fixed_target
        return [
            f"m = {_fmt(data['m'])} GeV, E_beam = {_fmt(data['E_beam'])} GeV",
            f"s = 2*{_fmt(data['m'])}*{_fmt(data['E_beam'])}"
            f" + 2*{_fmt(data['m'])}^2 = {_fmt(data['s'])}",
            f"sqrt(s) = sqrt({_fmt(data['s'])})",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the centre-of-mass energy.

        Args:
            data: Solution data.

        Returns:
            String with sqrt(s) value.
        """
        return f"sqrt(s) = {_fmt(data['sqrt_s'])} GeV"


# ===================================================================
# 8. Symmetry group  (tier 7)
# ===================================================================

@register
class SymmetryGroupGenerator(StepGenerator):
    """Identify the symmetry group of a fundamental interaction.

    Match interaction to its gauge group and force carrier:
    EM -> U(1), photon; weak -> SU(2), W/Z; strong -> SU(3), gluon.

    Difficulty scaling:
        Difficulty 1-3: identify group from force name.
        Difficulty 4-6: identify group and carrier from process.
        Difficulty 7-8: give generators count and coupling constant name.

    Prerequisites:
        group_table.
    """

    _INTERACTIONS = [
        {
            "force": "electromagnetic", "group": "U(1)",
            "carrier": "photon", "generators": 1,
            "coupling": "alpha_em",
            "processes": ["e- scattering", "Compton scattering",
                          "pair annihilation"],
        },
        {
            "force": "weak", "group": "SU(2)_L",
            "carrier": "W+/W-/Z0", "generators": 3,
            "coupling": "g_w",
            "processes": ["beta decay", "muon decay",
                          "neutrino scattering"],
        },
        {
            "force": "strong", "group": "SU(3)_c",
            "carrier": "gluon", "generators": 8,
            "coupling": "alpha_s",
            "processes": ["quark scattering", "gluon fusion",
                          "jet production"],
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "symmetry_group"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["group_table"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "identify symmetry group of interaction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate symmetry group identification problem.

        Args:
            difficulty: Controls answer detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        interaction = self._rng.choice(self._INTERACTIONS)
        process = self._rng.choice(interaction["processes"])

        return f"\\text{{{process}}}", {
            "process": process,
            "force": interaction["force"],
            "group": interaction["group"],
            "carrier": interaction["carrier"],
            "generators": interaction["generators"],
            "coupling": interaction["coupling"],
            "difficulty": difficulty,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate symmetry group identification steps.

        Args:
            data: Solution data with interaction details.

        Returns:
            List of step strings.
        """
        steps = [
            f"process: {data['process']}",
            f"force: {data['force']}",
            f"gauge group: {data['group']}",
            f"carrier: {data['carrier']}",
        ]
        if data["difficulty"] >= 7:
            steps.append(
                f"generators: {data['generators']}, "
                f"coupling: {data['coupling']}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the symmetry group and carrier.

        Args:
            data: Solution data.

        Returns:
            String with group and carrier.
        """
        return f"{data['group']}, carrier: {data['carrier']}"
