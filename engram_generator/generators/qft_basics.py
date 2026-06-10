"""Quantum field theory basics generators.

6 generators at tiers 6-7 covering scalar field Lagrangians,
Feynman propagators, vertex factors, tree-level amplitudes,
dimensional analysis in natural units, and Noether's theorem.
All produce step-by-step solutions with LaTeX formatting.
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


# ===================================================================
# 1. Field Lagrangian  (tier 6)
# ===================================================================

@register
class FieldLagrangianGenerator(StepGenerator):
    """Write Lagrangian density for a scalar field and derive the EOM.

    Given mass m and optional interaction term, construct the free
    scalar Lagrangian L = (1/2)(d_mu phi)(d^mu phi) - (1/2)m^2*phi^2
    and derive the Klein-Gordon equation of motion.

    Difficulty scaling:
        Difficulty 1-3: free scalar field, integer mass.
        Difficulty 4-6: free scalar field, decimal mass.
        Difficulty 7-8: scalar field with phi^4 interaction term.

    Prerequisites:
        lagrangian, partial_derivative.
    """

    _INTERACTION_NAMES = ["phi^4", "phi^3", "phi^6"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "field_lagrangian"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["lagrangian", "partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "write scalar field Lagrangian and derive EOM"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scalar field Lagrangian problem.

        Args:
            difficulty: Controls mass complexity and interaction terms.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m = float(self._rng.randint(1, 5))
        else:
            m = round(self._rng.uniform(0.5, 5.0), 4)

        m_sq = round(m * m, 4)
        has_interaction = difficulty >= 7

        if has_interaction:
            lam = round(self._rng.uniform(0.01, 1.0), 4)
            power = self._rng.choice([3, 4])
            interaction_str = (
                f" - \\frac{{\\lambda}}{{{power}!}}\\phi^{power}"
            )
            eom_extra = (
                f" - \\frac{{\\lambda}}{{{math.factorial(power - 1)}}}"
                f"\\phi^{{{power - 1}}}"
            )
        else:
            lam = 0.0
            power = 0
            interaction_str = ""
            eom_extra = ""

        problem = (
            f"\\mathcal{{L}} = \\frac{{1}}{{2}}(\\partial_\\mu \\phi)"
            f"(\\partial^\\mu \\phi) - \\frac{{1}}{{2}}"
            f"({_fmt(m)})^2 \\phi^2{interaction_str}"
        )

        return problem, {
            "m": m, "m_sq": m_sq,
            "has_interaction": has_interaction,
            "lambda": lam, "power": power,
            "interaction_str": interaction_str,
            "eom_extra": eom_extra,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps deriving the Klein-Gordon equation.

        Args:
            data: Solution data with mass and interaction details.

        Returns:
            List of step strings.
        """
        m = data["m"]
        steps = [
            f"L_free = (1/2)(d_mu phi)^2 - (1/2)*{_fmt(data['m_sq'])}*phi^2",
            f"Euler-Lagrange: d_mu(dL/d(d_mu phi)) - dL/dphi = 0",
            f"(d^2 + {_fmt(data['m_sq'])})*phi = 0  (Klein-Gordon)",
        ]
        if data["has_interaction"]:
            steps.append(
                f"interaction: lambda={_fmt(data['lambda'])}, "
                f"phi^{data['power']} term"
            )
            steps.append(
                f"EOM: (d^2 + {_fmt(data['m_sq'])})*phi"
                f"{data['eom_extra']} = 0"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the equation of motion.

        Args:
            data: Solution data.

        Returns:
            Klein-Gordon equation string.
        """
        base = f"(d^2 + {_fmt(data['m_sq'])})*phi"
        if data["has_interaction"]:
            return f"{base}{data['eom_extra']} = 0"
        return f"{base} = 0"


# ===================================================================
# 2. Feynman Propagator  (tier 7)
# ===================================================================

@register
class FeynmanPropagatorGenerator(StepGenerator):
    """Compute scalar propagator in momentum space and identify poles.

    The Feynman propagator for a scalar field of mass m is
    D(k) = i / (k^2 - m^2 + i*epsilon). Identify the pole locations
    at k_0 = +/- sqrt(|k|^2 + m^2).

    Difficulty scaling:
        Difficulty 1-3: integer mass, compute D for given k^2.
        Difficulty 4-6: decimal mass, compute pole locations.
        Difficulty 7-8: also compute residue at the pole.

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "feynman_propagator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["complex_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute scalar Feynman propagator and identify poles"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Feynman propagator problem.

        Args:
            difficulty: Controls mass type and answer detail.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            m = float(self._rng.randint(1, 5))
        else:
            m = round(self._rng.uniform(0.5, 5.0), 4)

        m_sq = round(m * m, 4)

        # Sample a 3-momentum magnitude
        k_mag = round(self._rng.uniform(0.5, 10.0), 4)
        k_sq_3 = round(k_mag * k_mag, 4)

        # Pole location: k_0 = +/- omega
        omega = round(math.sqrt(k_sq_3 + m_sq), 4)

        # Sample k^2 = k_0^2 - |k|^2 for propagator evaluation
        k_0 = round(self._rng.uniform(1.0, 10.0), 4)
        k_sq = round(k_0 * k_0 - k_sq_3, 4)
        denom = round(k_sq - m_sq, 4)

        if abs(denom) < 1e-6:
            denom = 1.0

        prop_val = round(1.0 / denom, 4)

        compute_residue = difficulty >= 7
        residue = round(1.0 / (2.0 * omega), 4) if compute_residue else 0.0

        problem = (
            f"D(k) = \\frac{{i}}{{k^2 - {_fmt(m_sq)} + i\\epsilon}}"
            f", \\; |\\mathbf{{k}}| = {_fmt(k_mag)}"
        )

        return problem, {
            "m": m, "m_sq": m_sq, "k_mag": k_mag,
            "k_sq_3": k_sq_3, "omega": omega,
            "k_0": k_0, "k_sq": k_sq, "denom": denom,
            "prop_val": prop_val,
            "compute_residue": compute_residue,
            "residue": residue,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate propagator computation steps.

        Args:
            data: Solution data with mass and momenta.

        Returns:
            List of step strings.
        """
        steps = [
            f"m^2 = {_fmt(data['m_sq'])}",
            f"|k|^2 = {_fmt(data['k_sq_3'])}",
            f"omega = sqrt({_fmt(data['k_sq_3'])} + {_fmt(data['m_sq'])})"
            f" = {_fmt(data['omega'])}",
            f"poles at k_0 = +/-{_fmt(data['omega'])}",
        ]
        if data["compute_residue"]:
            steps.append(
                f"residue = 1/(2*omega) = {_fmt(data['residue'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return pole locations and optional residue.

        Args:
            data: Solution data.

        Returns:
            String with poles and residue if applicable.
        """
        ans = f"poles: k_0 = +/-{_fmt(data['omega'])}"
        if data["compute_residue"]:
            ans += f", residue = {_fmt(data['residue'])}"
        return ans


# ===================================================================
# 3. Vertex Factor  (tier 7)
# ===================================================================

@register
class VertexFactorGenerator(StepGenerator):
    """Identify the correct Feynman rule vertex factor for a diagram.

    For phi^4 theory the vertex is -i*lambda; for QED the
    electron-photon vertex is -i*e*gamma_mu. Given a theory and
    diagram type, identify the correct vertex factor.

    Difficulty scaling:
        Difficulty 1-3: phi^4 theory, single vertex.
        Difficulty 4-6: QED vertex, identify gamma_mu structure.
        Difficulty 7-8: Yukawa coupling -i*g or phi^3 theory -i*g.

    Prerequisites:
        conservation_laws.
    """

    _THEORIES = [
        {
            "name": "phi^4", "vertex": "-i*lambda",
            "coupling": "lambda", "legs": 4,
            "description": "4-scalar vertex",
        },
        {
            "name": "QED", "vertex": "-i*e*gamma_mu",
            "coupling": "e", "legs": 3,
            "description": "electron-photon vertex",
        },
        {
            "name": "Yukawa", "vertex": "-i*g",
            "coupling": "g", "legs": 3,
            "description": "scalar-fermion vertex",
        },
        {
            "name": "phi^3", "vertex": "-i*g",
            "coupling": "g", "legs": 3,
            "description": "3-scalar vertex",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vertex_factor"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

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
        return "identify Feynman rule vertex factor"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vertex factor identification problem.

        Args:
            difficulty: Controls theory complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = self._THEORIES[:1]
        elif difficulty <= 6:
            pool = self._THEORIES[:2]
        else:
            pool = self._THEORIES

        theory = self._rng.choice(pool)

        # Sample a coupling constant value
        coupling_val = round(self._rng.uniform(0.01, 1.0), 4)
        vertex_magnitude = coupling_val

        n_vertices = 1
        if difficulty >= 5:
            n_vertices = self._rng.randint(1, 2)

        total_factor = round(coupling_val ** n_vertices, 4)

        problem = (
            f"\\text{{{theory['name']} theory}}: "
            f"{theory['description']}, "
            f"{theory['coupling']} = {_fmt(coupling_val)}"
        )

        return problem, {
            "theory": theory["name"],
            "vertex_str": theory["vertex"],
            "coupling": theory["coupling"],
            "coupling_val": coupling_val,
            "legs": theory["legs"],
            "description": theory["description"],
            "n_vertices": n_vertices,
            "total_factor": total_factor,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate vertex factor identification steps.

        Args:
            data: Solution data with theory and coupling.

        Returns:
            List of step strings.
        """
        steps = [
            f"theory: {data['theory']}",
            f"vertex rule: {data['vertex_str']}",
            f"{data['coupling']} = {_fmt(data['coupling_val'])}",
            f"legs per vertex: {data['legs']}",
        ]
        if data["n_vertices"] > 1:
            steps.append(
                f"n_vertices = {data['n_vertices']}, "
                f"total = ({data['coupling']})^{data['n_vertices']}"
                f" = {_fmt(data['total_factor'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the vertex factor.

        Args:
            data: Solution data.

        Returns:
            String with vertex factor and numeric value.
        """
        if data["n_vertices"] > 1:
            return (
                f"vertex: {data['vertex_str']}, "
                f"total: (-i)^{data['n_vertices']}*"
                f"{_fmt(data['total_factor'])}"
            )
        return (
            f"vertex: {data['vertex_str']}, "
            f"{data['coupling']} = {_fmt(data['coupling_val'])}"
        )


# ===================================================================
# 4. Tree-Level Amplitude  (tier 7)
# ===================================================================

@register
class TreeLevelAmplitudeGenerator(StepGenerator):
    """Compute simple 2->2 tree-level scattering amplitudes.

    For a contact interaction M = -i*lambda. For a single exchange
    diagram M = (-i*lambda)^2 * D(k) where D(k) = i/(k^2 - m^2).
    Compute the amplitude magnitude for given kinematics.

    Difficulty scaling:
        Difficulty 1-3: contact interaction (single vertex).
        Difficulty 4-6: s-channel exchange with given s.
        Difficulty 7-8: t-channel or u-channel exchange.

    Prerequisites:
        feynman_propagator.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tree_level_amplitude"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["feynman_propagator"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute tree-level scattering amplitude"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a tree-level amplitude problem.

        Args:
            difficulty: Controls diagram complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        lam = round(self._rng.uniform(0.1, 2.0), 4)

        if difficulty <= 3:
            # Contact interaction
            amplitude = lam
            problem = (
                f"\\mathcal{{M}} = -i\\lambda, \\;"
                f"\\lambda = {_fmt(lam)}"
            )
            return problem, {
                "mode": "contact", "lambda": lam,
                "amplitude": round(amplitude, 4),
            }

        # Exchange diagram
        m_ex = round(self._rng.uniform(1.0, 5.0), 4)
        m_ex_sq = round(m_ex * m_ex, 4)

        if difficulty <= 6:
            channel = "s"
            mandelstam = round(
                self._rng.uniform(m_ex_sq + 1.0, m_ex_sq + 20.0), 4
            )
        else:
            channel = self._rng.choice(["t", "u"])
            mandelstam = round(
                self._rng.uniform(-20.0, -0.5), 4
            )

        denom = round(mandelstam - m_ex_sq, 4)
        if abs(denom) < 1e-6:
            denom = 1.0
        propagator = round(1.0 / denom, 4)
        amplitude = round(lam * lam * abs(propagator), 4)

        problem = (
            f"\\mathcal{{M}} = (-i\\lambda)^2 "
            f"\\frac{{i}}{{{channel} - m^2}}, \\;"
            f"\\lambda = {_fmt(lam)}, m = {_fmt(m_ex)}, "
            f"{channel} = {_fmt(mandelstam)}"
        )

        return problem, {
            "mode": "exchange", "channel": channel,
            "lambda": lam, "m_ex": m_ex, "m_ex_sq": m_ex_sq,
            "mandelstam": mandelstam, "denom": denom,
            "propagator": propagator, "amplitude": amplitude,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate amplitude computation steps.

        Args:
            data: Solution data with kinematics.

        Returns:
            List of step strings.
        """
        if data["mode"] == "contact":
            return [
                f"contact vertex: -i*lambda",
                f"lambda = {_fmt(data['lambda'])}",
                f"|M| = {_fmt(data['amplitude'])}",
            ]

        return [
            f"channel: {data['channel']}",
            f"lambda = {_fmt(data['lambda'])}, m^2 = {_fmt(data['m_ex_sq'])}",
            f"{data['channel']} - m^2 = {_fmt(data['mandelstam'])}"
            f" - {_fmt(data['m_ex_sq'])} = {_fmt(data['denom'])}",
            f"D = 1/{_fmt(data['denom'])} = {_fmt(data['propagator'])}",
            f"|M| = lambda^2*|D| = {_fmt(data['amplitude'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the amplitude magnitude.

        Args:
            data: Solution data.

        Returns:
            String with |M| value.
        """
        return f"|M| = {_fmt(data['amplitude'])}"


# ===================================================================
# 5. Dimensional Analysis QFT  (tier 6)
# ===================================================================

@register
class DimensionalAnalysisQFTGenerator(StepGenerator):
    """Determine mass dimension of fields and couplings in natural units.

    In natural units (hbar=c=1), the action is dimensionless so
    [S] = 0. In d spacetime dimensions, [phi] = (d-2)/2 for a
    scalar field. Coupling dimensions follow from the interaction
    Lagrangian.

    Difficulty scaling:
        Difficulty 1-3: scalar field in d=4, compute [phi].
        Difficulty 4-6: determine coupling dimension for phi^n.
        Difficulty 7-8: fermion field dimension [psi] = (d-1)/2.

    Prerequisites:
        partial_derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dimensional_analysis_qft"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["partial_derivative"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine mass dimension in natural units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dimensional analysis problem.

        Args:
            difficulty: Controls field type and coupling analysis.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            d = 4
            phi_dim = round((d - 2) / 2.0, 4)
            problem = (
                f"[\\phi] \\text{{ in }} d = {d} \\text{{ dimensions}}"
            )
            return problem, {
                "mode": "scalar", "d": d,
                "phi_dim": phi_dim,
            }

        if difficulty <= 6:
            d = self._rng.choice([3, 4, 5, 6])
            n = self._rng.choice([3, 4, 6])
            phi_dim = round((d - 2) / 2.0, 4)
            # Lagrangian has dim d, so [g]*n*[phi] = d
            coupling_dim = round(d - n * phi_dim, 4)
            problem = (
                f"[g] \\text{{ for }} g\\phi^{n}"
                f" \\text{{ in }} d = {d}"
            )
            return problem, {
                "mode": "coupling", "d": d, "n": n,
                "phi_dim": phi_dim,
                "coupling_dim": coupling_dim,
            }

        # Fermion field dimension
        d = self._rng.choice([3, 4, 5])
        psi_dim = round((d - 1) / 2.0, 4)
        phi_dim = round((d - 2) / 2.0, 4)
        # Yukawa coupling g*psi_bar*psi*phi: dim = d
        yukawa_dim = round(d - 2 * psi_dim - phi_dim, 4)
        problem = (
            f"[\\psi], [g_Y] \\text{{ for Yukawa in }} d = {d}"
        )
        return problem, {
            "mode": "fermion", "d": d,
            "psi_dim": psi_dim, "phi_dim": phi_dim,
            "yukawa_dim": yukawa_dim,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate dimensional analysis steps.

        Args:
            data: Solution data with dimensions.

        Returns:
            List of step strings.
        """
        d = data["d"]

        if data["mode"] == "scalar":
            return [
                f"d = {d}, [S] = 0, [d^dx] = -d",
                f"[L] = d, kinetic: [(d phi)^2] = d",
                f"[phi] = (d-2)/2 = {_fmt(data['phi_dim'])}",
            ]

        if data["mode"] == "coupling":
            n = data["n"]
            return [
                f"d = {d}, [phi] = (d-2)/2 = {_fmt(data['phi_dim'])}",
                f"[g*phi^{n}] = d",
                f"[g] = d - {n}*{_fmt(data['phi_dim'])}"
                f" = {_fmt(data['coupling_dim'])}",
            ]

        # fermion
        return [
            f"d = {d}, [psi] = (d-1)/2 = {_fmt(data['psi_dim'])}",
            f"[phi] = (d-2)/2 = {_fmt(data['phi_dim'])}",
            f"[g_Y*psi_bar*psi*phi] = d",
            f"[g_Y] = d - 2*{_fmt(data['psi_dim'])}"
            f" - {_fmt(data['phi_dim'])} = {_fmt(data['yukawa_dim'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mass dimensions.

        Args:
            data: Solution data.

        Returns:
            String with mass dimensions.
        """
        if data["mode"] == "scalar":
            return f"[phi] = {_fmt(data['phi_dim'])}"
        if data["mode"] == "coupling":
            return f"[g] = {_fmt(data['coupling_dim'])}"
        return (
            f"[psi] = {_fmt(data['psi_dim'])}, "
            f"[g_Y] = {_fmt(data['yukawa_dim'])}"
        )


# ===================================================================
# 6. Symmetry and Conservation  (tier 6)
# ===================================================================

@register
class SymmetryAndConservationGenerator(StepGenerator):
    """Apply Noether's theorem to identify conserved currents.

    Given a continuous symmetry of the Lagrangian, identify the
    corresponding conserved current J^mu and conserved charge Q.
    U(1) -> electric charge, translations -> energy-momentum,
    Lorentz -> angular momentum.

    Difficulty scaling:
        Difficulty 1-3: U(1) phase symmetry, conserved charge.
        Difficulty 4-6: spacetime translations, energy-momentum tensor.
        Difficulty 7-8: Lorentz symmetry, angular momentum tensor.

    Prerequisites:
        conservation_laws.
    """

    _SYMMETRIES = [
        {
            "symmetry": "U(1) phase",
            "transformation": "phi -> e^{i*alpha}*phi",
            "current": "J^mu = i*(phi^* d^mu phi - phi d^mu phi^*)",
            "charge": "Q = electric charge",
            "level": "low",
        },
        {
            "symmetry": "global U(1)",
            "transformation": "psi -> e^{i*alpha}*psi",
            "current": "J^mu = e*psi_bar*gamma^mu*psi",
            "charge": "Q = fermion number",
            "level": "low",
        },
        {
            "symmetry": "spacetime translation",
            "transformation": "x^mu -> x^mu + a^mu",
            "current": "T^{mu nu} = dL/d(d_mu phi)*d^nu phi - eta^{mu nu}*L",
            "charge": "P^mu = energy-momentum",
            "level": "mid",
        },
        {
            "symmetry": "time translation",
            "transformation": "t -> t + epsilon",
            "current": "T^{0 nu}",
            "charge": "E = energy (Hamiltonian)",
            "level": "mid",
        },
        {
            "symmetry": "spatial translation",
            "transformation": "x^i -> x^i + a^i",
            "current": "T^{i nu}",
            "charge": "P^i = momentum",
            "level": "mid",
        },
        {
            "symmetry": "Lorentz boost",
            "transformation": "x^mu -> Lambda^mu_nu x^nu",
            "current": "M^{mu alpha beta} = x^alpha T^{mu beta} - x^beta T^{mu alpha}",
            "charge": "J^{alpha beta} = angular momentum",
            "level": "high",
        },
        {
            "symmetry": "spatial rotation",
            "transformation": "x^i -> R^i_j x^j",
            "current": "M^{0 ij}",
            "charge": "L^{ij} = angular momentum",
            "level": "high",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "symmetry_and_conservation"

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
        return "identify conserved current from symmetry via Noether theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Noether's theorem problem.

        Args:
            difficulty: Controls symmetry complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = [s for s in self._SYMMETRIES if s["level"] == "low"]
        elif difficulty <= 6:
            pool = [
                s for s in self._SYMMETRIES
                if s["level"] in ("low", "mid")
            ]
        else:
            pool = self._SYMMETRIES

        sym = self._rng.choice(pool)

        problem = f"\\text{{symmetry: {sym['symmetry']}}}"

        return problem, {
            "symmetry": sym["symmetry"],
            "transformation": sym["transformation"],
            "current": sym["current"],
            "charge": sym["charge"],
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Noether's theorem application steps.

        Args:
            data: Solution data with symmetry details.

        Returns:
            List of step strings.
        """
        return [
            f"symmetry: {data['symmetry']}",
            f"transform: {data['transformation']}",
            f"Noether current: {data['current']}",
            f"conserved charge: {data['charge']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the conserved current and charge.

        Args:
            data: Solution data.

        Returns:
            String with current and conserved quantity.
        """
        return f"{data['current']}, {data['charge']}"
