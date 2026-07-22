"""Knowledge atoms for statistics_ext, abstract_algebra_ext, and analysis_ext.

Each atom has a worked example and Wikipedia source for independent
verification of generator output.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── statistics_ext (tier 5-6) ──────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="anova_one_way",
    content=(
        "One-way analysis of variance (ANOVA) tests whether the means "
        "of three or more independent groups differ. The F-statistic is "
        "F = MS_between / MS_within, where MS_between = SS_between / "
        "(k-1) and MS_within = SS_within / (N-k). k is the number of "
        "groups and N is the total sample size."
    ),
    example=(
        "Groups [2,3,5], [8,10,12], [14,16,18]: grand mean=9.78, "
        "SS_between=186.89, SS_within=24.67, df_b=2, df_w=6, "
        "F=186.89/2 / (24.67/6) = 93.44/4.11 = 22.73"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'One-way analysis of variance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/One-way_analysis_of_variance",
    prerequisites=["variance", "mean"],
))

register_atom(Atom(
    atom_type="formula",
    name="chi_square_independence",
    content=(
        "The chi-squared test of independence determines whether two "
        "categorical variables are independent. chi^2 = sum((O-E)^2/E) "
        "where O is observed frequency and E is expected frequency "
        "E_ij = (row_i_total * col_j_total) / grand_total."
    ),
    example=(
        "2x2 table [[10,20],[20,50]]: row totals [30,70], col totals "
        "[30,70], N=100. E=[[9,21],[21,49]]. "
        "chi^2 = (10-9)^2/9 + (20-21)^2/21 + (20-21)^2/21 + (50-49)^2/49 "
        "= 0.111+0.048+0.048+0.020 = 0.227, df=1"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Chi-squared test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chi-squared_test",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="formula",
    name="regression_diagnostics",
    content=(
        "Regression diagnostics assess linear regression model quality. "
        "R^2 = 1 - SS_res/SS_tot measures explained variance. "
        "Adjusted R^2 = 1 - (1-R^2)(n-1)/(n-p-1) penalises extra "
        "predictors. Residual standard error = sqrt(SS_res/(n-p-1))."
    ),
    example=(
        "n=20, p=2, SS_res=40, SS_tot=200: R^2 = 1-40/200 = 0.8, "
        "Adj_R^2 = 1-(1-0.8)(19/17) = 1-0.2*1.118 = 0.776, "
        "RSE = sqrt(40/17) = 1.534"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Coefficient of determination', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coefficient_of_determination",
    prerequisites=["linear_regression"],
))

register_atom(Atom(
    atom_type="formula",
    name="paired_t_test",
    content=(
        "The paired t-test compares means of two related groups. "
        "t = d_bar / (s_d / sqrt(n)), where d_bar is the mean of "
        "differences, s_d is the standard deviation of differences, "
        "and n is the number of pairs. df = n - 1."
    ),
    example=(
        "Before [5,7,9], After [6,8,11]: differences [1,1,2], "
        "d_bar=4/3=1.333, s_d=0.577, t=1.333/(0.577/sqrt(3)) "
        "= 1.333/0.333 = 4.0, df=2"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Student's t-test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Student%27s_t-test#Paired_samples",
    prerequisites=["mean", "std_dev"],
))

register_atom(Atom(
    atom_type="formula",
    name="two_sample_t",
    content=(
        "The two-sample t-test compares means of two independent groups. "
        "t = (x1_bar - x2_bar) / sqrt(s1^2/n1 + s2^2/n2). "
        "Welch's df = (s1^2/n1 + s2^2/n2)^2 / "
        "((s1^2/n1)^2/(n1-1) + (s2^2/n2)^2/(n2-1))."
    ),
    example=(
        "Group A: mean=10, s=2, n=5. Group B: mean=14, s=3, n=5. "
        "SE = sqrt(4/5 + 9/5) = sqrt(2.6) = 1.612, "
        "t = (10-14)/1.612 = -2.48"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Welch's t-test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Welch%27s_t-test",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="f_test",
    content=(
        "The F-test compares two sample variances. "
        "F = s1^2 / s2^2 where s1^2 >= s2^2 by convention. "
        "df1 = n1 - 1, df2 = n2 - 1. Used to test the null hypothesis "
        "that two populations have equal variance."
    ),
    example=(
        "Sample 1: s1^2=2.8, n1=5. Sample 2: s2^2=1.0, n2=4. "
        "F = 2.8/1.0 = 2.8, df1=4, df2=3"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'F-test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/F-test",
    prerequisites=["variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="maximum_likelihood",
    content=(
        "Maximum likelihood estimation (MLE) finds the parameter values "
        "that maximise the likelihood function L(theta|x) = prod P(x_i|theta). "
        "Equivalently, maximise the log-likelihood: "
        "l(theta) = sum log P(x_i|theta). For a normal distribution, "
        "MLE gives mu_hat = x_bar, sigma_hat^2 = (1/n) sum (x_i - x_bar)^2."
    ),
    example=(
        "Data [2,4,6,8]: MLE for normal: mu_hat = 5.0, "
        "sigma_hat^2 = ((2-5)^2+(4-5)^2+(6-5)^2+(8-5)^2)/4 "
        "= (9+1+1+9)/4 = 5.0"
    ),
    tier=6,
    domain="statistics",
    source="Wikipedia contributors, 'Maximum likelihood estimation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maximum_likelihood_estimation",
    prerequisites=["mean", "variance"],
))

register_atom(Atom(
    atom_type="formula",
    name="goodness_of_fit",
    content=(
        "The chi-squared goodness-of-fit test compares observed frequencies "
        "to expected frequencies under a hypothesised distribution. "
        "chi^2 = sum((O_i - E_i)^2 / E_i), df = k - 1 - p where k is "
        "the number of categories and p is the number of estimated parameters."
    ),
    example=(
        "Die rolls: observed [18,15,22,17,13,15], expected [16.67]*6. "
        "chi^2 = (18-16.67)^2/16.67 + (15-16.67)^2/16.67 + ... "
        "= 0.107+0.167+1.707+0.007+0.808+0.167 = 2.96, df=5"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Goodness of fit', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Goodness_of_fit",
    prerequisites=["chi_square_genetics"],
))

register_atom(Atom(
    atom_type="formula",
    name="correlation_test",
    content=(
        "Tests whether a Pearson correlation coefficient is significantly "
        "different from zero. t = r * sqrt(n-2) / sqrt(1-r^2), "
        "with df = n - 2."
    ),
    example=(
        "r=0.8, n=10: t = 0.8*sqrt(8)/sqrt(1-0.64) "
        "= 0.8*2.828/0.6 = 3.771, df=8"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Pearson correlation coefficient', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Pearson_correlation_coefficient#Testing_using_Student's_t-distribution",
    prerequisites=["correlation"],
))

register_atom(Atom(
    atom_type="formula",
    name="power_analysis",
    content=(
        "Statistical power is the probability of correctly rejecting "
        "a false null hypothesis: power = 1 - beta. For a two-sample "
        "t-test, required n per group = (z_alpha + z_beta)^2 * "
        "2*sigma^2 / delta^2, where delta is the effect size."
    ),
    example=(
        "Effect delta=5, sigma=10, alpha=0.05 (z=1.96), power=0.8 "
        "(z_beta=0.84): n = (1.96+0.84)^2 * 2*100/25 "
        "= 7.84 * 8 = 62.7, round up to 63 per group"
    ),
    tier=5,
    domain="statistics",
    source="Wikipedia contributors, 'Statistical power', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Power_(statistics)",
    prerequisites=["hypothesis_test"],
))


# ── abstract_algebra_ext (tier 4-6) ────────────────────────────────

register_atom(Atom(
    atom_type="definition",
    name="dihedral_group",
    content=(
        "The dihedral group D_n is the symmetry group of a regular "
        "n-gon, with order 2n. It is generated by a rotation r of "
        "order n and a reflection s with s^2 = e and srs = r^{-1}. "
        "Elements: {e, r, r^2, ..., r^{n-1}, s, sr, sr^2, ..., sr^{n-1}}."
    ),
    example=(
        "D_3 (symmetries of equilateral triangle): order = 6. "
        "sr * r = sr^2. sr^2 * r = s (since r^3 = e). "
        "r * s = sr^{-1} = sr^2."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Dihedral group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Dihedral_group",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="group_center",
    content=(
        "The center Z(G) of a group G is the set of elements that "
        "commute with all elements: Z(G) = {z in G : zg = gz for all g in G}. "
        "The center is always a normal subgroup. A group is abelian "
        "iff Z(G) = G."
    ),
    example=(
        "D_3: check each element. r*s = sr^2, s*r = sr, so r not in Z. "
        "Only e commutes with all. Z(D_3) = {e}."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Center (group theory)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Center_(group_theory)",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="conjugacy_class",
    content=(
        "The conjugacy class of an element a in a group G is "
        "Cl(a) = {gag^{-1} : g in G}. Two elements are conjugate if "
        "they are in the same conjugacy class. The number of conjugacy "
        "classes equals the number of irreducible representations."
    ),
    example=(
        "S_3: Cl(e)={e}, Cl((12))={(12),(13),(23)}, "
        "Cl((123))={(123),(132)}. Three conjugacy classes."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Conjugacy class', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conjugacy_class",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="definition",
    name="group_action",
    content=(
        "A group action of G on a set X is a map G x X -> X "
        "satisfying e.x = x and (gh).x = g.(h.x). The orbit of x "
        "is Orb(x) = {g.x : g in G}. The stabiliser is "
        "Stab(x) = {g in G : g.x = x}. Orbit-stabiliser theorem: "
        "|G| = |Orb(x)| * |Stab(x)|."
    ),
    example=(
        "D_3 acts on vertices {1,2,3} of triangle. "
        "Orb(1) = {1,2,3}, |Orb|=3. |D_3|=6, so |Stab(1)|=2. "
        "Stab(1) = {e, s} (reflection fixing vertex 1)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Group action', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Group_action",
    prerequisites=["group_axiom_check", "coset_enumerate"],
))

register_atom(Atom(
    atom_type="definition",
    name="polynomial_ring",
    content=(
        "The polynomial ring R[x] over a ring R consists of all "
        "polynomials with coefficients in R. Addition and multiplication "
        "follow the usual rules. In Z_n[x], coefficients are reduced "
        "mod n after each operation."
    ),
    example=(
        "Z_5[x]: (2x^2 + 3x + 1) + (4x^2 + 2x + 3) "
        "= (6x^2 + 5x + 4) = (x^2 + 0x + 4) = x^2 + 4 in Z_5[x]."
    ),
    tier=5,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Polynomial ring', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Polynomial_ring",
    prerequisites=["ring_axiom_check"],
))

register_atom(Atom(
    atom_type="theorem",
    name="chinese_remainder_rings",
    content=(
        "If m and n are coprime, then Z/(mn) is isomorphic to "
        "Z/m x Z/n. For solving x = a (mod m), x = b (mod n) "
        "with gcd(m,n) = 1: x = a*n*n' + b*m*m' where "
        "n' = n^{-1} mod m and m' = m^{-1} mod n."
    ),
    example=(
        "x = 2 (mod 3), x = 3 (mod 5). n'=5^{-1} mod 3 = 2 "
        "(since 5*2=10=1 mod 3). m'=3^{-1} mod 5 = 2 "
        "(since 3*2=6=1 mod 5). x = 2*5*2 + 3*3*2 = 20+18 = 38 "
        "= 38 mod 15 = 8."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Chinese remainder theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Chinese_remainder_theorem",
    prerequisites=["gcd", "modular"],
))

register_atom(Atom(
    atom_type="definition",
    name="euclidean_domain",
    content=(
        "A Euclidean domain is an integral domain R with a Euclidean "
        "function d: R\\{0} -> N such that for a,b in R with b != 0, "
        "there exist q,r with a = bq + r and either r = 0 or "
        "d(r) < d(b). Z with d(n)=|n| and F[x] with d(f)=deg(f) "
        "are standard examples."
    ),
    example=(
        "Z[i] (Gaussian integers) with d(a+bi) = a^2+b^2: "
        "divide 11+3i by 3+i. (11+3i)(3-i)/|3+i|^2 "
        "= (33-11i+9i-3i^2)/10 = (36-2i)/10 = 3.6-0.2i. "
        "Round to q=4. r = (11+3i)-4(3+i) = -1-i. d(r)=2 < d(3+i)=10."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Euclidean domain', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Euclidean_domain",
    prerequisites=["ring_axiom_check", "gcd"],
))

register_atom(Atom(
    atom_type="definition",
    name="free_group",
    content=(
        "The free group F(S) on a set S consists of all reduced words "
        "over S and formal inverses S^{-1}. A word is reduced if it "
        "contains no adjacent pair xx^{-1} or x^{-1}x. The group "
        "operation is concatenation followed by reduction."
    ),
    example=(
        "F({a,b}): ab^{-1} * ba = ab^{-1}ba (already reduced). "
        "ab * b^{-1}a^{-1} = abb^{-1}a^{-1} -> aa^{-1} -> e (identity)."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Free group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Free_group",
    prerequisites=["group_axiom_check"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="permutation_cycle",
    content=(
        "A permutation can be written as a product of disjoint cycles. "
        "To find cycles: start at the smallest unmoved element, follow "
        "the permutation until returning to the start. Repeat for "
        "remaining elements. The order of the permutation is the LCM "
        "of the cycle lengths."
    ),
    example=(
        "sigma = (1->3, 2->1, 3->4, 4->2, 5->5) in S_5: "
        "start at 1: 1->3->4->2->1, cycle (1 3 4 2). "
        "5->5 is a fixed point. sigma = (1 3 4 2). Order = 4."
    ),
    tier=4,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Cyclic permutation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cyclic_permutation",
    prerequisites=["permutation"],
))

register_atom(Atom(
    atom_type="definition",
    name="automorphism_group",
    content=(
        "The automorphism group Aut(G) of a group G is the group of "
        "all isomorphisms from G to itself. Inner automorphisms are "
        "of the form phi_g(x) = gxg^{-1}. Inn(G) is a normal subgroup "
        "of Aut(G). The quotient Aut(G)/Inn(G) is the outer "
        "automorphism group Out(G)."
    ),
    example=(
        "Aut(Z_6): automorphisms are phi_k(x) = kx mod 6 where "
        "gcd(k,6)=1. k in {1,5}. So |Aut(Z_6)| = phi(6) = 2. "
        "Aut(Z_6) = Z_2."
    ),
    tier=6,
    domain="abstract_algebra",
    source="Wikipedia contributors, 'Automorphism group', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Automorphism_group",
    prerequisites=["group_homomorphism", "isomorphism_check"],
))


# ── analysis_ext (tier 5-6) ────────────────────────────────────────

register_atom(Atom(
    atom_type="theorem",
    name="bolzano_weierstrass",
    content=(
        "Every bounded sequence in R^n has a convergent subsequence. "
        "Equivalently, a subset of R^n is sequentially compact iff "
        "it is closed and bounded. This theorem is fundamental to "
        "real analysis and underpins many existence proofs."
    ),
    example=(
        "Sequence a_n = sin(n) in [-1,1] (bounded). By Bolzano-Weierstrass, "
        "there exists a convergent subsequence. For instance, "
        "a_22 = sin(22) ~ -0.009, a_44 ~ -0.018, a_66 ~ -0.027 "
        "is a subsequence converging to 0."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Bolzano-Weierstrass theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Bolzano%E2%80%93Weierstrass_theorem",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="weierstrass_mtest",
    content=(
        "If |f_n(x)| <= M_n for all x in S and sum M_n converges, "
        "then sum f_n(x) converges uniformly and absolutely on S. "
        "The bound M_n must be independent of x."
    ),
    example=(
        "f_n(x) = x^n/n^2 on [-1,1]. |f_n(x)| <= 1/n^2 = M_n. "
        "sum 1/n^2 = pi^2/6 converges. By M-test, sum x^n/n^2 "
        "converges uniformly on [-1,1]."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Weierstrass M-test', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Weierstrass_M-test",
    prerequisites=["uniform_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="abel_summation",
    content=(
        "Abel's summation formula (summation by parts): "
        "sum_{k=0}^{n} a_k b_k = A_n b_n - sum_{k=0}^{n-1} A_k (b_{k+1} - b_k), "
        "where A_k = sum_{j=0}^k a_j. This is the discrete analogue "
        "of integration by parts."
    ),
    example=(
        "a_k = 1, b_k = 1/(k+1) for k=0,1,2. A_k = k+1. "
        "sum a_k*b_k = 1 + 1/2 + 1/3 = 11/6. "
        "Abel: A_2*b_2 - A_0*(b_1-b_0) - A_1*(b_2-b_1) "
        "= 3*(1/3) - 1*(-1/2) - 2*(-1/6) = 1 + 1/2 + 1/3 = 11/6."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Abel's summation formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Abel%27s_summation_formula",
    prerequisites=["summation"],
))

register_atom(Atom(
    atom_type="theorem",
    name="integral_test",
    content=(
        "If f is a positive, continuous, monotonically decreasing "
        "function on [1,inf) with f(n) = a_n, then sum a_n converges "
        "iff integral_1^inf f(x)dx converges."
    ),
    example=(
        "a_n = 1/n^2, f(x) = 1/x^2. integral_1^inf 1/x^2 dx "
        "= [-1/x]_1^inf = 0-(-1) = 1 (converges). "
        "Therefore sum 1/n^2 converges (to pi^2/6)."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Integral test for convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Integral_test_for_convergence",
    prerequisites=["definite_integral", "series_convergence"],
))

register_atom(Atom(
    atom_type="definition",
    name="limsup_liminf",
    content=(
        "For a sequence (a_n), lim sup a_n = lim_{n->inf} sup_{k>=n} a_k "
        "and lim inf a_n = lim_{n->inf} inf_{k>=n} a_k. A sequence "
        "converges iff lim sup = lim inf, and the common value is the limit."
    ),
    example=(
        "a_n = (-1)^n + 1/n: terms are -1+1, 1+1/2, -1+1/3, 1+1/4, ... "
        "= 0, 1.5, -0.667, 1.25, -0.8, 1.167, ... "
        "lim sup = 1, lim inf = -1."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Limit inferior and limit superior', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Limit_inferior_and_limit_superior",
    prerequisites=["sequence_convergence", "supremum_infimum"],
))

register_atom(Atom(
    atom_type="theorem",
    name="contraction_mapping",
    content=(
        "Banach fixed-point theorem: if (X,d) is a complete metric "
        "space and f: X->X is a contraction (d(f(x),f(y)) <= q*d(x,y) "
        "for some q<1), then f has a unique fixed point. Iterating "
        "x_{n+1} = f(x_n) from any x_0 converges to this fixed point."
    ),
    example=(
        "f(x) = cos(x) on [0,1]. |f'(x)| = |sin(x)| <= sin(1) ~ 0.841 < 1. "
        "Starting x_0=0: x_1=1, x_2=0.5403, x_3=0.8576, x_4=0.6543... "
        "converges to fixed point x ~ 0.7391."
    ),
    tier=6,
    domain="real_analysis",
    source="Wikipedia contributors, 'Banach fixed-point theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Banach_fixed-point_theorem",
    prerequisites=["cauchy_sequence"],
))

register_atom(Atom(
    atom_type="formula",
    name="riemann_sum",
    content=(
        "A Riemann sum approximates a definite integral by dividing "
        "[a,b] into n subintervals of width dx=(b-a)/n and summing "
        "f(x_i)*dx. Left sum uses x_i = a + i*dx, right sum uses "
        "x_i = a + (i+1)*dx, midpoint uses x_i = a + (i+0.5)*dx."
    ),
    example=(
        "f(x)=x^2 on [0,2], n=4, dx=0.5. Left sum: "
        "f(0)*0.5 + f(0.5)*0.5 + f(1)*0.5 + f(1.5)*0.5 "
        "= 0 + 0.125 + 0.5 + 1.125 = 1.75. Exact = 8/3 = 2.667."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Riemann sum', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Riemann_sum",
    prerequisites=["definite_integral"],
))

register_atom(Atom(
    atom_type="theorem",
    name="squeeze_theorem",
    content=(
        "If g(x) <= f(x) <= h(x) for all x near c (except possibly "
        "at c), and lim g(x) = lim h(x) = L as x->c, then "
        "lim f(x) = L. Also called the sandwich theorem or "
        "pinching theorem."
    ),
    example=(
        "lim_{x->0} x^2*sin(1/x): -x^2 <= x^2*sin(1/x) <= x^2. "
        "lim x^2 = 0 and lim -x^2 = 0. By squeeze theorem, "
        "lim x^2*sin(1/x) = 0."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Squeeze theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Squeeze_theorem",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="theorem",
    name="mean_value_theorem",
    content=(
        "If f is continuous on [a,b] and differentiable on (a,b), "
        "then there exists c in (a,b) such that "
        "f'(c) = (f(b) - f(a)) / (b - a). This guarantees the "
        "existence of a tangent parallel to the secant line."
    ),
    example=(
        "f(x) = x^3 on [1,3]. f(3)-f(1) = 27-1 = 26. "
        "f'(c) = 26/(3-1) = 13. 3c^2 = 13, c = sqrt(13/3) ~ 2.082. "
        "c is in (1,3), confirming MVT."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'Mean value theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mean_value_theorem",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="theorem",
    name="lhopital_extended",
    content=(
        "L'Hopital's rule: if lim f(x)/g(x) gives 0/0 or inf/inf, "
        "then lim f(x)/g(x) = lim f'(x)/g'(x), provided the latter "
        "limit exists. Can be applied repeatedly if the result is "
        "still indeterminate."
    ),
    example=(
        "lim_{x->0} (e^x - 1)/x: 0/0 form. "
        "L'Hopital: lim e^x / 1 = e^0 = 1."
    ),
    tier=5,
    domain="real_analysis",
    source="Wikipedia contributors, 'L'Hopital's rule', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/L%27H%C3%B4pital%27s_rule",
    prerequisites=["derivative"],
))
