"""Knowledge atoms for thermodynamics_ext, optics_ext, and robotics_ext.

Each atom includes the canonical formula from Wikipedia, a worked
example with known input/output, and an authoritative source URL.
"""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom


# ── THERMODYNAMICS EXT ────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="otto_cycle",
    content=(
        "The Otto cycle is the idealized thermodynamic cycle for spark-ignition "
        "engines. Its thermal efficiency depends only on the compression ratio r "
        "and the heat capacity ratio gamma: eta = 1 - 1/r^(gamma-1). "
        "Higher compression ratios yield higher efficiency."
    ),
    example=(
        "Given r=8, gamma=1.4: eta = 1 - 1/8^0.4 = 1 - 1/2.2974 = 1 - 0.4352 = 0.5648 (56.5%)"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Otto cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Otto_cycle",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="diesel_cycle",
    content=(
        "The Diesel cycle models compression-ignition engines. Efficiency: "
        "eta = 1 - (1/r^(gamma-1)) * (rho^gamma - 1) / (gamma*(rho - 1)), "
        "where r is compression ratio and rho is cutoff ratio (V3/V2)."
    ),
    example=(
        "Given r=18, rho=2, gamma=1.4: eta = 1 - (1/18^0.4)*(2^1.4 - 1)/(1.4*(2-1)) "
        "= 1 - (1/3.178)*(2.639-1)/1.4 = 1 - 0.3147*1.1707 = 1 - 0.3685 = 0.6315 (63.2%)"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Diesel cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diesel_cycle",
    prerequisites=["otto_cycle"],
))

register_atom(Atom(
    atom_type="formula",
    name="rankine_cycle",
    content=(
        "The Rankine cycle is the idealized cycle for steam power plants. "
        "Thermal efficiency: eta = (h1 - h2) / (h1 - h4), where h1 is "
        "turbine inlet enthalpy, h2 is turbine outlet enthalpy, and h4 is "
        "boiler inlet enthalpy (after pump). Work output W_net = W_turbine - W_pump."
    ),
    example=(
        "Given h1=3400 kJ/kg, h2=2400 kJ/kg, h4=200 kJ/kg: "
        "eta = (3400-2400)/(3400-200) = 1000/3200 = 0.3125 (31.25%)"
    ),
    tier=6,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Rankine cycle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Rankine_cycle",
    prerequisites=["carnot_efficiency", "first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula",
    name="refrigeration_cop",
    content=(
        "The coefficient of performance (COP) of a refrigerator is the ratio "
        "of heat removed from the cold reservoir to work input: "
        "COP_ref = Q_cold / W = Q_cold / (Q_hot - Q_cold). "
        "For a Carnot refrigerator: COP = T_cold / (T_hot - T_cold)."
    ),
    example=(
        "Given T_cold=260K, T_hot=300K: COP = 260/(300-260) = 260/40 = 6.5"
    ),
    tier=4,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Coefficient of performance', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Coefficient_of_performance",
    prerequisites=["carnot_efficiency"],
))

register_atom(Atom(
    atom_type="formula",
    name="throttling_process",
    content=(
        "In a throttling process (isenthalpic expansion), a fluid passes "
        "through a restriction with no heat or work exchange: h1 = h2 "
        "(enthalpy is conserved). For an ideal gas, temperature remains "
        "constant. For real gases, the Joule-Thomson coefficient "
        "mu_JT = (dT/dP)_h determines whether cooling or heating occurs."
    ),
    example=(
        "Ideal gas throttling from P1=500kPa to P2=100kPa: "
        "h1=h2, T1=T2=300K (no temperature change for ideal gas)"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Joule-Thomson effect', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Joule%E2%80%93Thomson_effect",
    prerequisites=["first_law_thermo"],
))

register_atom(Atom(
    atom_type="formula",
    name="maxwell_relations",
    content=(
        "Maxwell relations are a set of equalities between second partial "
        "derivatives of thermodynamic potentials. From the Helmholtz free "
        "energy F: (dS/dV)_T = (dP/dT)_V. From the Gibbs free energy G: "
        "(dV/dT)_P = -(dS/dP)_T. These connect measurable quantities to "
        "entropy derivatives."
    ),
    example=(
        "From dF = -SdT - PdV: d^2F/dTdV = d^2F/dVdT gives "
        "(dS/dV)_T = (dP/dT)_V"
    ),
    tier=6,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Maxwell relations', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Maxwell_relations",
    prerequisites=["entropy_change"],
))

register_atom(Atom(
    atom_type="formula",
    name="van_der_waals",
    content=(
        "The van der Waals equation models real gas behavior: "
        "(P + a*n^2/V^2)(V - n*b) = nRT, where a accounts for "
        "intermolecular attractions and b for molecular volume. "
        "Reduces to ideal gas law when a=b=0."
    ),
    example=(
        "CO2 (a=3.59, b=0.0427): 1 mol at T=500K, V=1L: "
        "P = nRT/(V-nb) - a*n^2/V^2 = 1*8.314*500/(1-0.0427) - 3.59/1 "
        "= 4344.6 - 3.59 = 4341.0 kPa"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Van der Waals equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Van_der_Waals_equation",
    prerequisites=["ideal_gas"],
))

register_atom(Atom(
    atom_type="formula",
    name="entropy_mixing",
    content=(
        "The entropy of mixing for ideal gases: "
        "Delta_S_mix = -nR * sum(x_i * ln(x_i)), where x_i are mole "
        "fractions. This is always positive (mixing is spontaneous for "
        "ideal gases at constant T and P)."
    ),
    example=(
        "Mixing 2 mol N2 + 3 mol O2: x_N2=0.4, x_O2=0.6, n=5: "
        "Delta_S = -5*8.314*(0.4*ln(0.4) + 0.6*ln(0.6)) "
        "= -41.57*(-0.3665 - 0.3066) = -41.57*(-0.6731) = 27.98 J/K"
    ),
    tier=5,
    domain="thermodynamics",
    source="Wikipedia contributors, 'Entropy of mixing', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Entropy_of_mixing",
    prerequisites=["entropy_change"],
))


# ── OPTICS EXT ────────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="lens_makers",
    content=(
        "The lensmaker's equation relates the focal length of a thin lens "
        "to its radii of curvature and refractive index: "
        "1/f = (n-1) * (1/R1 - 1/R2), where n is the refractive index "
        "of the lens material, R1 and R2 are the radii of curvature."
    ),
    example=(
        "Given n=1.5, R1=20cm, R2=-30cm: "
        "1/f = (1.5-1)*(1/20 - 1/(-30)) = 0.5*(0.05+0.0333) = 0.5*0.0833 = 0.0417, "
        "f = 24.0 cm"
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Lensmaker's equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Lensmaker%27s_equation",
    prerequisites=["thin_lens"],
))

register_atom(Atom(
    atom_type="formula",
    name="two_lens_system",
    content=(
        "For two thin lenses separated by distance d, the combined focal "
        "length is: 1/f = 1/f1 + 1/f2 - d/(f1*f2). When d=0 (lenses in "
        "contact): 1/f = 1/f1 + 1/f2."
    ),
    example=(
        "f1=10cm, f2=20cm, d=5cm: 1/f = 1/10 + 1/20 - 5/(10*20) "
        "= 0.1 + 0.05 - 0.025 = 0.125, f = 8.0 cm"
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Thin lens', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thin_lens",
    prerequisites=["lens_makers"],
))

register_atom(Atom(
    atom_type="formula",
    name="single_slit_diffraction",
    content=(
        "Single-slit diffraction produces minima at angles where "
        "a*sin(theta) = m*lambda (m = +/-1, +/-2, ...), where a is the "
        "slit width, lambda is the wavelength. The central maximum has "
        "angular half-width theta_1 = arcsin(lambda/a)."
    ),
    example=(
        "Slit a=0.1mm, lambda=600nm: first minimum at "
        "sin(theta) = 600e-9/0.1e-3 = 0.006, theta = 0.344 degrees"
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Diffraction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Diffraction",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="thin_film_interference",
    content=(
        "Thin film interference occurs when light reflects from the top "
        "and bottom of a thin film. Constructive interference (in "
        "reflected light with one phase inversion): 2*n*t = (m+1/2)*lambda. "
        "Destructive: 2*n*t = m*lambda, where n is film refractive index "
        "and t is thickness."
    ),
    example=(
        "Oil film (n=1.4) on water, t=200nm, lambda=560nm: "
        "2*1.4*200 = 560 = 1*560 -> destructive (dark) in reflected light"
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Thin-film interference', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Thin-film_interference",
    prerequisites=["double_slit"],
))

register_atom(Atom(
    atom_type="formula",
    name="polarization",
    content=(
        "Malus's law describes the intensity of polarized light passing "
        "through a polarizer: I = I_0 * cos^2(theta), where theta is "
        "the angle between the light's polarization direction and the "
        "polarizer axis. At theta=90 degrees, no light passes."
    ),
    example=(
        "I_0=100 W/m^2, theta=60 degrees: I = 100*cos^2(60) = 100*0.25 = 25 W/m^2"
    ),
    tier=4,
    domain="optics",
    source="Wikipedia contributors, 'Malus's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Polarizer#Malus's_law_and_other_properties",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="resolving_power",
    content=(
        "The Rayleigh criterion gives the minimum resolvable angle for "
        "a circular aperture: theta_min = 1.22 * lambda / D, where D is "
        "the aperture diameter. Two point sources are just resolved when "
        "the central maximum of one falls on the first minimum of the other."
    ),
    example=(
        "Telescope D=0.1m, lambda=550nm: theta_min = 1.22*550e-9/0.1 "
        "= 6.71e-6 rad = 1.38 arcsec"
    ),
    tier=5,
    domain="optics",
    source="Wikipedia contributors, 'Angular resolution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Angular_resolution",
    prerequisites=["single_slit_diffraction"],
))

register_atom(Atom(
    atom_type="formula",
    name="optical_path_length",
    content=(
        "The optical path length (OPL) is the product of the geometric "
        "path length and the refractive index: OPL = n * d. For a ray "
        "passing through multiple media: OPL = sum(n_i * d_i). Fermat's "
        "principle states light takes the path of minimum OPL."
    ),
    example=(
        "Light through 10cm of glass (n=1.5) and 20cm of water (n=1.33): "
        "OPL = 1.5*10 + 1.33*20 = 15 + 26.6 = 41.6 cm"
    ),
    tier=4,
    domain="optics",
    source="Wikipedia contributors, 'Optical path length', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Optical_path_length",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="mirror_equation",
    content=(
        "The mirror equation relates object distance (u), image distance "
        "(v), and focal length (f): 1/f = 1/v + 1/u. Magnification: "
        "m = -v/u. For concave mirrors f>0, for convex f<0. "
        "Sign convention: distances measured from the mirror pole."
    ),
    example=(
        "Concave mirror f=15cm, object at u=-30cm: "
        "1/v = 1/15 - 1/(-30) = 1/15 + 1/30 = 3/30 = 1/10, v = 10cm (real, inverted)"
    ),
    tier=4,
    domain="optics",
    source="Wikipedia contributors, 'Mirror formula', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Curved_mirror#Mirror_equation",
    prerequisites=["thin_lens"],
))


# ── ROBOTICS EXT ──────────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="dh_transform",
    content=(
        "The Denavit-Hartenberg (DH) convention parameterizes each joint "
        "of a robot arm with four parameters: theta (joint angle), d "
        "(link offset), a (link length), alpha (link twist). The "
        "homogeneous transformation for each joint is: "
        "T = Rot_z(theta) * Trans_z(d) * Trans_x(a) * Rot_x(alpha)."
    ),
    example=(
        "Joint with theta=90deg, d=0, a=1, alpha=0: "
        "T = [[0,-1,0,0],[1,0,0,1],[0,0,1,0],[0,0,0,1]] "
        "(rotation by 90deg about z, then translate 1 along x)"
    ),
    tier=5,
    domain="robotics",
    source="Wikipedia contributors, 'Denavit-Hartenberg parameters', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Denavit%E2%80%93Hartenberg_parameters",
    prerequisites=["forward_kinematics"],
))

register_atom(Atom(
    atom_type="formula",
    name="jacobian_robot",
    content=(
        "The robot Jacobian J relates joint velocities to end-effector "
        "velocities: v = J * dq/dt. For a 2-link planar arm: "
        "J = [[-L1*sin(q1)-L2*sin(q1+q2), -L2*sin(q1+q2)], "
        "[L1*cos(q1)+L2*cos(q1+q2), L2*cos(q1+q2)]]. "
        "Singularities occur when det(J)=0."
    ),
    example=(
        "2-link arm L1=L2=1, q1=0, q2=90deg: "
        "J = [[-1, -1], [1, 0]], det(J) = 0-(-1) = 1 (non-singular)"
    ),
    tier=6,
    domain="robotics",
    source="Wikipedia contributors, 'Jacobian matrix and determinant', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Jacobian_matrix_and_determinant",
    prerequisites=["dh_transform"],
))

register_atom(Atom(
    atom_type="definition",
    name="workspace_analysis",
    content=(
        "The workspace of a robot manipulator is the set of all points "
        "reachable by the end-effector. For a 2-link planar arm with "
        "link lengths L1 and L2: the reachable workspace is an annulus "
        "with inner radius |L1-L2| and outer radius L1+L2."
    ),
    example=(
        "2-link arm L1=3, L2=2: reachable annulus inner=|3-2|=1, "
        "outer=3+2=5. Point at distance 4 is reachable, at distance 6 is not."
    ),
    tier=5,
    domain="robotics",
    source="Wikipedia contributors, 'Workspace (robotics)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Workspace_(robotics)",
    prerequisites=["forward_kinematics"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="trajectory_planning",
    content=(
        "Trajectory planning generates a smooth path q(t) for each joint "
        "over time. A cubic polynomial trajectory between two points: "
        "q(t) = a0 + a1*t + a2*t^2 + a3*t^3, with boundary conditions "
        "q(0)=q_start, q(T)=q_end, dq/dt(0)=0, dq/dt(T)=0."
    ),
    example=(
        "q_start=0, q_end=90deg, T=2s: a0=0, a1=0, "
        "a2=3*90/4=67.5, a3=-2*90/8=-22.5. At t=1: q(1)=67.5-22.5=45deg"
    ),
    tier=5,
    domain="robotics",
    source="Wikipedia contributors, 'Motion planning', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Motion_planning",
    prerequisites=["forward_kinematics"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="potential_field",
    content=(
        "The artificial potential field method for robot navigation creates "
        "an attractive potential toward the goal and repulsive potentials "
        "around obstacles. The robot moves in the direction of the negative "
        "gradient: F = -grad(U_att + U_rep). "
        "U_att = 0.5*k_att*d_goal^2, U_rep = 0.5*k_rep*(1/d_obs - 1/d0)^2."
    ),
    example=(
        "Robot at (3,4), goal at (10,10), k_att=1: "
        "F_att = -k_att*(pos-goal) = -(3-10, 4-10) = (7, 6)"
    ),
    tier=5,
    domain="robotics",
    source="Wikipedia contributors, 'Artificial potential field', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Motion_planning#Artificial_potential_fields",
    prerequisites=["path_planning"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="sensor_fusion",
    content=(
        "Sensor fusion combines data from multiple sensors to produce "
        "more accurate estimates. A simple weighted average for two "
        "sensors with variances sigma1^2 and sigma2^2: "
        "x_fused = (x1/sigma1^2 + x2/sigma2^2) / (1/sigma1^2 + 1/sigma2^2), "
        "sigma_fused^2 = 1 / (1/sigma1^2 + 1/sigma2^2)."
    ),
    example=(
        "Sensor1: x1=10.2, sigma1=0.5; Sensor2: x2=10.8, sigma2=1.0: "
        "x_fused = (10.2/0.25 + 10.8/1.0)/(1/0.25 + 1/1.0) "
        "= (40.8+10.8)/(4+1) = 51.6/5 = 10.32"
    ),
    tier=5,
    domain="robotics",
    source="Wikipedia contributors, 'Sensor fusion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Sensor_fusion",
    prerequisites=["kalman_gain"],
))

register_atom(Atom(
    atom_type="formula",
    name="odometry",
    content=(
        "Odometry estimates a robot's position from wheel encoder data. "
        "For a differential drive robot with wheel radius r and base "
        "width L: v = r*(omega_R + omega_L)/2, "
        "omega = r*(omega_R - omega_L)/L. Position update: "
        "x += v*cos(theta)*dt, y += v*sin(theta)*dt, theta += omega*dt."
    ),
    example=(
        "r=0.05m, L=0.3m, omega_R=10 rad/s, omega_L=8 rad/s, dt=0.1s: "
        "v = 0.05*(10+8)/2 = 0.45 m/s, omega = 0.05*(10-8)/0.3 = 0.333 rad/s. "
        "Starting (0,0,0): x=0.045, y=0, theta=0.0333"
    ),
    tier=4,
    domain="robotics",
    source="Wikipedia contributors, 'Odometry', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Odometry",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="reward_shaping",
    content=(
        "Reward shaping modifies a reward function to speed up "
        "reinforcement learning without changing the optimal policy. "
        "A potential-based shaping function F(s,s') = gamma*Phi(s') - Phi(s) "
        "preserves the optimal policy (Ng et al., 1999). The shaped reward "
        "is R'(s,a,s') = R(s,a,s') + F(s,s')."
    ),
    example=(
        "Phi(s) = -distance_to_goal. s at dist 10, s' at dist 8, gamma=0.99: "
        "F = 0.99*(-8) - (-10) = -7.92 + 10 = 2.08 (bonus for getting closer)"
    ),
    tier=6,
    domain="robotics",
    source="Wikipedia contributors, 'Reward shaping', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Reward_shaping",
    prerequisites=["q_learning"],
))
