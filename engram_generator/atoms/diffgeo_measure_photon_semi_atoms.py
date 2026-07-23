"""Knowledge atoms for differential geometry ext, measure theory ext, photonics, and semiconductors."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Differential Geometry Ext (tiers 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="frenet_serret",
    content="The Frenet-Serret formulas describe how the tangent T, normal N, and binormal B vectors change along a curve: dT/ds = kappa*N, dN/ds = -kappa*T + tau*B, dB/ds = -tau*N, where kappa is curvature and tau is torsion. s is arc length.",
    example="Helix r(t)=(cos t, sin t, t): T=(-sin t, cos t, 1)/sqrt(2), kappa=1/2, tau=1/2. The curve has constant curvature and torsion.",
    tier=6, domain="diffgeo_ext",
    source="Wikipedia contributors, 'Frenet-Serret formulas', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Frenet%E2%80%93Serret_formulas",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="surface_normal",
    content="The unit normal to a parametric surface r(u,v) is n = (r_u x r_v) / |r_u x r_v|, where r_u and r_v are partial derivatives. For an implicit surface F(x,y,z)=0: n = grad(F)/|grad(F)|.",
    example="Sphere x^2+y^2+z^2=1 at (1,0,0): grad(F)=(2x,2y,2z)=(2,0,0). n=(1,0,0).",
    tier=5, domain="diffgeo_ext",
    source="Wikipedia contributors, 'Normal (geometry)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Normal_(geometry)",
    prerequisites=["cross_product", "partial_derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="first_fundamental_form",
    content="The first fundamental form I = E*du^2 + 2*F*du*dv + G*dv^2 measures distances on a surface, where E = r_u . r_u, F = r_u . r_v, G = r_v . r_v. Arc length: ds^2 = I. Area element: dA = sqrt(EG-F^2)*du*dv.",
    example="Plane r(u,v)=(u,v,0): r_u=(1,0,0), r_v=(0,1,0). E=1, F=0, G=1. ds^2=du^2+dv^2 (Euclidean).",
    tier=6, domain="diffgeo_ext",
    source="Wikipedia contributors, 'First fundamental form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/First_fundamental_form",
    prerequisites=["dot_product"],
))

register_atom(Atom(
    atom_type="formula",
    name="second_fundamental_form",
    content="The second fundamental form II = e*du^2 + 2*f*du*dv + g*dv^2 measures curvature, where e = r_uu . n, f = r_uv . n, g = r_vv . n, and n is the unit normal. Gaussian curvature K = (eg-f^2)/(EG-F^2). Mean curvature H = (eG-2fF+gE)/(2(EG-F^2)).",
    example="Sphere r=R: e=R, f=0, g=R*sin^2(theta). K=1/R^2, H=1/R.",
    tier=7, domain="diffgeo_ext",
    source="Wikipedia contributors, 'Second fundamental form', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Second_fundamental_form",
    prerequisites=["first_fundamental_form"],
))

register_atom(Atom(
    atom_type="formula",
    name="mean_curvature",
    content="Mean curvature H = (kappa_1 + kappa_2)/2, where kappa_1 and kappa_2 are the principal curvatures. Equivalently H = (eG - 2fF + gE) / (2(EG-F^2)). A surface with H=0 everywhere is a minimal surface (soap films).",
    example="Cylinder radius R: kappa_1=1/R (circumferential), kappa_2=0 (axial). H = 1/(2R). Not minimal.",
    tier=7, domain="diffgeo_ext",
    source="Wikipedia contributors, 'Mean curvature', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mean_curvature",
    prerequisites=["second_fundamental_form"],
))

register_atom(Atom(
    atom_type="definition",
    name="parallel_transport",
    content="Parallel transport moves a vector along a curve on a surface while keeping it 'as parallel as possible' (covariant derivative = 0). On a curved surface, parallel transport around a closed loop rotates the vector by the holonomy angle, proportional to the enclosed Gaussian curvature.",
    example="Transport a tangent vector around a spherical triangle with three 90-degree angles. The vector rotates by the angular excess = area/R^2 = pi/2 radians.",
    tier=7, domain="diffgeo_ext",
    source="Wikipedia contributors, 'Parallel transport', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Parallel_transport",
    prerequisites=["christoffel_symbol"],
))

# ---------------------------------------------------------------------------
# Measure Theory Ext (tiers 5-7)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="outer_measure",
    content="An outer measure mu* on a set X is a function from subsets to [0, inf] satisfying: mu*(empty)=0, monotonicity (A subset B implies mu*(A)<=mu*(B)), and countable subadditivity (mu*(union A_i) <= sum mu*(A_i)). Lebesgue outer measure on R: mu*(A) = inf{sum |b_i-a_i| : A subset union (a_i,b_i)}.",
    example="mu*({0}) = inf of lengths of intervals covering {0} = 0. mu*([0,1]) = 1. mu*(Q intersect [0,1]) = 0 (rationals have measure zero).",
    tier=6, domain="measure_ext",
    source="Wikipedia contributors, 'Outer measure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Outer_measure",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="theorem",
    name="product_measure",
    content="The product measure mu x nu on X x Y is defined by (mu x nu)(A x B) = mu(A)*nu(B) for measurable rectangles. Fubini's theorem: if f is integrable with respect to the product measure, then the double integral equals the iterated integral in either order.",
    example="Lebesgue measure on R^2: m2([0,1]x[0,2]) = 1*2 = 2. integral_{[0,1]x[0,1]} (x+y) dA = integral_0^1 integral_0^1 (x+y) dy dx = 1.",
    tier=6, domain="measure_ext",
    source="Wikipedia contributors, 'Product measure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Product_measure",
    prerequisites=["fubini_compute"],
))

register_atom(Atom(
    atom_type="theorem",
    name="radon_nikodym",
    content="The Radon-Nikodym theorem: if nu is absolutely continuous with respect to mu (nu << mu), then there exists a measurable function f (the density/derivative dnu/dmu) such that nu(A) = integral_A f dmu for all measurable A. f is unique mu-a.e.",
    example="mu = Lebesgue measure, nu(A) = integral_A 2x dx on [0,1]. Then dnu/dmu = 2x. nu([0, 0.5]) = integral_0^{0.5} 2x dx = 0.25.",
    tier=7, domain="measure_ext",
    source="Wikipedia contributors, 'Radon-Nikodym theorem', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radon%E2%80%93Nikodym_theorem",
    prerequisites=["integral"],
))

register_atom(Atom(
    atom_type="definition",
    name="convergence_modes",
    content="Modes of convergence for sequences of functions: pointwise (f_n(x)->f(x) for each x), uniform (sup|f_n-f|->0), a.e. (pointwise except on measure-zero set), in measure (mu({|f_n-f|>epsilon})->0), in L^p (integral|f_n-f|^p->0). Implications: uniform => pointwise => a.e.; L^p => in measure.",
    example="f_n = x^n on [0,1]. Pointwise limit: f(x)=0 for x<1, f(1)=1. Convergence is a.e. and in L^p (p<inf) but NOT uniform (sup = 1 at x=1).",
    tier=6, domain="measure_ext",
    source="Wikipedia contributors, 'Modes of convergence', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Modes_of_convergence_(annotated_index)",
    prerequisites=["sequence_convergence"],
))

register_atom(Atom(
    atom_type="definition",
    name="probability_measure",
    content="A probability measure P on (Omega, F) is a measure with P(Omega)=1. Must satisfy: P(empty)=0, P(A)>=0, countable additivity. A random variable X is a measurable function from (Omega, F) to (R, B(R)). The distribution of X is the pushforward measure P_X(B) = P(X^{-1}(B)).",
    example="Fair die: Omega={1,...,6}, P({k})=1/6. X='is even': P(X=1)=P({2,4,6})=1/2.",
    tier=5, domain="measure_ext",
    source="Wikipedia contributors, 'Probability measure', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Probability_measure",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="definition",
    name="conditional_expectation_measure",
    content="The conditional expectation E[X|G] is a G-measurable random variable satisfying integral_A E[X|G] dP = integral_A X dP for all A in G. It is the best L^2 approximation of X by G-measurable functions. When G = sigma(Y), it gives E[X|Y].",
    example="X uniform on [0,1], G = sigma({[0,0.5], (0.5,1]}). E[X|G] = 0.25 on [0,0.5] and 0.75 on (0.5,1].",
    tier=7, domain="measure_ext",
    source="Wikipedia contributors, 'Conditional expectation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Conditional_expectation",
    prerequisites=["probability_measure"],
))

# ---------------------------------------------------------------------------
# Photonics (tiers 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="fiber_optics_na",
    content="Numerical aperture of an optical fibre: NA = sqrt(n_core^2 - n_clad^2), where n_core and n_clad are the refractive indices. NA determines the acceptance cone half-angle: theta_max = arcsin(NA). Higher NA captures more light but increases modal dispersion.",
    example="n_core=1.48, n_clad=1.46: NA = sqrt(1.48^2 - 1.46^2) = sqrt(2.1904-2.1316) = sqrt(0.0588) = 0.2425. theta_max = 14.04 degrees.",
    tier=4, domain="photonics",
    source="Wikipedia contributors, 'Numerical aperture', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Numerical_aperture",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="laser_gain",
    content="Laser gain per unit length: g = sigma * (N2 - N1), where sigma is the stimulated emission cross-section, N2 is the upper-level population, N1 is the lower-level population. Lasing requires population inversion: N2 > N1. Gain saturates as g(I) = g0/(1+I/I_sat).",
    example="sigma=3e-20 cm^2, N2=1e18/cm^3, N1=0.2e18/cm^3: g = 3e-20 * 0.8e18 = 2.4e-2 /cm = 0.024 /cm.",
    tier=5, domain="photonics",
    source="Wikipedia contributors, 'Laser gain medium', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Gain_(laser)",
    prerequisites=["multiplication"],
))

register_atom(Atom(
    atom_type="formula",
    name="photon_energy",
    content="The energy of a photon is E = h*f = h*c/lambda, where h = 6.626e-34 J*s is Planck's constant, f is frequency, c = 3e8 m/s, lambda is wavelength. In electron volts: E(eV) = 1240/lambda(nm).",
    example="Green light lambda=520 nm: E = 1240/520 = 2.385 eV = 3.82e-19 J.",
    tier=4, domain="photonics",
    source="Wikipedia contributors, 'Photon energy', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Photon_energy",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="law",
    name="total_internal_reflection",
    content="Total internal reflection occurs when light travels from a denser medium (n1) to a less dense medium (n2) at an angle exceeding the critical angle: theta_c = arcsin(n2/n1). Above this angle, all light is reflected with no transmission. Basis for optical fibres.",
    example="Glass (n1=1.5) to air (n2=1.0): theta_c = arcsin(1/1.5) = arcsin(0.667) = 41.8 degrees.",
    tier=4, domain="photonics",
    source="Wikipedia contributors, 'Total internal reflection', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Total_internal_reflection",
    prerequisites=["snells_law"],
))

register_atom(Atom(
    atom_type="formula",
    name="laser_threshold",
    content="The laser threshold condition requires round-trip gain to equal round-trip loss: 2*g*L = -ln(R1*R2) + 2*alpha*L, where g is gain, L is cavity length, R1,R2 are mirror reflectivities, alpha is internal loss. Threshold gain: g_th = alpha + ln(1/(R1*R2))/(2*L).",
    example="L=10 cm, R1=1.0, R2=0.95, alpha=0.01/cm: g_th = 0.01 + ln(1/0.95)/0.2 = 0.01 + 0.256 = 0.266 /cm.",
    tier=5, domain="photonics",
    source="Wikipedia contributors, 'Laser threshold', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Laser#Threshold_condition",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="definition",
    name="photonic_bandgap",
    content="A photonic bandgap is a range of frequencies where electromagnetic wave propagation is forbidden in a periodic dielectric structure (photonic crystal). Analogous to electronic band gaps in semiconductors. Created by Bragg reflection from periodic refractive index variations. Gap width depends on index contrast.",
    example="1D photonic crystal with n1=1.5, n2=3.5, period a=300nm. Centre frequency: f = c/(2*n_avg*a). Bandgap width proportional to Delta_n/n_avg.",
    tier=5, domain="photonics",
    source="Wikipedia contributors, 'Photonic crystal', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Photonic_crystal",
    prerequisites=["bragg_diffraction"],
))

# ---------------------------------------------------------------------------
# Semiconductor Physics (tiers 4-5)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="pn_junction",
    content="The p-n junction has a built-in potential V_bi = (k_B*T/q)*ln(N_A*N_D/n_i^2), where N_A, N_D are acceptor/donor concentrations, n_i is intrinsic carrier concentration. The depletion width W = sqrt(2*epsilon*(V_bi-V)*(1/N_A+1/N_D)/q).",
    example="Si at 300K: N_A=1e17, N_D=1e16, n_i=1.5e10. V_bi = 0.0259*ln(1e17*1e16/2.25e20) = 0.0259*ln(4.44e12) = 0.0259*29.12 = 0.754 V.",
    tier=5, domain="semiconductor",
    source="Wikipedia contributors, 'p-n junction', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/P%E2%80%93n_junction",
    prerequisites=["logarithm"],
))

register_atom(Atom(
    atom_type="formula",
    name="mosfet_threshold",
    content="The MOSFET threshold voltage V_th = V_FB + 2*phi_F + sqrt(2*epsilon_s*q*N_A*2*phi_F)/C_ox, where V_FB is flat-band voltage, phi_F = (kT/q)*ln(N_A/n_i) is Fermi potential, C_ox = epsilon_ox/t_ox is oxide capacitance.",
    example="N_A=1e17, t_ox=5nm: phi_F=0.0259*ln(1e17/1.5e10)=0.407V. Q_dep=sqrt(2*11.7*8.85e-12*1.6e-19*1e23*0.814)=3.68e-8 C/m^2. V_th = -0.9+0.814+3.68e-8/6.9e-3 = 0.45V approx.",
    tier=5, domain="semiconductor",
    source="Wikipedia contributors, 'Threshold voltage', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Threshold_voltage",
    prerequisites=["pn_junction"],
))

register_atom(Atom(
    atom_type="formula",
    name="diode_iv",
    content="The Shockley diode equation: I = I_s*(exp(V/(n*V_T))-1), where I_s is reverse saturation current, n is ideality factor (1-2), V_T = kT/q = 25.85 mV at 300K. Forward bias: exponential growth. Reverse bias: I = -I_s (constant).",
    example="I_s=1e-12 A, n=1, V=0.6V: I = 1e-12*(exp(0.6/0.02585)-1) = 1e-12*(exp(23.2)-1) = 1e-12*1.2e10 = 0.012 A = 12 mA.",
    tier=4, domain="semiconductor",
    source="Wikipedia contributors, 'Shockley diode equation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Shockley_diode_equation",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="led_wavelength",
    content="An LED emits photons with energy approximately equal to the bandgap: E_g = h*c/lambda, so lambda = h*c/E_g = 1240/E_g(eV) nm. GaAs (E_g=1.42 eV) emits at 873 nm (IR). GaN (E_g=3.4 eV) emits at 365 nm (UV/blue).",
    example="InGaP with E_g=1.9 eV: lambda = 1240/1.9 = 653 nm (red light).",
    tier=4, domain="semiconductor",
    source="Wikipedia contributors, 'Light-emitting diode', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Light-emitting_diode",
    prerequisites=["photon_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="carrier_concentration",
    content="In an intrinsic semiconductor: n_i = sqrt(N_c*N_v)*exp(-E_g/(2*k_B*T)), where N_c, N_v are effective density of states. For n-type doping with N_D >> n_i: n = N_D, p = n_i^2/N_D. For p-type: p = N_A, n = n_i^2/N_A.",
    example="Si at 300K: n_i=1.5e10/cm^3. N_D=1e16: n=1e16, p = (1.5e10)^2/1e16 = 2.25e20/1e16 = 2.25e4/cm^3.",
    tier=5, domain="semiconductor",
    source="Wikipedia contributors, 'Charge carrier density', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Charge_carrier_density",
    prerequisites=["exponentiation"],
))

register_atom(Atom(
    atom_type="formula",
    name="depletion_width",
    content="The depletion width of a p-n junction: W = sqrt(2*epsilon_s*(V_bi-V)*(N_A+N_D)/(q*N_A*N_D)), where epsilon_s is semiconductor permittivity, V_bi is built-in potential, V is applied voltage. W increases under reverse bias, decreases under forward.",
    example="N_A=1e17, N_D=1e16, V_bi=0.75V, V=0 (no bias), epsilon_s=11.7*8.85e-14: W = sqrt(2*1.035e-12*0.75*1.1e17/(1.6e-19*1e17*1e16)) = 0.32 um.",
    tier=5, domain="semiconductor",
    source="Wikipedia contributors, 'Depletion region', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Depletion_region",
    prerequisites=["pn_junction"],
))
