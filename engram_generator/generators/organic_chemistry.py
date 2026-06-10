"""Organic chemistry generators -- IUPAC naming, functional groups, reactions.

8 generators across tiers 4-6.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


class OrganicChemistryBase(StepGenerator):
    """Base class for organic chemistry generators with shared data.

    Provides common alkane names, functional group tables, and molecular
    formula utilities used across multiple organic chemistry generators.

    Attributes:
        ALKANE_NAMES: Mapping of carbon count to IUPAC alkane name.
        BRANCH_NAMES: Mapping of carbon count to branch substituent name.
        FUNCTIONAL_GROUPS: Mapping of structural markers to group names.
    """

    ALKANE_NAMES = {
        1: "methane", 2: "ethane", 3: "propane", 4: "butane",
        5: "pentane", 6: "hexane", 7: "heptane", 8: "octane",
        9: "nonane", 10: "decane",
    }

    ALKANE_PREFIXES = {
        1: "meth", 2: "eth", 3: "prop", 4: "but",
        5: "pent", 6: "hex", 7: "hept", 8: "oct",
        9: "non", 10: "dec",
    }

    BRANCH_NAMES = {1: "methyl", 2: "ethyl", 3: "propyl"}

    FUNCTIONAL_GROUPS = {
        "-OH": "alcohol (hydroxyl)",
        "-COOH": "carboxylic acid",
        "-NH2": "amine",
        "C=O (ketone)": "ketone (carbonyl)",
        "C=O (aldehyde)": "aldehyde (carbonyl)",
        "-O-": "ether",
        "-COO-": "ester",
        "-CONH2": "amide",
        "-SH": "thiol",
        "-X (halide)": "alkyl halide",
    }


@register
class IupacNamingGenerator(OrganicChemistryBase):
    """Name a simple alkane from carbon count and branch positions.

    At low difficulty, produces straight-chain alkanes (methane through
    decane). At higher difficulty, adds methyl or ethyl branches at
    valid positions along the main chain.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "iupac_naming"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "name the alkane using IUPAC nomenclature"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IUPAC naming problem.

        At difficulty 1-3, produces straight-chain alkanes. At 4+,
        adds one or two branch substituents at valid positions.

        Args:
            difficulty: Controls chain length and branch complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        main_chain = self._rng.randint(
            max(1, difficulty), min(10, 3 + difficulty),
        )

        branches: list[tuple[int, int]] = []
        if difficulty >= 4 and main_chain >= 3:
            num_branches = 1 if difficulty < 6 else self._rng.randint(1, 2)
            valid_positions = list(range(2, main_chain))
            if valid_positions:
                chosen_positions = self._rng.sample(
                    valid_positions, min(num_branches, len(valid_positions)),
                )
                for pos in sorted(chosen_positions):
                    branch_c = 1 if difficulty < 7 else self._rng.choice([1, 2])
                    branches.append((pos, branch_c))

        if branches:
            branch_strs = []
            for pos, bc in branches:
                branch_strs.append(f"{self.BRANCH_NAMES[bc]} at C-{pos}")
            desc = (
                f"{main_chain}-carbon main chain with "
                f"{', '.join(branch_strs)}"
            )
        else:
            desc = f"straight-chain alkane with {main_chain} carbons"

        # Build IUPAC name
        if not branches:
            name = self.ALKANE_NAMES[main_chain]
        else:
            # Group branches by type
            branch_groups: dict[int, list[int]] = {}
            for pos, bc in branches:
                branch_groups.setdefault(bc, []).append(pos)

            prefix_parts = []
            multi = {2: "di", 3: "tri"}
            for bc in sorted(branch_groups.keys()):
                positions = sorted(branch_groups[bc])
                pos_str = ",".join(str(p) for p in positions)
                multiplier = multi.get(len(positions), "")
                prefix_parts.append(
                    f"{pos_str}-{multiplier}{self.BRANCH_NAMES[bc]}"
                )
            prefix = "-".join(prefix_parts)
            base = self.ALKANE_PREFIXES[main_chain] + "ane"
            name = f"{prefix}{base}"

        return desc, {
            "main_chain": main_chain,
            "branches": branches,
            "name": name,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data from _create_problem.

        Returns:
            List of step strings.
        """
        steps = [f"main chain: {sd['main_chain']} carbons"]
        if sd["branches"]:
            for pos, bc in sd["branches"]:
                steps.append(f"branch at C-{pos}: {self.BRANCH_NAMES[bc]}")
            steps.append("number from end giving lowest locants")
        else:
            steps.append("no branches, use base alkane name")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the IUPAC name.

        Args:
            sd: Solution data.

        Returns:
            IUPAC name string.
        """
        return sd["name"]


@register
class FunctionalGroupIdGenerator(OrganicChemistryBase):
    """Identify the functional group from a molecular description.

    Given a description mentioning a structural feature (-OH, -COOH,
    -NH2, C=O, etc.), the task is to name the functional group.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "functional_group_id"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["counting"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "identify the functional group in the molecule"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a functional group identification problem.

        Selects one or more functional groups from the table and
        embeds them in a molecular description context.

        Args:
            difficulty: Controls number of groups to identify.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        groups = list(self.FUNCTIONAL_GROUPS.items())
        num_groups = 1 if difficulty < 5 else min(2, len(groups))
        chosen = self._rng.sample(groups, num_groups)

        contexts = [
            "a 4-carbon chain", "a 6-carbon ring", "a 3-carbon chain",
            "a 5-carbon chain", "a branched 4-carbon chain",
            "a 7-carbon chain", "an 8-carbon chain",
        ]
        context = self._rng.choice(contexts)

        markers = [marker for marker, _ in chosen]
        names = [name for _, name in chosen]
        marker_str = " and ".join(markers)
        desc = f"molecule with {context} containing {marker_str}"

        return desc, {"markers": markers, "names": names}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        for marker, name in zip(sd["markers"], sd["names"]):
            steps.append(f"{marker} -> {name}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the functional group name(s).

        Args:
            sd: Solution data.

        Returns:
            Functional group name(s) as a string.
        """
        return ", ".join(sd["names"])


@register
class DegreeUnsaturationGenerator(OrganicChemistryBase):
    """Compute degrees of unsaturation from a molecular formula.

    Uses the formula DoU = (2C + 2 + N - H) / 2 for molecules of the
    form CxHyOzNw. Oxygen does not affect the calculation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "degree_unsaturation"

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
        return "compute degrees of unsaturation for the molecular formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a degree of unsaturation problem.

        Creates a molecular formula CxHyOzNw with controlled atom
        counts, ensuring the DoU is a non-negative integer or half-
        integer.

        Args:
            difficulty: Controls atom count ranges.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        c = self._rng.randint(1, 2 + difficulty)
        n = self._rng.randint(0, min(2, difficulty // 2))
        # Ensure DoU is non-negative: H <= 2C + 2 + N
        max_h = 2 * c + 2 + n
        h = self._rng.randint(max(0, max_h - 2 * difficulty), max_h)
        o = self._rng.randint(0, min(3, difficulty // 2))

        dou_num = 2 * c + 2 + n - h
        dou = dou_num / 2

        # Build formula string
        formula = f"C{c}"
        formula += f"H{h}" if h > 0 else ""
        if o > 0:
            formula += f"O{o}"
        if n > 0:
            formula += f"N{n}"

        dou_display = int(dou) if dou == int(dou) else round(dou, 1)

        return f"degrees of unsaturation for {formula}", {
            "formula": formula, "c": c, "h": h, "o": o, "n": n,
            "dou_num": dou_num, "dou": dou_display,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            "DoU = (2C + 2 + N - H) / 2",
            f"DoU = (2*{sd['c']} + 2 + {sd['n']} - {sd['h']}) / 2",
            f"DoU = {sd['dou_num']} / 2",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the degrees of unsaturation.

        Args:
            sd: Solution data.

        Returns:
            DoU value as a string.
        """
        return f"DoU = {sd['dou']}"


@register
class StereocenterCountGenerator(OrganicChemistryBase):
    """Count stereocenters and compute maximum stereoisomers.

    Given a description of a molecule with chiral centres, counts the
    number of stereocenters n and computes the maximum number of
    stereoisomers as 2^n.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "stereocenter_count"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functional_group_id"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "count stereocenters and maximum stereoisomers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a stereocenter counting problem.

        Creates a molecule description with a specified number of
        chiral carbon centres bearing four different substituents.

        Args:
            difficulty: Controls the number of stereocenters (1-4).

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = self._rng.randint(1, min(4, 1 + difficulty // 2))
        max_isomers = 2 ** n

        substituent_sets = [
            ["-OH", "-CH3", "-H", "-Cl"],
            ["-NH2", "-CH3", "-H", "-Br"],
            ["-OH", "-C2H5", "-H", "-F"],
            ["-COOH", "-CH3", "-H", "-OH"],
            ["-CH3", "-C2H5", "-H", "-Cl"],
        ]

        chain_len = self._rng.randint(n + 2, n + 5)
        descriptions = []
        for i in range(n):
            subs = self._rng.choice(substituent_sets)
            self._rng.shuffle(subs)
            carbon_pos = self._rng.randint(2, chain_len - 1)
            descriptions.append(
                f"C-{carbon_pos} bonded to {', '.join(subs)}"
            )

        desc = (
            f"{chain_len}-carbon chain with {n} chiral "
            f"{'centre' if n == 1 else 'centres'}: "
            + "; ".join(descriptions)
        )

        return desc, {"n": n, "max_isomers": max_isomers, "desc": desc}

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"identify chiral centres with 4 different groups: n = {sd['n']}",
            f"max stereoisomers = 2^n = 2^{sd['n']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the stereocenter count and max stereoisomers.

        Args:
            sd: Solution data.

        Returns:
            Answer string with count and max isomers.
        """
        return (
            f"stereocenters = {sd['n']}, "
            f"max stereoisomers = {sd['max_isomers']}"
        )


@register
class Sn1VsSn2Generator(OrganicChemistryBase):
    """Predict substitution/elimination mechanism from substrate and nucleophile.

    Given substrate type (primary, secondary, tertiary) and nucleophile
    strength (strong/weak), predicts the dominant mechanism: SN1, SN2,
    E1, or E2.
    """

    MECHANISM_TABLE = {
        ("primary", "strong"): "SN2",
        ("primary", "weak"): "SN2",
        ("secondary", "strong"): "E2",
        ("secondary", "weak"): "SN1",
        ("tertiary", "strong"): "E2",
        ("tertiary", "weak"): "SN1",
    }

    NUCLEOPHILES_STRONG = ["NaOH", "NaOCH3", "KCN", "NaI", "NaSH"]
    NUCLEOPHILES_WEAK = ["H2O", "CH3OH", "CH3COOH"]

    SUBSTRATES = {
        "primary": ["1-bromobutane", "1-chloropentane", "ethyl bromide"],
        "secondary": [
            "2-bromobutane", "2-chloropentane", "cyclohexyl bromide",
        ],
        "tertiary": [
            "tert-butyl bromide", "2-bromo-2-methylpropane",
            "tert-butyl chloride",
        ],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sn1_vs_sn2"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functional_group_id"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "predict the substitution or elimination mechanism"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a mechanism prediction problem.

        Selects a substrate type and nucleophile, then looks up the
        expected dominant mechanism from the decision table.

        Args:
            difficulty: Controls variety of substrate types.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 2:
            sub_type = self._rng.choice(["primary", "tertiary"])
        elif difficulty <= 5:
            sub_type = self._rng.choice(
                ["primary", "secondary", "tertiary"],
            )
        else:
            sub_type = self._rng.choice(
                ["primary", "secondary", "tertiary"],
            )

        nuc_strength = self._rng.choice(["strong", "weak"])
        substrate = self._rng.choice(self.SUBSTRATES[sub_type])

        if nuc_strength == "strong":
            nucleophile = self._rng.choice(self.NUCLEOPHILES_STRONG)
        else:
            nucleophile = self._rng.choice(self.NUCLEOPHILES_WEAK)

        mechanism = self.MECHANISM_TABLE[(sub_type, nuc_strength)]

        reasons = {
            "SN2": "backside attack on unhindered carbon",
            "SN1": "stable carbocation forms, weak nucleophile",
            "E2": "strong base removes beta-hydrogen from hindered substrate",
            "E1": "carbocation forms, then elimination",
        }
        reason = reasons[mechanism]

        desc = (
            f"substrate: {substrate} ({sub_type}), "
            f"nucleophile: {nucleophile} ({nuc_strength})"
        )
        return desc, {
            "sub_type": sub_type, "nuc_strength": nuc_strength,
            "substrate": substrate, "nucleophile": nucleophile,
            "mechanism": mechanism, "reason": reason,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"substrate type: {sd['sub_type']}",
            f"nucleophile strength: {sd['nuc_strength']}",
            f"reasoning: {sd['reason']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the predicted mechanism.

        Args:
            sd: Solution data.

        Returns:
            Mechanism name string.
        """
        return sd["mechanism"]


@register
class ReactionProductGenerator(OrganicChemistryBase):
    """Predict the major product of a simple organic reaction.

    Covers three reaction types: electrophilic addition to alkenes,
    elimination reactions, and nucleophilic substitution. Applies
    Markovnikov's rule for addition and Zaitsev's rule for elimination.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reaction_product"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sn1_vs_sn2"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "predict the major product of the reaction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a reaction product prediction problem.

        Selects one of three reaction categories and generates a
        specific scenario with the expected major product.

        Args:
            difficulty: Controls reaction type variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            rxn_type = self._rng.choice(["addition", "substitution"])
        else:
            rxn_type = self._rng.choice(
                ["addition", "elimination", "substitution"],
            )

        if rxn_type == "addition":
            return self._addition_problem(difficulty)
        elif rxn_type == "elimination":
            return self._elimination_problem(difficulty)
        else:
            return self._substitution_problem(difficulty)

    def _addition_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an electrophilic addition problem.

        HX adds across a double bond following Markovnikov's rule.

        Args:
            difficulty: Controls alkene size.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        alkenes = [
            ("propene", "2-bromopropane", "HBr", "Markovnikov"),
            ("but-1-ene", "2-bromobutane", "HBr", "Markovnikov"),
            ("propene", "2-chloropropane", "HCl", "Markovnikov"),
            ("but-2-ene", "2-bromobutane", "HBr", "symmetric addition"),
            ("pent-1-ene", "2-bromopentane", "HBr", "Markovnikov"),
        ]
        pool = alkenes[: min(len(alkenes), 2 + difficulty)]
        alkene, product, reagent, rule = self._rng.choice(pool)

        desc = f"{alkene} + {reagent}"
        return desc, {
            "rxn_type": "addition", "substrate": alkene,
            "reagent": reagent, "product": product, "rule": rule,
        }

    def _elimination_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an elimination reaction problem.

        Strong base causes elimination following Zaitsev's rule
        (more substituted alkene is the major product).

        Args:
            difficulty: Controls substrate variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        scenarios = [
            ("2-bromobutane", "NaOCH3", "but-2-ene", "Zaitsev"),
            ("2-bromopentane", "KOH", "pent-2-ene", "Zaitsev"),
            ("2-chloro-2-methylbutane", "NaOEt", "2-methylbut-2-ene",
             "Zaitsev"),
        ]
        pool = scenarios[: min(len(scenarios), 1 + difficulty // 2)]
        substrate, base, product, rule = self._rng.choice(pool)

        desc = f"{substrate} + {base} (heat)"
        return desc, {
            "rxn_type": "elimination", "substrate": substrate,
            "reagent": base, "product": product, "rule": rule,
        }

    def _substitution_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a nucleophilic substitution problem.

        Strong nucleophile displaces a leaving group on a primary
        substrate via SN2.

        Args:
            difficulty: Controls scenario variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        scenarios = [
            ("1-bromobutane", "NaOH", "1-butanol", "SN2"),
            ("ethyl bromide", "NaCN", "propanenitrile", "SN2"),
            ("1-chloropentane", "NaI", "1-iodopentane", "SN2"),
        ]
        pool = scenarios[: min(len(scenarios), 1 + difficulty // 2)]
        substrate, nuc, product, mech = self._rng.choice(pool)

        desc = f"{substrate} + {nuc}"
        return desc, {
            "rxn_type": "substitution", "substrate": substrate,
            "reagent": nuc, "product": product, "rule": mech,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"reaction type: {sd['rxn_type']}",
            f"substrate: {sd['substrate']} + {sd['reagent']}",
            f"rule applied: {sd['rule']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the major product.

        Args:
            sd: Solution data.

        Returns:
            Product name string.
        """
        return f"major product: {sd['product']}"


@register
class PolymerRepeatUnitGenerator(OrganicChemistryBase):
    """Identify the repeat unit and polymerisation type from a monomer.

    Given a monomer structure, determines whether the polymer forms
    by addition or condensation polymerisation and identifies the
    repeat unit.
    """

    MONOMERS = [
        ("ethylene (CH2=CH2)", "-CH2-CH2-", "addition"),
        ("propylene (CH2=CHCH3)", "-CH2-CH(CH3)-", "addition"),
        ("vinyl chloride (CH2=CHCl)", "-CH2-CHCl-", "addition"),
        ("styrene (CH2=CHC6H5)", "-CH2-CH(C6H5)-", "addition"),
        ("tetrafluoroethylene (CF2=CF2)", "-CF2-CF2-", "addition"),
        ("amino acid (H2N-R-COOH)", "-NH-R-CO-", "condensation"),
        ("ethylene glycol + terephthalic acid",
         "-O-CH2CH2-O-CO-C6H4-CO-", "condensation"),
        ("lactic acid (HO-CH(CH3)-COOH)", "-O-CH(CH3)-CO-",
         "condensation"),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "polymer_repeat_unit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["functional_group_id"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "identify the repeat unit and polymerisation type"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a polymer repeat unit identification problem.

        Selects a monomer from the table and asks for the repeat
        unit structure and polymerisation mechanism.

        Args:
            difficulty: Controls pool size of available monomers.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.MONOMERS[: min(len(self.MONOMERS), 3 + difficulty)]
        monomer, repeat_unit, poly_type = self._rng.choice(pool)

        return f"monomer: {monomer}", {
            "monomer": monomer,
            "repeat_unit": repeat_unit,
            "poly_type": poly_type,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        if sd["poly_type"] == "addition":
            mechanism = "double bond opens to form single bonds"
        else:
            mechanism = "small molecule (H2O) lost between monomers"
        return [
            f"monomer: {sd['monomer']}",
            f"mechanism: {mechanism}",
            f"repeat unit: {sd['repeat_unit']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the repeat unit and polymerisation type.

        Args:
            sd: Solution data.

        Returns:
            Answer string with repeat unit and type.
        """
        return (
            f"repeat unit: {sd['repeat_unit']}, "
            f"type: {sd['poly_type']} polymerisation"
        )


@register
class IsomerCountGenerator(OrganicChemistryBase):
    """Count structural isomers for small molecular formulae.

    Uses a lookup table of known structural isomer counts for common
    small organic molecules (C3H8O, C4H10, C4H10O, C5H12, etc.).
    """

    ISOMER_DATA = [
        ("C2H6O", 2, ["ethanol", "dimethyl ether"]),
        ("C3H8O", 3, ["1-propanol", "2-propanol", "methyl ethyl ether"]),
        ("C3H8", 1, ["propane"]),
        ("C4H10", 2, ["butane", "isobutane"]),
        ("C4H10O", 4,
         ["1-butanol", "2-butanol", "isobutanol", "diethyl ether"]),
        ("C5H12", 3, ["pentane", "isopentane", "neopentane"]),
        ("C3H6O", 3, ["propanal", "acetone", "allyl alcohol"]),
        ("C2H4O2", 3,
         ["acetic acid", "methyl formate", "glycolaldehyde"]),
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "isomer_count"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["degree_unsaturation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "count the structural isomers for the molecular formula"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a structural isomer counting problem.

        Selects a molecular formula from the lookup table and asks
        for the number of structural isomers.

        Args:
            difficulty: Controls which formulae are available.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.ISOMER_DATA[
            : min(len(self.ISOMER_DATA), 2 + difficulty)
        ]
        formula, count, names = self._rng.choice(pool)

        return f"how many structural isomers for {formula}?", {
            "formula": formula,
            "count": count,
            "names": names,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"formula: {sd['formula']}"]
        for i, name in enumerate(sd["names"], 1):
            steps.append(f"isomer {i}: {name}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the isomer count.

        Args:
            sd: Solution data.

        Returns:
            Count as a string.
        """
        return f"{sd['count']} structural isomers"
