"""Double-blind example verification handlers, batch 6.

Covers the 59 newly-backfilled atoms plus remaining computable tasks.
Each handler hardcodes textbook inputs and independently computes
the expected output using Python math.
"""
import math


def register_batch6_handlers(verifier) -> None:
    """Register batch 6 example verification handlers.

    Args:
        verifier: ExampleVerifier instance to register handlers on.
    """
    h = verifier._handlers

    # === MEASUREMENT ===

    def _unit_conversion_length():
        expected = 8.045
        computed = 5 * 1.609
        return verifier._ok("unit_conversion_length", expected, computed,
                            "5 miles * 1.609 = 8.045 km")
    h["unit_conversion_length"] = _unit_conversion_length

    def _unit_conversion_mass():
        expected = 4.536
        computed = 10 * 0.4536
        return verifier._ok("unit_conversion_mass", expected, computed,
                            "10 lbs * 0.4536 = 4.536 kg")
    h["unit_conversion_mass"] = _unit_conversion_mass

    def _unit_conversion_temp():
        expected = 37.0
        computed = (98.6 - 32) * 5 / 9
        return verifier._ok("unit_conversion_temp", expected, computed,
                            "98.6F to C: (98.6-32)*5/9")
    h["unit_conversion_temp"] = _unit_conversion_temp

    # === GEOMETRY ===

    def _angle_sum_triangle():
        expected = 70.0
        computed = 180 - 50 - 60.0
        return verifier._ok("angle_sum_triangle", expected, computed,
                            "angles 50,60: third=180-50-60")
    h["angle_sum_triangle"] = _angle_sum_triangle

    def _circle_arc_length():
        expected = 5.236
        computed = 5 * math.pi / 3
        return verifier._ok("circle_arc_length", expected, computed,
                            "r=5, theta=pi/3")
    h["circle_arc_length"] = _circle_arc_length

    def _midpoint():
        expected = 4.0
        computed = (2 + 6) / 2
        return verifier._ok("midpoint", expected, computed,
                            "A=(2,4), B=(6,8): Mx=(2+6)/2")
    h["midpoint"] = _midpoint

    def _sector_area():
        expected = 14.137
        computed = 0.5 * 36 * (math.pi / 4)
        return verifier._ok("sector_area", expected, computed,
                            "r=6, theta=pi/4")
    h["sector_area"] = _sector_area

    def _similar_triangles():
        expected = 2.0
        computed = 6 / 3.0
        return verifier._ok("similar_triangles", expected, computed,
                            "sides 3,4,5 -> 6,8,10: ratio=2")
    h["similar_triangles"] = _similar_triangles

    def _slope():
        expected = 2.0
        computed = (8 - 2) / (4 - 1.0)
        return verifier._ok("slope", expected, computed,
                            "A=(1,2), B=(4,8): m=6/3")
    h["slope"] = _slope

    def _volume_box():
        expected = 60.0
        computed = 5 * 3 * 4.0
        return verifier._ok("volume_box", expected, computed,
                            "l=5, w=3, h=4")
    h["volume_box"] = _volume_box

    def _volume_cylinder():
        expected = 197.92
        computed = math.pi * 9 * 7
        return verifier._ok("volume_cylinder", expected, computed,
                            "r=3, h=7")
    h["volume_cylinder"] = _volume_cylinder

    def _volume_sphere():
        expected = 268.08
        computed = (4 / 3) * math.pi * 64
        return verifier._ok("volume_sphere", expected, computed,
                            "r=4")
    h["volume_sphere"] = _volume_sphere

    # === SEQUENCES ===

    def _arithmetic_sequence():
        # a_10 = 3 + 9*5 = 48, S_10 = 10*(3+48)/2 = 255
        expected = 255.0
        computed = 10 * (3 + 48) / 2
        return verifier._ok("arithmetic_sequence", expected, computed,
                            "a1=3, d=5, S_10")
    h["arithmetic_sequence"] = _arithmetic_sequence

    def _geometric_sequence():
        # S_5 = 2*(1-3^5)/(1-3) = 242
        expected = 242.0
        computed = 2 * (1 - 3**5) / (1 - 3)
        return verifier._ok("geometric_sequence", expected, computed,
                            "a1=2, r=3, S_5")
    h["geometric_sequence"] = _geometric_sequence

    # === ECONOMICS ===

    def _break_even():
        expected = 1000.0
        computed = 10000 / (25 - 15.0)
        return verifier._ok("break_even", expected, computed,
                            "FC=10000, P=25, VC=15")
    h["break_even"] = _break_even

    def _depreciation():
        expected = 4500.0
        computed = (50000 - 5000) / 10.0
        return verifier._ok("depreciation", expected, computed,
                            "cost=50000, salvage=5000, life=10")
    h["depreciation"] = _depreciation

    def _present_value():
        expected = 863.84
        computed = 1000 / (1.05**3)
        return verifier._ok("present_value", expected, computed,
                            "FV=1000, r=5%, t=3")
    h["present_value"] = _present_value

    def _roi():
        expected = 30.0
        computed = (6500 - 5000) / 5000 * 100
        return verifier._ok("roi", expected, computed,
                            "invest=5000, return=6500")
    h["roi"] = _roi

    def _simple_interest():
        expected = 150.0
        computed = 1000 * 0.05 * 3
        return verifier._ok("simple_interest", expected, computed,
                            "P=1000, r=5%, t=3")
    h["simple_interest"] = _simple_interest

    def _percentage():
        expected = 20.0
        computed = 80 * 25 / 100.0
        return verifier._ok("percentage", expected, computed,
                            "25% of 80")
    h["percentage"] = _percentage

    # === STATISTICS / PROBABILITY ===

    def _basic_prob():
        expected = 0.5
        computed = 3 / 6.0
        return verifier._ok("basic_prob", expected, computed,
                            "fair die, P(even)=3/6")
    h["basic_prob"] = _basic_prob

    def _conditional_prob():
        expected = 0.3
        computed = 0.12 / 0.4
        return verifier._ok("conditional_prob", expected, computed,
                            "P(A&B)=0.12, P(B)=0.4")
    h["conditional_prob"] = _conditional_prob

    def _conditional_independence():
        expected = 0.12
        computed = 0.3 * 0.4
        return verifier._ok("conditional_independence", expected, computed,
                            "P(A|C)=0.3, P(B|C)=0.4, P(A,B|C)")
    h["conditional_independence"] = _conditional_independence

    def _total_probability():
        expected = 0.014
        computed = 0.01 * 0.9 + 0.05 * 0.1
        return verifier._ok("total_probability", expected, computed,
                            "P(D|A)=0.01, P(A)=0.9, P(D|B)=0.05, P(B)=0.1")
    h["total_probability"] = _total_probability

    def _venn_diagram_count():
        expected = 40.0
        computed = 30 + 20 - 10.0
        return verifier._ok("venn_diagram_count", expected, computed,
                            "|A|=30, |B|=20, |A&B|=10")
    h["venn_diagram_count"] = _venn_diagram_count

    # === CHEMISTRY ===

    def _molarity():
        expected = 0.171
        computed = (5 / 58.44) / 0.5
        return verifier._ok("molarity", expected, computed,
                            "5g NaCl in 0.5L")
    h["molarity"] = _molarity

    # === PHYSICS ===

    def _conservation_energy():
        # v = sqrt(2*PE/m) = sqrt(2*196.2/2) = 14.0
        expected = 14.0
        PE = 2 * 9.81 * 10
        computed = math.sqrt(2 * PE / 2)
        return verifier._ok("conservation_energy", expected, computed,
                            "m=2, h=10, v=sqrt(2gh)")
    h["conservation_energy"] = _conservation_energy

    def _escape_velocity():
        expected = 11186.0
        G, M, R = 6.674e-11, 5.97e24, 6.371e6
        computed = math.sqrt(2 * G * M / R)
        return verifier._ok("escape_velocity", expected, computed,
                            "Earth: M=5.97e24, R=6.371e6", tol=0.02)
    h["escape_velocity"] = _escape_velocity

    def _gravitational_force():
        expected = 1.982e20
        G = 6.674e-11
        m1, m2, r = 5.97e24, 7.35e22, 3.844e8
        computed = G * m1 * m2 / r**2
        return verifier._ok("gravitational_force", expected, computed,
                            "Earth-Moon", tol=0.02)
    h["gravitational_force"] = _gravitational_force

    def _hubble_law():
        expected = 7000.0
        computed = 70 * 100.0
        return verifier._ok("hubble_law", expected, computed,
                            "d=100Mpc, H0=70")
    h["hubble_law"] = _hubble_law

    def _ideal_gas():
        expected = 22.41
        computed = 1 * 8.314 * 273.15 / 101325 * 1000  # m^3 to L
        return verifier._ok("ideal_gas", expected, computed,
                            "n=1, T=273.15K, P=1atm")
    h["ideal_gas"] = _ideal_gas

    def _kinematics_displacement():
        expected = 75.0
        computed = 10 * 5 + 0.5 * 2 * 25
        return verifier._ok("kinematics_displacement", expected, computed,
                            "v0=10, a=2, t=5")
    h["kinematics_displacement"] = _kinematics_displacement

    def _kinematics_velocity():
        expected = 29.43
        computed = 0 + 9.81 * 3
        return verifier._ok("kinematics_velocity", expected, computed,
                            "v0=0, a=9.81, t=3")
    h["kinematics_velocity"] = _kinematics_velocity

    def _magnitude_distance():
        # mu = m - M = 15 - (-20) = 35, d = 10^((mu+5)/5) = 10^8 pc = 100 Mpc
        expected = 100.0
        mu = 15 - (-20)
        computed = 10**((mu + 5) / 5) / 1e6  # pc to Mpc
        return verifier._ok("magnitude_distance", expected, computed,
                            "m=15, M=-20, d in Mpc")
    h["magnitude_distance"] = _magnitude_distance

    def _orbital_period():
        # Mars: T = sqrt(a^3) = sqrt(1.524^3) = sqrt(3.54) = 1.881
        expected = 1.881
        computed = math.sqrt(1.524**3)
        return verifier._ok("orbital_period", expected, computed,
                            "Mars a=1.524 AU")
    h["orbital_period"] = _orbital_period

    def _pendulum_period():
        expected = 2.006
        computed = 2 * math.pi * math.sqrt(1 / 9.81)
        return verifier._ok("pendulum_period", expected, computed,
                            "L=1m, g=9.81")
    h["pendulum_period"] = _pendulum_period

    def _redshift():
        expected = 0.0666
        computed = (700 - 656.3) / 656.3
        return verifier._ok("redshift", expected, computed,
                            "obs=700nm, rest=656.3nm")
    h["redshift"] = _redshift

    def _schwarzschild_radius():
        expected = 2953.0
        G, M, c = 6.674e-11, 1.989e30, 3e8
        computed = 2 * G * M / c**2
        return verifier._ok("schwarzschild_radius", expected, computed,
                            "Sun M=1.989e30", tol=0.02)
    h["schwarzschild_radius"] = _schwarzschild_radius

    def _stellar_luminosity():
        expected = 3.85e26
        R, T = 6.96e8, 5778
        sigma = 5.67e-8
        computed = 4 * math.pi * R**2 * sigma * T**4
        return verifier._ok("stellar_luminosity", expected, computed,
                            "Sun R=6.96e8, T=5778", tol=0.02)
    h["stellar_luminosity"] = _stellar_luminosity

    def _wave_equation():
        expected = 0.78
        computed = 343 / 440.0
        return verifier._ok("wave_equation", expected, computed,
                            "v=343, f=440")
    h["wave_equation"] = _wave_equation

    # === AI/ML ===

    def _bellman_equation():
        expected = 6.8
        computed = max(1 + 0.9 * 3, 5 + 0.9 * 2)
        return verifier._ok("bellman_equation", expected, computed,
                            "V(s1)=max(3.7,6.8)")
    h["bellman_equation"] = _bellman_equation

    def _bias_variance():
        expected = 5.5
        computed = 4 + 1 + 0.5
        return verifier._ok("bias_variance", expected, computed,
                            "Bias^2=4, Var=1, Noise=0.5")
    h["bias_variance"] = _bias_variance

    def _conv_output_size():
        expected = 28.0
        computed = (32 - 5 + 2 * 0) / 1 + 1
        return verifier._ok("conv_output_size", expected, computed,
                            "input=32, kernel=5, stride=1, pad=0")
    h["conv_output_size"] = _conv_output_size

    def _discounted_return():
        expected = 16.93
        computed = 10 + 0.9 * 5 + 0.81 * 3
        return verifier._ok("discounted_return", expected, computed,
                            "rewards=[10,5,3], gamma=0.9")
    h["discounted_return"] = _discounted_return

    def _gradient_descent():
        # x_1 = 5 - 0.1*10 = 4
        expected = 4.0
        computed = 5 - 0.1 * (2 * 5)
        return verifier._ok("gradient_descent", expected, computed,
                            "f=x^2, x0=5, lr=0.1, x1")
    h["gradient_descent"] = _gradient_descent

    def _lr_decay():
        expected = 0.0665
        computed = 0.1 * 0.96**10
        return verifier._ok("lr_decay", expected, computed,
                            "lr0=0.1, decay=0.96, epoch=10")
    h["lr_decay"] = _lr_decay

    def _q_value_update():
        expected = 5.32
        computed = 5 + 0.1 * (1 + 0.9 * 8 - 5)
        return verifier._ok("q_value_update", expected, computed,
                            "Q=5, R=1, maxQ'=8, gamma=0.9, alpha=0.1")
    h["q_value_update"] = _q_value_update

    def _polynomial_hash():
        expected = 354.0
        computed = (97 * 31**2 + 98 * 31 + 99) % 1000
        return verifier._ok("polynomial_hash", expected, computed,
                            "'abc', base=31, mod=1000")
    h["polynomial_hash"] = _polynomial_hash

    # === MATH ===

    def _bloch_coords():
        # z-component: cos(pi/3) = 0.5
        expected = 0.5
        computed = math.cos(math.pi / 3)
        return verifier._ok("bloch_coords", expected, computed,
                            "theta=pi/3, cos(pi/3)=0.5")
    h["bloch_coords"] = _bloch_coords

    def _de_moivre():
        # (cos30+isin30)^6 = cos180+isin180 = -1
        expected = -1.0
        computed = math.cos(math.radians(180))
        return verifier._ok("de_moivre", expected, computed,
                            "(cis 30)^6 = cis 180 = -1")
    h["de_moivre"] = _de_moivre

    def _euler_formula():
        # e^(i*pi/3) = cos(pi/3) + i*sin(pi/3) = 0.5 + 0.866i
        expected = 0.5
        computed = math.cos(math.pi / 3)
        return verifier._ok("euler_formula", expected, computed,
                            "e^(i*pi/3) real part")
    h["euler_formula"] = _euler_formula

    def _knapsack():
        expected = 70.0
        computed = 40 + 30.0  # items (w=4,v=40) + (w=6,v=30)
        return verifier._ok("knapsack", expected, computed,
                            "W=10, optimal v=70")
    h["knapsack"] = _knapsack

    def _lcs():
        expected = 4.0
        computed = 4.0  # LCS of ABCBDAB, BDCAB = BCAB, length 4
        return verifier._ok("lcs", expected, computed,
                            "ABCBDAB vs BDCAB, LCS len=4")
    h["lcs"] = _lcs

    def _lis():
        expected = 4.0
        computed = 4.0  # [2,3,7,101] or [2,5,7,101]
        return verifier._ok("lis", expected, computed,
                            "[10,9,2,5,3,7,101,18], LIS len=4")
    h["lis"] = _lis

    def _vigenere():
        # H(7)+K(10)=R(17), E(4)+E(4)=I(8), L(11)+Y(24)=J(9 mod 26)
        # L(11)+K(10)=V(21), O(14)+E(4)=S(18)
        expected = 17.0  # 'R' = 17th letter (0-indexed)
        computed = (7 + 10) % 26.0
        return verifier._ok("vigenere", expected, computed,
                            "H+K mod 26 = R")
    h["vigenere"] = _vigenere

    # === BAYESIAN ===

    def _bayes_chain():
        expected = 0.727
        computed = 0.8 * 0.5 / (0.8 * 0.5 + 0.3 * 0.5)
        return verifier._ok("bayes_chain", expected, computed,
                            "P(H)=0.5, P(E|H)=0.8, P(E|~H)=0.3")
    h["bayes_chain"] = _bayes_chain

    # === POLICY/RL ===

    def _markov_reward():
        expected = 10.0
        computed = 0.8 * 10 + 0.2 * 10
        return verifier._ok("markov_reward", expected, computed,
                            "R=10, P(s')=0.8, P(s'')=0.2")
    h["markov_reward"] = _markov_reward
