"""Extended organic chemistry generators -- reaction mechanisms.

8 generators across tiers 5-7 covering Markovnikov/Zaitsev rules,
Grignard reactions, oxidation/reduction, EAS, Fischer projections,
retrosynthesis, and spectroscopy interpretation.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Markovnikov Rule (tier 5)
# ---------------------------------------------------------------------------

@register
class MarkovnikovRuleGenerator(StepGenerator):
    """Apply Markovnikov's rule to HX addition to an alkene.

    Given an asymmetric alkene and HX, determines which carbon the H
    attaches to (the one with more existing H atoms) and identifies
    the major product carbon for X attachment.
    """

    ALKENES = [
        {
            "name": "propene",
            "formula": "CH3-CH=CH2",
            "hx": "HBr",
            "h_carbon": "C3 (CH2, 2 H's)",
            "x_carbon": "C2 (CH, 1 H)",
            "product": "2-bromopropane",
            "reason": "C3 has more H -> H adds there, Br to C2",
        },
        {
            "name": "but-1-ene",
            "formula": "CH3CH2-CH=CH2",
            "hx": "HBr",
            "h_carbon": "C4 (CH2, 2 H's)",
            "x_carbon": "C3 (CH, 1 H)",
            "product": "2-bromobutane",
            "reason": "C4 has more H -> H adds there, Br to C3",
        },
        {
            "name": "propene",
            "formula": "CH3-CH=CH2",
            "hx": "HCl",
            "h_carbon": "C3 (CH2, 2 H's)",
            "x_carbon": "C2 (CH, 1 H)",
            "product": "2-chloropropane",
            "reason": "C3 has more H -> H adds there, Cl to C2",
        },
        {
            "name": "2-methylpropene",
            "formula": "(CH3)2C=CH2",
            "hx": "HBr",
            "h_carbon": "C3 (CH2, 2 H's)",
            "x_carbon": "C2 (tertiary)",
            "product": "2-bromo-2-methylpropane",
            "reason": "H to less substituted C, Br to more substituted C",
        },
        {
            "name": "pent-1-ene",
            "formula": "CH3CH2CH2-CH=CH2",
            "hx": "HCl",
            "h_carbon": "C5 (CH2, 2 H's)",
            "x_carbon": "C4 (CH, 1 H)",
            "product": "2-chloropentane",
            "reason": "C5 has more H -> H adds there, Cl to C4",
        },
        {
            "name": "styrene",
            "formula": "C6H5-CH=CH2",
            "hx": "HBr",
            "h_carbon": "C2 (CH2, 2 H's)",
            "x_carbon": "C1 (benzylic, stabilised)",
            "product": "1-bromo-1-phenylethane",
            "reason": "benzylic carbocation stabilised by resonance",
        },
        {
            "name": "but-1-ene",
            "formula": "CH3CH2-CH=CH2",
            "hx": "HCl",
            "h_carbon": "C4 (CH2, 2 H's)",
            "x_carbon": "C3 (CH, 1 H)",
            "product": "2-chlorobutane",
            "reason": "C4 has more H -> H adds there, Cl to C3",
        },
        {
            "name": "2-methylbut-1-ene",
            "formula": "CH3CH2C(CH3)=CH2",
            "hx": "HBr",
            "h_carbon": "terminal CH2",
            "x_carbon": "C2 (tertiary)",
            "product": "2-bromo-2-methylbutane",
            "reason": "H to less substituted, Br to tertiary carbon",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "markovnikov_rule"

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
        return "apply Markovnikov's rule to predict the major product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Markovnikov addition problem.

        Args:
            difficulty: Controls pool of available alkenes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.ALKENES[: min(len(self.ALKENES), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = f"{entry['name']} ({entry['formula']}) + {entry['hx']}"
        return problem, {
            "alkene": entry["name"], "hx": entry["hx"],
            "h_carbon": entry["h_carbon"],
            "x_carbon": entry["x_carbon"],
            "product": entry["product"],
            "reason": entry["reason"],
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"identify double bond in {sd['alkene']}",
            f"H adds to {sd['h_carbon']} (more H's)",
            f"X adds to {sd['x_carbon']}",
            f"reason: {sd['reason']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the major product.

        Args:
            sd: Solution data.

        Returns:
            Product name string.
        """
        return f"major product: {sd['product']}"


# ---------------------------------------------------------------------------
# 2. Zaitsev Rule (tier 5)
# ---------------------------------------------------------------------------

@register
class ZaitsevRuleGenerator(StepGenerator):
    """Apply Zaitsev's rule to predict the major E2 elimination product.

    Given a substrate and strong base, identifies all possible alkene
    products and selects the most substituted one as the major product.
    """

    SCENARIOS = [
        {
            "substrate": "2-bromobutane",
            "base": "NaOEt",
            "possible": ["but-1-ene (monosubstituted)", "but-2-ene (disubstituted)"],
            "major": "but-2-ene",
            "sub_count": "disubstituted (2 alkyl groups on C=C)",
        },
        {
            "substrate": "2-bromopentane",
            "base": "KOH",
            "possible": ["pent-1-ene (monosubstituted)", "pent-2-ene (disubstituted)"],
            "major": "pent-2-ene",
            "sub_count": "disubstituted",
        },
        {
            "substrate": "2-bromo-2-methylbutane",
            "base": "NaOEt",
            "possible": ["2-methylbut-1-ene (disubstituted)", "2-methylbut-2-ene (trisubstituted)"],
            "major": "2-methylbut-2-ene",
            "sub_count": "trisubstituted",
        },
        {
            "substrate": "3-bromopentane",
            "base": "KOtBu",
            "possible": ["pent-2-ene (disubstituted)"],
            "major": "pent-2-ene",
            "sub_count": "disubstituted (symmetric elimination)",
        },
        {
            "substrate": "2-chloro-2-methylpentane",
            "base": "NaOEt",
            "possible": ["2-methylpent-1-ene (di)", "2-methylpent-2-ene (tri)"],
            "major": "2-methylpent-2-ene",
            "sub_count": "trisubstituted",
        },
        {
            "substrate": "2-bromo-3-methylbutane",
            "base": "NaOEt",
            "possible": ["3-methylbut-1-ene (mono)", "2-methylbut-2-ene (tri)"],
            "major": "2-methylbut-2-ene",
            "sub_count": "trisubstituted",
        },
        {
            "substrate": "2-bromohexane",
            "base": "KOH",
            "possible": ["hex-1-ene (mono)", "hex-2-ene (di)"],
            "major": "hex-2-ene",
            "sub_count": "disubstituted",
        },
        {
            "substrate": "3-bromo-2-methylpentane",
            "base": "NaOEt",
            "possible": ["2-methylpent-2-ene (tri)", "2-methylpent-3-ene (di)"],
            "major": "2-methylpent-2-ene",
            "sub_count": "trisubstituted",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "zaitsev_rule"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

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
        return "apply Zaitsev's rule to predict the major elimination product"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Zaitsev elimination problem.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.SCENARIOS[: min(len(self.SCENARIOS), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = f"{entry['substrate']} + {entry['base']} (E2)"
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"substrate: {sd['substrate']}, base: {sd['base']}",
            "identify all possible beta-hydrogens",
        ]
        for p in sd["possible"]:
            steps.append(f"  possible product: {p}")
        steps.append(f"Zaitsev: most substituted = {sd['sub_count']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the major product.

        Args:
            sd: Solution data.

        Returns:
            Major product string.
        """
        return f"major product: {sd['major']}"


# ---------------------------------------------------------------------------
# 3. Grignard Reaction (tier 6)
# ---------------------------------------------------------------------------

@register
class GrignardReactionGenerator(StepGenerator):
    """Predict the product of a Grignard reaction.

    RMgBr reacts with a carbonyl compound: aldehyde gives secondary
    alcohol, ketone gives tertiary alcohol, CO2 gives carboxylic acid.
    """

    SCENARIOS = [
        {
            "grignard": "CH3MgBr",
            "carbonyl": "formaldehyde (HCHO)",
            "carbonyl_type": "aldehyde",
            "product": "ethanol (primary alcohol)",
            "mechanism": "R attacks C=O, then acid workup",
        },
        {
            "grignard": "CH3MgBr",
            "carbonyl": "acetaldehyde (CH3CHO)",
            "carbonyl_type": "aldehyde",
            "product": "2-propanol (secondary alcohol)",
            "mechanism": "R attacks aldehyde C -> secondary alkoxide",
        },
        {
            "grignard": "CH3MgBr",
            "carbonyl": "acetone ((CH3)2CO)",
            "carbonyl_type": "ketone",
            "product": "2-methyl-2-propanol (tertiary alcohol)",
            "mechanism": "R attacks ketone C -> tertiary alkoxide",
        },
        {
            "grignard": "C2H5MgBr",
            "carbonyl": "acetaldehyde (CH3CHO)",
            "carbonyl_type": "aldehyde",
            "product": "2-butanol (secondary alcohol)",
            "mechanism": "ethyl attacks aldehyde C -> secondary alkoxide",
        },
        {
            "grignard": "CH3MgBr",
            "carbonyl": "CO2",
            "carbonyl_type": "carbon dioxide",
            "product": "acetic acid (carboxylic acid)",
            "mechanism": "R attacks CO2 -> carboxylate, then acid workup",
        },
        {
            "grignard": "C6H5MgBr",
            "carbonyl": "CO2",
            "carbonyl_type": "carbon dioxide",
            "product": "benzoic acid",
            "mechanism": "phenyl attacks CO2 -> carboxylate",
        },
        {
            "grignard": "C2H5MgBr",
            "carbonyl": "acetone ((CH3)2CO)",
            "carbonyl_type": "ketone",
            "product": "2-methyl-2-butanol (tertiary alcohol)",
            "mechanism": "ethyl attacks ketone C -> tertiary alkoxide",
        },
        {
            "grignard": "CH3MgBr",
            "carbonyl": "benzaldehyde (C6H5CHO)",
            "carbonyl_type": "aldehyde",
            "product": "1-phenylethanol (secondary alcohol)",
            "mechanism": "methyl attacks aldehyde C -> secondary alkoxide",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "grignard_reaction"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "predict the product of the Grignard reaction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Grignard reaction problem.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.SCENARIOS[: min(len(self.SCENARIOS), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = f"{entry['grignard']} + {entry['carbonyl']}"
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"Grignard reagent: {sd['grignard']}",
            f"carbonyl: {sd['carbonyl']} ({sd['carbonyl_type']})",
            f"mechanism: {sd['mechanism']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the product.

        Args:
            sd: Solution data.

        Returns:
            Product string.
        """
        return f"product: {sd['product']}"


# ---------------------------------------------------------------------------
# 4. Oxidation / Reduction (tier 5)
# ---------------------------------------------------------------------------

@register
class OxidationReductionOrganicGenerator(StepGenerator):
    """Predict the product of organic oxidation or reduction.

    Covers: primary alcohol to aldehyde (PCC) or carboxylic acid
    (KMnO4/CrO3), ketone to secondary alcohol (NaBH4/LiAlH4),
    and aldehyde to carboxylic acid.
    """

    REACTIONS = [
        {
            "substrate": "1-propanol (primary alcohol)",
            "reagent": "PCC (mild oxidation)",
            "rxn_type": "oxidation",
            "product": "propanal (aldehyde)",
            "rule": "PCC oxidises primary alcohol to aldehyde only",
        },
        {
            "substrate": "1-propanol (primary alcohol)",
            "reagent": "KMnO4 (strong oxidation)",
            "rxn_type": "oxidation",
            "product": "propanoic acid (carboxylic acid)",
            "rule": "strong oxidant goes all the way to carboxylic acid",
        },
        {
            "substrate": "acetone (ketone)",
            "reagent": "NaBH4 (reduction)",
            "rxn_type": "reduction",
            "product": "2-propanol (secondary alcohol)",
            "rule": "NaBH4 reduces ketone to secondary alcohol",
        },
        {
            "substrate": "butanal (aldehyde)",
            "reagent": "KMnO4 (oxidation)",
            "rxn_type": "oxidation",
            "product": "butanoic acid (carboxylic acid)",
            "rule": "aldehyde easily oxidised to carboxylic acid",
        },
        {
            "substrate": "cyclohexanone (ketone)",
            "reagent": "LiAlH4 (strong reduction)",
            "rxn_type": "reduction",
            "product": "cyclohexanol (secondary alcohol)",
            "rule": "LiAlH4 reduces ketone to secondary alcohol",
        },
        {
            "substrate": "ethanol (primary alcohol)",
            "reagent": "CrO3/H2SO4 (Jones oxidation)",
            "rxn_type": "oxidation",
            "product": "acetic acid (carboxylic acid)",
            "rule": "Jones reagent oxidises to carboxylic acid",
        },
        {
            "substrate": "benzaldehyde",
            "reagent": "NaBH4",
            "rxn_type": "reduction",
            "product": "benzyl alcohol (primary alcohol)",
            "rule": "NaBH4 reduces aldehyde to primary alcohol",
        },
        {
            "substrate": "2-butanol (secondary alcohol)",
            "reagent": "Na2Cr2O7 (oxidation)",
            "rxn_type": "oxidation",
            "product": "2-butanone (ketone)",
            "rule": "secondary alcohol oxidised to ketone",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "oxidation_reduction_organic"

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
        return "predict the product of the oxidation or reduction"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an oxidation/reduction problem.

        Args:
            difficulty: Controls scenario pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.REACTIONS[: min(len(self.REACTIONS), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = f"{entry['substrate']} + {entry['reagent']}"
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"substrate: {sd['substrate']}",
            f"reagent: {sd['reagent']}",
            f"type: {sd['rxn_type']}",
            f"rule: {sd['rule']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the product.

        Args:
            sd: Solution data.

        Returns:
            Product string.
        """
        return f"product: {sd['product']}"


# ---------------------------------------------------------------------------
# 5. Aromatic Substitution (tier 6)
# ---------------------------------------------------------------------------

@register
class AromaticSubstitutionGenerator(StepGenerator):
    """Predict major product position in electrophilic aromatic substitution.

    Determines whether an existing substituent is ortho/para-directing
    (activating) or meta-directing (deactivating), then predicts where
    the new electrophile attaches.
    """

    SUBSTITUENTS = [
        {
            "group": "-OH",
            "name": "hydroxyl",
            "type": "activating",
            "directing": "ortho/para",
            "reason": "lone pair donation into ring",
        },
        {
            "group": "-NH2",
            "name": "amino",
            "type": "activating",
            "directing": "ortho/para",
            "reason": "lone pair donation into ring",
        },
        {
            "group": "-CH3",
            "name": "methyl",
            "type": "activating",
            "directing": "ortho/para",
            "reason": "hyperconjugation / inductive donation",
        },
        {
            "group": "-NO2",
            "name": "nitro",
            "type": "deactivating",
            "directing": "meta",
            "reason": "electron withdrawal destabilises ortho/para intermediates",
        },
        {
            "group": "-COOH",
            "name": "carboxyl",
            "type": "deactivating",
            "directing": "meta",
            "reason": "carbonyl withdraws electrons",
        },
        {
            "group": "-OCH3",
            "name": "methoxy",
            "type": "activating",
            "directing": "ortho/para",
            "reason": "lone pair donation from oxygen",
        },
        {
            "group": "-Cl",
            "name": "chloro",
            "type": "deactivating but ortho/para",
            "directing": "ortho/para",
            "reason": "lone pair donates despite inductive withdrawal",
        },
        {
            "group": "-CN",
            "name": "cyano",
            "type": "deactivating",
            "directing": "meta",
            "reason": "triple bond withdraws electron density",
        },
    ]

    ELECTROPHILES = ["Br2/FeBr3", "HNO3/H2SO4", "CH3Cl/AlCl3", "Cl2/AlCl3"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "aromatic_substitution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "predict the major product position in EAS"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an aromatic substitution problem.

        Args:
            difficulty: Controls substituent pool variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.SUBSTITUENTS[: min(len(self.SUBSTITUENTS), 3 + difficulty)]
        sub = self._rng.choice(pool)
        electrophile = self._rng.choice(self.ELECTROPHILES)

        problem = f"benzene with {sub['group']} ({sub['name']}) + {electrophile}"
        return problem, {
            "group": sub["group"], "name": sub["name"],
            "type": sub["type"], "directing": sub["directing"],
            "reason": sub["reason"], "electrophile": electrophile,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"existing substituent: {sd['group']} ({sd['name']})",
            f"effect: {sd['type']}",
            f"reason: {sd['reason']}",
            f"directing: {sd['directing']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the predicted position.

        Args:
            sd: Solution data.

        Returns:
            Directing position string.
        """
        return f"major product at {sd['directing']} position"


# ---------------------------------------------------------------------------
# 6. Fischer Projection (tier 5)
# ---------------------------------------------------------------------------

@register
class FischerProjectionGenerator(StepGenerator):
    """Determine R/S configuration from a Fischer projection.

    Given a chiral centre drawn as a Fischer projection with four
    substituents, applies the CIP priority rules and determines
    absolute configuration.
    """

    TEMPLATES = [
        {
            "centre": "C-2 of alanine",
            "top": "CHO", "bottom": "CH2OH",
            "left": "OH", "right": "H",
            "priorities": "OH > CHO > CH2OH > H",
            "config": "R",
            "note": "lowest priority (H) on right -> check rotation",
        },
        {
            "centre": "C-2 of glyceraldehyde",
            "top": "CHO", "bottom": "CH2OH",
            "left": "H", "right": "OH",
            "priorities": "OH > CHO > CH2OH > H",
            "config": "S",
            "note": "D-glyceraldehyde: OH on right = R in most conventions",
        },
        {
            "centre": "C-2 of serine",
            "top": "COOH", "bottom": "CH2OH",
            "left": "NH2", "right": "H",
            "priorities": "NH2 > COOH > CH2OH > H",
            "config": "S",
            "note": "L-serine: NH2 on left",
        },
        {
            "centre": "C-2 of threonine",
            "top": "COOH", "bottom": "CHOH-CH3",
            "left": "NH2", "right": "H",
            "priorities": "NH2 > COOH > CHOH-CH3 > H",
            "config": "S",
            "note": "L-threonine",
        },
        {
            "centre": "C-2 of lactic acid",
            "top": "COOH", "bottom": "CH3",
            "left": "OH", "right": "H",
            "priorities": "OH > COOH > CH3 > H",
            "config": "R",
            "note": "L-lactic acid corresponds to (S) by CIP",
        },
        {
            "centre": "simple chiral alcohol",
            "top": "CH3", "bottom": "C2H5",
            "left": "OH", "right": "H",
            "priorities": "OH > C2H5 > CH3 > H",
            "config": "S",
            "note": "OH highest, H lowest",
        },
        {
            "centre": "amino acid template",
            "top": "COOH", "bottom": "CH3",
            "left": "NH2", "right": "H",
            "priorities": "NH2 > COOH > CH3 > H",
            "config": "S",
            "note": "generic L-amino acid",
        },
        {
            "centre": "halide centre",
            "top": "CH3", "bottom": "C2H5",
            "left": "Cl", "right": "H",
            "priorities": "Cl > C2H5 > CH3 > H",
            "config": "S",
            "note": "Cl highest atomic number -> priority 1",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fischer_projection"

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
        return "determine R or S configuration from the Fischer projection"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fischer projection problem.

        Args:
            difficulty: Controls template pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.TEMPLATES[: min(len(self.TEMPLATES), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = (
            f"Fischer: top={entry['top']}, bottom={entry['bottom']}, "
            f"left={entry['left']}, right={entry['right']}"
        )
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"centre: {sd['centre']}",
            f"horizontal = wedge (towards viewer): {sd['left']}, {sd['right']}",
            f"CIP priorities: {sd['priorities']}",
            f"{sd['note']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the configuration.

        Args:
            sd: Solution data.

        Returns:
            R or S configuration string.
        """
        return f"configuration: ({sd['config']})"


# ---------------------------------------------------------------------------
# 7. Retrosynthesis (tier 7)
# ---------------------------------------------------------------------------

@register
class RetrosynthesisGenerator(StepGenerator):
    """Perform a 1-2 step retrosynthetic analysis of a target molecule.

    Works backwards from a target to identify disconnections, synthons,
    and synthetic equivalents using template-based transformations.
    """

    TARGETS = [
        {
            "target": "2-methyl-2-butanol",
            "disconnection": "C-C bond at tertiary carbon",
            "synthon_a": "acetone (electrophile)",
            "synthon_b": "CH3MgBr (nucleophile)",
            "route": "acetone + CH3MgBr -> 2-methyl-2-butanol",
            "steps": 1,
        },
        {
            "target": "benzoic acid",
            "disconnection": "C-COOH bond",
            "synthon_a": "C6H5MgBr (nucleophile)",
            "synthon_b": "CO2 (electrophile)",
            "route": "C6H5MgBr + CO2, then H3O+",
            "steps": 1,
        },
        {
            "target": "1-phenylethanol",
            "disconnection": "C-C bond adjacent to OH",
            "synthon_a": "benzaldehyde (electrophile)",
            "synthon_b": "CH3MgBr (nucleophile)",
            "route": "benzaldehyde + CH3MgBr, then H3O+",
            "steps": 1,
        },
        {
            "target": "acetic acid",
            "disconnection": "C-COOH bond",
            "synthon_a": "CH3MgBr",
            "synthon_b": "CO2",
            "route": "CH3MgBr + CO2, then H3O+",
            "steps": 1,
        },
        {
            "target": "propanoic acid",
            "disconnection": "C-COOH bond",
            "synthon_a": "C2H5MgBr",
            "synthon_b": "CO2",
            "route": "C2H5MgBr + CO2, then H3O+",
            "steps": 1,
        },
        {
            "target": "4-methylpentan-2-ol",
            "disconnection": "C2-C3 bond",
            "synthon_a": "3-methylbutanal (electrophile)",
            "synthon_b": "CH3MgBr (nucleophile)",
            "route": "3-methylbutanal + CH3MgBr, then H3O+",
            "steps": 1,
        },
        {
            "target": "cyclohexanol from cyclohexanone",
            "disconnection": "reduce C=O",
            "synthon_a": "cyclohexanone",
            "synthon_b": "NaBH4 (reducing agent)",
            "route": "cyclohexanone + NaBH4 -> cyclohexanol",
            "steps": 1,
        },
        {
            "target": "2-butanol from butanal",
            "disconnection": "C1-C2 from aldehyde + Grignard",
            "synthon_a": "propanal (electrophile)",
            "synthon_b": "CH3MgBr (nucleophile)",
            "route": "propanal + CH3MgBr, then H3O+ -> 2-butanol",
            "steps": 1,
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "retrosynthesis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 7

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["grignard_reaction"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description string.
        """
        return "propose a retrosynthetic route to the target"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a retrosynthesis problem.

        Args:
            difficulty: Controls target pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.TARGETS[: min(len(self.TARGETS), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = f"retrosynthesis of {entry['target']}"
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"target: {sd['target']}",
            f"disconnection: {sd['disconnection']}",
            f"synthon A: {sd['synthon_a']}",
            f"synthon B: {sd['synthon_b']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the synthetic route.

        Args:
            sd: Solution data.

        Returns:
            Route string.
        """
        return f"route: {sd['route']}"


# ---------------------------------------------------------------------------
# 8. Spectroscopy Interpretation (tier 6)
# ---------------------------------------------------------------------------

@register
class SpectroscopyInterpretationGenerator(StepGenerator):
    """Identify a structure from IR and NMR spectral data.

    Given characteristic IR absorption peaks and 1H NMR peak patterns,
    identifies functional groups and proposes a molecular structure.
    Template-based for simple organic molecules.
    """

    SPECTRA = [
        {
            "ir_peaks": "broad 3200-3550 cm-1 (O-H stretch), 1050 cm-1 (C-O stretch)",
            "nmr_peaks": "triplet at 1.2 ppm (3H), quartet at 3.7 ppm (2H), broad singlet at 2.5 ppm (1H)",
            "formula": "C2H6O",
            "groups": ["hydroxyl (O-H)", "C-O"],
            "structure": "ethanol (CH3CH2OH)",
        },
        {
            "ir_peaks": "sharp 1715 cm-1 (C=O stretch), no broad O-H",
            "nmr_peaks": "singlet at 2.1 ppm (6H)",
            "formula": "C3H6O",
            "groups": ["carbonyl (C=O)"],
            "structure": "acetone ((CH3)2CO)",
        },
        {
            "ir_peaks": "broad 2500-3300 cm-1 (O-H carboxylic acid), 1710 cm-1 (C=O)",
            "nmr_peaks": "singlet at 2.1 ppm (3H), broad at 11.4 ppm (1H)",
            "formula": "C2H4O2",
            "groups": ["carboxylic acid (O-H, C=O)"],
            "structure": "acetic acid (CH3COOH)",
        },
        {
            "ir_peaks": "sharp 2720 cm-1 (C-H aldehyde), 1720 cm-1 (C=O)",
            "nmr_peaks": "triplet at 1.1 ppm (3H), quartet at 2.4 ppm (2H), singlet at 9.8 ppm (1H)",
            "formula": "C3H6O",
            "groups": ["aldehyde (C-H, C=O)"],
            "structure": "propanal (CH3CH2CHO)",
        },
        {
            "ir_peaks": "3300 cm-1 (N-H stretch, two peaks), 1600 cm-1 (N-H bend)",
            "nmr_peaks": "triplet at 1.2 ppm (3H), quartet at 2.6 ppm (2H), broad at 1.0 ppm (2H)",
            "formula": "C2H7N",
            "groups": ["primary amine (N-H)"],
            "structure": "ethylamine (CH3CH2NH2)",
        },
        {
            "ir_peaks": "sharp 1735 cm-1 (C=O ester), 1200 cm-1 (C-O stretch)",
            "nmr_peaks": "singlet at 2.0 ppm (3H), singlet at 3.7 ppm (3H)",
            "formula": "C3H6O2",
            "groups": ["ester (C=O, C-O-C)"],
            "structure": "methyl acetate (CH3COOCH3)",
        },
        {
            "ir_peaks": "2260 cm-1 (C triple bond N stretch)",
            "nmr_peaks": "triplet at 1.3 ppm (3H), quartet at 2.4 ppm (2H)",
            "formula": "C3H5N",
            "groups": ["nitrile (C#N)"],
            "structure": "propanenitrile (CH3CH2CN)",
        },
        {
            "ir_peaks": "broad 3200-3550 cm-1 (O-H), 1050 cm-1 (C-O), no carbonyl",
            "nmr_peaks": "doublet at 1.2 ppm (6H), septet at 4.0 ppm (1H), singlet at 2.3 ppm (1H)",
            "formula": "C3H8O",
            "groups": ["hydroxyl (O-H)", "C-O"],
            "structure": "2-propanol ((CH3)2CHOH)",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "spectroscopy_interpretation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

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
        return "identify the structure from IR and NMR data"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a spectroscopy interpretation problem.

        Args:
            difficulty: Controls spectrum pool.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        pool = self.SPECTRA[: min(len(self.SPECTRA), 3 + difficulty)]
        entry = self._rng.choice(pool)

        problem = (
            f"formula: {entry['formula']}; "
            f"IR: {entry['ir_peaks']}; "
            f"NMR: {entry['nmr_peaks']}"
        )
        return problem, dict(entry)

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"molecular formula: {sd['formula']}"]
        for g in sd["groups"]:
            steps.append(f"IR indicates: {g}")
        steps.append(f"NMR: {sd['nmr_peaks']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the proposed structure.

        Args:
            sd: Solution data.

        Returns:
            Structure identification string.
        """
        return f"structure: {sd['structure']}"
