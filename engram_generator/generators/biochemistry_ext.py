"""Extended biochemistry generators -- allosteric, inhibition, thermodynamics.

8 generators across tiers 5-6 deepening enzyme kinetics, energetics,
and nucleic acid biochemistry.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class BiochemistryExtBase(StepGenerator):
    """Base class for extended biochemistry generators.

    Provides shared thermodynamic constants and helper methods for
    enzyme kinetics and bioenergetics calculations.
    """

    R_GAS = 8.314   # J/(mol*K)
    FARADAY = 96485  # C/mol
    STANDARD_TEMP = 298.15  # K (25 C)


@register
class AllostericRegulationGenerator(BiochemistryExtBase):
    """Compute reaction velocity using the Hill equation for allosteric enzymes.

    v = Vmax * [S]^n / (K_0.5^n + [S]^n). Classifies cooperativity
    based on the Hill coefficient n: n > 1 positive, n < 1 negative,
    n = 1 non-cooperative (Michaelis-Menten).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "allosteric_regulation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute Hill equation velocity and classify cooperativity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an allosteric regulation problem.

        Creates Vmax, K_0.5, Hill coefficient n, and substrate
        concentration. Computes velocity and classifies cooperativity.

        Args:
            difficulty: Controls parameter complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vmax = round(self._rng.uniform(50.0, 500.0), 4)
        k_half = round(self._rng.uniform(1.0, 20.0), 4)
        n = round(self._rng.choice([0.5, 0.7, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0]), 1)
        s = round(self._rng.uniform(0.5, 40.0), 4)

        s_n = round(s ** n, 4)
        k_n = round(k_half ** n, 4)
        denom = round(k_n + s_n, 4)
        v = round(vmax * s_n / denom, 4)

        if n > 1:
            cooperativity = "positive cooperativity"
        elif n < 1:
            cooperativity = "negative cooperativity"
        else:
            cooperativity = "non-cooperative (Michaelis-Menten)"

        desc = f"Vmax={vmax}, K_0.5={k_half}, n={n}, [S]={s}; find v"
        return desc, {
            "vmax": vmax, "k_half": k_half, "n": n, "s": s,
            "s_n": s_n, "k_n": k_n, "denom": denom, "v": v,
            "cooperativity": cooperativity,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "v = Vmax * [S]^n / (K_0.5^n + [S]^n)",
            f"[S]^n = {sd['s']}^{sd['n']} = {sd['s_n']}",
            f"K_0.5^n = {sd['k_half']}^{sd['n']} = {sd['k_n']}",
            f"denominator = {sd['k_n']} + {sd['s_n']} = {sd['denom']}",
            f"v = {sd['vmax']} * {sd['s_n']} / {sd['denom']}",
            f"n = {sd['n']} -> {sd['cooperativity']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return velocity and cooperativity classification.

        Args:
            sd: Solution data.

        Returns:
            Velocity and cooperativity type.
        """
        return f"v = {sd['v']}, {sd['cooperativity']}"


@register
class EnzymeKineticsInhibitionExtGenerator(BiochemistryExtBase):
    """Compute apparent Km and Vmax under competitive or uncompetitive inhibition.

    Competitive: Km_app = Km*(1+[I]/Ki), Vmax unchanged.
    Uncompetitive: Km_app = Km/(1+[I]/Ki), Vmax_app = Vmax/(1+[I]/Ki).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "enzyme_kinetics_inhibition_ext"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "compute apparent Km and Vmax under enzyme inhibition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an enzyme inhibition kinetics problem.

        Creates Km, Vmax, Ki, inhibitor concentration, and inhibition
        type. Computes apparent kinetic parameters and the reaction
        velocity at a given substrate concentration.

        Args:
            difficulty: Controls inhibition type selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        km = round(self._rng.uniform(1.0, 15.0), 4)
        vmax = round(self._rng.uniform(50.0, 400.0), 4)
        ki = round(self._rng.uniform(0.5, 10.0), 4)
        inhib_conc = round(self._rng.uniform(0.5, 10.0), 4)
        s = round(self._rng.uniform(1.0, 30.0), 4)

        factor = round(1 + inhib_conc / ki, 4)

        if difficulty <= 4:
            mode = "competitive"
        else:
            mode = self._rng.choice(["competitive", "uncompetitive"])

        if mode == "competitive":
            km_app = round(km * factor, 4)
            vmax_app = vmax
        else:
            km_app = round(km / factor, 4)
            vmax_app = round(vmax / factor, 4)

        v_app = round(vmax_app * s / (km_app + s), 4)

        desc = (
            f"Km={km}, Vmax={vmax}, Ki={ki}, [I]={inhib_conc}, "
            f"[S]={s}, {mode}; find apparent parameters"
        )
        return desc, {
            "km": km, "vmax": vmax, "ki": ki,
            "inhib_conc": inhib_conc, "s": s,
            "factor": factor, "mode": mode,
            "km_app": km_app, "vmax_app": vmax_app,
            "v_app": v_app,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"inhibition type: {sd['mode']}",
            f"1 + [I]/Ki = 1 + {sd['inhib_conc']}/{sd['ki']} = {sd['factor']}",
        ]
        if sd["mode"] == "competitive":
            steps.append(f"Km_app = Km * factor = {sd['km']}*{sd['factor']} = {sd['km_app']}")
            steps.append(f"Vmax_app = Vmax = {sd['vmax_app']}")
        else:
            steps.append(f"Km_app = Km / factor = {sd['km']}/{sd['factor']} = {sd['km_app']}")
            steps.append(f"Vmax_app = Vmax / factor = {sd['vmax']}/{sd['factor']} = {sd['vmax_app']}")
        steps.append(
            f"v = Vmax_app*[S]/(Km_app+[S]) = {sd['vmax_app']}*{sd['s']}/({sd['km_app']}+{sd['s']})"
        )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return apparent parameters and velocity.

        Args:
            sd: Solution data.

        Returns:
            Km_app, Vmax_app, and v as a string.
        """
        return (
            f"Km_app = {sd['km_app']}, Vmax_app = {sd['vmax_app']}, "
            f"v = {sd['v_app']}"
        )


@register
class HendersonHasselbalchGenerator(BiochemistryExtBase):
    """Compute pH or buffer ratios using the Henderson-Hasselbalch equation.

    pH = pKa + log([A-]/[HA]). Given two of pH, pKa, and ratio,
    computes the third. Also estimates buffer capacity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "henderson_hasselbalch"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["ph_calculation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Henderson-Hasselbalch pH or buffer ratio"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Henderson-Hasselbalch problem.

        At lower difficulty, gives pKa and ratio, asks for pH.
        At higher difficulty, gives pH and pKa, asks for ratio.

        Args:
            difficulty: Controls problem mode.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pka = round(self._rng.uniform(3.0, 10.0), 4)

        if difficulty <= 4:
            mode = "find_ph"
            ratio = round(self._rng.uniform(0.1, 10.0), 4)
            log_ratio = round(math.log10(ratio), 4)
            ph = round(pka + log_ratio, 4)
            desc = f"pKa={pka}, [A-]/[HA]={ratio}; find pH"
        else:
            mode = "find_ratio"
            ph = round(self._rng.uniform(pka - 2, pka + 2), 4)
            log_ratio = round(ph - pka, 4)
            ratio = round(10 ** log_ratio, 4)
            desc = f"pKa={pka}, pH={ph}; find [A-]/[HA]"

        return desc, {
            "pka": pka, "ph": ph, "ratio": ratio,
            "log_ratio": log_ratio, "mode": mode,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = ["pH = pKa + log([A-]/[HA])"]
        if sd["mode"] == "find_ph":
            steps.append(f"log({sd['ratio']}) = {sd['log_ratio']}")
            steps.append(f"pH = {sd['pka']} + {sd['log_ratio']}")
        else:
            steps.append(f"log([A-]/[HA]) = pH - pKa = {sd['ph']} - {sd['pka']} = {sd['log_ratio']}")
            steps.append(f"[A-]/[HA] = 10^{sd['log_ratio']} = {sd['ratio']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the computed value.

        Args:
            sd: Solution data.

        Returns:
            pH or ratio as a string.
        """
        if sd["mode"] == "find_ph":
            return f"pH = {sd['ph']}"
        return f"[A-]/[HA] = {sd['ratio']}"


@register
class GibbsFreeEnergyBiochemGenerator(BiochemistryExtBase):
    """Compute Gibbs free energy under non-standard biochemical conditions.

    dG = dG0' + RT*ln(Q). dG0' = -RT*ln(Keq). Given reaction
    quotient Q and standard free energy, computes actual dG.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "gibbs_free_energy_biochem"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute Gibbs free energy at non-standard conditions"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a biochemical free energy problem.

        Creates standard free energy dG0', temperature, and reaction
        quotient Q. Computes actual dG = dG0' + RT*ln(Q).

        Args:
            difficulty: Controls parameter ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        dg0 = round(self._rng.uniform(-50.0, 10.0), 4)
        temp = self.STANDARD_TEMP
        q = round(self._rng.uniform(0.001, 100.0), 4)

        rt = round(self.R_GAS * temp / 1000, 4)  # kJ/mol
        ln_q = round(math.log(q), 4)
        rt_ln_q = round(rt * ln_q, 4)
        dg = round(dg0 + rt_ln_q, 4)

        spontaneous = "spontaneous" if dg < 0 else "non-spontaneous"

        desc = f"dG0'={dg0} kJ/mol, Q={q}, T={temp} K; find dG"
        return desc, {
            "dg0": dg0, "temp": temp, "q": q,
            "rt": rt, "ln_q": ln_q, "rt_ln_q": rt_ln_q,
            "dg": dg, "spontaneous": spontaneous,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "dG = dG0' + RT*ln(Q)",
            f"RT = {self.R_GAS}*{sd['temp']}/1000 = {sd['rt']} kJ/mol",
            f"ln(Q) = ln({sd['q']}) = {sd['ln_q']}",
            f"RT*ln(Q) = {sd['rt']}*{sd['ln_q']} = {sd['rt_ln_q']} kJ/mol",
            f"dG = {sd['dg0']} + {sd['rt_ln_q']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return dG and spontaneity classification.

        Args:
            sd: Solution data.

        Returns:
            dG value and spontaneity.
        """
        return f"dG = {sd['dg']} kJ/mol ({sd['spontaneous']})"


@register
class MetabolicPathwayEnergyGenerator(BiochemistryExtBase):
    """Compute total ATP yield from glucose through aerobic respiration.

    Sums ATP from glycolysis, pyruvate decarboxylation, Krebs cycle,
    and oxidative phosphorylation. Accounts for NADH and FADH2
    yields at standard P/O ratios.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "metabolic_pathway_energy"

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
        return "compute total ATP yield from aerobic glucose oxidation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a metabolic pathway energy problem.

        At lower difficulty, uses standard P/O ratios (2.5 ATP/NADH,
        1.5 ATP/FADH2). At higher difficulty, varies the number of
        glucose molecules or asks about specific stages.

        Args:
            difficulty: Controls glucose count and detail level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_glucose = 1
        if difficulty >= 5:
            n_glucose = self._rng.randint(2, min(difficulty, 6))

        nadh_yield = 2.5
        fadh2_yield = 1.5

        # Per glucose: 2 ATP glycolysis, 2 NADH glycolysis
        # 2 NADH pyruvate decarboxylation, 2 GTP Krebs
        # 6 NADH Krebs, 2 FADH2 Krebs
        glycolysis_atp = 2
        glycolysis_nadh = 2
        pyr_nadh = 2
        krebs_gtp = 2
        krebs_nadh = 6
        krebs_fadh2 = 2

        total_nadh = glycolysis_nadh + pyr_nadh + krebs_nadh  # 10
        total_fadh2 = krebs_fadh2  # 2
        nadh_atp = round(total_nadh * nadh_yield, 4)
        fadh2_atp = round(total_fadh2 * fadh2_yield, 4)

        per_glucose = round(glycolysis_atp + krebs_gtp + nadh_atp + fadh2_atp, 4)
        total = round(per_glucose * n_glucose, 4)

        desc = (
            f"{n_glucose} glucose molecule(s), P/O: NADH={nadh_yield}, "
            f"FADH2={fadh2_yield}; find total ATP"
        )
        return desc, {
            "n_glucose": n_glucose,
            "glycolysis_atp": glycolysis_atp,
            "total_nadh": total_nadh, "total_fadh2": total_fadh2,
            "nadh_atp": nadh_atp, "fadh2_atp": fadh2_atp,
            "krebs_gtp": krebs_gtp,
            "per_glucose": per_glucose, "total": total,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"glycolysis: {sd['glycolysis_atp']} ATP (substrate level)",
            f"total NADH per glucose: {sd['total_nadh']}",
            f"NADH -> ATP: {sd['total_nadh']}*2.5 = {sd['nadh_atp']}",
            f"total FADH2 per glucose: {sd['total_fadh2']}",
            f"FADH2 -> ATP: {sd['total_fadh2']}*1.5 = {sd['fadh2_atp']}",
            f"Krebs GTP: {sd['krebs_gtp']}",
            f"per glucose = {sd['per_glucose']} ATP",
        ]
        if sd["n_glucose"] > 1:
            steps.append(f"total = {sd['per_glucose']}*{sd['n_glucose']} = {sd['total']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return total ATP yield.

        Args:
            sd: Solution data.

        Returns:
            ATP count as a string.
        """
        return f"{sd['total']} ATP"


@register
class ProteinFoldingEnergyGenerator(BiochemistryExtBase):
    """Compute Gibbs free energy of protein folding from enthalpy and entropy.

    dG_folding = dH - T*dS. Combines hydrophobic contribution,
    hydrogen bond energy, and conformational entropy from tabulated
    values to determine folding stability.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "protein_folding_energy"

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
        return "compute protein folding free energy from dH and dS"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a protein folding energy problem.

        Creates enthalpy and entropy contributions from hydrophobic
        effect, hydrogen bonds, and conformational entropy. Computes
        net dG_folding = dH - T*dS.

        Args:
            difficulty: Controls number of energy terms.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        temp = round(self._rng.uniform(293.0, 310.0), 1)

        # Hydrophobic contribution (stabilising, negative dH)
        n_hydrophobic = self._rng.randint(5, 10 * max(1, difficulty // 2))
        dh_hydrophobic = round(-n_hydrophobic * self._rng.uniform(2.0, 5.0), 4)

        # Hydrogen bonds (stabilising)
        n_hbonds = self._rng.randint(10, 30 * max(1, difficulty // 2))
        dh_hbond = round(-n_hbonds * self._rng.uniform(1.0, 3.0), 4)

        total_dh = round(dh_hydrophobic + dh_hbond, 4)

        # Conformational entropy (destabilising, negative dS for folding)
        ds_conf = round(-self._rng.uniform(0.1, 0.5) * max(1, difficulty), 4)

        t_ds = round(temp * ds_conf, 4)
        dg = round(total_dh - t_ds, 4)

        stable = "stable (folded)" if dg < 0 else "unstable (unfolded)"

        desc = (
            f"dH_hydrophobic={dh_hydrophobic} kJ/mol, "
            f"dH_hbond={dh_hbond} kJ/mol, "
            f"dS_conf={ds_conf} kJ/(mol*K), T={temp} K; "
            f"find dG_folding"
        )
        return desc, {
            "dh_hydrophobic": dh_hydrophobic, "dh_hbond": dh_hbond,
            "total_dh": total_dh, "ds_conf": ds_conf,
            "temp": temp, "t_ds": t_ds,
            "dg": dg, "stable": stable,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"dH = dH_hydrophobic + dH_hbond = {sd['dh_hydrophobic']} + {sd['dh_hbond']} = {sd['total_dh']}",
            f"T*dS = {sd['temp']} * {sd['ds_conf']} = {sd['t_ds']} kJ/mol",
            f"dG = dH - T*dS = {sd['total_dh']} - ({sd['t_ds']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return folding free energy and stability.

        Args:
            sd: Solution data.

        Returns:
            dG and stability classification.
        """
        return f"dG_folding = {sd['dg']} kJ/mol ({sd['stable']})"


@register
class NucleicAcidMeltingGenerator(BiochemistryExtBase):
    """Compute DNA melting temperature from sequence composition.

    Tm = 81.5 + 16.6*log10([Na+]) + 41*(G+C)/(A+T+G+C) - 500/length.
    Given a DNA sequence or base counts, computes the melting
    temperature.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nucleic_acid_melting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "compute DNA melting temperature from sequence composition"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nucleic acid melting temperature problem.

        Creates base counts for A, T, G, C and Na+ concentration,
        then computes Tm using the empirical formula.

        Args:
            difficulty: Controls sequence length.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        length = self._rng.randint(10, 30 * max(1, difficulty))
        gc_frac = round(self._rng.uniform(0.3, 0.7), 2)
        gc_count = int(length * gc_frac)
        at_count = length - gc_count

        # Split into individual bases
        g_count = gc_count // 2
        c_count = gc_count - g_count
        a_count = at_count // 2
        t_count = at_count - a_count

        na_conc = round(self._rng.uniform(0.01, 1.0), 4)
        log_na = round(math.log10(na_conc), 4)

        gc_pct = round(100 * gc_count / length, 4)
        gc_term = round(41 * gc_count / length, 4)
        na_term = round(16.6 * log_na, 4)
        length_term = round(500 / length, 4)

        tm = round(81.5 + na_term + gc_term - length_term, 4)

        desc = (
            f"A={a_count}, T={t_count}, G={g_count}, C={c_count}, "
            f"[Na+]={na_conc} M; find Tm"
        )
        return desc, {
            "a": a_count, "t": t_count, "g": g_count, "c": c_count,
            "length": length, "gc_count": gc_count, "gc_pct": gc_pct,
            "na_conc": na_conc, "log_na": log_na,
            "gc_term": gc_term, "na_term": na_term,
            "length_term": length_term, "tm": tm,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "Tm = 81.5 + 16.6*log([Na+]) + 41*(G+C)/length - 500/length",
            f"length = {sd['length']}, G+C = {sd['gc_count']}",
            f"16.6*log10({sd['na_conc']}) = 16.6*{sd['log_na']} = {sd['na_term']}",
            f"41*{sd['gc_count']}/{sd['length']} = {sd['gc_term']}",
            f"500/{sd['length']} = {sd['length_term']}",
            f"Tm = 81.5 + {sd['na_term']} + {sd['gc_term']} - {sd['length_term']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the melting temperature.

        Args:
            sd: Solution data.

        Returns:
            Tm in degrees Celsius.
        """
        return f"Tm = {sd['tm']} C"


@register
class RedoxPotentialGenerator(BiochemistryExtBase):
    """Compute Gibbs free energy from standard reduction potentials.

    dG0' = -n*F*dE0'. Given standard reduction potentials for two
    half-reactions, computes dE0' and the corresponding dG0' for
    the overall electron transfer reaction.
    """

    HALF_REACTIONS = {
        "NAD+/NADH": -0.32,
        "FAD/FADH2": -0.22,
        "O2/H2O": 0.816,
        "cytochrome c (ox/red)": 0.254,
        "ubiquinone (ox/red)": 0.045,
        "fumarate/succinate": 0.031,
        "pyruvate/lactate": -0.185,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "redox_potential"

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
        return "compute dG0' from standard reduction potentials"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a redox potential to free energy problem.

        Selects two half-reactions, assigns electron donor and acceptor,
        computes dE0' and dG0'.

        Args:
            difficulty: Controls half-reaction selection.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pairs = list(self.HALF_REACTIONS.keys())
        donor_name, acceptor_name = self._rng.sample(pairs, 2)

        e_donor = self.HALF_REACTIONS[donor_name]
        e_acceptor = self.HALF_REACTIONS[acceptor_name]

        # Electrons flow from lower to higher E0'
        # dE0' = E_acceptor - E_donor (for spontaneous reaction)
        if e_donor > e_acceptor:
            donor_name, acceptor_name = acceptor_name, donor_name
            e_donor, e_acceptor = e_acceptor, e_donor

        de0 = round(e_acceptor - e_donor, 4)
        n_electrons = self._rng.choice([1, 2])
        dg0 = round(-n_electrons * self.FARADAY * de0 / 1000, 4)  # kJ/mol

        desc = (
            f"donor: {donor_name} (E0'={e_donor} V), "
            f"acceptor: {acceptor_name} (E0'={e_acceptor} V), "
            f"n={n_electrons}; find dG0'"
        )
        return desc, {
            "donor": donor_name, "acceptor": acceptor_name,
            "e_donor": e_donor, "e_acceptor": e_acceptor,
            "de0": de0, "n": n_electrons,
            "dg0": dg0,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        nf = round(sd["n"] * self.FARADAY / 1000, 4)
        return [
            f"dE0' = E_acceptor - E_donor = {sd['e_acceptor']} - {sd['e_donor']} = {sd['de0']} V",
            f"dG0' = -n*F*dE0'",
            f"n*F = {sd['n']}*{self.FARADAY}/1000 = {nf} kJ/(mol*V)",
            f"dG0' = -{nf}*{sd['de0']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the standard free energy change.

        Args:
            sd: Solution data.

        Returns:
            dG0' in kJ/mol.
        """
        return f"dG0' = {sd['dg0']} kJ/mol"
