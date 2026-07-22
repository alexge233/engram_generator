"""Knowledge atoms for networks deep, economics deep, and spectroscopy deep."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ── Networks Deep ──────────────────────────────────────────────────

register_atom(Atom(
    atom_type="algorithm",
    name="tcp_handshake",
    content=(
        "The TCP three-way handshake establishes a reliable connection "
        "between client and server. Step 1: client sends SYN with initial "
        "sequence number (ISN). Step 2: server responds with SYN-ACK, "
        "acknowledging client ISN+1 and sending its own ISN. Step 3: "
        "client sends ACK acknowledging server ISN+1. After completion, "
        "both sides have agreed on sequence numbers for reliable delivery."
    ),
    example=(
        "Client ISN=100: sends SYN(seq=100). Server ISN=300: sends "
        "SYN-ACK(seq=300, ack=101). Client sends ACK(seq=101, ack=301). "
        "Connection established."
    ),
    tier=4, domain="networking",
    source="Wikipedia contributors, 'Transmission Control Protocol', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Transmission_Control_Protocol",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="congestion_avoidance",
    content=(
        "TCP congestion avoidance uses the AIMD (Additive Increase / "
        "Multiplicative Decrease) algorithm. During congestion avoidance, "
        "the congestion window (cwnd) increases by 1 MSS per RTT (additive "
        "increase). On packet loss (triple duplicate ACK or timeout), cwnd "
        "is halved (multiplicative decrease). ssthresh is set to cwnd/2."
    ),
    example=(
        "cwnd=16 MSS, loss detected: ssthresh = 16/2 = 8 MSS, "
        "cwnd = 8 MSS. Then cwnd grows: 9, 10, 11... per RTT."
    ),
    tier=5, domain="networking",
    source="Wikipedia contributors, 'TCP congestion control', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/TCP_congestion_control",
    prerequisites=["tcp_handshake"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="bgp_routing",
    content=(
        "Border Gateway Protocol (BGP) is the inter-domain routing protocol "
        "of the Internet. BGP uses path-vector routing: each route "
        "advertisement carries the full AS path. Route selection uses "
        "attributes in order: highest LOCAL_PREF, shortest AS_PATH, "
        "lowest ORIGIN type, lowest MED, prefer eBGP over iBGP, "
        "lowest IGP cost to next hop, lowest router ID."
    ),
    example=(
        "Route A: AS_PATH=[AS1,AS2] (length 2), LOCAL_PREF=100. "
        "Route B: AS_PATH=[AS3] (length 1), LOCAL_PREF=100. "
        "Same LOCAL_PREF, B has shorter AS_PATH, select B."
    ),
    tier=5, domain="networking",
    source="Wikipedia contributors, 'Border Gateway Protocol', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Border_Gateway_Protocol",
    prerequisites=["shortest_path"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="nat_translation",
    content=(
        "Network Address Translation (NAT) maps private IP addresses to "
        "public addresses. In NAPT (port-based NAT), the router maintains "
        "a translation table mapping (private_ip, private_port) to "
        "(public_ip, public_port). Outbound packets get source rewritten; "
        "inbound packets get destination rewritten using the table."
    ),
    example=(
        "Host 192.168.1.5:4000 sends to 8.8.8.8:80. NAT router (public "
        "203.0.113.1) rewrites source to 203.0.113.1:50001. Table entry: "
        "(192.168.1.5:4000) <-> (203.0.113.1:50001)."
    ),
    tier=4, domain="networking",
    source="Wikipedia contributors, 'Network address translation', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Network_address_translation",
    prerequisites=["binary_arithmetic"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="dhcp_process",
    content=(
        "Dynamic Host Configuration Protocol (DHCP) assigns IP addresses "
        "via a four-step process: DISCOVER (client broadcasts request), "
        "OFFER (server offers an address), REQUEST (client accepts offer), "
        "ACK (server confirms assignment). The lease has a duration after "
        "which the client must renew."
    ),
    example=(
        "Client broadcasts DISCOVER. Server offers 192.168.1.100 with "
        "lease=3600s. Client sends REQUEST for 192.168.1.100. Server "
        "sends ACK. Client uses 192.168.1.100 for 1 hour."
    ),
    tier=4, domain="networking",
    source="Wikipedia contributors, 'Dynamic Host Configuration Protocol', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Dynamic_Host_Configuration_Protocol",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="wifi_throughput",
    content=(
        "Wi-Fi throughput depends on channel bandwidth, modulation, coding "
        "rate, spatial streams, and overhead. Theoretical max throughput: "
        "T = B * log2(1 + SNR) * N_streams * (1 - overhead). In practice, "
        "802.11ac with 80 MHz channel, 256-QAM (8 bits/symbol), 5/6 "
        "coding rate, and 2 spatial streams gives ~867 Mbps PHY rate."
    ),
    example=(
        "802.11n: 40 MHz channel, 64-QAM, 5/6 coding, 2 streams: "
        "PHY rate = 300 Mbps. Typical throughput ~150 Mbps (50% overhead)."
    ),
    tier=5, domain="networking",
    source="Wikipedia contributors, 'Wi-Fi', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Wi-Fi",
    prerequisites=["information_theory"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="load_balancing",
    content=(
        "Load balancing distributes network traffic across multiple "
        "servers. Common algorithms: Round Robin (cyclic assignment), "
        "Weighted Round Robin (proportional to server capacity), "
        "Least Connections (assign to server with fewest active "
        "connections), IP Hash (consistent mapping by client IP)."
    ),
    example=(
        "3 servers, weights [3, 2, 1]. Weighted Round Robin: first 3 "
        "requests to S1, next 2 to S2, next 1 to S3, then repeat. "
        "6 requests per cycle."
    ),
    tier=4, domain="networking",
    source="Wikipedia contributors, 'Load balancing (computing)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Load_balancing_(computing)",
    prerequisites=[],
))

register_atom(Atom(
    atom_type="formula",
    name="packet_loss_retransmit",
    content=(
        "With packet loss probability p, the expected number of "
        "transmissions to successfully deliver one packet is 1/(1-p) "
        "(geometric distribution). For n independent packets, expected "
        "total transmissions = n/(1-p). Effective throughput = "
        "nominal_rate * (1-p)."
    ),
    example=(
        "Loss rate p=0.05, nominal rate 100 Mbps: effective throughput = "
        "100 * (1-0.05) = 95 Mbps. Expected transmissions per packet = "
        "1/0.95 = 1.053."
    ),
    tier=5, domain="networking",
    source="Wikipedia contributors, 'Packet loss', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Packet_loss",
    prerequisites=["geometric_dist"],
))

# ── Economics Deep ─────────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="is_lm_model",
    content=(
        "The IS-LM model describes the interaction between the goods "
        "market (IS curve) and the money market (LM curve). "
        "IS: Y = C(Y-T) + I(r) + G. LM: M/P = L(r, Y). Equilibrium "
        "is at the intersection where both markets clear simultaneously, "
        "determining output Y* and interest rate r*."
    ),
    example=(
        "IS: Y = 200 + 0.5(Y-100) + 300 - 50r + 100. Solve: "
        "Y = 550 + 0.5Y - 50 - 50r, 0.5Y = 500 - 50r, Y = 1000 - 100r. "
        "LM: 500 = 0.5Y - 100r. Substitute: r=2.5, Y=750."
    ),
    tier=5, domain="economics",
    source="Wikipedia contributors, 'IS-LM model', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/IS%E2%80%93LM_model",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="solow_growth",
    content=(
        "The Solow growth model describes long-run economic growth. "
        "Capital accumulation: dk/dt = s*f(k) - (n+delta)*k, where k is "
        "capital per worker, s is savings rate, f(k) is production "
        "function, n is population growth, delta is depreciation. "
        "Steady state: s*f(k*) = (n+delta)*k*."
    ),
    example=(
        "f(k) = k^0.5, s=0.3, n=0.02, delta=0.05. Steady state: "
        "0.3*k*^0.5 = 0.07*k*, k*^0.5 = 0.3/0.07 = 4.286, "
        "k* = 18.37. y* = 4.286."
    ),
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Solow-Swan model', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Solow%E2%80%93Swan_model",
    prerequisites=["derivative"],
))

register_atom(Atom(
    atom_type="formula",
    name="phillips_curve",
    content=(
        "The Phillips curve describes the inverse relationship between "
        "unemployment and inflation. Original: pi = -a*(u - u_n), where "
        "pi is inflation rate, u is unemployment, u_n is natural rate, "
        "a is sensitivity parameter. Expectations-augmented: "
        "pi = pi_e - a*(u - u_n)."
    ),
    example=(
        "u_n=5%, a=0.5, pi_e=2%: at u=3%, pi = 2 - 0.5*(3-5) = "
        "2 + 1 = 3%. At u=7%, pi = 2 - 0.5*(7-5) = 2 - 1 = 1%."
    ),
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Phillips curve', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Phillips_curve",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="formula",
    name="option_greeks",
    content=(
        "Option Greeks measure sensitivity of option price to parameters. "
        "Delta = dV/dS (price sensitivity to underlying). "
        "Gamma = d^2V/dS^2 (rate of change of delta). "
        "Theta = dV/dt (time decay). Vega = dV/d_sigma (volatility "
        "sensitivity). Rho = dV/dr (interest rate sensitivity). "
        "For Black-Scholes call: Delta = N(d1)."
    ),
    example=(
        "Black-Scholes call: S=100, K=100, T=1, r=0.05, sigma=0.2. "
        "d1 = (ln(1) + (0.05+0.02)*1)/(0.2*1) = 0.35. "
        "Delta = N(0.35) = 0.637."
    ),
    tier=6, domain="economics",
    source="Wikipedia contributors, 'Greeks (finance)', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Greeks_(finance)",
    prerequisites=["derivative", "normal_dist_compute"],
))

register_atom(Atom(
    atom_type="formula",
    name="present_value_annuity",
    content=(
        "Present value of an ordinary annuity: PV = PMT * [1-(1+r)^(-n)]/r, "
        "where PMT is the periodic payment, r is the discount rate per "
        "period, and n is the number of periods. For an annuity due, "
        "multiply by (1+r)."
    ),
    example=(
        "PMT=1000, r=0.05, n=10: PV = 1000 * [1-(1.05)^(-10)]/0.05 = "
        "1000 * [1-0.6139]/0.05 = 1000 * 7.722 = 7722."
    ),
    tier=4, domain="economics",
    source="Wikipedia contributors, 'Annuity', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Annuity",
    prerequisites=["compound_interest"],
))

register_atom(Atom(
    atom_type="formula",
    name="oligopoly_bertrand",
    content=(
        "In Bertrand competition, firms compete on price. With identical "
        "products and constant marginal cost c, the Nash equilibrium is "
        "p1 = p2 = c (perfect competition outcome). With differentiated "
        "products: reaction functions p_i = (a + c + b*p_j) / 2, where "
        "a is demand intercept, b is cross-price sensitivity."
    ),
    example=(
        "Homogeneous Bertrand: MC=10. Equilibrium: p1=p2=10, profit=0. "
        "Differentiated: a=20, c=10, b=0.5. Reaction: p=(20+10+0.5p_j)/2. "
        "Symmetric: p=(30+0.5p)/2, 1.5p=30, p=20."
    ),
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Bertrand competition', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Bertrand_competition",
    prerequisites=["linear_equation"],
))

register_atom(Atom(
    atom_type="definition",
    name="adverse_selection",
    content=(
        "Adverse selection occurs when asymmetric information between "
        "buyers and sellers leads to market failure. The party with less "
        "information faces a disproportionate share of low-quality goods. "
        "Akerlof's 'Market for Lemons': if buyers cannot distinguish "
        "quality, they pay average price, driving high-quality sellers "
        "out. Expected value: E[V] = p_H*V_H + p_L*V_L."
    ),
    example=(
        "Used cars: 50% worth 10000 (good), 50% worth 5000 (lemon). "
        "Buyer offers E[V] = 0.5*10000 + 0.5*5000 = 7500. Good-car "
        "sellers refuse (worth 10000). Only lemons remain."
    ),
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Adverse selection', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Adverse_selection",
    prerequisites=["expected_value"],
))

register_atom(Atom(
    atom_type="definition",
    name="moral_hazard",
    content=(
        "Moral hazard occurs when a party takes more risk because another "
        "party bears the cost. In insurance: the insured party may take "
        "less care once covered. Principal-agent model: agent effort e "
        "affects outcome probability p(e), but principal cannot observe e. "
        "Optimal contract balances incentives and risk sharing."
    ),
    example=(
        "Insurance: without coverage, driver accident prob = 0.05. "
        "With full coverage, prob rises to 0.10 (less careful). "
        "Expected cost without: 0.05*10000=500. With moral hazard: "
        "0.10*10000=1000."
    ),
    tier=5, domain="economics",
    source="Wikipedia contributors, 'Moral hazard', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Moral_hazard",
    prerequisites=["expected_value"],
))

# ── Spectroscopy Deep ──────────────────────────────────────────────

register_atom(Atom(
    atom_type="formula",
    name="nmr_chemical_shift",
    content=(
        "NMR chemical shift delta (in ppm) measures the resonance "
        "frequency of a nucleus relative to a reference: "
        "delta = (nu_sample - nu_ref) / nu_ref * 10^6. Typical 1H "
        "shifts: TMS=0, alkyl=0.9-1.5, aromatic=6.5-8, aldehyde=9-10, "
        "carboxylic acid=10-12 ppm."
    ),
    example=(
        "Spectrometer at 400 MHz. Sample resonates at 400.001200 MHz, "
        "ref (TMS) at 400.000000 MHz. delta = (1200/400000000)*10^6 = "
        "3.0 ppm (likely CH2 near electronegative group)."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Chemical shift', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Chemical_shift",
    prerequisites=["wavelength_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="nmr_integration",
    content=(
        "NMR peak integration gives the relative number of protons "
        "contributing to each signal. The integral ratio equals the "
        "proton ratio. Normalise by dividing all integrals by the "
        "smallest to get integer ratios."
    ),
    example=(
        "Ethanol CH3CH2OH: three peaks with integrals 3.0, 2.0, 1.0. "
        "Ratio 3:2:1 corresponds to 3H (CH3), 2H (CH2), 1H (OH)."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Nuclear magnetic resonance spectroscopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Nuclear_magnetic_resonance_spectroscopy",
    prerequisites=["nmr_chemical_shift"],
))

register_atom(Atom(
    atom_type="formula",
    name="mass_spec_molecular_ion",
    content=(
        "In mass spectrometry, the molecular ion (M+) peak gives the "
        "molecular weight. For electron ionisation (EI), M+ is formed "
        "by removing one electron: M -> M+ + e-. The m/z of M+ equals "
        "the molecular mass. Isotope patterns (M+1, M+2) reveal "
        "elemental composition."
    ),
    example=(
        "Methanol CH3OH (MW=32): M+ at m/z=32. Loss of H gives "
        "m/z=31 (CHO+). Loss of OH gives m/z=15 (CH3+). "
        "Base peak at m/z=31."
    ),
    tier=4, domain="spectroscopy",
    source="Wikipedia contributors, 'Mass spectrometry', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mass_spectrometry",
    prerequisites=["molar_mass"],
))

register_atom(Atom(
    atom_type="formula",
    name="ir_interpretation",
    content=(
        "Infrared spectroscopy identifies functional groups by their "
        "characteristic absorption frequencies. Key absorptions: "
        "O-H stretch 3200-3600 cm-1 (broad), N-H 3300-3500 cm-1, "
        "C-H 2850-3000 cm-1, C=O 1650-1750 cm-1, C=C 1600-1680 cm-1, "
        "C-O 1000-1300 cm-1. Hooke's law: nu = (1/2pi)*sqrt(k/mu)."
    ),
    example=(
        "Spectrum shows broad absorption at 3300 cm-1 (O-H), sharp peak "
        "at 1710 cm-1 (C=O). Suggests carboxylic acid. Confirm with "
        "C-O stretch at 1200 cm-1."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Infrared spectroscopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Infrared_spectroscopy",
    prerequisites=["wavelength_energy"],
))

register_atom(Atom(
    atom_type="formula",
    name="uv_vis_absorption",
    content=(
        "UV-Vis spectroscopy measures electronic transitions. "
        "Beer-Lambert law: A = epsilon * l * c, where A is absorbance, "
        "epsilon is molar absorptivity (L/mol/cm), l is path length (cm), "
        "c is concentration (mol/L). Transmittance T = I/I0 = 10^(-A)."
    ),
    example=(
        "Compound with epsilon=15000 L/mol/cm at 260 nm. c=2e-5 M, "
        "l=1 cm: A = 15000*1*2e-5 = 0.30. T = 10^(-0.30) = 0.50 (50%)."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Ultraviolet-visible spectroscopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Ultraviolet%E2%80%93visible_spectroscopy",
    prerequisites=["beer_lambert"],
))

register_atom(Atom(
    atom_type="formula",
    name="coupling_constant",
    content=(
        "In NMR, spin-spin coupling splits peaks into multiplets. "
        "The coupling constant J (in Hz) measures the splitting. "
        "n+1 rule: a proton with n equivalent neighbours gives n+1 peaks. "
        "Typical J values: vicinal 3J = 6-8 Hz, geminal 2J = 12-15 Hz, "
        "trans-alkene = 12-18 Hz, cis-alkene = 6-12 Hz."
    ),
    example=(
        "CH3-CH2- group: CH3 has 2 neighbours (CH2), splits into "
        "triplet (2+1=3). CH2 has 3 neighbours (CH3), splits into "
        "quartet (3+1=4). J = 7.0 Hz for both."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'J-coupling', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/J-coupling",
    prerequisites=["nmr_chemical_shift"],
))

register_atom(Atom(
    atom_type="formula",
    name="mass_spec_isotope",
    content=(
        "Isotope patterns in mass spectrometry reveal elemental "
        "composition. Key isotope ratios: 13C natural abundance 1.1% "
        "(M+1 = n*1.1% of M+), 37Cl 32.5% of 35Cl (M+2 pattern), "
        "81Br 97.3% of 79Br (near-equal M and M+2). Sulfur: 34S "
        "gives 4.4% M+2."
    ),
    example=(
        "CH2Cl2 (MW=84): M+ at 84, M+2 at 86, M+4 at 88. "
        "Two Cl atoms: M:M+2:M+4 ratio = 9:6:1 (binomial "
        "distribution of 35Cl/37Cl)."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Mass spectrometry', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Mass_spectrometry",
    prerequisites=["mass_spec_molecular_ion"],
))

register_atom(Atom(
    atom_type="definition",
    name="raman_vs_ir",
    content=(
        "Raman and IR spectroscopy are complementary. IR-active: "
        "vibrations that change dipole moment (asymmetric stretches, "
        "bending). Raman-active: vibrations that change polarisability "
        "(symmetric stretches). Rule of mutual exclusion: for "
        "centrosymmetric molecules, no vibration is both IR and "
        "Raman active."
    ),
    example=(
        "CO2 (centrosymmetric): symmetric stretch (Raman active, "
        "IR inactive, 1388 cm-1). Asymmetric stretch (IR active, "
        "Raman inactive, 2349 cm-1). Bend (IR active, 667 cm-1)."
    ),
    tier=5, domain="spectroscopy",
    source="Wikipedia contributors, 'Raman spectroscopy', Wikipedia",
    source_url="https://en.wikipedia.org/wiki/Raman_spectroscopy",
    prerequisites=["ir_interpretation"],
))
