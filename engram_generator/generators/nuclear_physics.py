"""Nuclear physics generators -- mass defect, binding energy, decay, reactions.

Covers mass defect and E=mc^2, binding energy per nucleon, radioactive
decay, half-life, decay chains (alpha/beta), and nuclear reaction
balancing with Q-value. All tiers are 5-6 (intermediate to advanced).
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class _NuclearFormatter:
    """Formats numeric values for nuclear physics problems.

    Provides consistent rounding and clean string representations
    to keep target text compact.
    """

    @staticmethod
    def fmt(value: float, decimals: int = 4) -> str:
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


_f = _NuclearFormatter.fmt

# Physical constants
_MP = 1.007276  # proton mass (u)
_MN = 1.008665  # neutron mass (u)
_C2_MEV = 931.5  # c^2 in MeV/u


# ===================================================================
# 1. Mass defect  (tier 5)
# ===================================================================

@register
class MassDefectGenerator(StepGenerator):
    """Mass defect: dm = Z*mp + N*mn - M_atom, E = dm * 931.5 MeV/u.

    Computes the mass defect and corresponding binding energy
    for a nucleus with Z protons and N neutrons.

    Difficulty scaling:
        Difficulty 1-3: light nuclei (He-4, Li-7, C-12).
        Difficulty 4-6: medium nuclei (Fe-56, Ni-62).
        Difficulty 7-8: heavy nuclei (U-235, Pu-239).

    Prerequisites:
        subtraction, multiplication.
    """

    _NUCLEI = {
        "He-4": (2, 2, 4.002602),
        "Li-7": (3, 4, 7.016003),
        "C-12": (6, 6, 12.0),
        "N-14": (7, 7, 14.003074),
        "O-16": (8, 8, 15.994915),
        "Fe-56": (26, 30, 55.934937),
        "Ni-62": (28, 34, 61.928345),
        "Cu-63": (29, 34, 62.929598),
        "U-235": (92, 143, 235.043930),
        "U-238": (92, 146, 238.050788),
        "Pu-239": (94, 145, 239.052163),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mass_defect"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute mass defect and binding energy"

    def _select_nucleus(self, difficulty: int) -> tuple[str, int, int, float]:
        """Select a nucleus appropriate for the difficulty level.

        Args:
            difficulty: Controls nucleus complexity.

        Returns:
            Tuple of (name, Z, N, atomic_mass).
        """
        names = list(self._NUCLEI.keys())
        if difficulty <= 3:
            pool = names[:5]
        elif difficulty <= 6:
            pool = names[:8]
        else:
            pool = names
        name = self._rng.choice(pool)
        z, n, m = self._NUCLEI[name]
        return name, z, n, m

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate mass defect problem for a chosen nucleus.

        Args:
            difficulty: Controls nucleus selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        name, z, n, m_atom = self._select_nucleus(difficulty)
        constituents = round(z * _MP + n * _MN, 4)
        dm = round(constituents - m_atom, 4)
        be = round(dm * _C2_MEV, 4)

        return "\\Delta m = Z m_p + N m_n - M, E = \\Delta m c^2", {
            "name": name, "Z": z, "N": n, "A": z + n,
            "M": m_atom, "constituents": constituents,
            "dm": dm, "BE": be,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate mass defect computation steps.

        Args:
            data: Solution data with Z, N, masses.

        Returns:
            List of step strings.
        """
        return [
            f"{data['name']}: Z={data['Z']}, N={data['N']}, "
            f"A={data['A']}",
            f"Z*mp + N*mn = {data['Z']}*{_MP} + {data['N']}*{_MN}"
            f" = {_f(data['constituents'])} u",
            f"dm = {_f(data['constituents'])} - {data['M']}"
            f" = {_f(data['dm'])} u",
            f"E = {_f(data['dm'])}*{_C2_MEV}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the mass defect and binding energy.

        Args:
            data: Solution data.

        Returns:
            String with dm and BE.
        """
        return f"dm = {_f(data['dm'])} u, BE = {_f(data['BE'])} MeV"


# ===================================================================
# 2. Binding energy per nucleon  (tier 5)
# ===================================================================

@register
class BindingEnergyPerNucleonGenerator(StepGenerator):
    """Binding energy per nucleon: BE/A from mass defect.

    First computes the total binding energy via the mass defect,
    then divides by the mass number A.

    Difficulty scaling:
        Difficulty 1-3: light nuclei.
        Difficulty 4-6: medium nuclei near Fe-56 peak.
        Difficulty 7-8: heavy nuclei.

    Prerequisites:
        mass_defect.
    """

    _NUCLEI = MassDefectGenerator._NUCLEI

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "binding_energy_per_nucleon"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mass_defect"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute binding energy per nucleon"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate BE/A problem for a chosen nucleus.

        Args:
            difficulty: Controls nucleus selection.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        names = list(self._NUCLEI.keys())
        if difficulty <= 3:
            pool = names[:5]
        elif difficulty <= 6:
            pool = names[:8]
        else:
            pool = names
        name = self._rng.choice(pool)
        z, n, m_atom = self._NUCLEI[name]
        a = z + n

        dm = round(z * _MP + n * _MN - m_atom, 4)
        be = round(dm * _C2_MEV, 4)
        be_per_a = round(be / a, 4)

        return "BE/A = \\frac{\\Delta m \\cdot c^2}{A}", {
            "name": name, "Z": z, "N": n, "A": a,
            "M": m_atom, "dm": dm, "BE": be,
            "BE_per_A": be_per_a,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate BE/A computation steps.

        Args:
            data: Solution data with mass defect and A.

        Returns:
            List of step strings.
        """
        return [
            f"{data['name']}: Z={data['Z']}, N={data['N']}, A={data['A']}",
            f"dm = {_f(data['dm'])} u",
            f"BE = {_f(data['dm'])}*{_C2_MEV} = {_f(data['BE'])} MeV",
            f"BE/A = {_f(data['BE'])}/{data['A']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the binding energy per nucleon.

        Args:
            data: Solution data.

        Returns:
            String with BE/A value.
        """
        return f"BE/A = {_f(data['BE_per_A'])} MeV/nucleon"


# ===================================================================
# 3. Radioactive decay  (tier 5)
# ===================================================================

@register
class RadioactiveDecayGenerator(StepGenerator):
    """Radioactive decay: N(t) = N0 * exp(-lambda * t).

    Computes the number of remaining nuclei or the activity
    after a given time.

    Difficulty scaling:
        Difficulty 1-3: compute N(t) given N0, lambda, t.
        Difficulty 4-6: compute activity A(t) = lambda*N(t).
        Difficulty 7-8: find time for N(t)/N0 to reach a target fraction.

    Prerequisites:
        exponentiation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "radioactive_decay"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute radioactive decay"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate radioactive decay parameters.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n0 = self._rng.randint(1000, 10000 + difficulty * 5000)
        half_life = round(self._rng.uniform(1.0, 100.0 + difficulty * 50), 1)
        lam = round(math.log(2) / half_life, 4)
        t = round(self._rng.uniform(0.5, 3.0) * half_life, 1)
        n_t = round(n0 * math.exp(-lam * t), 4)
        activity = round(lam * n_t, 4)

        if difficulty <= 3:
            target = "N"
        elif difficulty <= 6:
            target = "activity"
        else:
            fraction = round(self._rng.uniform(0.1, 0.5), 2)
            t_frac = round(-math.log(fraction) / lam, 4)
            return "N(t) = N_0 e^{-\\lambda t}", {
                "N0": n0, "half_life": half_life, "lambda": lam,
                "t": t_frac, "fraction": fraction,
                "N_t": round(n0 * fraction, 4),
                "target": "time",
            }

        return "N(t) = N_0 e^{-\\lambda t}", {
            "N0": n0, "half_life": half_life, "lambda": lam,
            "t": t, "N_t": n_t, "activity": activity,
            "target": target,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate radioactive decay computation steps.

        Args:
            data: Solution data with N0, lambda, t.

        Returns:
            List of step strings.
        """
        target = data["target"]
        if target == "N":
            exp_val = round(-data["lambda"] * data["t"], 4)
            return [
                f"N0={data['N0']}, lambda={_f(data['lambda'])}/s, "
                f"t={data['t']}s",
                f"-lambda*t = {_f(exp_val)}",
                f"N(t) = {data['N0']}*e^{{{_f(exp_val)}}}",
            ]
        if target == "activity":
            exp_val = round(-data["lambda"] * data["t"], 4)
            return [
                f"N0={data['N0']}, lambda={_f(data['lambda'])}/s, "
                f"t={data['t']}s",
                f"N(t) = {data['N0']}*e^{{{_f(exp_val)}}}"
                f" = {_f(data['N_t'])}",
                f"A(t) = lambda*N(t) = {_f(data['lambda'])}*{_f(data['N_t'])}",
            ]
        # target == "time"
        return [
            f"N0={data['N0']}, lambda={_f(data['lambda'])}/s, "
            f"fraction={data['fraction']}",
            f"N/N0 = {data['fraction']} => -lambda*t = ln({data['fraction']})",
            f"t = -ln({data['fraction']})/lambda",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the decay result.

        Args:
            data: Solution data.

        Returns:
            String with the appropriate result and units.
        """
        target = data["target"]
        if target == "N":
            return f"N(t) = {_f(data['N_t'])}"
        if target == "activity":
            return f"A(t) = {_f(data['activity'])} decays/s"
        return f"t = {_f(data['t'])} s"


# ===================================================================
# 4. Half-life  (tier 5)
# ===================================================================

@register
class HalfLifeGenerator(StepGenerator):
    """Half-life: t_half = ln(2) / lambda.

    Converts between half-life and decay constant. Can also
    compute the number of half-lives elapsed.

    Difficulty scaling:
        Difficulty 1-3: given lambda, find t_half.
        Difficulty 4-6: given t_half, find lambda.
        Difficulty 7-8: given N0 and N(t), find number of half-lives.

    Prerequisites:
        logarithm.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "half_life"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "convert between half-life and decay constant"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate half-life conversion problem.

        Args:
            difficulty: Controls problem variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        half_life = round(self._rng.uniform(1.0, 1000.0 + difficulty * 500), 2)
        lam = round(math.log(2) / half_life, 4)

        if difficulty <= 3:
            return "t_{1/2} = \\frac{\\ln 2}{\\lambda}", {
                "half_life": half_life, "lambda": lam,
                "target": "t_half",
            }
        if difficulty <= 6:
            return "\\lambda = \\frac{\\ln 2}{t_{1/2}}", {
                "half_life": half_life, "lambda": lam,
                "target": "lambda",
            }
        # Number of half-lives
        n0 = self._rng.randint(1000, 100000)
        num_halves = self._rng.randint(1, 6)
        n_t = round(n0 / (2 ** num_halves), 4)
        t = round(num_halves * half_life, 4)
        return "N(t) = N_0 (1/2)^{t/t_{1/2}}", {
            "half_life": half_life, "lambda": lam,
            "N0": n0, "N_t": n_t, "num_halves": num_halves,
            "t": t, "target": "num_halves",
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate half-life computation steps.

        Args:
            data: Solution data with half-life and lambda.

        Returns:
            List of step strings.
        """
        target = data["target"]
        ln2 = round(math.log(2), 4)
        if target == "t_half":
            return [
                f"lambda = {_f(data['lambda'])}/s",
                f"t_{{1/2}} = ln(2)/lambda = {_f(ln2)}/{_f(data['lambda'])}",
            ]
        if target == "lambda":
            return [
                f"t_{{1/2}} = {_f(data['half_life'])} s",
                f"lambda = ln(2)/t_{{1/2}} = {_f(ln2)}/{_f(data['half_life'])}",
            ]
        # num_halves
        return [
            f"N0={data['N0']}, N(t)={_f(data['N_t'])}, "
            f"t_{{1/2}}={_f(data['half_life'])}s",
            f"N/N0 = {_f(data['N_t'])}/{data['N0']}"
            f" = 1/2^{data['num_halves']}",
            f"t = {data['num_halves']}*{_f(data['half_life'])}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the half-life, decay constant, or elapsed time.

        Args:
            data: Solution data.

        Returns:
            String with the computed result.
        """
        target = data["target"]
        if target == "t_half":
            return f"t_{{1/2}} = {_f(data['half_life'])} s"
        if target == "lambda":
            return f"lambda = {_f(data['lambda'])}/s"
        return f"n = {data['num_halves']} half-lives, t = {_f(data['t'])} s"


# ===================================================================
# 5. Decay chain  (tier 5)
# ===================================================================

@register
class DecayChainGenerator(StepGenerator):
    """Decay chain: track Z, A through alpha and beta decays.

    Alpha decay: Z -> Z-2, A -> A-4.
    Beta-minus decay: Z -> Z+1, A -> A (neutron to proton).
    Generates a random sequence of decays and tracks the resulting
    nucleus.

    Difficulty scaling:
        Difficulty 1-3: 1-2 decay steps.
        Difficulty 4-6: 3-4 decay steps.
        Difficulty 7-8: 5-6 decay steps.

    Prerequisites:
        subtraction.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "decay_chain"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "track nuclear decay chain"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a decay chain starting from a heavy nucleus.

        Args:
            difficulty: Controls number of decay steps.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        z = self._rng.randint(82, 94)
        a = z + self._rng.randint(z + 40, z + 50)  # realistic N > Z

        if difficulty <= 3:
            n_steps = self._rng.randint(1, 2)
        elif difficulty <= 6:
            n_steps = self._rng.randint(3, 4)
        else:
            n_steps = self._rng.randint(5, 6)

        chain = [(z, a)]
        decays = []
        cur_z, cur_a = z, a

        for _ in range(n_steps):
            if cur_z < 3 or cur_a < 5:
                break
            if cur_a >= 8 and self._rng.random() < 0.6:
                decay_type = "alpha"
                cur_z -= 2
                cur_a -= 4
            else:
                decay_type = "beta"
                cur_z += 1
            decays.append(decay_type)
            chain.append((cur_z, cur_a))

        return "\\alpha: (Z-2,A-4), \\beta^-: (Z+1,A)", {
            "Z_init": z, "A_init": a,
            "decays": decays, "chain": chain,
            "Z_final": cur_z, "A_final": cur_a,
            "n_steps": len(decays),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate decay chain tracking steps.

        Args:
            data: Solution data with initial nucleus and decay sequence.

        Returns:
            List of step strings.
        """
        steps = [f"start: Z={data['Z_init']}, A={data['A_init']}"]
        chain = data["chain"]
        decays = data["decays"]
        for i, decay in enumerate(decays):
            z_prev, a_prev = chain[i]
            z_next, a_next = chain[i + 1]
            steps.append(
                f"{decay}: ({z_prev},{a_prev}) -> ({z_next},{a_next})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final nucleus after all decays.

        Args:
            data: Solution data.

        Returns:
            String with final Z and A.
        """
        return f"Z = {data['Z_final']}, A = {data['A_final']}"


# ===================================================================
# 6. Nuclear reaction Q-value  (tier 6)
# ===================================================================

@register
class NuclearReactionGenerator(StepGenerator):
    """Nuclear reaction: balance and compute Q = (m_react - m_prod) * c^2.

    Generates a nuclear reaction, checks that Z and A are conserved,
    and computes the Q-value (energy released or absorbed).

    Difficulty scaling:
        Difficulty 1-3: simple reactions (e.g., D-T fusion).
        Difficulty 4-6: fission fragments.
        Difficulty 7-8: multi-body reactions, compute threshold energy.

    Prerequisites:
        mass_defect.
    """

    _REACTIONS = [
        # (name, reactants, products, m_react, m_prod)
        ("D-T_fusion",
         [("H-2", 1, 2, 2.014102), ("H-3", 1, 3, 3.016049)],
         [("He-4", 2, 4, 4.002602), ("n", 0, 1, 1.008665)]),
        ("D-D_fusion",
         [("H-2", 1, 2, 2.014102), ("H-2", 1, 2, 2.014102)],
         [("He-3", 2, 3, 3.016029), ("n", 0, 1, 1.008665)]),
        ("p-Li7",
         [("p", 1, 1, 1.007276), ("Li-7", 3, 7, 7.016003)],
         [("He-4", 2, 4, 4.002602), ("He-4", 2, 4, 4.002602)]),
        ("C-12_p_cap",
         [("C-12", 6, 12, 12.0), ("p", 1, 1, 1.007276)],
         [("N-13", 7, 13, 13.005739)]),
        ("U235_fission",
         [("U-235", 92, 235, 235.043930), ("n", 0, 1, 1.008665)],
         [("Ba-141", 56, 141, 140.914411), ("Kr-92", 36, 92, 91.926156),
          ("n", 0, 1, 1.008665), ("n", 0, 1, 1.008665),
          ("n", 0, 1, 1.008665)]),
        ("B-10_n",
         [("B-10", 5, 10, 10.012937), ("n", 0, 1, 1.008665)],
         [("Li-7", 3, 7, 7.016003), ("He-4", 2, 4, 4.002602)]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nuclear_reaction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["mass_defect"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "balance nuclear reaction and compute Q-value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nuclear reaction problem.

        Args:
            difficulty: Controls reaction complexity.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            pool = self._REACTIONS[:3]
        elif difficulty <= 6:
            pool = self._REACTIONS[:5]
        else:
            pool = self._REACTIONS

        name, reactants, products = self._rng.choice(pool)

        m_react = round(sum(p[3] for p in reactants), 4)
        m_prod = round(sum(p[3] for p in products), 4)
        dm = round(m_react - m_prod, 4)
        q = round(dm * _C2_MEV, 4)

        z_react = sum(p[1] for p in reactants)
        a_react = sum(p[2] for p in reactants)
        z_prod = sum(p[1] for p in products)
        a_prod = sum(p[2] for p in products)

        react_str = " + ".join(p[0] for p in reactants)
        prod_str = " + ".join(p[0] for p in products)

        return f"{react_str} \\to {prod_str}", {
            "name": name,
            "reactants": [(p[0], p[1], p[2], p[3]) for p in reactants],
            "products": [(p[0], p[1], p[2], p[3]) for p in products],
            "m_react": m_react, "m_prod": m_prod, "dm": dm,
            "Q": q,
            "Z_react": z_react, "A_react": a_react,
            "Z_prod": z_prod, "A_prod": a_prod,
            "balanced": (z_react == z_prod and a_react == a_prod),
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate nuclear reaction computation steps.

        Args:
            data: Solution data with masses and Q-value.

        Returns:
            List of step strings.
        """
        steps = [
            f"check Z: {data['Z_react']} = {data['Z_prod']}, "
            f"A: {data['A_react']} = {data['A_prod']}",
            f"m_react = {_f(data['m_react'])} u",
            f"m_prod = {_f(data['m_prod'])} u",
            f"dm = {_f(data['m_react'])} - {_f(data['m_prod'])}"
            f" = {_f(data['dm'])} u",
            f"Q = {_f(data['dm'])}*{_C2_MEV}",
        ]
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Q-value and reaction type.

        Args:
            data: Solution data.

        Returns:
            String with Q-value and exothermic/endothermic label.
        """
        label = "exothermic" if data["Q"] > 0 else "endothermic"
        return f"Q = {_f(data['Q'])} MeV ({label})"
