"""Deep pharmacology generators -- PKPD, drug interactions, receptor theory.

6 generators across tiers 5-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class PharmacologyDeepBase(StepGenerator):
    """Base class for deep pharmacology generators with shared constants.

    Provides common pharmacokinetic constants and utility methods
    used across advanced PKPD and receptor pharmacology generators.

    Attributes:
        LN2: Natural log of 2, precomputed to 4 dp.
    """

    LN2 = round(math.log(2), 4)


@register
class TwoCompartmentModelGenerator(PharmacologyDeepBase):
    """Compute drug concentration in a two-compartment model.

    C(t) = A * e^(-alpha*t) + B * e^(-beta*t) where alpha is the
    distribution rate constant and beta is the elimination rate
    constant. Identifies distribution and elimination phases.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_compartment_model"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute two-compartment model drug concentration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a two-compartment model problem.

        Creates pharmacologically plausible A, B, alpha, beta values
        and asks for C(t) at a specified time. Alpha must be greater
        than beta (distribution is faster than elimination).

        Args:
            difficulty: Controls time range and parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        a_coeff = round(self._rng.uniform(10.0, 80.0), 2)
        b_coeff = round(self._rng.uniform(5.0, 40.0), 2)
        alpha = round(self._rng.uniform(1.0, 5.0), 4)
        beta = round(self._rng.uniform(0.05, min(0.5, alpha * 0.3)), 4)

        t = round(self._rng.uniform(0.5, 2.0 + difficulty * 1.5), 2)

        dist_term = round(a_coeff * math.exp(-alpha * t), 4)
        elim_term = round(b_coeff * math.exp(-beta * t), 4)
        c_t = round(dist_term + elim_term, 4)

        # Identify dominant phase
        if dist_term > elim_term * 0.1:
            phase = "distribution phase (both terms significant)"
        else:
            phase = "elimination phase (A*e^(-alpha*t) negligible)"

        desc = (
            f"A={a_coeff}, B={b_coeff}, "
            f"alpha={alpha} h^-1, beta={beta} h^-1, "
            f"t={t} h. Find C(t)."
        )
        return desc, {
            "A": a_coeff, "B": b_coeff,
            "alpha": alpha, "beta": beta, "t": t,
            "dist_term": dist_term, "elim_term": elim_term,
            "c_t": c_t, "phase": phase,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "C(t) = A*e^(-alpha*t) + B*e^(-beta*t)",
            f"A*e^(-{sd['alpha']}*{sd['t']}) = {sd['A']}*e^{round(-sd['alpha']*sd['t'], 4)} = {sd['dist_term']}",
            f"B*e^(-{sd['beta']}*{sd['t']}) = {sd['B']}*e^{round(-sd['beta']*sd['t'], 4)} = {sd['elim_term']}",
            f"C({sd['t']}) = {sd['dist_term']} + {sd['elim_term']}",
            f"phase: {sd['phase']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the concentration at time t.

        Args:
            sd: Solution data dict.

        Returns:
            Concentration with phase identification.
        """
        return f"C({sd['t']}) = {sd['c_t']} mg/L, {sd['phase']}"


@register
class DrugInteractionGenerator(PharmacologyDeepBase):
    """Predict drug interaction effects on steady-state concentration.

    Enzyme induction increases metabolism, lowering C_ss.
    Enzyme inhibition decreases metabolism, raising C_ss.
    Computes new C_ss given the fold-change in clearance.
    """

    INTERACTIONS = [
        {
            "inhibitor": "ketoconazole", "substrate": "midazolam",
            "enzyme": "CYP3A4", "type": "inhibition",
            "cl_factor_range": (0.2, 0.5),
        },
        {
            "inhibitor": "rifampin", "substrate": "warfarin",
            "enzyme": "CYP2C9", "type": "induction",
            "cl_factor_range": (1.5, 3.0),
        },
        {
            "inhibitor": "fluoxetine", "substrate": "dextromethorphan",
            "enzyme": "CYP2D6", "type": "inhibition",
            "cl_factor_range": (0.1, 0.4),
        },
        {
            "inhibitor": "carbamazepine", "substrate": "ethinylestradiol",
            "enzyme": "CYP3A4", "type": "induction",
            "cl_factor_range": (1.5, 2.5),
        },
        {
            "inhibitor": "cimetidine", "substrate": "theophylline",
            "enzyme": "CYP1A2", "type": "inhibition",
            "cl_factor_range": (0.3, 0.6),
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "drug_interaction"

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
        return "predict drug interaction effect on steady-state concentration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a drug interaction problem.

        Selects an interaction pair, computes original C_ss, then
        applies the clearance fold-change to predict the new C_ss.

        Args:
            difficulty: Controls interaction pool and parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool_size = min(len(self.INTERACTIONS), 2 + difficulty)
        interaction = self._rng.choice(self.INTERACTIONS[:pool_size])

        dose = self._rng.randint(50, 500)
        tau = self._rng.choice([6, 8, 12, 24])
        f_bio = round(self._rng.uniform(0.5, 1.0), 2)
        cl_original = round(self._rng.uniform(5.0, 50.0), 2)

        c_ss_original = round((f_bio * dose) / (cl_original * tau), 4)

        low, high = interaction["cl_factor_range"]
        cl_factor = round(self._rng.uniform(low, high), 4)
        cl_new = round(cl_original * cl_factor, 4)
        c_ss_new = round((f_bio * dose) / (cl_new * tau), 4)

        if interaction["type"] == "inhibition":
            direction = "increased (inhibition reduces clearance)"
        else:
            direction = "decreased (induction increases clearance)"

        desc = (
            f"{interaction['inhibitor']} + {interaction['substrate']} "
            f"({interaction['enzyme']} {interaction['type']}). "
            f"F={f_bio}, dose={dose} mg, tau={tau} h, "
            f"CL={cl_original} L/h, CL factor={cl_factor}. "
            f"Find new C_ss."
        )
        return desc, {
            "interaction": interaction, "dose": dose, "tau": tau,
            "f_bio": f_bio, "cl_original": cl_original,
            "c_ss_original": c_ss_original,
            "cl_factor": cl_factor, "cl_new": cl_new,
            "c_ss_new": c_ss_new, "direction": direction,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "C_ss = (F * dose) / (CL * tau)",
            f"original C_ss = ({sd['f_bio']}*{sd['dose']}) / ({sd['cl_original']}*{sd['tau']}) = {sd['c_ss_original']}",
            f"CL_new = {sd['cl_original']} * {sd['cl_factor']} = {sd['cl_new']}",
            f"new C_ss = ({sd['f_bio']}*{sd['dose']}) / ({sd['cl_new']}*{sd['tau']})",
            f"C_ss {sd['direction']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the new steady-state concentration.

        Args:
            sd: Solution data dict.

        Returns:
            New C_ss with direction of change.
        """
        return f"C_ss = {sd['c_ss_new']} mg/L ({sd['direction']})"


@register
class ReceptorOccupancyGenerator(PharmacologyDeepBase):
    """Compute receptor occupancy from drug concentration and Kd.

    Occupancy = [D] / (Kd + [D]). EC50 equals Kd for a full agonist.
    For partial agonists, E_max is less than the full agonist maximum.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "receptor_occupancy"

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
        if difficulty <= 4:
            return "compute receptor occupancy from drug concentration"
        return "compute effect for full vs partial agonist"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a receptor occupancy problem.

        At low difficulty, computes fractional occupancy. At higher
        difficulty, compares full and partial agonist effects.

        Args:
            difficulty: Controls whether partial agonist is included.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        kd = round(self._rng.uniform(0.1, 50.0), 4)
        dose = round(self._rng.uniform(0.5, kd * (1 + difficulty)), 4)
        occupancy = round(dose / (kd + dose), 4)

        if difficulty <= 4:
            desc = (
                f"[D]={dose} nM, Kd={kd} nM. "
                f"Find fractional receptor occupancy."
            )
            return desc, {
                "dose": dose, "kd": kd, "occupancy": occupancy,
                "mode": "simple",
            }

        # Partial agonist comparison
        e_max_full = round(self._rng.uniform(80.0, 100.0), 2)
        e_max_partial = round(self._rng.uniform(20.0, 60.0), 2)
        effect_full = round(e_max_full * occupancy, 4)
        effect_partial = round(e_max_partial * occupancy, 4)

        desc = (
            f"[D]={dose} nM, Kd={kd} nM. "
            f"Full agonist E_max={e_max_full}%, "
            f"partial agonist E_max={e_max_partial}%. "
            f"Find effects."
        )
        return desc, {
            "dose": dose, "kd": kd, "occupancy": occupancy,
            "e_max_full": e_max_full, "e_max_partial": e_max_partial,
            "effect_full": effect_full, "effect_partial": effect_partial,
            "mode": "partial",
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        steps = [
            "occupancy = [D] / (Kd + [D])",
            f"occupancy = {sd['dose']} / ({sd['kd']} + {sd['dose']})",
            f"occupancy = {sd['occupancy']}",
        ]
        if sd["mode"] == "partial":
            steps.extend([
                f"full agonist: E = {sd['e_max_full']} * {sd['occupancy']} = {sd['effect_full']}",
                f"partial agonist: E = {sd['e_max_partial']} * {sd['occupancy']} = {sd['effect_partial']}",
            ])
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the occupancy and optionally effects.

        Args:
            sd: Solution data dict.

        Returns:
            Occupancy fraction, optionally with effect values.
        """
        if sd["mode"] == "simple":
            return f"occupancy = {sd['occupancy']}"
        return (
            f"occupancy = {sd['occupancy']}, "
            f"E_full = {sd['effect_full']}%, "
            f"E_partial = {sd['effect_partial']}%"
        )


@register
class LoadingDoseGenerator(PharmacologyDeepBase):
    """Compute loading and maintenance doses from PK parameters.

    Loading dose: D_L = C_ss * V_d.
    Maintenance dose: D_M = C_ss * CL * tau.
    Computes both from given pharmacokinetic parameters.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "loading_dose"

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
        return "compute loading and maintenance doses"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a loading/maintenance dose problem.

        Creates target C_ss, V_d, CL, and dosing interval tau, then
        computes both loading and maintenance doses.

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c_ss = round(self._rng.uniform(1.0, 20.0), 2)
        v_d = round(self._rng.uniform(10.0, 100.0 * max(1, difficulty // 2)), 2)
        cl = round(self._rng.uniform(1.0, 30.0), 2)
        tau = self._rng.choice([4, 6, 8, 12, 24])

        d_l = round(c_ss * v_d, 4)
        d_m = round(c_ss * cl * tau, 4)

        desc = (
            f"Target C_ss={c_ss} mg/L, V_d={v_d} L, "
            f"CL={cl} L/h, tau={tau} h. "
            f"Find loading dose D_L and maintenance dose D_M."
        )
        return desc, {
            "c_ss": c_ss, "v_d": v_d, "cl": cl, "tau": tau,
            "d_l": d_l, "d_m": d_m,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "D_L = C_ss * V_d",
            f"D_L = {sd['c_ss']} * {sd['v_d']} = {sd['d_l']} mg",
            "D_M = C_ss * CL * tau",
            f"D_M = {sd['c_ss']} * {sd['cl']} * {sd['tau']} = {sd['d_m']} mg",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return both doses.

        Args:
            sd: Solution data dict.

        Returns:
            Loading and maintenance dose values.
        """
        return f"D_L = {sd['d_l']} mg, D_M = {sd['d_m']} mg"


@register
class PkNonlinearGenerator(PharmacologyDeepBase):
    """Classify Michaelis-Menten elimination kinetics regime.

    Rate: -dC/dt = Vmax * C / (Km + C). At low C (C << Km):
    first-order elimination. At high C (C >> Km): zero-order
    elimination. Computes rate and classifies the regime.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pk_nonlinear"

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
        return "classify Michaelis-Menten elimination kinetics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nonlinear PK problem.

        Creates Vmax and Km, then generates a concentration that falls
        in a specific regime (low C, high C, or intermediate).

        Args:
            difficulty: Controls whether the regime is clear-cut.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vmax = round(self._rng.uniform(5.0, 50.0 * max(1, difficulty)), 2)
        km = round(self._rng.uniform(1.0, 30.0), 2)

        regime_choice = self._rng.choice(["low", "high", "intermediate"])
        if regime_choice == "low":
            conc = round(self._rng.uniform(0.01, km * 0.1), 4)
        elif regime_choice == "high":
            conc = round(km * self._rng.uniform(10.0, 50.0), 4)
        else:
            conc = round(km * self._rng.uniform(0.5, 2.0), 4)

        rate = round(vmax * conc / (km + conc), 4)
        ratio = round(conc / km, 4)

        if ratio < 0.1:
            regime = "first-order (C << Km)"
            approx_rate = round(vmax * conc / km, 4)
        elif ratio > 10:
            regime = "zero-order (C >> Km)"
            approx_rate = round(vmax, 4)
        else:
            regime = "mixed-order (C ~ Km)"
            approx_rate = rate

        desc = (
            f"Vmax={vmax} mg/(L*h), Km={km} mg/L, "
            f"C={conc} mg/L. Find elimination rate and classify regime."
        )
        return desc, {
            "vmax": vmax, "km": km, "conc": conc,
            "rate": rate, "ratio": ratio,
            "regime": regime, "approx_rate": approx_rate,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            "-dC/dt = Vmax * C / (Km + C)",
            f"rate = {sd['vmax']} * {sd['conc']} / ({sd['km']} + {sd['conc']})",
            f"rate = {sd['rate']} mg/(L*h)",
            f"C/Km = {sd['ratio']}",
            f"regime: {sd['regime']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the rate and regime classification.

        Args:
            sd: Solution data dict.

        Returns:
            Elimination rate and kinetics regime.
        """
        return f"rate = {sd['rate']} mg/(L*h), {sd['regime']}"


@register
class BioequivalenceGenerator(PharmacologyDeepBase):
    """Assess bioequivalence between test and reference formulations.

    Compares AUC, Cmax, and Tmax between test and reference. The 90%
    confidence interval of the ratio must fall within 80-125% for
    bioequivalence.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bioequivalence"

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
        return "assess bioequivalence from PK parameters"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a bioequivalence assessment problem.

        Creates test and reference AUC and Cmax values, computes
        ratios, and determines whether the 80-125% criterion is met.

        Args:
            difficulty: Controls closeness to boundary values.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        auc_ref = round(self._rng.uniform(50.0, 500.0), 2)
        cmax_ref = round(self._rng.uniform(5.0, 80.0), 2)
        tmax_ref = round(self._rng.uniform(0.5, 6.0), 2)

        # Generate test values with controlled ratio
        if difficulty <= 4:
            # Clear pass or fail
            outcome = self._rng.choice(["pass", "fail"])
            if outcome == "pass":
                auc_ratio = round(self._rng.uniform(0.85, 1.15), 4)
                cmax_ratio = round(self._rng.uniform(0.85, 1.15), 4)
            else:
                auc_ratio = round(self._rng.uniform(0.6, 0.78), 4)
                cmax_ratio = round(self._rng.uniform(0.6, 0.78), 4)
        else:
            # Borderline cases
            auc_ratio = round(self._rng.uniform(0.75, 1.30), 4)
            cmax_ratio = round(self._rng.uniform(0.75, 1.30), 4)

        auc_test = round(auc_ref * auc_ratio, 2)
        cmax_test = round(cmax_ref * cmax_ratio, 2)
        tmax_test = round(tmax_ref * self._rng.uniform(0.8, 1.2), 2)

        auc_ratio_pct = round(auc_ratio * 100, 4)
        cmax_ratio_pct = round(cmax_ratio * 100, 4)

        auc_pass = 80 <= auc_ratio_pct <= 125
        cmax_pass = 80 <= cmax_ratio_pct <= 125
        bioequivalent = auc_pass and cmax_pass

        desc = (
            f"Reference: AUC={auc_ref}, Cmax={cmax_ref}, Tmax={tmax_ref} h. "
            f"Test: AUC={auc_test}, Cmax={cmax_test}, Tmax={tmax_test} h. "
            f"Assess bioequivalence (80-125%)."
        )
        return desc, {
            "auc_ref": auc_ref, "cmax_ref": cmax_ref,
            "tmax_ref": tmax_ref,
            "auc_test": auc_test, "cmax_test": cmax_test,
            "tmax_test": tmax_test,
            "auc_ratio": auc_ratio, "cmax_ratio": cmax_ratio,
            "auc_ratio_pct": auc_ratio_pct,
            "cmax_ratio_pct": cmax_ratio_pct,
            "auc_pass": auc_pass, "cmax_pass": cmax_pass,
            "bioequivalent": bioequivalent,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data dict.

        Returns:
            List of step strings.
        """
        return [
            f"AUC ratio = {sd['auc_test']}/{sd['auc_ref']} = {sd['auc_ratio']} ({sd['auc_ratio_pct']}%)",
            f"Cmax ratio = {sd['cmax_test']}/{sd['cmax_ref']} = {sd['cmax_ratio']} ({sd['cmax_ratio_pct']}%)",
            f"AUC in 80-125%: {'yes' if sd['auc_pass'] else 'no'}",
            f"Cmax in 80-125%: {'yes' if sd['cmax_pass'] else 'no'}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the bioequivalence assessment.

        Args:
            sd: Solution data dict.

        Returns:
            Bioequivalent or not with ratios.
        """
        status = "bioequivalent" if sd["bioequivalent"] else "not bioequivalent"
        return (
            f"{status}: AUC={sd['auc_ratio_pct']}%, "
            f"Cmax={sd['cmax_ratio_pct']}%"
        )
