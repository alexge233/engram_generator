"""Deep quantum mechanics generators -- scattering, angular momentum,
many-body, and advanced quantum phenomena.

10 generators across tiers 5-7 covering Born rule, time evolution,
ladder operators, hydrogen orbitals, spin-1/2 rotations,
Wigner-Eckart theorem, variational method, degenerate perturbation
theory, scattering cross sections, and WKB approximation.
"""
from __future__ import annotations

import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _fmt(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if isinstance(rounded, float) and rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


# ===================================================================
# 1. Born Rule  (tier 5)
# ===================================================================

@register
class BornRuleGenerator(StepGenerator):
    """Compute measurement probabilities via the Born rule.

    Given a quantum state |psi> = sum c_n |a_n>, the probability of
    measuring outcome a_n is P(a_n) = |c_n|^2.  Verifies that the
    probabilities sum to 1.

    Difficulty scaling:
        Difficulty 1-3: 2 basis states, integer-ratio amplitudes.
        Difficulty 4-6: 3 basis states.
        Difficulty 7-8: 4 basis states with irrational amplitudes.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "born_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute measurement probabilities via Born rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Born rule measurement probability problem.

        Constructs a normalised state vector and computes |c_n|^2
        for each component.

        Args:
            difficulty: Controls number of basis states.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n_states = 2
        elif difficulty <= 6:
            n_states = 3
        else:
            n_states = 4

        # Generate unnormalised integer weights and normalise
        weights = [self._rng.randint(1, 5) for _ in range(n_states)]
        norm_sq = sum(w * w for w in weights)
        norm = math.sqrt(norm_sq)
        coeffs = [round(w / norm, 4) for w in weights]

        # Recompute probabilities from rounded coefficients
        probs = [round(c * c, 4) for c in coeffs]
        prob_sum = round(sum(probs), 4)

        labels = [f"|a_{i}\\rangle" for i in range(n_states)]
        state_str = " + ".join(
            f"{_fmt(c)}{labels[i]}" for i, c in enumerate(coeffs)
        )
        problem = f"|\\psi\\rangle = {state_str}"

        return problem, {
            "coeffs": coeffs, "probs": probs,
            "prob_sum": prob_sum, "labels": labels,
            "n_states": n_states,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate computation steps for Born rule probabilities.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for i in range(sd["n_states"]):
            c = sd["coeffs"][i]
            p = sd["probs"][i]
            steps.append(f"P(a_{i}) = |{_fmt(c)}|^2 = {_fmt(p)}")
        steps.append(f"sum = {_fmt(sd['prob_sum'])}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the measurement probabilities.

        Args:
            sd: Solution data.

        Returns:
            Probability values as a comma-separated string.
        """
        parts = [f"P(a_{i})={_fmt(sd['probs'][i])}"
                 for i in range(sd["n_states"])]
        return ", ".join(parts)


# ===================================================================
# 2. Time Evolution  (tier 6)
# ===================================================================

@register
class TimeEvolutionGenerator(StepGenerator):
    """Compute time-evolved quantum state for energy eigenstates.

    For |psi(t)> = sum c_n exp(-i E_n t / hbar) |n>, compute the
    coefficients at a given time t.  Uses hbar = 1 (natural units).

    Difficulty scaling:
        Difficulty 1-3: 2 energy eigenstates, integer energies.
        Difficulty 4-6: 3 eigenstates.
        Difficulty 7-8: 4 eigenstates with fractional energies.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "time_evolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute time-evolved state coefficients"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a time evolution problem.

        Args:
            difficulty: Controls number of eigenstates.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 2
            energies = [self._rng.randint(1, 5) for _ in range(n)]
        elif difficulty <= 6:
            n = 3
            energies = [self._rng.randint(1, 8) for _ in range(n)]
        else:
            n = 4
            energies = [round(self._rng.uniform(0.5, 10.0), 2)
                        for _ in range(n)]

        t = round(self._rng.uniform(0.1, 3.0), 2)

        # Phases: -E_n * t (hbar = 1)
        phases = [round(-e * t, 4) for e in energies]
        cos_vals = [round(math.cos(p), 4) for p in phases]
        sin_vals = [round(math.sin(p), 4) for p in phases]

        e_str = ", ".join(f"E_{i}={_fmt(energies[i])}" for i in range(n))
        problem = f"|\\psi(0)\\rangle = sum c_n|n\\rangle, {e_str}, t={_fmt(t)}"

        return problem, {
            "n": n, "energies": energies, "t": t,
            "phases": phases, "cos_vals": cos_vals,
            "sin_vals": sin_vals,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate time evolution computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"hbar = 1, t = {_fmt(sd['t'])}"]
        for i in range(sd["n"]):
            phase = sd["phases"][i]
            steps.append(
                f"phase_{i} = -E_{i}*t = {_fmt(phase)}, "
                f"exp(i*{_fmt(phase)}) = "
                f"{_fmt(sd['cos_vals'][i])} + i*{_fmt(sd['sin_vals'][i])}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the phase factors at time t.

        Args:
            sd: Solution data.

        Returns:
            Phase factor values as comma-separated string.
        """
        parts = []
        for i in range(sd["n"]):
            parts.append(
                f"e^{{-iE_{i}t}}="
                f"{_fmt(sd['cos_vals'][i])}+i*{_fmt(sd['sin_vals'][i])}"
            )
        return ", ".join(parts)


# ===================================================================
# 3. Ladder Operators  (tier 6)
# ===================================================================

@register
class LadderOperatorsGenerator(StepGenerator):
    """Compute ladder operator actions on harmonic oscillator states.

    Annihilation: a|n> = sqrt(n)|n-1>.
    Creation: a^+|n> = sqrt(n+1)|n+1>.
    Number operator: a^+ a|n> = n|n>.
    Computes matrix elements <m|a^+|n> and <m|a|n>.

    Difficulty scaling:
        Difficulty 1-3: n in [0, 3], single operator action.
        Difficulty 4-6: n in [0, 6], combined a^+ a.
        Difficulty 7-8: n in [0, 10], products like a^2 or (a^+)^2.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ladder_operators"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute ladder operator action on Fock state"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a ladder operator problem.

        Args:
            difficulty: Controls quantum number range and operation.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(0, 3)
            op = self._rng.choice(["a", "a_dag"])
        elif difficulty <= 6:
            n = self._rng.randint(0, 6)
            op = self._rng.choice(["a", "a_dag", "N"])
        else:
            n = self._rng.randint(0, 10)
            op = self._rng.choice(["a", "a_dag", "N", "a_sq", "a_dag_sq"])

        if op == "a":
            if n == 0:
                coeff = 0.0
                result_n = 0
            else:
                coeff = round(math.sqrt(n), 4)
                result_n = n - 1
            op_str = "a"
            desc = f"a|{n}\\rangle"
        elif op == "a_dag":
            coeff = round(math.sqrt(n + 1), 4)
            result_n = n + 1
            op_str = "a^\\dagger"
            desc = f"a^\\dagger|{n}\\rangle"
        elif op == "N":
            coeff = float(n)
            result_n = n
            op_str = "a^\\dagger a"
            desc = f"a^\\dagger a|{n}\\rangle"
        elif op == "a_sq":
            if n <= 1:
                coeff = 0.0
                result_n = max(0, n - 2)
            else:
                coeff = round(math.sqrt(n) * math.sqrt(n - 1), 4)
                result_n = n - 2
            op_str = "a^2"
            desc = f"a^2|{n}\\rangle"
        else:  # a_dag_sq
            coeff = round(math.sqrt(n + 1) * math.sqrt(n + 2), 4)
            result_n = n + 2
            op_str = "(a^\\dagger)^2"
            desc = f"(a^\\dagger)^2|{n}\\rangle"

        problem = f"compute {desc}"
        return problem, {
            "n": n, "op": op, "op_str": op_str,
            "coeff": coeff, "result_n": result_n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate ladder operator computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        n = sd["n"]
        op = sd["op"]
        steps = [f"initial state: |{n}\\rangle"]

        if op == "a":
            if n == 0:
                steps.append("a|0> = 0 (vacuum)")
            else:
                steps.append(f"a|{n}> = sqrt({n})|{n - 1}> = {_fmt(sd['coeff'])}|{n - 1}>")
        elif op == "a_dag":
            steps.append(f"a^+|{n}> = sqrt({n + 1})|{n + 1}> = {_fmt(sd['coeff'])}|{n + 1}>")
        elif op == "N":
            steps.append(f"a^+a|{n}> = {n}|{n}>")
        elif op == "a_sq":
            if n <= 1:
                steps.append(f"a^2|{n}> = 0")
            else:
                steps.append(f"a|{n}> = sqrt({n})|{n - 1}>")
                steps.append(f"a(sqrt({n})|{n - 1}>) = sqrt({n})*sqrt({n - 1})|{n - 2}>")
                steps.append(f"= {_fmt(sd['coeff'])}|{n - 2}>")
        else:  # a_dag_sq
            steps.append(f"a^+|{n}> = sqrt({n + 1})|{n + 1}>")
            steps.append(
                f"a^+(sqrt({n + 1})|{n + 1}>) = "
                f"sqrt({n + 1})*sqrt({n + 2})|{n + 2}>"
            )
            steps.append(f"= {_fmt(sd['coeff'])}|{n + 2}>")

        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the result of the ladder operator action.

        Args:
            sd: Solution data.

        Returns:
            Coefficient and resulting state.
        """
        if sd["coeff"] == 0.0:
            return "0"
        return f"{_fmt(sd['coeff'])}|{sd['result_n']}>"


# ===================================================================
# 4. Hydrogen Orbitals  (tier 5)
# ===================================================================

@register
class HydrogenOrbitalsGenerator(StepGenerator):
    """Compute hydrogen orbital properties from quantum numbers.

    Radial nodes = n - l - 1.  Angular nodes = l.  Total nodes = n - 1.
    Degeneracy of level n is n^2 (ignoring spin) or 2n^2 (with spin).
    Energy: E_n = -13.6 / n^2 eV.

    Difficulty scaling:
        Difficulty 1-3: n in [1, 3], compute nodes and energy.
        Difficulty 4-6: n in [1, 5], include degeneracy.
        Difficulty 7-8: n in [1, 7], full orbital characterisation.

    Prerequisites:
        hydrogen_energy.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hydrogen_orbitals"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hydrogen_energy"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute hydrogen orbital properties"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a hydrogen orbital properties problem.

        Args:
            difficulty: Controls n range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(1, 3)
        elif difficulty <= 6:
            n = self._rng.randint(1, 5)
        else:
            n = self._rng.randint(1, 7)

        l_val = self._rng.randint(0, n - 1)
        radial_nodes = n - l_val - 1
        angular_nodes = l_val
        total_nodes = n - 1
        degeneracy = n * n
        degeneracy_spin = 2 * n * n
        energy = round(-13.6 / (n * n), 4)

        orbital_letters = {0: "s", 1: "p", 2: "d", 3: "f", 4: "g", 5: "h", 6: "i"}
        letter = orbital_letters.get(l_val, f"l={l_val}")
        problem = f"n={n}, l={l_val} ({n}{letter})"

        return problem, {
            "n": n, "l": l_val, "letter": letter,
            "radial_nodes": radial_nodes,
            "angular_nodes": angular_nodes,
            "total_nodes": total_nodes,
            "degeneracy": degeneracy,
            "degeneracy_spin": degeneracy_spin,
            "energy": energy,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate hydrogen orbital computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"n={sd['n']}, l={sd['l']} ({sd['n']}{sd['letter']})",
            f"radial nodes = n-l-1 = {sd['n']}-{sd['l']}-1 = {sd['radial_nodes']}",
            f"angular nodes = l = {sd['angular_nodes']}",
            f"total nodes = n-1 = {sd['total_nodes']}",
            f"degeneracy = n^2 = {sd['degeneracy']} (2n^2 = {sd['degeneracy_spin']} with spin)",
            f"E_{sd['n']} = -13.6/{sd['n']}^2 = {_fmt(sd['energy'])} eV",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the orbital properties.

        Args:
            sd: Solution data.

        Returns:
            Summary of nodes, degeneracy, and energy.
        """
        return (
            f"nodes={sd['total_nodes']}, "
            f"degeneracy={sd['degeneracy']}, "
            f"E={_fmt(sd['energy'])} eV"
        )


# ===================================================================
# 5. Spin-1/2 Rotations  (tier 5)
# ===================================================================

@register
class SpinHalfGenerator(StepGenerator):
    """Compute spin-1/2 rotation using Pauli matrices.

    Rotation operator: R_n(theta) = cos(theta/2)*I - i*sin(theta/2)*sigma_n.
    Apply to |up> = (1,0) or |down> = (0,1) along x, y, or z axis.
    Eigenvalues of sigma_n are +/-1, corresponding to +/-hbar/2.

    Difficulty scaling:
        Difficulty 1-3: rotation about z-axis, simple angles (pi/2, pi).
        Difficulty 4-6: rotation about x or y, various angles.
        Difficulty 7-8: arbitrary axis angles, compute expectation values.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spin_half"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute spin-1/2 state after rotation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spin-1/2 rotation problem.

        Args:
            difficulty: Controls axis choice and angle complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        angles = [math.pi / 4, math.pi / 3, math.pi / 2, math.pi,
                   2 * math.pi / 3]
        angle_names = ["pi/4", "pi/3", "pi/2", "pi", "2pi/3"]

        if difficulty <= 3:
            axis = "z"
            idx = self._rng.choice([2, 3])  # pi/2 or pi
        elif difficulty <= 6:
            axis = self._rng.choice(["x", "y"])
            idx = self._rng.randint(0, 4)
        else:
            axis = self._rng.choice(["x", "y", "z"])
            idx = self._rng.randint(0, 4)

        theta = angles[idx]
        theta_name = angle_names[idx]
        initial = self._rng.choice(["up", "down"])

        cos_half = round(math.cos(theta / 2), 4)
        sin_half = round(math.sin(theta / 2), 4)

        # Compute rotated state components
        if initial == "up":
            a0, a1 = 1.0, 0.0
        else:
            a0, a1 = 0.0, 1.0

        if axis == "z":
            # R_z = [[cos-i*sin, 0], [0, cos+i*sin]]
            r0_re = round(cos_half * a0, 4)
            r0_im = round(-sin_half * a0, 4)
            r1_re = round(cos_half * a1, 4)
            r1_im = round(sin_half * a1, 4)
        elif axis == "x":
            # R_x = [[cos, -i*sin], [-i*sin, cos]]
            r0_re = round(cos_half * a0, 4)
            r0_im = round(-sin_half * a1, 4)
            r1_re = round(cos_half * a1, 4)
            r1_im = round(-sin_half * a0, 4)
        else:  # y
            # R_y = [[cos, -sin], [sin, cos]]
            r0_re = round(cos_half * a0 - sin_half * a1, 4)
            r0_im = 0.0
            r1_re = round(sin_half * a0 + cos_half * a1, 4)
            r1_im = 0.0

        prob_up = round(r0_re ** 2 + r0_im ** 2, 4)
        prob_down = round(r1_re ** 2 + r1_im ** 2, 4)

        problem = (
            f"rotate |{initial}> about {axis}-axis by theta={theta_name}"
        )
        return problem, {
            "axis": axis, "theta_name": theta_name,
            "initial": initial,
            "cos_half": cos_half, "sin_half": sin_half,
            "r0_re": r0_re, "r0_im": r0_im,
            "r1_re": r1_re, "r1_im": r1_im,
            "prob_up": prob_up, "prob_down": prob_down,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate spin rotation computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"axis={sd['axis']}, theta={sd['theta_name']}, |{sd['initial']}>",
            f"cos(theta/2) = {_fmt(sd['cos_half'])}, sin(theta/2) = {_fmt(sd['sin_half'])}",
            f"rotated: ({_fmt(sd['r0_re'])}+{_fmt(sd['r0_im'])}i, "
            f"{_fmt(sd['r1_re'])}+{_fmt(sd['r1_im'])}i)",
            f"P(up) = {_fmt(sd['prob_up'])}, P(down) = {_fmt(sd['prob_down'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rotated state and probabilities.

        Args:
            sd: Solution data.

        Returns:
            Rotated state components and measurement probabilities.
        """
        return (
            f"P(up)={_fmt(sd['prob_up'])}, "
            f"P(down)={_fmt(sd['prob_down'])}"
        )


# ===================================================================
# 6. Wigner-Eckart Theorem  (tier 7)
# ===================================================================

@register
class WignerEckartGenerator(StepGenerator):
    """Apply selection rules from the Wigner-Eckart theorem.

    <j'm'|T^k_q|jm> is nonzero only if |j-k| <= j' <= j+k and m'=m+q.
    Given j, m, k, q, determine allowed j' and m' values.

    Difficulty scaling:
        Difficulty 1-3: k=1 (dipole), small j.
        Difficulty 4-6: k=1 or k=2, medium j.
        Difficulty 7-8: k=2 or k=3, larger j values.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wigner_eckart"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "apply Wigner-Eckart selection rules"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Wigner-Eckart selection rule problem.

        Args:
            difficulty: Controls tensor rank and angular momentum.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = 1
            j = self._rng.randint(0, 2)
        elif difficulty <= 6:
            k = self._rng.choice([1, 2])
            j = self._rng.randint(1, 4)
        else:
            k = self._rng.choice([2, 3])
            j = self._rng.randint(2, 5)

        m = self._rng.randint(-j, j)
        q = self._rng.randint(-k, k)
        m_prime = m + q

        j_min = abs(j - k)
        j_max = j + k
        allowed_j = list(range(j_min, j_max + 1))

        # Filter: j' must satisfy |m'| <= j'
        valid_j = [jp for jp in allowed_j if abs(m_prime) <= jp]

        problem = f"<j'm'|T^{k}_{q}|j={j},m={m}>"
        return problem, {
            "j": j, "m": m, "k": k, "q": q,
            "m_prime": m_prime, "j_min": j_min, "j_max": j_max,
            "allowed_j": allowed_j, "valid_j": valid_j,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate Wigner-Eckart selection rule steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"j={sd['j']}, m={sd['m']}, k={sd['k']}, q={sd['q']}",
            f"m' = m + q = {sd['m']} + {sd['q']} = {sd['m_prime']}",
            f"|j-k| <= j' <= j+k: {sd['j_min']} <= j' <= {sd['j_max']}",
            f"allowed j': {sd['allowed_j']}",
            f"valid j' (|m'|<=j'): {sd['valid_j']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the allowed transitions.

        Args:
            sd: Solution data.

        Returns:
            Valid j' and m' values.
        """
        if not sd["valid_j"]:
            return "forbidden transition"
        j_str = ",".join(str(jp) for jp in sd["valid_j"])
        return f"j'={{{j_str}}}, m'={sd['m_prime']}"


# ===================================================================
# 7. Variational Method  (tier 6)
# ===================================================================

@register
class VariationalMethodGenerator(StepGenerator):
    """Estimate ground-state energy using the variational method.

    For a trial wavefunction with parameter alpha applied to a given
    Hamiltonian, compute E_trial = <psi|H|psi>/<psi|psi> and find
    the optimal alpha.  Uses harmonic oscillator H = p^2/2m + kx^2/2
    with Gaussian trial psi = exp(-alpha*x^2).

    Difficulty scaling:
        Difficulty 1-3: standard HO with known result.
        Difficulty 4-6: varied spring constants.
        Difficulty 7-8: anharmonic perturbation.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "variational_method"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "estimate ground-state energy via variational method"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a variational method problem.

        For Gaussian trial on HO: E(alpha) = hbar^2*alpha/(2m) + k/(8*alpha).
        Minimise: dE/dalpha = 0 => alpha_opt = sqrt(mk)/(2*hbar).
        Using hbar=m=1: E(alpha) = alpha/2 + k/(8*alpha).
        alpha_opt = sqrt(k)/2, E_min = sqrt(k)/2.

        Args:
            difficulty: Controls spring constant range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            k = self._rng.choice([1, 2, 4])
        elif difficulty <= 6:
            k = self._rng.choice([1, 2, 3, 4, 5, 8])
        else:
            k = round(self._rng.uniform(0.5, 10.0), 2)

        # hbar = m = 1
        # E(alpha) = alpha/2 + k/(8*alpha)
        # dE/dalpha = 1/2 - k/(8*alpha^2) = 0 => alpha = sqrt(k/4) = sqrt(k)/2
        alpha_opt = round(math.sqrt(k) / 2, 4)
        e_min = round(alpha_opt / 2 + k / (8 * alpha_opt), 4)
        # Exact HO ground state: E_0 = hbar*omega/2 = sqrt(k/m)/2 = sqrt(k)/2
        e_exact = round(math.sqrt(k) / 2, 4)

        problem = (
            f"H = p^2/2 + {_fmt(k)}x^2/2, "
            f"trial: psi = exp(-alpha*x^2), hbar=m=1"
        )
        return problem, {
            "k": k, "alpha_opt": alpha_opt,
            "e_min": e_min, "e_exact": e_exact,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate variational method computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"E(alpha) = alpha/2 + {_fmt(sd['k'])}/(8*alpha)",
            f"dE/dalpha = 1/2 - {_fmt(sd['k'])}/(8*alpha^2) = 0",
            f"alpha_opt = sqrt({_fmt(sd['k'])})/2 = {_fmt(sd['alpha_opt'])}",
            f"E_min = {_fmt(sd['e_min'])}",
            f"E_exact = sqrt({_fmt(sd['k'])})/2 = {_fmt(sd['e_exact'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the variational energy estimate.

        Args:
            sd: Solution data.

        Returns:
            Optimal alpha and minimum energy.
        """
        return (
            f"alpha_opt={_fmt(sd['alpha_opt'])}, "
            f"E_min={_fmt(sd['e_min'])}"
        )


# ===================================================================
# 8. Degenerate Perturbation Theory  (tier 7)
# ===================================================================

@register
class DegeneratePerturbationGenerator(StepGenerator):
    """Diagonalise perturbation in a degenerate subspace.

    For 2-fold degeneracy, form the 2x2 perturbation matrix W with
    W_{ij} = <i|H'|j>, then find its eigenvalues to get first-order
    energy corrections.

    Difficulty scaling:
        Difficulty 1-3: diagonal W (trivial diagonalisation).
        Difficulty 4-6: symmetric W with integer entries.
        Difficulty 7-8: complex off-diagonal elements.

    Prerequisites:
        eigenvalue.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "degenerate_perturbation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["eigenvalue"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "find energy corrections via degenerate perturbation theory"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a degenerate perturbation theory problem.

        Args:
            difficulty: Controls matrix complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            w11 = self._rng.randint(-3, 3)
            w22 = self._rng.randint(-3, 3)
            w12 = 0
        elif difficulty <= 6:
            w11 = self._rng.randint(-5, 5)
            w22 = self._rng.randint(-5, 5)
            w12 = self._rng.randint(-4, 4)
        else:
            w11 = self._rng.randint(-8, 8)
            w22 = self._rng.randint(-8, 8)
            w12 = self._rng.randint(-6, 6)

        # Eigenvalues of [[w11, w12], [w12, w22]]
        trace = w11 + w22
        det = w11 * w22 - w12 * w12
        discriminant = trace * trace - 4 * det
        sqrt_disc = round(math.sqrt(max(0, discriminant)), 4)
        e1 = round((trace - sqrt_disc) / 2, 4)
        e2 = round((trace + sqrt_disc) / 2, 4)

        problem = (
            f"W = [[{w11}, {w12}], [{w12}, {w22}]]; "
            f"find first-order energy corrections"
        )
        return problem, {
            "w11": w11, "w22": w22, "w12": w12,
            "trace": trace, "det": det,
            "discriminant": discriminant,
            "sqrt_disc": sqrt_disc,
            "e1": e1, "e2": e2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate perturbation theory computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"W = [[{sd['w11']}, {sd['w12']}], [{sd['w12']}, {sd['w22']}]]",
            f"tr(W) = {sd['trace']}, det(W) = {sd['det']}",
            f"discriminant = {sd['trace']}^2 - 4*{sd['det']} = {_fmt(sd['discriminant'])}",
            f"sqrt(disc) = {_fmt(sd['sqrt_disc'])}",
            f"E1' = ({sd['trace']} - {_fmt(sd['sqrt_disc'])})/2 = {_fmt(sd['e1'])}",
            f"E2' = ({sd['trace']} + {_fmt(sd['sqrt_disc'])})/2 = {_fmt(sd['e2'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the first-order energy corrections.

        Args:
            sd: Solution data.

        Returns:
            Energy correction eigenvalues.
        """
        return f"E1'={_fmt(sd['e1'])}, E2'={_fmt(sd['e2'])}"


# ===================================================================
# 9. Scattering Cross Section  (tier 6)
# ===================================================================

@register
class ScatteringCrossSectionGenerator(StepGenerator):
    """Compute scattering cross sections in quantum mechanics.

    For s-wave scattering: f_0 = -a (scattering length),
    sigma = 4*pi*a^2.  For partial-wave sum up to l_max:
    sigma = (4*pi/k^2) * sum (2l+1)*sin^2(delta_l).

    Difficulty scaling:
        Difficulty 1-3: s-wave only, compute sigma = 4*pi*a^2.
        Difficulty 4-6: s-wave + p-wave, sum two partial waves.
        Difficulty 7-8: up to l=2 (d-wave), three partial waves.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "scattering_cross_section"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute quantum scattering cross section"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a scattering cross section problem.

        Args:
            difficulty: Controls number of partial waves.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            l_max = 0
        elif difficulty <= 6:
            l_max = 1
        else:
            l_max = 2

        # Scattering length / wave number
        a = round(self._rng.uniform(0.5, 5.0), 2)
        k = round(self._rng.uniform(0.1, 2.0), 2)

        # Phase shifts for each l
        phase_shifts = []
        for l_val in range(l_max + 1):
            if l_val == 0:
                delta = round(self._rng.uniform(0.1, 1.5), 4)
            else:
                # Higher l typically has smaller phase shift
                delta = round(self._rng.uniform(0.01, 0.5), 4)
            phase_shifts.append(delta)

        # Partial wave contributions
        contributions = []
        for l_val, delta in enumerate(phase_shifts):
            sin_sq = round(math.sin(delta) ** 2, 4)
            contrib = round((2 * l_val + 1) * sin_sq, 4)
            contributions.append(contrib)

        total_sum = round(sum(contributions), 4)
        sigma = round(4 * math.pi / (k * k) * total_sum, 4)

        # Also compute s-wave approximation
        sigma_swave = round(4 * math.pi * a * a, 4)

        if l_max == 0:
            problem = f"s-wave: a={_fmt(a)}, k={_fmt(k)}"
        else:
            deltas_str = ", ".join(
                f"delta_{l}={_fmt(d)}" for l, d in enumerate(phase_shifts)
            )
            problem = f"k={_fmt(k)}, {deltas_str}"

        return problem, {
            "a": a, "k": k, "l_max": l_max,
            "phase_shifts": phase_shifts,
            "contributions": contributions,
            "total_sum": total_sum,
            "sigma": sigma, "sigma_swave": sigma_swave,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate scattering cross section computation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"k = {_fmt(sd['k'])}, l_max = {sd['l_max']}"]

        if sd["l_max"] == 0:
            steps.append(
                f"s-wave: sigma = 4*pi*a^2 = "
                f"4*pi*{_fmt(sd['a'])}^2 = {_fmt(sd['sigma_swave'])}"
            )
        else:
            for l_val in range(sd["l_max"] + 1):
                d = sd["phase_shifts"][l_val]
                sin_sq = round(math.sin(d) ** 2, 4)
                steps.append(
                    f"l={l_val}: sin^2(delta_{l_val}) = {_fmt(sin_sq)}, "
                    f"(2l+1)*sin^2 = {_fmt(sd['contributions'][l_val])}"
                )
            steps.append(f"sum = {_fmt(sd['total_sum'])}")
            steps.append(
                f"sigma = 4*pi/k^2 * sum = {_fmt(sd['sigma'])}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the cross section.

        Args:
            sd: Solution data.

        Returns:
            Cross section value.
        """
        if sd["l_max"] == 0:
            return f"sigma = {_fmt(sd['sigma_swave'])}"
        return f"sigma = {_fmt(sd['sigma'])}"


# ===================================================================
# 10. WKB Approximation  (tier 6)
# ===================================================================

@register
class WKBApproximationGenerator(StepGenerator):
    """Apply the WKB (Bohr-Sommerfeld) quantisation condition.

    Phase integral: integral p(x) dx = (n + 1/2)*pi*hbar over one
    period.  For harmonic oscillator V = kx^2/2 with energy E:
    turning points at +/- sqrt(2E/k).  Integral yields
    E_n = (n + 1/2)*hbar*omega.  Uses hbar = 1, m = 1.

    Difficulty scaling:
        Difficulty 1-3: harmonic oscillator, small n.
        Difficulty 4-6: varied spring constants, medium n.
        Difficulty 7-8: large n, verify against exact result.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wkb_approximation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "apply WKB quantisation to harmonic oscillator"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a WKB approximation problem.

        For HO: E_n = (n+1/2)*omega, omega = sqrt(k/m) = sqrt(k).
        Turning points: x_tp = +/- sqrt(2*E_n / k).

        Args:
            difficulty: Controls quantum number and spring constant.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = self._rng.randint(0, 3)
            k = self._rng.choice([1, 2, 4])
        elif difficulty <= 6:
            n = self._rng.randint(0, 8)
            k = self._rng.choice([1, 2, 3, 4, 5, 8])
        else:
            n = self._rng.randint(0, 20)
            k = round(self._rng.uniform(0.5, 10.0), 2)

        omega = round(math.sqrt(k), 4)
        e_n = round((n + 0.5) * omega, 4)
        x_tp = round(math.sqrt(2 * e_n / k), 4) if k > 0 else 0.0

        problem = f"V = {_fmt(k)}x^2/2, hbar=m=1, find E_{n} via WKB"
        return problem, {
            "n": n, "k": k, "omega": omega,
            "e_n": e_n, "x_tp": x_tp,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate WKB quantisation steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"omega = sqrt(k/m) = sqrt({_fmt(sd['k'])}) = {_fmt(sd['omega'])}",
            f"Bohr-Sommerfeld: E_n = (n+1/2)*omega",
            f"n = {sd['n']}, E_{sd['n']} = ({sd['n']}+0.5)*{_fmt(sd['omega'])} = {_fmt(sd['e_n'])}",
            f"turning points: x = +/-{_fmt(sd['x_tp'])}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the WKB energy and turning points.

        Args:
            sd: Solution data.

        Returns:
            Energy and turning point values.
        """
        return (
            f"E_{sd['n']}={_fmt(sd['e_n'])}, "
            f"x_tp=+/-{_fmt(sd['x_tp'])}"
        )
