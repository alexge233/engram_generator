"""Knowledge atoms for continuum mechanics generators."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

register_atom(Atom(
    atom_type="definition",
    name="stress_tensor",
    content=(
        "The Cauchy stress tensor sigma_ij represents the internal forces "
        "per unit area at a material point. It is a symmetric 3x3 tensor "
        "where sigma_ij is the force per unit area acting on a surface "
        "with normal in the j-direction, in the i-direction. The diagonal "
        "components are normal stresses, off-diagonal are shear stresses."
    ),
    example=(
        "sigma = [[100, 20, 0], [20, 50, 0], [0, 0, -30]] MPa. "
        "Normal stresses: sigma_xx=100, sigma_yy=50, sigma_zz=-30 MPa. "
        "Shear stress: tau_xy=20 MPa."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Cauchy stress tensor', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Cauchy_stress_tensor",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="strain_tensor",
    content=(
        "The infinitesimal strain tensor epsilon_ij measures small "
        "deformations: epsilon_ij = (1/2)(du_i/dx_j + du_j/dx_i), "
        "where u is the displacement field. Diagonal components are "
        "normal strains (extension/compression), off-diagonal are "
        "shear strains (angular distortion). The tensor is symmetric."
    ),
    example=(
        "Displacement u = [0.01*x, -0.005*y, 0]. "
        "epsilon_xx = du_x/dx = 0.01, epsilon_yy = du_y/dy = -0.005, "
        "epsilon_xy = (1/2)(du_x/dy + du_y/dx) = 0."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Infinitesimal strain theory', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Infinitesimal_strain_theory",
    prerequisites=["partial_derivative"],
))

register_atom(Atom(
    atom_type="law",
    name="hookes_law_3d",
    content=(
        "Generalised Hooke's law relates stress and strain in 3D: "
        "sigma_ij = C_ijkl * epsilon_kl (summation convention). For "
        "isotropic materials: sigma_ij = lambda * delta_ij * epsilon_kk + "
        "2*mu * epsilon_ij, where lambda and mu are Lame parameters. "
        "Equivalently: epsilon_ij = (1/E)[(1+nu)*sigma_ij - nu*delta_ij*sigma_kk], "
        "E = Young's modulus, nu = Poisson's ratio."
    ),
    example=(
        "Steel (E=200 GPa, nu=0.3): uniaxial sigma_xx=100 MPa. "
        "epsilon_xx = 100/200000 = 0.0005, "
        "epsilon_yy = -0.3*100/200000 = -0.00015."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Hooke's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hooke%27s_law",
    prerequisites=["stress_tensor", "strain_tensor"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="mohr_circle",
    content=(
        "Mohr's circle is a graphical method to find principal stresses "
        "and maximum shear stress from a 2D stress state. Centre: "
        "C = (sigma_x + sigma_y)/2. Radius: R = sqrt(((sigma_x - sigma_y)/2)^2 "
        "+ tau_xy^2). Principal stresses: sigma_1 = C + R, sigma_2 = C - R. "
        "Maximum shear: tau_max = R."
    ),
    example=(
        "sigma_x=80 MPa, sigma_y=40 MPa, tau_xy=30 MPa. "
        "C = (80+40)/2 = 60. R = sqrt(20^2 + 30^2) = sqrt(1300) = 36.06. "
        "sigma_1 = 96.06 MPa, sigma_2 = 23.94 MPa, tau_max = 36.06 MPa."
    ),
    tier=5,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Mohr's circle', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Mohr%27s_circle",
    prerequisites=["square_root"],
))

register_atom(Atom(
    atom_type="formula",
    name="von_mises",
    content=(
        "The von Mises yield criterion predicts yielding when the von Mises "
        "stress reaches the yield strength: sigma_vm = sqrt(0.5*((s1-s2)^2 + "
        "(s2-s3)^2 + (s3-s1)^2)) where s1, s2, s3 are principal stresses. "
        "For 2D: sigma_vm = sqrt(sigma_x^2 - sigma_x*sigma_y + sigma_y^2 + "
        "3*tau_xy^2). Yields when sigma_vm >= sigma_y."
    ),
    example=(
        "sigma_x=100, sigma_y=50, tau_xy=30 MPa, sigma_y_yield=250 MPa. "
        "sigma_vm = sqrt(100^2 - 100*50 + 50^2 + 3*30^2) "
        "= sqrt(10000-5000+2500+2700) = sqrt(10200) = 101.0 MPa. Safe."
    ),
    tier=6,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Von Mises yield criterion', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Von_Mises_yield_criterion",
    prerequisites=["stress_tensor"],
))

register_atom(Atom(
    atom_type="definition",
    name="elastic_moduli",
    content=(
        "Elastic moduli characterise material stiffness. Young's modulus "
        "E = stress/strain (uniaxial). Shear modulus G = tau/gamma. "
        "Bulk modulus K = -V*dP/dV. Poisson's ratio nu = -epsilon_transverse/"
        "epsilon_axial. Relations: G = E/(2*(1+nu)), K = E/(3*(1-2*nu)), "
        "E = 9*K*G/(3*K+G)."
    ),
    example=(
        "Steel: E=200 GPa, nu=0.3. "
        "G = 200/(2*1.3) = 76.9 GPa. "
        "K = 200/(3*0.4) = 166.7 GPa."
    ),
    tier=5,
    domain="continuum_mechanics",
    source="Wikipedia contributors, 'Elastic modulus', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Elastic_modulus",
    prerequisites=["division"],
))
