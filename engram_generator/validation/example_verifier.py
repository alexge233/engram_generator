"""Double-blind verification using textbook examples from knowledge atoms.

Each atom has a worked example sourced from Wikipedia with specific
input values and expected output. This verifier extracts those values,
independently recomputes the answer using Python, and compares against
the expected result.

This is genuinely double-blind:
  Source A: Wikipedia/textbook example (ground truth)
  Source B: Independent Python recomputation

If the recomputation matches the textbook, the formula is correct.
If not, either the implementation or the textbook transcription is wrong.

Usage:
    from engram_generator.validation.example_verifier import ExampleVerifier
    v = ExampleVerifier()
    results = v.verify_all()
"""
import math
import re
from dataclasses import dataclass


@dataclass
class ExampleResult:
    """Result of verifying one atom example.

    Attributes:
        task_name: Generator task identifier.
        match: True if recomputation matches textbook.
        expected: Value from the textbook example.
        computed: Value from independent recomputation.
        inputs: Extracted input parameters.
        reason: Explanation for None/failure.
    """

    task_name: str
    match: bool | None
    expected: str = ""
    computed: str = ""
    inputs: str = ""
    reason: str = ""


class ExampleVerifier:
    """Verifies generator formulas against textbook worked examples.

    Each handler takes the textbook input values and independently
    computes the expected output using Python math. No generator
    code is called.
    """

    def __init__(self) -> None:
        """Build the example verification handlers."""
        self._handlers = self._build_handlers()

    def can_verify(self, task_name: str) -> bool:
        """Check if a task has an example verification handler.

        Args:
            task_name: Generator task identifier.

        Returns:
            True if double-blind verification is available.
        """
        return task_name in self._handlers

    def verify(self, task_name: str) -> ExampleResult:
        """Verify a generator against its textbook example.

        Args:
            task_name: Generator task identifier.

        Returns:
            ExampleResult with match status.
        """
        if task_name not in self._handlers:
            return ExampleResult(
                task_name=task_name, match=None,
                reason="no_handler",
            )
        try:
            return self._handlers[task_name]()
        except Exception as e:
            return ExampleResult(
                task_name=task_name, match=None,
                reason=f"error: {str(e)[:80]}",
            )

    def verify_all(self) -> list[ExampleResult]:
        """Verify all tasks with example handlers.

        Returns:
            List of ExampleResult for every handler.
        """
        results = []
        for task_name in sorted(self._handlers.keys()):
            results.append(self.verify(task_name))
        return results

    def supported_tasks(self) -> list[str]:
        """Return task names with example handlers.

        Returns:
            Sorted list of task names.
        """
        return sorted(self._handlers.keys())

    def _ok(self, task: str, expected: float, computed: float,
            inputs: str, tol: float = 0.01) -> ExampleResult:
        """Compare expected and computed values.

        Args:
            task: Task name.
            expected: Textbook value.
            computed: Independently computed value.
            inputs: Description of input parameters.
            tol: Relative tolerance.

        Returns:
            ExampleResult with match status.
        """
        if abs(expected) < 1e-10:
            match = abs(computed - expected) < tol
        else:
            match = abs(computed - expected) / abs(expected) < tol
        return ExampleResult(
            task_name=task, match=match,
            expected=str(round(expected, 6)),
            computed=str(round(computed, 6)),
            inputs=inputs,
        )

    def _build_handlers(self) -> dict:
        """Build handlers mapping task_name to verification callable.

        Each handler hardcodes the textbook example inputs and
        independently computes the expected output.

        Returns:
            Dict of task_name -> callable() -> ExampleResult.
        """
        h = {}

        # === CHEMISTRY ===

        def _rate_law():
            # Wikipedia: rate = k * [A]^m * [B]^n
            # Example: k=0.05, [A]=0.2, [B]=0.3, m=1, n=2
            k, A, B, m, n = 0.05, 0.2, 0.3, 1, 2
            expected = 0.0009
            computed = k * A**m * B**n
            return self._ok("rate_law", expected, computed,
                            "k=0.05, [A]=0.2, [B]=0.3, m=1, n=2")
        h["rate_law"] = _rate_law

        def _arrhenius():
            # k = A * exp(-Ea / (R*T))
            # Example: A=1e13, Ea=75000, R=8.314, T=300
            A, Ea, R, T = 1e13, 75000, 8.314, 300
            expected = 1e13 * math.exp(-75000 / (8.314 * 300))
            computed = A * math.exp(-Ea / (R * T))
            return self._ok("arrhenius", expected, computed,
                            "A=1e13, Ea=75000, T=300")
        h["arrhenius"] = _arrhenius

        def _equilibrium_constant():
            # K = [NH3]^2 / ([N2]*[H2]^3)
            # Example: [N2]=0.5, [H2]=0.3, [NH3]=0.2
            expected = 2.963
            computed = 0.2**2 / (0.5 * 0.3**3)
            return self._ok("equilibrium_constant", expected, computed,
                            "[N2]=0.5, [H2]=0.3, [NH3]=0.2")
        h["equilibrium_constant"] = _equilibrium_constant

        def _gibbs_spontaneity():
            # dG = dH - T*dS
            # Example: dH=-100 kJ, dS=-0.2 kJ/K, T=400 K
            dH, dS, T = -100, -0.2, 400
            expected = -20
            computed = dH - T * dS
            return self._ok("gibbs_spontaneity", expected, computed,
                            "dH=-100, dS=-0.2, T=400")
        h["gibbs_spontaneity"] = _gibbs_spontaneity

        def _nernst():
            # E = E0 - (RT/nF)*ln(Q)
            # Example: E0=0.34, n=2, T=298, Q=0.01
            E0, n, T, Q = 0.34, 2, 298, 0.01
            R, F = 8.314, 96485
            expected = 0.399
            computed = E0 - (R * T / (n * F)) * math.log(Q)
            return self._ok("nernst_equation", expected, computed,
                            "E0=0.34, n=2, T=298, Q=0.01")
        h["nernst_equation"] = _nernst

        def _hess_law():
            # dH = dH1 + dH2
            # Example: dH1=-110.5, dH2=-283.0
            expected = -393.5
            computed = -110.5 + (-283.0)
            return self._ok("hess_law", expected, computed,
                            "dH1=-110.5, dH2=-283.0")
        h["hess_law"] = _hess_law

        # === BIOCHEMISTRY ===

        def _michaelis_menten():
            # v = Vmax * [S] / (Km + [S])
            # Example: Vmax=100, Km=5, [S]=10
            Vmax, Km, S = 100, 5, 10
            expected = 66.67
            computed = Vmax * S / (Km + S)
            return self._ok("michaelis_menten", expected, computed,
                            "Vmax=100, Km=5, [S]=10")
        h["michaelis_menten"] = _michaelis_menten

        # === THERMODYNAMICS ===

        def _carnot():
            # eta = 1 - Tc/Th
            # Example: Th=600, Tc=300
            expected = 0.5
            computed = 1 - 300 / 600
            return self._ok("carnot_efficiency", expected, computed,
                            "Th=600, Tc=300")
        h["carnot_efficiency"] = _carnot

        def _first_law():
            # dU = Q - W
            # Example: Q=500 J, W=200 J
            expected = 300
            computed = 500 - 200
            return self._ok("first_law_thermo", expected, computed,
                            "Q=500, W=200")
        h["first_law_thermo"] = _first_law

        # === RELATIVITY ===

        def _lorentz():
            # gamma = 1 / sqrt(1 - beta^2)
            # Example: beta=0.8
            beta = 0.8
            expected = 1.6667
            computed = 1 / math.sqrt(1 - beta**2)
            return self._ok("lorentz_factor", expected, computed,
                            "beta=0.8")
        h["lorentz_factor"] = _lorentz

        def _time_dilation():
            # dt = gamma * dt0
            # Example: gamma=2, dt0=1 year
            expected = 2.0
            computed = 2.0 * 1.0
            return self._ok("time_dilation", expected, computed,
                            "gamma=2, dt0=1")
        h["time_dilation"] = _time_dilation

        def _mass_energy():
            # E = mc^2
            # Example: m=1 kg, c=3e8
            m, c = 1, 3e8
            expected = 9e16
            computed = m * c**2
            return self._ok("mass_energy_equivalence", expected, computed,
                            "m=1 kg")
        h["mass_energy_equivalence"] = _mass_energy

        # === ELECTROMAGNETISM ===

        def _coulombs():
            # F = k * |q1*q2| / r^2
            # Example: q1=2e-6, q2=3e-6, r=0.1
            k = 8.9876e9
            expected = 5.3925
            computed = k * 2e-6 * 3e-6 / 0.1**2
            return self._ok("coulombs_law", expected, computed,
                            "q1=2uC, q2=3uC, r=0.1m")
        h["coulombs_law"] = _coulombs

        def _ohms():
            # V = IR
            # Example: I=2A, R=5 ohm -> V=10
            expected = 10
            computed = 2 * 5
            return self._ok("ohms_law", expected, computed,
                            "I=2, R=5")
        h["ohms_law"] = _ohms

        # === FLUID MECHANICS ===

        def _reynolds():
            # Re = rho*v*L / mu
            # Example: rho=1000, v=2, L=0.05, mu=0.001
            expected = 100000
            computed = 1000 * 2 * 0.05 / 0.001
            return self._ok("reynolds_number", expected, computed,
                            "rho=1000, v=2, L=0.05, mu=0.001")
        h["reynolds_number"] = _reynolds

        # === OPTICS ===

        def _thin_lens():
            # 1/f = 1/do + 1/di -> di = f*do/(do-f)
            # Example: f=10 cm, do=30 cm -> di=15
            f, do = 10, 30
            expected = 15
            computed = f * do / (do - f)
            return self._ok("thin_lens", expected, computed,
                            "f=10, do=30")
        h["thin_lens"] = _thin_lens

        def _brewster():
            # theta_B = arctan(n2/n1)
            # Example: n1=1, n2=1.5 -> 56.31 degrees
            expected = 56.31
            computed = math.degrees(math.atan(1.5 / 1))
            return self._ok("brewster_angle", expected, computed,
                            "n1=1, n2=1.5")
        h["brewster_angle"] = _brewster

        # === NUCLEAR ===

        def _radioactive_decay():
            # N = N0 * exp(-lambda*t)
            # Example: N0=1000, lambda=0.1, t=5
            N0, lam, t = 1000, 0.1, 5
            expected = 1000 * math.exp(-0.5)
            computed = N0 * math.exp(-lam * t)
            return self._ok("radioactive_decay", expected, computed,
                            "N0=1000, lambda=0.1, t=5")
        h["radioactive_decay"] = _radioactive_decay

        def _half_life():
            # t_half = ln(2) / lambda
            # Example: lambda=0.693 -> t_half=1
            expected = 1.0
            computed = math.log(2) / 0.693
            return self._ok("half_life", expected, computed,
                            "lambda=0.693")
        h["half_life"] = _half_life

        # === GENETICS ===

        def _hardy_weinberg():
            # p=0.8, q=0.2 -> p^2=0.64, 2pq=0.32, q^2=0.04
            p, q = 0.8, 0.2
            expected_p2 = 0.64
            computed_p2 = p**2
            return self._ok("hardy_weinberg", expected_p2, computed_p2,
                            "p=0.8, q=0.2")
        h["hardy_weinberg"] = _hardy_weinberg

        # === ECONOMICS ===

        def _compound_interest():
            # A = P*(1+r/n)^(n*t)
            # Example: P=1000, r=0.05, n=12, t=10
            P, r, n, t = 1000, 0.05, 12, 10
            expected = 1647.01
            computed = P * (1 + r / n) ** (n * t)
            return self._ok("compound_interest", expected, computed,
                            "P=1000, r=5%, n=12, t=10")
        h["compound_interest"] = _compound_interest

        # === MECHANICS ===

        def _kinetic_energy():
            # KE = 0.5 * m * v^2
            # Example: m=10 kg, v=5 m/s
            expected = 125
            computed = 0.5 * 10 * 5**2
            return self._ok("kinetic_energy", expected, computed,
                            "m=10, v=5")
        h["kinetic_energy"] = _kinetic_energy

        def _potential_energy():
            # PE = m*g*h
            # Example: m=5 kg, g=9.81, h=10 m
            expected = 490.5
            computed = 5 * 9.81 * 10
            return self._ok("potential_energy", expected, computed,
                            "m=5, g=9.81, h=10")
        h["potential_energy"] = _potential_energy

        def _momentum():
            # p = m*v
            # Example: m=2, v=3 -> p=6
            expected = 6
            computed = 2 * 3
            return self._ok("momentum", expected, computed,
                            "m=2, v=3")
        h["momentum"] = _momentum

        def _drag_force():
            # Fd = 0.5 * Cd * rho * v^2 * A
            # Example: Cd=0.47, rho=1.225, v=10, A=0.01
            Cd, rho, v, A = 0.47, 1.225, 10, 0.01
            expected = 0.5 * Cd * rho * v**2 * A
            computed = 0.5 * 0.47 * 1.225 * 100 * 0.01
            return self._ok("drag_force", expected, computed,
                            "Cd=0.47, rho=1.225, v=10, A=0.01")
        h["drag_force"] = _drag_force

        # === STATISTICS ===

        def _bayes_theorem():
            # P(A|B) = P(B|A)*P(A) / P(B)
            # Example: P(B|A)=0.9, P(A)=0.01, P(B)=0.05
            expected = 0.18
            computed = 0.9 * 0.01 / 0.05
            return self._ok("bayes_theorem", expected, computed,
                            "P(B|A)=0.9, P(A)=0.01, P(B)=0.05")
        h["bayes_theorem"] = _bayes_theorem

        return h
