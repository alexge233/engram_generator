"""Pharmacology generators -- drug kinetics, dose-response, therapeutic indices.

6 generators across tiers 4-5.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PharmacologyBase(StepGenerator):
    """Base class for pharmacology generators with shared helpers.

    Provides common pharmacokinetic constants and utility methods
    used across drug metabolism and dosing generators.
    """

    LN2 = round(math.log(2), 4)


@register
class HalfLifeDrugGenerator(PharmacologyBase):
    """Compute drug concentration after elapsed time using half-life decay.

    Applies C(t) = C_0 * (1/2)^(t / t_half) to compute the remaining
    drug concentration after a given number of half-lives or arbitrary
    time.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "half_life_drug"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["exponentiation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute drug concentration after elapsed time"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a drug half-life decay problem.

        Creates an initial concentration, half-life, and elapsed time,
        then computes the remaining concentration using exponential
        decay.

        Args:
            difficulty: Controls parameter complexity and whether time
                aligns exactly with half-lives.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c0 = round(self._rng.uniform(10.0, 100.0 * max(1, difficulty)), 2)
        t_half = round(self._rng.uniform(1.0, 12.0), 2)

        if difficulty <= 4:
            # Time is an exact multiple of half-life
            n_halves = self._rng.randint(1, min(5, 1 + difficulty))
            t = round(n_halves * t_half, 2)
        else:
            # Arbitrary time
            t = round(self._rng.uniform(1.0, t_half * (2 + difficulty)), 2)

        exponent = round(t / t_half, 4)
        decay_factor = round(0.5 ** exponent, 4)
        c_t = round(c0 * decay_factor, 4)

        desc = f"C_0={c0} mg/L, t_half={t_half} h, t={t} h; find C(t)"
        return desc, {
            "c0": c0, "t_half": t_half, "t": t,
            "exponent": exponent, "decay_factor": decay_factor,
            "c_t": c_t,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "C(t) = C_0 * (1/2)^(t/t_half)",
            f"t/t_half = {sd['t']}/{sd['t_half']} = {sd['exponent']}",
            f"(1/2)^{sd['exponent']} = {sd['decay_factor']}",
            f"C(t) = {sd['c0']} * {sd['decay_factor']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the concentration at time t.

        Args:
            sd: Solution data.

        Returns:
            Concentration value with units.
        """
        return f"C({sd['t']}) = {sd['c_t']} mg/L"


@register
class DoseResponseGenerator(PharmacologyBase):
    """Compute drug effect using the Hill equation.

    Applies E = E_max * [D]^n / (EC50^n + [D]^n) to compute the
    pharmacological effect at a given drug concentration using the
    Hill coefficient for cooperativity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dose_response"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["michaelis_menten"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute drug effect using the Hill equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a dose-response Hill equation problem.

        Creates pharmacologically plausible E_max, EC50, Hill
        coefficient n, and drug concentration [D], then computes
        the effect E.

        Args:
            difficulty: Controls parameter ranges and Hill coefficient.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        e_max = round(self._rng.uniform(50.0, 100.0), 2)
        ec50 = round(self._rng.uniform(1.0, 20.0), 2)
        n = self._rng.randint(1, min(4, 1 + difficulty // 2))
        dose = round(self._rng.uniform(0.5, ec50 * (1 + difficulty)), 2)

        d_n = round(dose ** n, 4)
        ec50_n = round(ec50 ** n, 4)
        denominator = round(ec50_n + d_n, 4)
        effect = round(e_max * d_n / denominator, 4)

        desc = (
            f"E_max={e_max}, EC50={ec50}, n={n}, [D]={dose}; "
            f"find effect E"
        )
        return desc, {
            "e_max": e_max, "ec50": ec50, "n": n, "dose": dose,
            "d_n": d_n, "ec50_n": ec50_n,
            "denominator": denominator, "effect": effect,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "E = E_max * [D]^n / (EC50^n + [D]^n)",
            f"[D]^{sd['n']} = {sd['dose']}^{sd['n']} = {sd['d_n']}",
            f"EC50^{sd['n']} = {sd['ec50']}^{sd['n']} = {sd['ec50_n']}",
            f"denominator = {sd['ec50_n']} + {sd['d_n']} = {sd['denominator']}",
            f"E = {sd['e_max']} * {sd['d_n']} / {sd['denominator']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the computed drug effect.

        Args:
            sd: Solution data.

        Returns:
            Effect value as a string.
        """
        return f"E = {sd['effect']}"


@register
class BioavailabilityGenerator(PharmacologyBase):
    """Compute oral bioavailability from AUC values.

    Calculates F = (AUC_oral / AUC_iv) * 100% to determine the
    fraction of an orally administered drug that reaches systemic
    circulation compared to intravenous administration.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bioavailability"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute oral bioavailability from AUC values"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bioavailability calculation problem.

        Creates AUC values for oral and intravenous routes, with
        optional dose correction at higher difficulty (when oral
        and IV doses differ).

        Args:
            difficulty: Controls whether dose correction is needed.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        auc_iv = round(self._rng.uniform(50.0, 500.0), 2)

        if difficulty <= 4:
            # Same dose for both routes
            auc_oral = round(self._rng.uniform(10.0, auc_iv * 0.95), 2)
            ratio = round(auc_oral / auc_iv, 4)
            f_pct = round(ratio * 100, 4)
            desc = (
                f"AUC_oral={auc_oral} mg*h/L, AUC_iv={auc_iv} mg*h/L "
                f"(same dose); find bioavailability F"
            )
            return desc, {
                "auc_oral": auc_oral, "auc_iv": auc_iv,
                "ratio": ratio, "f_pct": f_pct,
                "mode": "same_dose",
            }

        # Different doses require correction
        dose_oral = self._rng.randint(100, 500)
        dose_iv = self._rng.randint(50, dose_oral)
        auc_oral = round(self._rng.uniform(10.0, auc_iv * 1.5), 2)
        ratio = round((auc_oral / auc_iv) * (dose_iv / dose_oral), 4)
        f_pct = round(ratio * 100, 4)

        desc = (
            f"AUC_oral={auc_oral} (dose={dose_oral} mg), "
            f"AUC_iv={auc_iv} (dose={dose_iv} mg); "
            f"find bioavailability F"
        )
        return desc, {
            "auc_oral": auc_oral, "auc_iv": auc_iv,
            "dose_oral": dose_oral, "dose_iv": dose_iv,
            "ratio": ratio, "f_pct": f_pct,
            "mode": "diff_dose",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "same_dose":
            return [
                "F = (AUC_oral / AUC_iv) * 100%",
                f"F = ({sd['auc_oral']} / {sd['auc_iv']}) * 100%",
                f"ratio = {sd['ratio']}",
            ]
        return [
            "F = (AUC_oral/AUC_iv) * (dose_iv/dose_oral) * 100%",
            f"AUC ratio = {sd['auc_oral']}/{sd['auc_iv']}",
            f"dose correction = {sd['dose_iv']}/{sd['dose_oral']}",
            f"F = {sd['ratio']} * 100%",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the bioavailability percentage.

        Args:
            sd: Solution data.

        Returns:
            F as a percentage.
        """
        return f"F = {sd['f_pct']}%"


@register
class ClearanceRateGenerator(PharmacologyBase):
    """Compute drug clearance from dosing and pharmacokinetic parameters.

    Supports two methods: CL = dose / AUC (from dosing data) or
    CL = k_e * V_d (from elimination constant and volume of
    distribution).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "clearance_rate"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "compute drug clearance from pharmacokinetic data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a clearance rate problem.

        At lower difficulty, uses CL = dose / AUC. At higher
        difficulty, uses CL = k_e * V_d or asks to compute k_e
        from half-life first.

        Args:
            difficulty: Controls which formula is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 4:
            dose = self._rng.randint(50, 500)
            auc = round(self._rng.uniform(20.0, 300.0), 2)
            cl = round(dose / auc, 4)
            desc = f"dose={dose} mg, AUC={auc} mg*h/L; find clearance CL"
            return desc, {
                "dose": dose, "auc": auc, "cl": cl,
                "mode": "dose_auc",
            }

        # CL = k_e * V_d, derive k_e from half-life
        t_half = round(self._rng.uniform(2.0, 24.0), 2)
        v_d = round(self._rng.uniform(10.0, 100.0 * max(1, difficulty // 2)), 2)
        k_e = round(self.LN2 / t_half, 4)
        cl = round(k_e * v_d, 4)

        desc = (
            f"t_half={t_half} h, V_d={v_d} L; "
            f"find clearance CL"
        )
        return desc, {
            "t_half": t_half, "v_d": v_d, "k_e": k_e, "cl": cl,
            "ln2": self.LN2, "mode": "ke_vd",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "dose_auc":
            return [
                "CL = dose / AUC",
                f"CL = {sd['dose']} / {sd['auc']}",
            ]
        return [
            "k_e = ln(2) / t_half",
            f"k_e = {sd['ln2']} / {sd['t_half']} = {sd['k_e']}",
            "CL = k_e * V_d",
            f"CL = {sd['k_e']} * {sd['v_d']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the clearance value.

        Args:
            sd: Solution data.

        Returns:
            Clearance with units.
        """
        return f"CL = {sd['cl']} L/h"


@register
class SteadyStateGenerator(PharmacologyBase):
    """Compute steady-state drug concentration for repeated dosing.

    Supports two formulations: C_ss = (F * dose) / (CL * tau) for
    average steady-state, or C_ss = C_0 / (1 - e^(-k*tau)) for
    peak steady-state from accumulation of geometric series.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "steady_state"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["geometric_sequence"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute steady-state drug concentration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a steady-state concentration problem.

        At lower difficulty, uses the average steady-state formula.
        At higher difficulty, uses the accumulation (geometric series)
        formula.

        Args:
            difficulty: Controls which formulation is used.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        tau = self._rng.choice([4, 6, 8, 12, 24])

        if difficulty <= 4:
            # Average steady-state: C_ss_avg = (F * dose) / (CL * tau)
            f_val = round(self._rng.uniform(0.3, 1.0), 2)
            dose = self._rng.randint(50, 500)
            cl = round(self._rng.uniform(2.0, 30.0), 2)

            numerator = round(f_val * dose, 4)
            denominator = round(cl * tau, 4)
            c_ss = round(numerator / denominator, 4)

            desc = (
                f"F={f_val}, dose={dose} mg, CL={cl} L/h, "
                f"tau={tau} h; find C_ss_avg"
            )
            return desc, {
                "f_val": f_val, "dose": dose, "cl": cl, "tau": tau,
                "numerator": numerator, "denominator": denominator,
                "c_ss": c_ss, "mode": "average",
            }

        # Accumulation: C_ss = C_0 / (1 - e^(-k*tau))
        c0 = round(self._rng.uniform(5.0, 50.0), 2)
        t_half = round(self._rng.uniform(2.0, 20.0), 2)
        k = round(self.LN2 / t_half, 4)

        exp_term = round(math.exp(-k * tau), 4)
        one_minus_exp = round(1 - exp_term, 4)
        c_ss = round(c0 / one_minus_exp, 4)

        desc = (
            f"C_0={c0} mg/L, t_half={t_half} h, tau={tau} h; "
            f"find peak C_ss"
        )
        return desc, {
            "c0": c0, "t_half": t_half, "k": k, "tau": tau,
            "exp_term": exp_term, "one_minus_exp": one_minus_exp,
            "c_ss": c_ss, "ln2": self.LN2, "mode": "accumulation",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["mode"] == "average":
            return [
                "C_ss_avg = (F * dose) / (CL * tau)",
                f"numerator = {sd['f_val']} * {sd['dose']} = {sd['numerator']}",
                f"denominator = {sd['cl']} * {sd['tau']} = {sd['denominator']}",
                f"C_ss_avg = {sd['numerator']} / {sd['denominator']}",
            ]
        return [
            "k = ln(2) / t_half",
            f"k = {sd['ln2']} / {sd['t_half']} = {sd['k']}",
            "C_ss = C_0 / (1 - e^(-k*tau))",
            f"e^(-{sd['k']}*{sd['tau']}) = {sd['exp_term']}",
            f"1 - {sd['exp_term']} = {sd['one_minus_exp']}",
            f"C_ss = {sd['c0']} / {sd['one_minus_exp']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the steady-state concentration.

        Args:
            sd: Solution data.

        Returns:
            Steady-state concentration with units.
        """
        label = "C_ss_avg" if sd["mode"] == "average" else "C_ss"
        return f"{label} = {sd['c_ss']} mg/L"


@register
class TherapeuticIndexGenerator(PharmacologyBase):
    """Compute therapeutic index and classify drug safety.

    Calculates TI = TD50 / ED50 where TD50 is the dose causing
    toxicity in 50% of subjects and ED50 is the effective dose for
    50%. Classifies: TI > 10 as safe, TI < 2 as dangerous, and
    intermediate values as requiring monitoring.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "therapeutic_index"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
        return "compute therapeutic index and classify drug safety"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a therapeutic index problem.

        Creates ED50 and TD50 values that produce a range of TI
        outcomes across difficulty levels, then classifies the
        safety profile.

        Args:
            difficulty: Controls parameter ranges and TI distribution.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ed50 = round(self._rng.uniform(1.0, 50.0 * max(1, difficulty)), 2)

        # Create a mix of safe, moderate, and dangerous drugs
        ti_target = self._rng.choice([
            self._rng.uniform(0.5, 1.8),   # dangerous
            self._rng.uniform(2.0, 9.0),    # moderate
            self._rng.uniform(10.0, 30.0),  # safe
        ])
        td50 = round(ed50 * ti_target, 2)
        ti = round(td50 / ed50, 4)

        if ti > 10:
            classification = "safe"
        elif ti < 2:
            classification = "dangerous"
        else:
            classification = "requires monitoring"

        desc = f"TD50={td50} mg, ED50={ed50} mg; compute TI and classify"
        return desc, {
            "td50": td50, "ed50": ed50,
            "ti": ti, "classification": classification,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "TI = TD50 / ED50",
            f"TI = {sd['td50']} / {sd['ed50']} = {sd['ti']}",
            f"TI {'>' if sd['ti'] > 10 else '<' if sd['ti'] < 2 else 'in [2,10]'} => {sd['classification']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the therapeutic index and safety classification.

        Args:
            sd: Solution data.

        Returns:
            TI value and classification.
        """
        return f"TI = {sd['ti']}, {sd['classification']}"
