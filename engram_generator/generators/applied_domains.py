"""Chemistry, economics, game theory, automata, spatial, numerical generators.

Adds 37 generators across tiers 1-4 for applied domains.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ═══════════════════════════════════════════════════════════════════
# CHEMISTRY (5 generators, tiers 2-3)
# ═══════════════════════════════════════════════════════════════════

_ATOMIC_MASSES = {
    "H": 1.008, "He": 4.003, "C": 12.011, "N": 14.007,
    "O": 15.999, "Na": 22.990, "Cl": 35.453, "S": 32.065,
    "Ca": 40.078, "Fe": 55.845, "K": 39.098, "Mg": 24.305,
}


@register
class MolarMassGenerator(StepGenerator):
    """Calculate the molar mass of a molecule."""

    @property
    def task_name(self) -> str:
        return "molar_mass"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication", "addition"]

    def task_description(self, difficulty: int) -> str:
        return "calculate molar mass"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        molecules = [
            ("H2O", [("H", 2), ("O", 1)]),
            ("CO2", [("C", 1), ("O", 2)]),
            ("NaCl", [("Na", 1), ("Cl", 1)]),
            ("CaCO3", [("Ca", 1), ("C", 1), ("O", 3)]),
            ("H2SO4", [("H", 2), ("S", 1), ("O", 4)]),
            ("NaOH", [("Na", 1), ("O", 1), ("H", 1)]),
            ("Fe2O3", [("Fe", 2), ("O", 3)]),
            ("C6H12O6", [("C", 6), ("H", 12), ("O", 6)]),
        ]
        formula, parts = self._rng.choice(molecules[:min(len(molecules), 3 + difficulty)])
        mass = round(sum(_ATOMIC_MASSES[e] * n for e, n in parts), 3)
        return f"molar mass of {formula}", {"formula": formula, "parts": parts, "mass": mass}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for elem, count in sd["parts"]:
            steps.append(f"{elem}: {_ATOMIC_MASSES[elem]} × {count} = {round(_ATOMIC_MASSES[elem] * count, 3)}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['mass']} g/mol"


@register
class BalancingEquationGenerator(StepGenerator):
    """Balance a simple chemical equation."""

    @property
    def task_name(self) -> str:
        return "balancing_equation"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "balance chemical equation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        equations = [
            ("H2 + O2 -> H2O", "2H2 + O2 -> 2H2O"),
            ("N2 + H2 -> NH3", "N2 + 3H2 -> 2NH3"),
            ("Fe + O2 -> Fe2O3", "4Fe + 3O2 -> 2Fe2O3"),
            ("CH4 + O2 -> CO2 + H2O", "CH4 + 2O2 -> CO2 + 2H2O"),
            ("Na + Cl2 -> NaCl", "2Na + Cl2 -> 2NaCl"),
            ("C3H8 + O2 -> CO2 + H2O", "C3H8 + 5O2 -> 3CO2 + 4H2O"),
        ]
        unbalanced, balanced = self._rng.choice(equations[:min(len(equations), 2 + difficulty)])
        return f"balance: {unbalanced}", {"unbalanced": unbalanced, "balanced": balanced}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"count atoms each side", f"adjust coefficients"]

    def _create_answer(self, sd: dict) -> str:
        return sd["balanced"]


@register
class StoichiometryGenerator(StepGenerator):
    """Calculate amounts using mole ratios."""

    @property
    def task_name(self) -> str:
        return "stoichiometry"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["molar_mass", "multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "stoichiometry calculation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        reactions = [
            ("2H2 + O2 -> 2H2O", "H2", "H2O", 2, 2),
            ("N2 + 3H2 -> 2NH3", "N2", "NH3", 1, 2),
            ("CH4 + 2O2 -> CO2 + 2H2O", "CH4", "CO2", 1, 1),
        ]
        eq, reactant, product, r_coeff, p_coeff = self._rng.choice(
            reactions[:min(len(reactions), 1 + difficulty)]
        )
        moles_r = self._rng.randint(1, 5 * difficulty)
        moles_p = round(moles_r * p_coeff / r_coeff, 2)
        return (
            f"{eq}: {moles_r} mol {reactant} produces how many mol {product}?",
            {"eq": eq, "reactant": reactant, "product": product,
             "r_coeff": r_coeff, "p_coeff": p_coeff,
             "moles_r": moles_r, "moles_p": moles_p},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"ratio: {sd['r_coeff']} mol {sd['reactant']} : {sd['p_coeff']} mol {sd['product']}",
            f"{sd['moles_r']} * {sd['p_coeff']}/{sd['r_coeff']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['moles_p']} mol"


@register
class MolarityGenerator(StepGenerator):
    """Calculate molarity or dilution."""

    @property
    def task_name(self) -> str:
        return "molarity"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["molar_mass", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate molarity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        mode = self._rng.choice(["concentration", "dilution"])
        if mode == "concentration":
            moles = round(self._rng.uniform(0.1, 5.0 * difficulty), 2)
            litres = round(self._rng.uniform(0.1, 5.0), 2)
            m = round(moles / litres, 4)
            return f"{moles} mol in {litres} L", {"moles": moles, "litres": litres, "M": m, "mode": mode}
        else:
            m1 = round(self._rng.uniform(0.5, 5.0), 2)
            v1 = round(self._rng.uniform(0.05, 1.0), 3)
            v2 = round(v1 + self._rng.uniform(0.5, 3.0), 3)
            m2 = round(m1 * v1 / v2, 4)
            return (
                f"dilute {m1}M ({v1}L) to {v2}L",
                {"m1": m1, "v1": v1, "v2": v2, "m2": m2, "mode": mode},
            )

    def _create_steps(self, sd: dict) -> list[str]:
        if sd["mode"] == "concentration":
            return [f"M = moles / litres = {sd['moles']} / {sd['litres']}"]
        return [f"M1*V1 = M2*V2", f"{sd['m1']}*{sd['v1']} = M2*{sd['v2']}"]

    def _create_answer(self, sd: dict) -> str:
        if sd["mode"] == "concentration":
            return f"{sd['M']} M"
        return f"{sd['m2']} M"


@register
class PhCalculationGenerator(StepGenerator):
    """Calculate pH from hydrogen ion concentration."""

    @property
    def task_name(self) -> str:
        return "ph_calculation"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        return "calculate pH"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        exp = -self._rng.randint(1, min(13, 2 + 2 * difficulty))
        conc = 10.0 ** exp
        ph = -exp
        return f"[H+] = {conc}", {"conc": conc, "ph": ph}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"pH = -log10([H+])", f"pH = -log10({sd['conc']})"]

    def _create_answer(self, sd: dict) -> str:
        return str(sd["ph"])


# ═══════════════════════════════════════════════════════════════════
# ECONOMICS / FINANCE (6 generators, tiers 1-3)
# ═══════════════════════════════════════════════════════════════════

@register
class SimpleInterestGenerator(StepGenerator):
    """Calculate simple interest."""

    @property
    def task_name(self) -> str:
        return "simple_interest"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        return "calculate simple interest"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.randint(100, 1000 * difficulty) * 10
        r = round(self._rng.uniform(0.01, 0.15), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        interest = round(p * r * t, 2)
        total = round(p + interest, 2)
        return (
            f"P={p}, r={r*100}%, t={t} years",
            {"P": p, "r": r, "t": t, "interest": interest, "total": total},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"I = P*r*t = {sd['P']}*{sd['r']}*{sd['t']}", f"A = P + I"]

    def _create_answer(self, sd: dict) -> str:
        return f"I={sd['interest']}, A={sd['total']}"


@register
class CompoundInterestGenerator(StepGenerator):
    """Calculate compound interest."""

    @property
    def task_name(self) -> str:
        return "compound_interest"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["simple_interest", "exponentiation"]

    def task_description(self, difficulty: int) -> str:
        return "calculate compound interest"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        p = self._rng.randint(100, 500 * difficulty) * 10
        r = round(self._rng.uniform(0.02, 0.12), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        n = self._rng.choice([1, 4, 12])
        a = round(p * (1 + r / n) ** (n * t), 2)
        return (
            f"P={p}, r={r*100}%, t={t}y, n={n}/year",
            {"P": p, "r": r, "t": t, "n": n, "A": a},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"A = P(1 + r/n)^(nt)",
            f"A = {sd['P']}(1 + {sd['r']}/{sd['n']})^({sd['n']}*{sd['t']})",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['A']}"


@register
class ROIGenerator(StepGenerator):
    """Calculate return on investment."""

    @property
    def task_name(self) -> str:
        return "roi"

    @property
    def tier(self) -> int:
        return 1

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate ROI"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cost = self._rng.randint(100, 500 * difficulty) * 10
        gain_pct = self._rng.uniform(-0.3, 0.8)
        gain = round(cost * (1 + gain_pct))
        roi = round((gain - cost) / cost * 100, 2)
        return f"cost={cost}, return={gain}", {"cost": cost, "gain": gain, "roi": roi}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"ROI = (gain - cost) / cost * 100", f"({sd['gain']} - {sd['cost']}) / {sd['cost']} * 100"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['roi']}%"


@register
class BreakEvenGenerator(StepGenerator):
    """Calculate break-even point."""

    @property
    def task_name(self) -> str:
        return "break_even"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        return "find break-even point"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fixed = self._rng.randint(1000, 10000 * difficulty)
        price = self._rng.randint(20, 100 * difficulty)
        variable = self._rng.randint(5, price - 1)
        units = math.ceil(fixed / (price - variable))
        return (
            f"fixed={fixed}, price={price}, variable_cost={variable}",
            {"fixed": fixed, "price": price, "variable": variable, "units": units},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        margin = sd["price"] - sd["variable"]
        return [f"margin = {sd['price']} - {sd['variable']} = {margin}", f"units = {sd['fixed']} / {margin}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['units']} units"


@register
class DepreciationGenerator(StepGenerator):
    """Calculate straight-line depreciation."""

    @property
    def task_name(self) -> str:
        return "depreciation"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction", "division"]

    def task_description(self, difficulty: int) -> str:
        return "calculate depreciation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        cost = self._rng.randint(1000, 10000 * difficulty)
        salvage = self._rng.randint(0, cost // 3)
        life = self._rng.randint(3, min(15, 3 + difficulty))
        annual = round((cost - salvage) / life, 2)
        year = self._rng.randint(1, life)
        book_value = round(cost - annual * year, 2)
        return (
            f"cost={cost}, salvage={salvage}, life={life}y, find value at year {year}",
            {"cost": cost, "salvage": salvage, "life": life, "annual": annual,
             "year": year, "book_value": book_value},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"annual = ({sd['cost']} - {sd['salvage']}) / {sd['life']} = {sd['annual']}",
            f"value at year {sd['year']} = {sd['cost']} - {sd['annual']}*{sd['year']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['book_value']}"


@register
class PresentValueGenerator(StepGenerator):
    """Calculate present value of a future amount."""

    @property
    def task_name(self) -> str:
        return "present_value"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["compound_interest"]

    def task_description(self, difficulty: int) -> str:
        return "calculate present value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fv = self._rng.randint(1000, 10000 * difficulty)
        r = round(self._rng.uniform(0.03, 0.12), 3)
        t = self._rng.randint(1, min(10, 2 + difficulty))
        pv = round(fv / (1 + r) ** t, 2)
        return f"FV={fv}, r={r*100}%, t={t}y", {"fv": fv, "r": r, "t": t, "pv": pv}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"PV = FV / (1+r)^t = {sd['fv']} / (1+{sd['r']})^{sd['t']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['pv']}"


# ═══════════════════════════════════════════════════════════════════
# GAME THEORY (4 generators, tiers 3-4)
# ═══════════════════════════════════════════════════════════════════

@register
class PayoffMatrixGenerator(StepGenerator):
    """Read payoffs from a game matrix."""

    @property
    def task_name(self) -> str:
        return "payoff_matrix"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        return "read payoff matrix"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        matrix = [[
            (self._rng.randint(-5, 10), self._rng.randint(-5, 10))
            for _ in range(n)
        ] for _ in range(n)]
        r = self._rng.randint(0, n - 1)
        c = self._rng.randint(0, n - 1)
        payoff = matrix[r][c]
        mat_str = "; ".join(
            "[" + ", ".join(f"({a},{b})" for a, b in row) + "]"
            for row in matrix
        )
        return (
            f"matrix: {mat_str}. Payoff at row {r}, col {c}?",
            {"matrix": matrix, "r": r, "c": c, "payoff": payoff},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"row {sd['r']}, col {sd['c']}: {sd['payoff']}"]

    def _create_answer(self, sd: dict) -> str:
        return f"({sd['payoff'][0]},{sd['payoff'][1]})"


@register
class DominantStrategyGenerator(StepGenerator):
    """Find dominant strategies in a 2x2 game."""

    @property
    def task_name(self) -> str:
        return "dominant_strategy"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["payoff_matrix"]

    def task_description(self, difficulty: int) -> str:
        return "find dominant strategy"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m = [[(self._rng.randint(0, 10), self._rng.randint(0, 10)) for _ in range(2)] for _ in range(2)]
        row_dom = None
        if m[0][0][0] >= m[1][0][0] and m[0][1][0] >= m[1][1][0]:
            if m[0][0][0] > m[1][0][0] or m[0][1][0] > m[1][1][0]:
                row_dom = "row 0"
        if m[1][0][0] >= m[0][0][0] and m[1][1][0] >= m[0][1][0]:
            if m[1][0][0] > m[0][0][0] or m[1][1][0] > m[0][1][0]:
                row_dom = "row 1"
        mat_str = f"[({m[0][0][0]},{m[0][0][1]}),({m[0][1][0]},{m[0][1][1]})];" \
                  f"[({m[1][0][0]},{m[1][0][1]}),({m[1][1][0]},{m[1][1][1]})]"
        return (
            f"row player dominant? matrix: {mat_str}",
            {"matrix": m, "row_dominant": row_dom},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        m = sd["matrix"]
        return [
            f"row 0 payoffs: {m[0][0][0]},{m[0][1][0]}",
            f"row 1 payoffs: {m[1][0][0]},{m[1][1][0]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return sd["row_dominant"] if sd["row_dominant"] else "none"


@register
class NashEquilibriumGenerator(StepGenerator):
    """Find Nash equilibria in a 2x2 game."""

    @property
    def task_name(self) -> str:
        return "nash_equilibrium"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["dominant_strategy"]

    def task_description(self, difficulty: int) -> str:
        return "find Nash equilibrium"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        m = [[(self._rng.randint(0, 10), self._rng.randint(0, 10)) for _ in range(2)] for _ in range(2)]
        ne = []
        for r in range(2):
            for c in range(2):
                row_best = m[r][c][0] >= m[1 - r][c][0]
                col_best = m[r][c][1] >= m[r][1 - c][1]
                if row_best and col_best:
                    ne.append((r, c))
        mat_str = f"[({m[0][0][0]},{m[0][0][1]}),({m[0][1][0]},{m[0][1][1]})];" \
                  f"[({m[1][0][0]},{m[1][0][1]}),({m[1][1][0]},{m[1][1][1]})]"
        return mat_str, {"matrix": m, "ne": ne}

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for r in range(2):
            for c in range(2):
                steps.append(f"({r},{c}): check best responses")
        return steps

    def _create_answer(self, sd: dict) -> str:
        if not sd["ne"]:
            return "no pure NE"
        return ", ".join(f"({r},{c})" for r, c in sd["ne"])


@register
class MinimaxGenerator(StepGenerator):
    """Find the minimax value of a zero-sum game."""

    @property
    def task_name(self) -> str:
        return "minimax"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["payoff_matrix"]

    def task_description(self, difficulty: int) -> str:
        return "find minimax value"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(2 + difficulty // 2, 4)
        matrix = [[self._rng.randint(-5, 10) for _ in range(n)] for _ in range(n)]
        row_mins = [min(row) for row in matrix]
        maximin = max(row_mins)
        col_maxs = [max(matrix[r][c] for r in range(n)) for c in range(n)]
        minimax = min(col_maxs)
        mat_str = "; ".join("[" + ",".join(str(v) for v in row) + "]" for row in matrix)
        return (
            f"zero-sum: {mat_str}",
            {"matrix": matrix, "maximin": maximin, "minimax": minimax},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"row mins: {[min(row) for row in sd['matrix']]}",
            f"maximin = {sd['maximin']}",
            f"col maxs: {[max(sd['matrix'][r][c] for r in range(len(sd['matrix']))) for c in range(len(sd['matrix'][0]))]}",
            f"minimax = {sd['minimax']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"maximin={sd['maximin']}, minimax={sd['minimax']}"


# ═══════════════════════════════════════════════════════════════════
# AUTOMATA (3 generators, tiers 3-4)
# ═══════════════════════════════════════════════════════════════════

@register
class DFAAcceptGenerator(StepGenerator):
    """Simulate a DFA on an input string."""

    @property
    def task_name(self) -> str:
        return "dfa_accept"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["boolean_eval"]

    def task_description(self, difficulty: int) -> str:
        return "simulate DFA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_states = min(3 + difficulty // 2, 6)
        accept_states = {self._rng.randint(1, n_states - 1)}
        transitions = {}
        for s in range(n_states):
            for sym in "01":
                transitions[(s, sym)] = self._rng.randint(0, n_states - 1)
        length = min(3 + difficulty, 10)
        input_str = "".join(self._rng.choice("01") for _ in range(length))
        state = 0
        trace = [state]
        for sym in input_str:
            state = transitions[(state, sym)]
            trace.append(state)
        accepted = state in accept_states
        trans_str = "; ".join(f"({s},{sym})->{transitions[(s,sym)]}" for s in range(n_states) for sym in "01")
        return (
            f"states=0..{n_states-1}, accept={accept_states}, input='{input_str}', transitions: {trans_str}",
            {"input": input_str, "trace": trace, "accepted": accepted, "accept_states": accept_states},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i, sym in enumerate(sd["input"]):
            steps.append(f"state {sd['trace'][i]} + '{sym}' -> state {sd['trace'][i+1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "ACCEPT" if sd["accepted"] else "REJECT"


@register
class NFASimulateGenerator(StepGenerator):
    """Simulate an NFA (track set of states)."""

    @property
    def task_name(self) -> str:
        return "nfa_simulate"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["dfa_accept", "set_union"]

    def task_description(self, difficulty: int) -> str:
        return "simulate NFA"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n_states = min(3 + difficulty // 2, 5)
        accept_states = {self._rng.randint(1, n_states - 1)}
        transitions = {}
        for s in range(n_states):
            for sym in "01":
                n_targets = self._rng.randint(0, 2)
                transitions[(s, sym)] = set(self._rng.sample(range(n_states), min(n_targets, n_states)))
        length = min(2 + difficulty, 6)
        input_str = "".join(self._rng.choice("01") for _ in range(length))
        current = {0}
        trace = [frozenset(current)]
        for sym in input_str:
            nxt = set()
            for s in current:
                nxt |= transitions.get((s, sym), set())
            current = nxt
            trace.append(frozenset(current))
        accepted = bool(current & accept_states)
        return (
            f"NFA: states=0..{n_states-1}, accept={accept_states}, input='{input_str}'",
            {"input": input_str, "trace": [set(t) for t in trace], "accepted": accepted},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        steps = []
        for i, sym in enumerate(sd["input"]):
            steps.append(f"{sd['trace'][i]} + '{sym}' -> {sd['trace'][i+1]}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        return "ACCEPT" if sd["accepted"] else "REJECT"


@register
class TuringMachineStepGenerator(StepGenerator):
    """Execute steps of a simple Turing machine."""

    @property
    def task_name(self) -> str:
        return "turing_machine_step"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["dfa_accept"]

    def task_description(self, difficulty: int) -> str:
        return "execute Turing machine steps"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        tape = list("".join(self._rng.choice("01") for _ in range(min(5 + difficulty, 10))))
        rules = {
            ("q0", "0"): ("q0", "1", "R"),
            ("q0", "1"): ("q1", "0", "R"),
            ("q1", "0"): ("q1", "0", "R"),
            ("q1", "1"): ("q0", "1", "L"),
            ("q0", "_"): ("halt", "_", "S"),
            ("q1", "_"): ("halt", "_", "S"),
        }
        state = "q0"
        head = 0
        n_steps = min(3 + difficulty, 8)
        steps_log = []
        for _ in range(n_steps):
            sym = tape[head] if head < len(tape) else "_"
            if (state, sym) not in rules:
                break
            new_state, write, move = rules[(state, sym)]
            if head < len(tape):
                tape[head] = write
            steps_log.append(f"({state},{sym})->({new_state},{write},{move})")
            state = new_state
            if move == "R":
                head += 1
            elif move == "L":
                head = max(0, head - 1)
            if state == "halt":
                break
        return (
            f"tape={''.join(tape[:10])}, run {n_steps} steps",
            {"tape": "".join(tape[:10]), "steps_log": steps_log, "final_state": state},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        return f"tape={sd['tape']}, state={sd['final_state']}"


# ═══════════════════════════════════════════════════════════════════
# SPATIAL REASONING (3 generators, tiers 2-4)
# ═══════════════════════════════════════════════════════════════════

@register
class BoundingBoxGenerator(StepGenerator):
    """Find the axis-aligned bounding box of a point set."""

    @property
    def task_name(self) -> str:
        return "bounding_box"

    @property
    def tier(self) -> int:
        return 2

    @property
    def prerequisites(self) -> list[str]:
        return ["subtraction"]

    def task_description(self, difficulty: int) -> str:
        return "find bounding box"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(3 + difficulty * 2, 12)
        r = 10 * difficulty
        pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
        min_x = min(x for x, y in pts)
        max_x = max(x for x, y in pts)
        min_y = min(y for x, y in pts)
        max_y = max(y for x, y in pts)
        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return pts_str, {"min_x": min_x, "max_x": max_x, "min_y": min_y, "max_y": max_y}

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"x range: [{sd['min_x']}, {sd['max_x']}]",
            f"y range: [{sd['min_y']}, {sd['max_y']}]",
        ]

    def _create_answer(self, sd: dict) -> str:
        w = sd["max_x"] - sd["min_x"]
        h = sd["max_y"] - sd["min_y"]
        return f"[{sd['min_x']},{sd['min_y']}]-[{sd['max_x']},{sd['max_y']}] ({w}×{h})"


@register
class PointInPolygonGenerator(StepGenerator):
    """Test if a point is inside a convex polygon."""

    @property
    def task_name(self) -> str:
        return "point_in_polygon"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["line_intersection"]

    def task_description(self, difficulty: int) -> str:
        return "point in polygon test"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        r = 5 * difficulty
        n = min(3 + difficulty, 6)
        angles = sorted(self._rng.uniform(0, 2 * math.pi) for _ in range(n))
        poly = [(round(r * math.cos(a)), round(r * math.sin(a))) for a in angles]

        if self._rng.random() < 0.5:
            px = self._rng.randint(-r // 3, r // 3)
            py = self._rng.randint(-r // 3, r // 3)
        else:
            px = r * 2
            py = r * 2

        crossings = 0
        for i in range(n):
            x1, y1 = poly[i]
            x2, y2 = poly[(i + 1) % n]
            if (y1 <= py < y2 or y2 <= py < y1):
                xint = x1 + (py - y1) * (x2 - x1) / (y2 - y1 + 1e-10)
                if px < xint:
                    crossings += 1
        inside = crossings % 2 == 1

        poly_str = " ".join(f"({x},{y})" for x, y in poly)
        return (
            f"point ({px},{py}) in polygon {poly_str}?",
            {"px": px, "py": py, "poly": poly, "inside": inside, "crossings": crossings},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"ray casting: {sd['crossings']} crossings", f"{'odd' if sd['inside'] else 'even'} = {'inside' if sd['inside'] else 'outside'}"]

    def _create_answer(self, sd: dict) -> str:
        return "INSIDE" if sd["inside"] else "OUTSIDE"


@register
class ConvexHullCheckGenerator(StepGenerator):
    """Check if a set of points forms a convex polygon."""

    @property
    def task_name(self) -> str:
        return "convex_hull_check"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["polygon_area"]

    def task_description(self, difficulty: int) -> str:
        return "check convexity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        n = min(4 + difficulty, 8)
        r = 5 * difficulty

        if self._rng.random() < 0.5:
            angles = sorted(self._rng.uniform(0, 2 * math.pi) for _ in range(n))
            pts = [(round(r * math.cos(a)), round(r * math.sin(a))) for a in angles]
            is_convex = True
        else:
            pts = [(self._rng.randint(-r, r), self._rng.randint(-r, r)) for _ in range(n)]
            cross_signs = []
            for i in range(n):
                o = pts[i]
                a = pts[(i + 1) % n]
                b = pts[(i + 2) % n]
                cross = (a[0] - o[0]) * (b[1] - o[1]) - (a[1] - o[1]) * (b[0] - o[0])
                cross_signs.append(cross > 0)
            is_convex = len(set(cross_signs)) <= 1

        pts_str = " ".join(f"({x},{y})" for x, y in pts)
        return f"convex? {pts_str}", {"pts": pts, "is_convex": is_convex}

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"check cross products of consecutive edges"]

    def _create_answer(self, sd: dict) -> str:
        return "CONVEX" if sd["is_convex"] else "NOT CONVEX"


# ═══════════════════════════════════════════════════════════════════
# NUMERICAL METHODS (4 generators, tiers 3-4)
# ═══════════════════════════════════════════════════════════════════

@register
class BisectionMethodGenerator(StepGenerator):
    """Find a root using the bisection method."""

    @property
    def task_name(self) -> str:
        return "bisection_method"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        return "bisection method step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        root = self._rng.randint(1, 10 * difficulty)
        a = root - self._rng.randint(1, 5)
        b = root + self._rng.randint(1, 5)
        n_steps = min(2 + difficulty, 6)
        steps_log = []
        for _ in range(n_steps):
            mid = (a + b) / 2
            f_mid = mid - root
            steps_log.append(f"[{a:.2f},{b:.2f}] mid={mid:.2f} f(mid)={f_mid:.2f}")
            if f_mid > 0:
                b = mid
            else:
                a = mid
        final = round((a + b) / 2, 4)
        return (
            f"f(x) = x - {root}, interval [{a:.2f},{b:.2f}], {n_steps} steps",
            {"root": root, "steps_log": steps_log, "final": final},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return sd["steps_log"]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['final']}"


@register
class TrapezoidalRuleGenerator(StepGenerator):
    """Approximate an integral using the trapezoidal rule."""

    @property
    def task_name(self) -> str:
        return "trapezoidal_rule"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["area_rectangle"]

    def task_description(self, difficulty: int) -> str:
        return "trapezoidal rule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        a_val = self._rng.randint(0, 3)
        b_val = a_val + self._rng.randint(1, 3 + difficulty)
        n = min(2 + difficulty, 8)
        h = (b_val - a_val) / n
        xs = [a_val + i * h for i in range(n + 1)]
        fn_type = self._rng.choice(["x^2", "x^3", "x"])
        if fn_type == "x^2":
            fxs = [x ** 2 for x in xs]
        elif fn_type == "x^3":
            fxs = [x ** 3 for x in xs]
        else:
            fxs = [x for x in xs]
        integral = h / 2 * (fxs[0] + fxs[-1] + 2 * sum(fxs[1:-1]))
        return (
            f"integral of {fn_type} from {a_val} to {b_val}, n={n}",
            {"fn": fn_type, "a": a_val, "b": b_val, "n": n, "h": h,
             "xs": xs, "fxs": fxs, "integral": round(integral, 4)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"h = ({sd['b']}-{sd['a']})/{sd['n']} = {sd['h']:.4f}",
            f"f values: {[round(f, 2) for f in sd['fxs']]}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['integral']}"


@register
class EulerMethodODEGenerator(StepGenerator):
    """Take Euler method steps for a simple ODE."""

    @property
    def task_name(self) -> str:
        return "euler_method_ode"

    @property
    def tier(self) -> int:
        return 4

    @property
    def prerequisites(self) -> list[str]:
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        return "Euler method step"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        y0 = round(self._rng.uniform(0.5, 3.0), 1)
        h = round(self._rng.choice([0.1, 0.2, 0.5]), 2)
        n_steps = min(3 + difficulty, 8)
        ode = self._rng.choice(["y", "-y", "2*y", "x+y"])
        x, y = 0.0, y0
        trace = [(round(x, 4), round(y, 4))]
        for _ in range(n_steps):
            if ode == "y":
                dy = y
            elif ode == "-y":
                dy = -y
            elif ode == "2*y":
                dy = 2 * y
            else:
                dy = x + y
            y = y + h * dy
            x = x + h
            trace.append((round(x, 4), round(y, 4)))
        return (
            f"dy/dx = {ode}, y(0)={y0}, h={h}, {n_steps} steps",
            {"ode": ode, "y0": y0, "h": h, "trace": trace},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [f"x={x}, y={y}" for x, y in sd["trace"]]

    def _create_answer(self, sd: dict) -> str:
        x, y = sd["trace"][-1]
        return f"y({x}) = {y}"


@register
class NumericalDerivativeGenerator(StepGenerator):
    """Approximate a derivative using finite differences."""

    @property
    def task_name(self) -> str:
        return "numerical_derivative"

    @property
    def tier(self) -> int:
        return 3

    @property
    def prerequisites(self) -> list[str]:
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        return "numerical derivative"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        fn = self._rng.choice(["x^2", "x^3", "sin(x)"])
        x = round(self._rng.uniform(0.5, 5.0), 2)
        h = round(10 ** (-self._rng.randint(1, min(4, 1 + difficulty))), 6)

        if fn == "x^2":
            f = lambda v: v ** 2
            exact = 2 * x
        elif fn == "x^3":
            f = lambda v: v ** 3
            exact = 3 * x ** 2
        else:
            f = lambda v: math.sin(v)
            exact = math.cos(x)

        central = (f(x + h) - f(x - h)) / (2 * h)
        error = abs(central - exact)
        return (
            f"d/dx({fn}) at x={x}, h={h}",
            {"fn": fn, "x": x, "h": h, "approx": round(central, 6),
             "exact": round(exact, 6), "error": round(error, 8)},
        )

    def _create_steps(self, sd: dict) -> list[str]:
        return [
            f"central diff: (f(x+h) - f(x-h)) / (2h)",
            f"approx = {sd['approx']}",
            f"exact = {sd['exact']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        return f"{sd['approx']} (error={sd['error']})"
