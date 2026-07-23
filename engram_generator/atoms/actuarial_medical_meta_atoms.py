"""Knowledge atoms for actuarial, medical imaging, and meta-reasoning t10 ext2."""
from engram_generator.base import Atom
from engram_generator.atoms.registry import register_atom

# ---------------------------------------------------------------------------
# Actuarial Science (tiers 5-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="formula",
    name="life_table_actuarial",
    content="A life table records l_x (survivors to age x), d_x = l_x - l_{x+1} (deaths), q_x = d_x/l_x (probability of dying between x and x+1), and e_x = integral(l_t/l_x)dt (life expectancy). Standard tables start with l_0 = 100,000.",
    example="l_60 = 80,000, l_61 = 78,400. d_60 = 1,600. q_60 = 1600/80000 = 0.02. Two-percent chance of dying at age 60.",
    tier=5, domain="actuarial",
    source="Wikipedia contributors, 'Life table', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Life_table",
    prerequisites=["division"],
))

register_atom(Atom(
    atom_type="formula",
    name="annuity_pv",
    content="The present value of an annuity-immediate of 1 per period for n periods at interest rate i is a_n = (1 - v^n) / i, where v = 1/(1+i). An annuity-due pays at the start: a_n_due = a_n * (1+i). The accumulated value is s_n = a_n * (1+i)^n.",
    example="n=10, i=0.05: v=1/1.05=0.9524. a_10 = (1-0.9524^10)/0.05 = (1-0.6139)/0.05 = 7.7217.",
    tier=5, domain="actuarial",
    source="Wikipedia contributors, 'Annuity', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Annuity_(finance_theory)",
    prerequisites=["compound_interest"],
))

register_atom(Atom(
    atom_type="formula",
    name="insurance_premium",
    content="The net single premium for a whole life insurance of 1 on (x) is A_x = sum_{k=0}^{inf} v^{k+1} * k_p_x * q_{x+k}, where v=1/(1+i), k_p_x is probability of surviving k years, q_{x+k} is mortality rate. The annual premium is P = A_x / a_x.",
    example="Simplified: A_x=0.3, a_x=12. Annual premium P = 0.3/12 = 0.025 per unit.",
    tier=5, domain="actuarial",
    source="Wikipedia contributors, 'Actuarial notation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Actuarial_notation",
    prerequisites=["annuity_pv", "life_table_actuarial"],
))

register_atom(Atom(
    atom_type="formula",
    name="loss_distribution",
    content="Loss distributions model the severity of insurance claims. Common models: exponential (thin tail), lognormal, Pareto (heavy tail). For exponential with mean mu: f(x) = (1/mu)*exp(-x/mu), E[X] = mu. Excess loss: E[X-d|X>d] = mu for exponential (memoryless).",
    example="Exponential losses, mu=1000. P(X>2000) = exp(-2) = 0.1353. E[X|X>2000] = 2000 + 1000 = 3000.",
    tier=5, domain="actuarial",
    source="Wikipedia contributors, 'Loss distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Loss_distribution",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="compound_poisson",
    content="The compound Poisson distribution models total claims S = X_1+...+X_N where N~Poisson(lambda) and X_i are iid claim sizes. E[S] = lambda*E[X], Var[S] = lambda*E[X^2]. The aggregate distribution is used for ruin theory and reinsurance pricing.",
    example="lambda=10 claims/year, E[X]=500, E[X^2]=300000. E[S]=5000. Var[S]=10*300000=3,000,000. SD[S]=1732.",
    tier=6, domain="actuarial",
    source="Wikipedia contributors, 'Compound Poisson distribution', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Compound_Poisson_distribution",
    prerequisites=["poisson_dist"],
))

register_atom(Atom(
    atom_type="formula",
    name="reserve_calculation",
    content="The prospective reserve at time t for a whole life policy is t_V = A_{x+t} - P*a_{x+t}, where A_{x+t} is the insurance value and a_{x+t} is the annuity value at the attained age. This represents the excess of future benefits over future premiums.",
    example="At time 10: A_{x+10}=0.45, a_{x+10}=10, P=0.025. 10_V = 0.45 - 0.025*10 = 0.45 - 0.25 = 0.20.",
    tier=6, domain="actuarial",
    source="Wikipedia contributors, 'Actuarial reserves', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Actuarial_reserves",
    prerequisites=["insurance_premium"],
))

# ---------------------------------------------------------------------------
# Medical Imaging (tiers 4-6)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="algorithm",
    name="ct_backprojection",
    content="CT reconstruction from projections uses filtered backprojection. Each projection (line integral of attenuation) is filtered with a ramp filter in frequency domain, then smeared back across the image at the projection angle. Summation over all angles reconstructs the image.",
    example="180 projections at 1-degree intervals. Each projection filtered then backprojected. Pixel value at (x,y) = sum over angles of filtered projection value at offset x*cos(theta)+y*sin(theta).",
    tier=6, domain="medical_imaging",
    source="Wikipedia contributors, 'Radon transform', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Radon_transform",
    prerequisites=["fourier_transform_pde"],
))

register_atom(Atom(
    atom_type="formula",
    name="mri_signal",
    content="MRI signal intensity depends on tissue relaxation times T1 (spin-lattice) and T2 (spin-spin). For spin-echo: S = rho * (1-exp(-TR/T1)) * exp(-TE/T2), where rho is proton density, TR is repetition time, TE is echo time.",
    example="Brain grey matter: T1=900ms, T2=100ms, rho=0.8. TR=2000ms, TE=80ms: S = 0.8*(1-exp(-2000/900))*exp(-80/100) = 0.8*0.891*0.449 = 0.320.",
    tier=5, domain="medical_imaging",
    source="Wikipedia contributors, 'Physics of magnetic resonance imaging', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Physics_of_magnetic_resonance_imaging",
    prerequisites=["exponential_dist"],
))

register_atom(Atom(
    atom_type="algorithm",
    name="image_convolution",
    content="Image convolution applies a kernel K to an image I: (I*K)(x,y) = sum_{i,j} I(x+i,y+j)*K(i,j). Common kernels: blur (all 1s, normalised), Sobel (edge detection), Gaussian (weighted blur). Output pixel is the weighted sum of the neighbourhood.",
    example="3x3 blur kernel [[1,1,1],[1,1,1],[1,1,1]]/9 on pixel with neighbourhood values [[1,2,3],[4,5,6],[7,8,9]]: output = (1+2+3+4+5+6+7+8+9)/9 = 5.0.",
    tier=4, domain="medical_imaging",
    source="Wikipedia contributors, 'Kernel (image processing)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Kernel_(image_processing)",
    prerequisites=["matrix_multiply"],
))

register_atom(Atom(
    atom_type="definition",
    name="fourier_kspace",
    content="In MRI, k-space is the Fourier transform of the image. Each point in k-space corresponds to a spatial frequency. The centre encodes contrast (low frequencies), edges encode detail (high frequencies). The image is obtained by inverse 2D FFT of the k-space data.",
    example="k-space centre (0,0) = sum of all image pixels = total signal. Point (1,0) encodes the horizontal frequency-1 component.",
    tier=5, domain="medical_imaging",
    source="Wikipedia contributors, 'K-space (magnetic resonance imaging)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/K-space_(magnetic_resonance_imaging)",
    prerequisites=["fourier_transform_pde"],
))

register_atom(Atom(
    atom_type="formula",
    name="snr_calculation",
    content="Signal-to-noise ratio in imaging: SNR = S/sigma_noise. In MRI: SNR proportional to voxel_volume * sqrt(N_averages) * sqrt(bandwidth^{-1}). Higher SNR means clearer images. Trade-off: smaller voxels give better resolution but lower SNR.",
    example="Signal S=100, noise sigma=20: SNR=100/20=5. With 4 averages: SNR improves by sqrt(4)=2x to 10.",
    tier=4, domain="medical_imaging",
    source="Wikipedia contributors, 'Signal-to-noise ratio', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Signal-to-noise_ratio_(imaging)",
    prerequisites=["division", "square_root"],
))

register_atom(Atom(
    atom_type="definition",
    name="hounsfield_unit",
    content="The Hounsfield unit (HU) is a quantitative scale for CT attenuation: HU = 1000 * (mu - mu_water) / (mu_water - mu_air), where mu is the linear attenuation coefficient. Water = 0 HU, air = -1000 HU, bone = +1000 HU, soft tissue = 20-80 HU.",
    example="Tissue with mu=0.022/mm, mu_water=0.019/mm, mu_air=0.0002/mm: HU = 1000*(0.022-0.019)/(0.019-0.0002) = 1000*0.003/0.0188 = 159.6 HU.",
    tier=4, domain="medical_imaging",
    source="Wikipedia contributors, 'Hounsfield scale', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Hounsfield_scale",
    prerequisites=["division"],
))

# ---------------------------------------------------------------------------
# Meta-reasoning T10 Ext2 (tier 10)
# ---------------------------------------------------------------------------

register_atom(Atom(
    atom_type="definition",
    name="self_improvement_propose",
    content="Self-improvement in ML involves a model proposing modifications to its own architecture, training procedure, or objective function. This includes neural architecture search (NAS), learned optimisers, and meta-learning. The model evaluates candidate improvements via holdout performance.",
    example="Model proposes adding a residual connection between layers 2 and 5. Evaluate: train modified architecture for 1000 steps, compare validation loss. If improved by >2%, adopt.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Neural architecture search', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Neural_architecture_search",
    prerequisites=["architecture_analysis"],
))

register_atom(Atom(
    atom_type="definition",
    name="compute_budget_allocate",
    content="Compute budget allocation distributes a fixed training FLOP budget across model size, data size, and training steps. Chinchilla scaling laws suggest tokens = 20 * parameters for compute-optimal training. Given budget C, optimal N = sqrt(C/6D) approximately.",
    example="Budget: 1e21 FLOPs. Chinchilla-optimal: ~10B params, ~200B tokens (20:1 ratio). Training for ~3000 steps at batch 4M tokens.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Neural scaling law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Neural_scaling_law",
    prerequisites=["scaling_prediction"],
))

register_atom(Atom(
    atom_type="definition",
    name="evaluation_metric_design",
    content="Evaluation metric design selects or creates metrics that faithfully measure model capability. Considerations: does the metric correlate with downstream performance? Is it gameable? Does it capture both precision and recall? Examples: exact match, BLEU, F1, perplexity, human preference.",
    example="For a QA system: exact match is strict (ignores paraphrases), F1 is lenient (partial credit). Choose F1 for open-ended, exact match for factoid.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Evaluation measures (information retrieval)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Evaluation_measures_(information_retrieval)",
    prerequisites=["loss_design"],
))

register_atom(Atom(
    atom_type="definition",
    name="data_augmentation_strategy",
    content="Data augmentation creates synthetic training examples by applying transformations that preserve labels. For images: rotation, flipping, colour jittering, mixup. For text: back-translation, synonym replacement, random insertion/deletion. For tabular: SMOTE, noise injection.",
    example="Image classification: apply random horizontal flip (p=0.5), random crop (224x224 from 256x256), colour jitter (brightness +/-0.2). Increases effective dataset size 5-10x.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Data augmentation', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Data_augmentation",
    prerequisites=["training_diagnosis"],
))

register_atom(Atom(
    atom_type="definition",
    name="objective_function_critique",
    content="Objective function critique evaluates whether a loss function aligns with the true goal. Goodhart's law: when a measure becomes a target, it ceases to be a good measure. Common issues: reward hacking, specification gaming, proxy objectives that diverge from true performance.",
    example="Cross-entropy loss for language modelling: penalises all wrong tokens equally, but 'cat' and 'dog' are closer than 'cat' and '17'. A distribution-matching loss might better capture semantic similarity.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Goodhart's law', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Goodhart%27s_law",
    prerequisites=["loss_design"],
))

register_atom(Atom(
    atom_type="definition",
    name="architecture_ablation_design",
    content="Ablation studies systematically remove or modify components to measure their contribution. Design principles: change one thing at a time, use the same random seed, report confidence intervals, include both additive (add component) and subtractive (remove component) experiments.",
    example="Transformer ablation: remove layer norm (accuracy drops 15%), remove residual connections (drops 40%), remove positional encoding (drops 8%). Residual connections are most critical.",
    tier=10, domain="meta_reasoning",
    source="Wikipedia contributors, 'Ablation (artificial intelligence)', Wikipedia.",
    source_url="https://en.wikipedia.org/wiki/Ablation_(artificial_intelligence)",
    prerequisites=["architecture_analysis"],
))
