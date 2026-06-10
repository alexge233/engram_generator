"""Quantum mechanics extension generators -- expectation values through identical particles.

Deepens the existing quantum mechanics domain with expectation values,
quantum harmonic oscillator, first-order perturbation theory, selection
rules, tunneling probability, density operator, two-level systems, and
identical particles. Tiers range from 6 to 7.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register
from engram_generator.generators.quantum_mechanics import QuantumFormatter

_fmt = QuantumFormatter.format_sci
_fval = QuantumFormatter.format_value

_HBAR = 1.055e-34  # reduced Planck constant (J s)
_M_E = 9.109e-31   # electron mass (kg)


# ===================================================================
# 1. Expectation value (tier 6)
# ===================================================================

@register
class ExpectationValueGenerator(StepGenerator):
    """Compute expectation value <A> = <psi|A|psi> for simple operators.

    For particle-in-a-box state psi_n: <x> = L/2, <x^2> = L^2(1/(3) - 1/(2n^2*pi^2)).
    <p> = 0, <p^2> = n^2*pi^2*hbar^2/L^2.

    Difficulty scaling:
        Difficulty 1-3: compute <x> and <p> only (n in [1,3]).
        Difficulty 4-6: compute <x^2> and <p^2> (n in [1,5]).
        Difficulty 7-8: compute uncertainty products (n in [1,8]).

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "expectation_value"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute expectation value for particle-in-a-box"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate expectation value problem for particle-in-a-box.

        Args:
            difficulty: Controls which expectation values to compute.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 3)
        elif difficulty <= 6:
            n = self._rng.randint(1, 5)
        else:
            n = self._rng.randint(1, 8)

        l_exp = self._rng.choice([-10, -9])
        l_mantissa = self._rng.randint(1, 9)
        length = l_mantissa * (10.0 ** l_exp)

        exp_x = round(length / 2, 4)
        exp_p = 0.0
        exp_x2 = round(
            length ** 2 * (1.0 / 3.0 - 1.0 / (2 * n ** 2 * math.pi ** 2)),
            4,
        )
        exp_p2 = round(n ** 2 * math.pi ** 2 * _HBAR ** 2 / length ** 2, 4)

        dx = round(math.sqrt(exp_x2 - exp_x ** 2), 4)
        dp = round(math.sqrt(exp_p2), 4)
        dx_dp = round(dx * dp, 4)

        return "\\langle A \\rangle = \\langle \\psi|A|\\psi \\rangle", {
            "n": n, "L": length,
            "exp_x": exp_x, "exp_p": exp_p,
            "exp_x2": exp_x2, "exp_p2": exp_p2,
            "dx": dx, "dp": dp, "dx_dp": dx_dp,
            "full": difficulty >= 4,
            "uncertainty": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate expectation value computation steps.

        Args:
            data: Solution data with n, L, and expectation values.

        Returns:
            List of step strings.
        """
        steps = [
            f"n={data['n']}, L={_fmt(data['L'])} m",
            f"<x> = L/2 = {_fmt(data['exp_x'])} m",
            f"<p> = 0",
        ]
        if data["full"]:
            steps.append(f"<x^2> = {_fmt(data['exp_x2'])} m^2")
            steps.append(f"<p^2> = {_fmt(data['exp_p2'])} (kg*m/s)^2")
        if data["uncertainty"]:
            steps.append(f"dx*dp = {_fmt(data['dx_dp'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the expectation values.

        Args:
            data: Solution data.

        Returns:
            Expectation values as a string.
        """
        if data["uncertainty"]:
            return (
                f"<x>={_fmt(data['exp_x'])}m, "
                f"dx*dp={_fmt(data['dx_dp'])}"
            )
        return f"<x>={_fmt(data['exp_x'])}m, <p>=0"


# ===================================================================
# 2. Quantum harmonic oscillator (tier 6)
# ===================================================================

@register
class HarmonicOscillatorQMGenerator(StepGenerator):
    """Compute quantum harmonic oscillator energy levels.

    E_n = hbar*omega*(n+1/2). Zero-point energy E_0 = hbar*omega/2.
    Transition energy dE = hbar*omega.

    Difficulty scaling:
        Difficulty 1-3: compute E_n for n in [0,3], omega given directly.
        Difficulty 4-6: compute E_n for n in [0,5], omega from k and m.
        Difficulty 7-8: compute transition energies between levels.

    Prerequisites:
        schrodinger_1d.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "harmonic_oscillator_qm"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["schrodinger_1d"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute quantum harmonic oscillator energy levels"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate QHO energy level problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(0, 3)
            omega = round(self._rng.uniform(1e12, 1e14), 4)
        elif difficulty <= 6:
            n = self._rng.randint(0, 5)
            k = self._rng.randint(1, 50)
            m_kg = round(self._rng.uniform(1e-27, 1e-25), 4)
            omega = round(math.sqrt(k / m_kg), 4)
        else:
            n = self._rng.randint(0, 8)
            k = self._rng.randint(1, 100)
            m_kg = round(self._rng.uniform(1e-27, 1e-25), 4)
            omega = round(math.sqrt(k / m_kg), 4)

        e_n = _HBAR * omega * (n + 0.5)
        e_0 = _HBAR * omega * 0.5
        de = _HBAR * omega

        return "E_n = \\hbar\\omega(n+1/2)", {
            "n": n, "omega": omega,
            "E_n": e_n, "E_0": e_0, "dE": de,
            "transition": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate QHO computation steps.

        Args:
            data: Solution data with n, omega, and energies.

        Returns:
            List of step strings.
        """
        steps = [
            f"omega={_fmt(data['omega'])} rad/s",
            f"E_0 = hbar*omega/2 = {_fmt(data['E_0'])} J",
            f"E_{data['n']} = hbar*omega*({data['n']}+1/2)"
            f" = {_fmt(data['E_n'])} J",
        ]
        if data["transition"]:
            steps.append(f"dE = hbar*omega = {_fmt(data['dE'])} J")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the energy level.

        Args:
            data: Solution data.

        Returns:
            E_n as a string.
        """
        return f"E_{data['n']}={_fmt(data['E_n'])}J"


# ===================================================================
# 3. First-order perturbation theory (tier 7)
# ===================================================================

@register
class PerturbationFirstOrderGenerator(StepGenerator):
    """Compute first-order energy correction E_n^(1) = <n|H'|n>.

    For particle-in-a-box with a constant perturbation H' = V_0 on
    [0, L/2], the first-order correction is E_n^(1) = V_0/2 for all n.
    For a linear perturbation H' = V_0*x/L, E_n^(1) = V_0/2.

    Difficulty scaling:
        Difficulty 1-3: constant perturbation, n in [1,3].
        Difficulty 4-6: linear perturbation, n in [1,5].
        Difficulty 7-8: delta perturbation H' = alpha*delta(x-L/2).

    Prerequisites:
        expectation_value.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "perturbation_first_order"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["expectation_value"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute first-order energy correction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate perturbation theory problem.

        Args:
            difficulty: Controls perturbation type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 3)
            v0 = round(self._rng.uniform(0.01, 1.0), 4)
            correction = round(v0 / 2, 4)
            return "E_n^{(1)} = \\langle n|H'|n \\rangle", {
                "mode": "constant", "n": n, "V0": v0,
                "correction": correction,
            }

        if difficulty <= 6:
            n = self._rng.randint(1, 5)
            v0 = round(self._rng.uniform(0.01, 1.0), 4)
            correction = round(v0 / 2, 4)
            return "E_n^{(1)} = \\langle n|H'|n \\rangle", {
                "mode": "linear", "n": n, "V0": v0,
                "correction": correction,
            }

        # Delta perturbation at x=L/2: <n|alpha*delta(x-L/2)|n> = alpha*(2/L)*sin^2(n*pi/2)
        n = self._rng.randint(1, 8)
        alpha = round(self._rng.uniform(0.01, 1.0), 4)
        l_mantissa = self._rng.randint(1, 5)
        length = l_mantissa * 1e-10
        sin_sq = round(math.sin(n * math.pi / 2) ** 2, 4)
        correction = round(alpha * (2 / length) * sin_sq, 4)
        return "E_n^{(1)} = \\alpha \\frac{2}{L}\\sin^2(n\\pi/2)", {
            "mode": "delta", "n": n, "alpha": alpha,
            "L": length, "sin_sq": sin_sq,
            "correction": correction,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate perturbation theory computation steps.

        Args:
            data: Solution data with mode, n, and correction.

        Returns:
            List of step strings.
        """
        mode = data["mode"]
        if mode == "constant":
            return [
                f"H' = V_0 on [0, L/2], V_0={data['V0']} eV",
                f"n={data['n']}",
                f"E_n^(1) = V_0/2 = {_fval(data['correction'])} eV",
            ]
        if mode == "linear":
            return [
                f"H' = V_0*x/L, V_0={data['V0']} eV",
                f"n={data['n']}",
                f"E_n^(1) = V_0/2 = {_fval(data['correction'])} eV",
            ]
        return [
            f"H' = alpha*delta(x-L/2), alpha={data['alpha']}",
            f"n={data['n']}, L={_fmt(data['L'])} m",
            f"sin^2({data['n']}*pi/2) = {_fval(data['sin_sq'])}",
            f"E_n^(1) = alpha*(2/L)*sin^2 = {_fmt(data['correction'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the first-order energy correction.

        Args:
            data: Solution data.

        Returns:
            E_n^(1) as a string.
        """
        if data["mode"] == "delta":
            return f"E_n^(1) = {_fmt(data['correction'])}"
        return f"E_n^(1) = {_fval(data['correction'])} eV"


# ===================================================================
# 4. Selection rules (tier 6)
# ===================================================================

@register
class SelectionRulesGenerator(StepGenerator):
    """Determine if an electric dipole transition is allowed.

    Electric dipole selection rules: delta_l = +/-1, delta_m = 0,+/-1.
    Given initial (n,l,m) and final (n',l',m'), determine if allowed.

    Difficulty scaling:
        Difficulty 1-3: small quantum numbers (n<=3, l<=2).
        Difficulty 4-6: medium quantum numbers (n<=5, l<=4).
        Difficulty 7-8: large quantum numbers (n<=8, l<=7).

    Prerequisites:
        hydrogen_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "selection_rules"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["hydrogen_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "determine if electric dipole transition is allowed"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a transition and check selection rules.

        Args:
            difficulty: Controls quantum number ranges.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            n_max, l_max = 3, 2
        elif difficulty <= 6:
            n_max, l_max = 5, 4
        else:
            n_max, l_max = 8, 7

        n_i = self._rng.randint(2, n_max)
        l_i = self._rng.randint(0, min(n_i - 1, l_max))
        m_i = self._rng.randint(-l_i, l_i)

        n_f = self._rng.randint(1, n_max)
        while n_f == n_i:
            n_f = self._rng.randint(1, n_max)

        # Randomly make it allowed or forbidden
        if self._rng.random() < 0.5:
            # Allowed: delta_l = +/-1, delta_m in {-1,0,1}
            dl = self._rng.choice([-1, 1])
            l_f = l_i + dl
            if l_f < 0 or l_f >= n_f:
                l_f = max(0, min(n_f - 1, l_i + 1))
                dl = l_f - l_i
            dm = self._rng.choice([-1, 0, 1])
            m_f = m_i + dm
            m_f = max(-l_f, min(l_f, m_f))
        else:
            # Forbidden: delta_l != +/-1
            dl_choices = [d for d in [0, 2, -2] if 0 <= l_i + d < n_f]
            if dl_choices:
                dl = self._rng.choice(dl_choices)
                l_f = l_i + dl
            else:
                l_f = l_i
            m_f = self._rng.randint(-l_f, l_f)

        dl = l_f - l_i
        dm = m_f - m_i
        allowed = (abs(dl) == 1) and (abs(dm) <= 1)

        return "\\Delta l = \\pm 1, \\Delta m = 0, \\pm 1", {
            "n_i": n_i, "l_i": l_i, "m_i": m_i,
            "n_f": n_f, "l_f": l_f, "m_f": m_f,
            "dl": dl, "dm": dm, "allowed": allowed,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate selection rule checking steps.

        Args:
            data: Solution data with quantum numbers and result.

        Returns:
            List of step strings.
        """
        return [
            f"({data['n_i']},{data['l_i']},{data['m_i']}) -> "
            f"({data['n_f']},{data['l_f']},{data['m_f']})",
            f"dl = {data['dl']}, dm = {data['dm']}",
            f"|dl|=1? {'yes' if abs(data['dl']) == 1 else 'no'}, "
            f"|dm|<=1? {'yes' if abs(data['dm']) <= 1 else 'no'}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return whether the transition is allowed.

        Args:
            data: Solution data.

        Returns:
            'allowed' or 'forbidden'.
        """
        return "allowed" if data["allowed"] else "forbidden"


# ===================================================================
# 5. Tunneling probability (tier 6)
# ===================================================================

@register
class TunnelingProbabilityGenerator(StepGenerator):
    """Compute quantum tunneling transmission coefficient.

    T ~ exp(-2*kappa*L) where kappa = sqrt(2*m*(V-E))/hbar.
    For a rectangular barrier of height V, width L, particle energy E < V.

    Difficulty scaling:
        Difficulty 1-3: V-E small, L in [1e-10,5e-10].
        Difficulty 4-6: V-E moderate, L in [1e-10,1e-9].
        Difficulty 7-8: V-E large, L in [1e-10,5e-9].

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tunneling_probability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute quantum tunneling transmission coefficient"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate tunneling problem parameters and compute T.

        Args:
            difficulty: Controls barrier dimensions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        # Energy in eV, convert to Joules for computation
        v_eV = round(self._rng.uniform(1.0, 5.0 + difficulty), 2)
        e_eV = round(self._rng.uniform(0.1, v_eV * 0.9), 2)
        v_minus_e_eV = round(v_eV - e_eV, 4)
        v_minus_e_J = v_minus_e_eV * 1.602e-19

        if difficulty <= 3:
            l_ang = self._rng.randint(1, 5)
        elif difficulty <= 6:
            l_ang = self._rng.randint(1, 10)
        else:
            l_ang = self._rng.randint(1, 50)
        length = l_ang * 1e-10

        kappa = math.sqrt(2 * _M_E * v_minus_e_J) / _HBAR
        exponent = round(-2 * kappa * length, 4)
        t_coeff = round(math.exp(exponent), 4)

        return "T \\approx e^{-2\\kappa L}", {
            "V_eV": v_eV, "E_eV": e_eV,
            "V_minus_E_eV": v_minus_e_eV,
            "V_minus_E_J": v_minus_e_J,
            "L_ang": l_ang, "L": length,
            "kappa": round(kappa, 4), "exponent": exponent,
            "T": t_coeff,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate tunneling computation steps.

        Args:
            data: Solution data with V, E, L, kappa, T.

        Returns:
            List of step strings.
        """
        return [
            f"V={data['V_eV']}eV, E={data['E_eV']}eV, "
            f"V-E={data['V_minus_E_eV']}eV",
            f"L={data['L_ang']} Angstrom",
            f"kappa = sqrt(2m(V-E))/hbar = {_fmt(data['kappa'])} m^-1",
            f"2*kappa*L = {_fval(abs(data['exponent']))}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the transmission coefficient.

        Args:
            data: Solution data.

        Returns:
            T as a string.
        """
        return f"T = {_fmt(data['T'])}"


# ===================================================================
# 6. Density operator (tier 6)
# ===================================================================

@register
class DensityOperatorGenerator(StepGenerator):
    """Compute density matrix properties: Tr(rho), Tr(rho^2), purity.

    rho = sum p_i |psi_i><psi_i|. Pure if Tr(rho^2)=1, mixed if <1.
    For a 2x2 system with two states and probabilities p and 1-p.

    Difficulty scaling:
        Difficulty 1-3: pure state (p=1), verify Tr(rho^2)=1.
        Difficulty 4-6: mixed state, two basis states with probabilities.
        Difficulty 7-8: three states in the mixture.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "density_operator"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute density matrix trace and purity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate density operator problem.

        Args:
            difficulty: Controls purity and number of states.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            # Pure state: rho = |0><0| or |1><1|
            state = self._rng.choice([0, 1])
            if state == 0:
                rho = [[1, 0], [0, 0]]
            else:
                rho = [[0, 0], [0, 1]]
            tr_rho = 1
            tr_rho2 = 1
            pure = True
            probs = [1.0] if state == 0 else [0.0, 1.0]
        elif difficulty <= 6:
            # Mixed state: p|0><0| + (1-p)|1><1|
            p = round(self._rng.uniform(0.1, 0.9), 2)
            rho = [[p, 0], [0, round(1 - p, 4)]]
            tr_rho = 1
            tr_rho2 = round(p ** 2 + (1 - p) ** 2, 4)
            pure = abs(tr_rho2 - 1.0) < 1e-6
            probs = [p, round(1 - p, 4)]
        else:
            # Three-state mixture (using 3x3 diagonal)
            p1 = round(self._rng.uniform(0.1, 0.5), 2)
            p2 = round(self._rng.uniform(0.1, min(0.5, 1 - p1 - 0.05)), 2)
            p3 = round(1 - p1 - p2, 4)
            tr_rho = 1
            tr_rho2 = round(p1 ** 2 + p2 ** 2 + p3 ** 2, 4)
            pure = abs(tr_rho2 - 1.0) < 1e-6
            rho = [[p1, 0, 0], [0, p2, 0], [0, 0, p3]]
            probs = [p1, p2, p3]

        return "\\rho = \\sum p_i |\\psi_i\\rangle\\langle\\psi_i|", {
            "rho": rho, "probs": probs,
            "Tr_rho": tr_rho, "Tr_rho2": tr_rho2,
            "pure": pure,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate density operator computation steps.

        Args:
            data: Solution data with rho and traces.

        Returns:
            List of step strings.
        """
        probs_str = ", ".join(f"p_{i+1}={p}" for i, p in enumerate(data["probs"]))
        return [
            f"probabilities: {probs_str}",
            f"Tr(rho) = {data['Tr_rho']}",
            f"Tr(rho^2) = {_fval(data['Tr_rho2'])}",
            f"{'pure' if data['pure'] else 'mixed'} state",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return trace and purity classification.

        Args:
            data: Solution data.

        Returns:
            Tr(rho^2) and classification as a string.
        """
        state_type = "pure" if data["pure"] else "mixed"
        return f"Tr(rho^2)={_fval(data['Tr_rho2'])}, {state_type}"


# ===================================================================
# 7. Two-level system (tier 6)
# ===================================================================

@register
class TwoLevelSystemGenerator(StepGenerator):
    """Diagonalise a 2x2 Hamiltonian for a two-level system.

    H = [[E1, V],[V, E2]]. Eigenvalues E_+/- = (E1+E2)/2 +/- sqrt(delta^2 + V^2)
    where delta = (E1-E2)/2. Avoided crossing gap = 2*V.

    Difficulty scaling:
        Difficulty 1-3: E1,E2 in [1,5] eV, V in [0.1,1] eV.
        Difficulty 4-6: E1,E2 in [1,10] eV, V in [0.1,3] eV.
        Difficulty 7-8: near-degenerate (E1~E2), V small.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_level_system"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "diagonalise two-level system Hamiltonian"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate two-level system parameters and diagonalise.

        Args:
            difficulty: Controls energy scales.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            e1 = round(self._rng.uniform(1.0, 5.0), 2)
            e2 = round(self._rng.uniform(1.0, 5.0), 2)
            v = round(self._rng.uniform(0.1, 1.0), 2)
        elif difficulty <= 6:
            e1 = round(self._rng.uniform(1.0, 10.0), 2)
            e2 = round(self._rng.uniform(1.0, 10.0), 2)
            v = round(self._rng.uniform(0.1, 3.0), 2)
        else:
            base = round(self._rng.uniform(3.0, 8.0), 2)
            e1 = base
            e2 = round(base + self._rng.uniform(-0.1, 0.1), 4)
            v = round(self._rng.uniform(0.01, 0.5), 4)

        avg = (e1 + e2) / 2
        delta = (e1 - e2) / 2
        discriminant = math.sqrt(delta ** 2 + v ** 2)
        e_plus = round(avg + discriminant, 4)
        e_minus = round(avg - discriminant, 4)
        gap = round(2 * discriminant, 4)

        return "H = \\begin{pmatrix} E_1 & V \\\\ V & E_2 \\end{pmatrix}", {
            "E1": e1, "E2": e2, "V": v,
            "avg": round(avg, 4), "delta": round(delta, 4),
            "discriminant": round(discriminant, 4),
            "E_plus": e_plus, "E_minus": e_minus, "gap": gap,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate two-level system diagonalisation steps.

        Args:
            data: Solution data with E1, E2, V, and eigenvalues.

        Returns:
            List of step strings.
        """
        return [
            f"E1={data['E1']}eV, E2={data['E2']}eV, V={data['V']}eV",
            f"avg = (E1+E2)/2 = {_fval(data['avg'])} eV",
            f"delta = (E1-E2)/2 = {_fval(data['delta'])} eV",
            f"sqrt(delta^2+V^2) = {_fval(data['discriminant'])} eV",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the eigenvalues and gap.

        Args:
            data: Solution data.

        Returns:
            E_+, E_-, and gap as a string.
        """
        return (
            f"E+={_fval(data['E_plus'])}eV, "
            f"E-={_fval(data['E_minus'])}eV, "
            f"gap={_fval(data['gap'])}eV"
        )


# ===================================================================
# 8. Identical particles (tier 6)
# ===================================================================

@register
class IdenticalParticlesGenerator(StepGenerator):
    """Symmetrise/antisymmetrise two-particle wavefunctions.

    Bosons: psi_+ = (psi_a*psi_b + psi_b*psi_a)/sqrt(2).
    Fermions: psi_- = (psi_a*psi_b - psi_b*psi_a)/sqrt(2).
    Check normalisation: |coeff|^2 + |coeff|^2 = 1.

    Difficulty scaling:
        Difficulty 1-3: two distinct states, compute normalisation.
        Difficulty 4-6: verify orthogonality of symmetric/antisymmetric.
        Difficulty 7-8: three-particle system (Slater determinant).

    Prerequisites:
        complex_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "identical_particles"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "symmetrise wavefunction for identical particles"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate identical particles symmetrisation problem.

        Args:
            difficulty: Controls complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        particle_type = self._rng.choice(["boson", "fermion"])

        if difficulty <= 6:
            # Two-particle system
            state_a = self._rng.randint(1, 3 + difficulty)
            state_b = self._rng.randint(1, 3 + difficulty)
            while state_b == state_a:
                state_b = self._rng.randint(1, 3 + difficulty)

            norm_factor = round(1.0 / math.sqrt(2), 4)
            if particle_type == "boson":
                sign = "+"
            else:
                sign = "-"

            return "\\psi = \\frac{1}{\\sqrt{2}}(\\psi_a \\psi_b \\pm \\psi_b \\psi_a)", {
                "n_particles": 2,
                "type": particle_type, "sign": sign,
                "state_a": state_a, "state_b": state_b,
                "norm": norm_factor,
                "normalised": True,
            }

        # Three-particle Slater determinant (fermions always)
        states = []
        while len(states) < 3:
            s = self._rng.randint(1, 8)
            if s not in states:
                states.append(s)
        states.sort()
        norm_factor = round(1.0 / math.sqrt(6), 4)

        return "\\psi = \\frac{1}{\\sqrt{3!}}\\det(\\psi_{ij})", {
            "n_particles": 3,
            "type": "fermion", "sign": "-",
            "states": states,
            "norm": norm_factor,
            "normalised": True,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate identical particles computation steps.

        Args:
            data: Solution data with particle type, states, norm.

        Returns:
            List of step strings.
        """
        if data["n_particles"] == 2:
            return [
                f"type: {data['type']}",
                f"states: n_a={data['state_a']}, n_b={data['state_b']}",
                f"psi = (1/sqrt(2))(psi_{data['state_a']}*psi_{data['state_b']}"
                f" {data['sign']} psi_{data['state_b']}*psi_{data['state_a']})",
                f"normalisation: 1/sqrt(2) = {_fval(data['norm'])}",
            ]
        states_str = ",".join(str(s) for s in data["states"])
        return [
            f"type: fermion (3 particles)",
            f"states: {states_str}",
            f"Slater determinant: 3! = 6 terms",
            f"normalisation: 1/sqrt(6) = {_fval(data['norm'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the normalisation factor and state type.

        Args:
            data: Solution data.

        Returns:
            Norm and classification as a string.
        """
        return (
            f"norm={_fval(data['norm'])}, "
            f"{'normalised' if data['normalised'] else 'unnormalised'}"
        )
