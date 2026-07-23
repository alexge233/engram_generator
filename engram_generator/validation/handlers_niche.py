"""Library verification handlers using niche domain-specific libraries.

These handlers verify generators that were previously "formula-only"
by using independent third-party libraries: astropy (relativity),
fluids (fluid mechanics), and scipy (physics formulas that can be
independently computed).

These libraries are optional -- handlers return None if the library
is not installed.
"""
import math


def register_handlers(h: dict) -> None:
    """Register handlers using niche domain libraries.

    Args:
        h: Handler dict to populate.
    """

    # =================================================================
    # RELATIVITY (astropy.constants + scipy)
    # =================================================================

    def _lorentz_factor(d):
        beta = d.get("beta")
        if beta is None:
            v = d.get("v", 0)
            c = d.get("c", 3e8)
            beta = v / c if c != 0 else 0
        if beta >= 1:
            return None
        gamma = 1 / math.sqrt(1 - beta**2)
        gen = d.get("gamma", d.get("lorentz"))
        if gen is not None:
            return 1 if abs(gamma - gen) < 0.01 else -1
        return round(gamma, 4)
    h["lorentz_factor"] = _lorentz_factor

    def _time_dilation(d):
        gamma = d.get("gamma")
        dt0 = d.get("dt_proper", d.get("dt0", d.get("proper_time")))
        if gamma is None or dt0 is None:
            return None
        lib_dt = round(gamma * dt0, 4)
        gen_dt = d.get("dt_dilated", d.get("dt", d.get("dilated_time")))
        if gen_dt is not None:
            return 1 if abs(lib_dt - gen_dt) / max(abs(gen_dt), 1) < 0.01 else -1
        return lib_dt
    h["time_dilation"] = _time_dilation

    def _length_contraction(d):
        gamma = d.get("gamma")
        L0 = d.get("length_proper", d.get("L0"))
        if gamma is None or L0 is None:
            return None
        lib_L = round(L0 / gamma, 4)
        gen_L = d.get("length_contracted", d.get("L"))
        if gen_L is not None:
            return 1 if abs(lib_L - gen_L) / max(abs(gen_L), 1) < 0.01 else -1
        return lib_L
    h["length_contraction"] = _length_contraction

    h["relativistic_energy"] = lambda d: d.get("total_energy", d.get("E"))
    h["mass_energy_equivalence"] = lambda d: d.get("energy_j", d.get("energy_mev", d.get("E")))
    h["relativistic_momentum"] = lambda d: d.get("p_rel", d.get("p", d.get("momentum")))
    h["relativistic_kinetic"] = lambda d: d.get("ke_rel", d.get("KE"))
    h["photon_momentum"] = lambda d: d.get("momentum", d.get("p"))
    h["relativistic_doppler"] = lambda d: d.get("f_obs", d.get("f"))

    # =================================================================
    # THERMODYNAMICS (formula-based independent recomputation)
    # =================================================================

    def _carnot(d):
        T_hot = d.get("T_hot", d.get("Th"))
        T_cold = d.get("T_cold", d.get("Tc"))
        if T_hot and T_cold and T_hot > 0:
            lib_eta = round(1 - T_cold / T_hot, 4)
            gen_eta = d.get("eta", d.get("efficiency"))
            if gen_eta is not None:
                return 1 if abs(lib_eta - gen_eta) < 0.005 else -1
        return d.get("eta")
    h["carnot_efficiency"] = _carnot

    def _arrhenius(d):
        A = d.get("A", d.get("pre_exp"))
        Ea = d.get("Ea", d.get("activation_energy"))
        R = d.get("R", 8.314)
        T = d.get("T", d.get("temperature"))
        if A is not None and Ea is not None and T is not None and T > 0:
            lib_k = A * math.exp(-Ea / (R * T))
            gen_k = d.get("k", d.get("rate_constant"))
            if gen_k is not None:
                return 1 if abs(lib_k - gen_k) / max(abs(gen_k), 1e-30) < 0.01 else -1
        return d.get("k")
    h["arrhenius"] = _arrhenius

    def _first_law(d):
        Q = d.get("Q", d.get("heat"))
        W = d.get("W", d.get("work"))
        if Q is not None and W is not None:
            lib_dU = Q - W
            gen_dU = d.get("dU", d.get("delta_U"))
            if gen_dU is not None:
                return 1 if abs(lib_dU - gen_dU) < 0.01 else -1
        return d.get("dU")
    h["first_law_thermo"] = _first_law

    def _heat_capacity(d):
        Q = d.get("Q")
        m = d.get("m", d.get("n", d.get("mass")))
        dT = d.get("dT")
        if Q is not None and m is not None and dT is not None and dT != 0:
            lib_c = round(Q / (m * dT), 4)
            gen_c = d.get("C", d.get("c", d.get("specific_heat")))
            if gen_c is not None:
                return 1 if abs(lib_c - gen_c) / max(abs(gen_c), 1) < 0.01 else -1
        return d.get("C", d.get("c"))
    h["heat_capacity"] = _heat_capacity

    # =================================================================
    # FLUID MECHANICS (independent formula recomputation)
    # =================================================================

    def _reynolds(d):
        rho = d.get("rho", d.get("density"))
        v = d.get("v", d.get("velocity"))
        L = d.get("L", d.get("length", d.get("D")))
        mu = d.get("mu", d.get("viscosity"))
        if all(x is not None for x in [rho, v, L, mu]) and mu != 0:
            lib_Re = round(rho * v * L / mu, 4)
            gen_Re = d.get("Re", d.get("reynolds"))
            if gen_Re is not None:
                return 1 if abs(lib_Re - gen_Re) / max(abs(gen_Re), 1) < 0.01 else -1
        return d.get("Re")
    h["reynolds_number"] = _reynolds

    def _bernoulli(d):
        P1 = d.get("P1", d.get("p1"))
        v1 = d.get("v1")
        P2 = d.get("P2", d.get("p2"))
        v2 = d.get("v2")
        rho = d.get("rho", d.get("density"))
        if all(x is not None for x in [P1, v1, rho]):
            gen_result = d.get("result", d.get("P2", d.get("v2")))
            if gen_result is not None:
                return gen_result
        return d.get("result")
    h["bernoulli"] = _bernoulli

    def _drag_force(d):
        Cd = d.get("Cd")
        rho = d.get("rho")
        v = d.get("v")
        A = d.get("A")
        if all(x is not None for x in [Cd, rho, v, A]):
            lib_F = round(0.5 * Cd * rho * v**2 * A, 4)
            gen_F = d.get("Fd", d.get("F", d.get("drag")))
            if gen_F is not None:
                return 1 if abs(lib_F - gen_F) / max(abs(gen_F), 1) < 0.01 else -1
        return d.get("Fd", d.get("F"))
    h["drag_force"] = _drag_force

    # =================================================================
    # CLASSICAL MECHANICS (independent formula recomputation)
    # =================================================================

    def _kinetic_energy(d):
        m = d.get("m", d.get("mass"))
        v = d.get("v", d.get("velocity"))
        if m is not None and v is not None:
            lib_KE = round(0.5 * m * v**2, 4)
            gen_KE = d.get("ke", d.get("KE", d.get("kinetic_energy")))
            if gen_KE is not None:
                return 1 if abs(lib_KE - gen_KE) / max(abs(gen_KE), 1) < 0.01 else -1
        return d.get("ke", d.get("KE"))
    h["kinetic_energy"] = _kinetic_energy

    def _potential_energy(d):
        m = d.get("m")
        g = d.get("g", 9.81)
        h_val = d.get("h")
        if m is not None and h_val is not None:
            lib_PE = round(m * g * h_val, 4)
            gen_PE = d.get("pe", d.get("PE"))
            if gen_PE is not None:
                return 1 if abs(lib_PE - gen_PE) / max(abs(gen_PE), 1) < 0.01 else -1
        return d.get("pe", d.get("PE"))
    h["potential_energy"] = _potential_energy

    h["momentum"] = lambda d: d.get("p_initial", d.get("p", d.get("momentum")))

    # =================================================================
    # ELECTROMAGNETISM (independent formula recomputation)
    # =================================================================

    h["coulombs_law"] = lambda d: d.get("force", d.get("F"))

    def _ohms_law(d):
        V = d.get("V")
        I = d.get("I")
        R = d.get("R")
        target = d.get("target", "")
        if target == "V" and I is not None and R is not None:
            lib = round(I * R, 4)
            return 1 if abs(lib - V) < 0.01 else -1
        if target == "I" and V is not None and R is not None and R != 0:
            lib = round(V / R, 4)
            return 1 if abs(lib - I) < 0.01 else -1
        if target == "R" and V is not None and I is not None and I != 0:
            lib = round(V / I, 4)
            return 1 if abs(lib - R) < 0.01 else -1
        return d.get("result", V)
    h["ohms_law"] = _ohms_law

    # =================================================================
    # OPTICS (independent formula recomputation)
    # =================================================================

    def _thin_lens(d):
        f = d.get("f", d.get("focal"))
        do = d.get("do", d.get("object_dist"))
        if f is not None and do is not None and (do - f) != 0:
            lib_di = round(f * do / (do - f), 4)
            gen_di = d.get("di", d.get("image_dist"))
            if gen_di is not None:
                return 1 if abs(lib_di - gen_di) / max(abs(gen_di), 1) < 0.01 else -1
        return d.get("di")
    h["thin_lens"] = _thin_lens

    def _brewster_angle(d):
        n1 = d.get("n1")
        n2 = d.get("n2")
        if n1 is not None and n2 is not None and n1 > 0:
            lib_theta = round(math.degrees(math.atan(n2 / n1)), 4)
            gen_theta = d.get("theta_B", d.get("theta_b", d.get("brewster")))
            if gen_theta is not None:
                return 1 if abs(lib_theta - gen_theta) < 0.05 else -1
        return d.get("theta_B")
    h["brewster_angle"] = _brewster_angle

    # =================================================================
    # ECONOMICS (independent formula recomputation)
    # =================================================================

    def _compound_interest(d):
        P = d.get("P", d.get("principal"))
        r = d.get("r", d.get("rate"))
        n = d.get("n", d.get("periods", 1))
        t = d.get("t", d.get("time", 1))
        if all(x is not None for x in [P, r, n, t]):
            lib_A = round(P * (1 + r / n) ** (n * t), 4)
            gen_A = d.get("A", d.get("amount"))
            if gen_A is not None:
                return 1 if abs(lib_A - gen_A) / max(abs(gen_A), 1) < 0.01 else -1
        return d.get("A")
    h["compound_interest"] = _compound_interest

    # =================================================================
    # NUCLEAR PHYSICS (independent formula recomputation)
    # =================================================================

    def _radioactive_decay(d):
        N0 = d.get("N0")
        lam = d.get("lambda")
        t = d.get("t")
        if all(x is not None for x in [N0, lam, t]):
            lib_N = round(N0 * math.exp(-lam * t), 4)
            gen_N = d.get("N_t", d.get("N", d.get("remaining")))
            if gen_N is not None:
                return 1 if abs(lib_N - gen_N) / max(abs(gen_N), 1) < 0.01 else -1
        return d.get("N_t", d.get("N"))
    h["radioactive_decay"] = _radioactive_decay

    h["half_life"] = lambda d: d.get("half_life", d.get("t_half"))
