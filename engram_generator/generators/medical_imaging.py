"""Medical imaging generators -- CT, MRI, convolution, k-space, SNR, HU.

6 generators across tiers 4-6.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _r4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


@register
class CTBackprojectionGenerator(StepGenerator):
    """Compute simple backprojection for a 3x3 image from two projections.

    For each projection angle, the measured projection value is smeared
    uniformly along the ray across the reconstruction grid. Contributions
    from all angles are summed at each pixel.

    Difficulty scaling:
        Difficulty 1-4: 2 projection angles (0 and 90 degrees).
        Difficulty 5-8: 3 projection angles (0, 90, and 45 degrees).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ct_backprojection"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute backprojection reconstruction on 3x3 grid"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CT backprojection problem.

        Args:
            difficulty: Controls number of projection angles.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        # Projections at 0 degrees (horizontal sums per row)
        proj_0 = [self._rng.randint(1, 9) for _ in range(3)]
        # Projections at 90 degrees (vertical sums per column)
        proj_90 = [self._rng.randint(1, 9) for _ in range(3)]

        # Backproject: each pixel gets sum of corresponding projections
        # At 0 deg: smear row projection uniformly -> each pixel in row gets proj/3
        # At 90 deg: smear col projection uniformly -> each pixel in col gets proj/3
        grid = [[0.0] * 3 for _ in range(3)]
        for r in range(3):
            for c in range(3):
                grid[r][c] = _r4(proj_0[r] / 3.0 + proj_90[c] / 3.0)

        if difficulty >= 5:
            proj_45 = [self._rng.randint(1, 9) for _ in range(3)]
            # Simplified 45-deg: diagonal smear, each main diag pixel gets proj/3
            for idx in range(3):
                grid[idx][idx] = _r4(grid[idx][idx] + proj_45[idx] / 3.0)
            problem = (
                f"3x3 grid, proj_0={proj_0}, proj_90={proj_90}, "
                f"proj_45={proj_45}"
            )
            return problem, {
                "proj_0": proj_0, "proj_90": proj_90,
                "proj_45": proj_45, "grid": grid, "n_angles": 3,
            }

        problem = f"3x3 grid, proj_0={proj_0}, proj_90={proj_90}"
        return problem, {
            "proj_0": proj_0, "proj_90": proj_90,
            "grid": grid, "n_angles": 2,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            "backproject 0-deg: smear each row projection / 3",
            "backproject 90-deg: add each col projection / 3",
        ]
        if sd["n_angles"] == 3:
            steps.append("backproject 45-deg: add diagonal projection / 3")
        row_strs = [str(sd["grid"][r]) for r in range(3)]
        steps.append(f"result grid: [{', '.join(row_strs)}]")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Reconstructed pixel at (1,1) as a string.
        """
        return f"pixel(1,1)={sd['grid'][1][1]}"


@register
class MRISignalGenerator(StepGenerator):
    """Compute MRI signal intensity from tissue relaxation parameters.

    S(TE) = S_0 * exp(-TE / T2) for a spin-echo sequence. Given T2,
    TE, and initial signal S_0, compute the signal intensity.

    Difficulty scaling:
        Difficulty 1-3: single tissue type.
        Difficulty 4-6: compare two tissues.
        Difficulty 7-8: include T1 weighting: S_0 = (1 - exp(-TR/T1)).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mri_signal"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["logarithm"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute MRI signal intensity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an MRI signal problem.

        Args:
            difficulty: Controls complexity of signal model.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        t2 = self._rng.randint(20, 200)
        te = self._rng.randint(5, min(t2, 80))

        if difficulty <= 6:
            s0 = _r4(self._rng.uniform(50.0, 200.0))
            signal = _r4(s0 * math.exp(-te / t2))
            problem = f"S_0={s0}, T2={t2}ms, TE={te}ms"
            return problem, {
                "s0": s0, "t2": t2, "te": te, "signal": signal,
                "has_t1": False,
            }

        # T1-weighted: S_0 = 1 - exp(-TR/T1)
        t1 = self._rng.randint(200, 2000)
        tr = self._rng.randint(200, 3000)
        s0_eff = _r4(1.0 - math.exp(-tr / t1))
        signal = _r4(s0_eff * math.exp(-te / t2))
        problem = f"T1={t1}ms, T2={t2}ms, TR={tr}ms, TE={te}ms"
        return problem, {
            "t1": t1, "t2": t2, "tr": tr, "te": te,
            "s0": s0_eff, "signal": signal, "has_t1": True,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = []
        if sd["has_t1"]:
            steps.append(
                f"S_0 = 1 - exp(-TR/T1) = 1 - exp(-{sd['tr']}/{sd['t1']})"
                f" = {sd['s0']}"
            )
        steps.append(
            f"S = S_0 * exp(-TE/T2) = {sd['s0']} * exp(-{sd['te']}/{sd['t2']})"
        )
        steps.append(f"S = {sd['signal']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Signal intensity as a string.
        """
        return str(sd["signal"])


@register
class ImageConvolutionGenerator(StepGenerator):
    """Apply a 3x3 kernel to a 5x5 image patch and compute one output pixel.

    Selects a kernel type (blur, sharpen, or edge detect) and applies it
    at a chosen position in the image, computing the weighted sum.

    Difficulty scaling:
        Difficulty 1-3: averaging (blur) kernel.
        Difficulty 4-6: sharpening kernel.
        Difficulty 7-8: edge detection kernel (Laplacian).
    """

    _KERNELS = {
        "blur": [[1, 1, 1], [1, 1, 1], [1, 1, 1]],
        "sharpen": [[0, -1, 0], [-1, 5, -1], [0, -1, 0]],
        "edge": [[0, 1, 0], [1, -4, 1], [0, 1, 0]],
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "image_convolution"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["summation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "apply 3x3 kernel to image patch and compute output pixel"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an image convolution problem.

        Args:
            difficulty: Controls kernel type.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            kernel_name = "blur"
        elif difficulty <= 6:
            kernel_name = "sharpen"
        else:
            kernel_name = "edge"

        kernel = self._KERNELS[kernel_name]

        # Generate a 5x5 image with small integer values
        image = [[self._rng.randint(0, 9) for _ in range(5)] for _ in range(5)]

        # Compute output at center position (2, 2)
        row, col = 2, 2
        result = 0
        products = []
        for kr in range(3):
            for kc in range(3):
                ir = row - 1 + kr
                ic = col - 1 + kc
                p = image[ir][ic] * kernel[kr][kc]
                products.append(p)
                result += p

        # For blur kernel, divide by 9
        if kernel_name == "blur":
            result = _r4(result / 9.0)

        patch = [image[row - 1 + r][col - 1:col + 2] for r in range(3)]
        problem = (
            f"kernel={kernel_name}, K={kernel}, "
            f"patch={patch}"
        )
        return problem, {
            "kernel_name": kernel_name, "kernel": kernel,
            "patch": patch, "products": products, "result": result,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"element-wise products: {sd['products']}",
            f"sum = {sum(sd['products'])}",
        ]
        if sd["kernel_name"] == "blur":
            steps.append(f"blur: divide by 9 = {sd['result']}")
        else:
            steps.append(f"output pixel = {sd['result']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Output pixel value as a string.
        """
        return str(sd["result"])


@register
class FourierKspaceGenerator(StepGenerator):
    """Compute one k-space point from a 2x2 image using the DFT.

    F(kx,ky) = sum_{x,y} f(x,y) * exp(-2*pi*i*(kx*x/N + ky*y/N)).
    Given a 2x2 image, compute the real and imaginary parts of one
    k-space sample.

    Difficulty scaling:
        Difficulty 1-4: k=(0,0) -- DC component (just sum).
        Difficulty 5-8: k=(1,0) or k=(0,1) -- requires trig evaluation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "fourier_kspace"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute k-space point from 2x2 image via DFT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Fourier k-space problem.

        Args:
            difficulty: Controls which k-space point.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n = 2
        image = [[self._rng.randint(1, 9) for _ in range(n)] for _ in range(n)]

        if difficulty <= 4:
            kx, ky = 0, 0
        else:
            kx, ky = self._rng.choice([(1, 0), (0, 1)])

        real_part = 0.0
        imag_part = 0.0
        terms = []
        for x in range(n):
            for y in range(n):
                angle = -2.0 * math.pi * (kx * x / n + ky * y / n)
                cos_val = _r4(math.cos(angle))
                sin_val = _r4(math.sin(angle))
                real_part += image[x][y] * cos_val
                imag_part += image[x][y] * sin_val
                terms.append(
                    f"f({x},{y})={image[x][y]}: "
                    f"cos={cos_val}, sin={sin_val}"
                )

        real_part = _r4(real_part)
        imag_part = _r4(imag_part)

        img_str = f"[{image[0]}, {image[1]}]"
        problem = f"image={img_str}, k=({kx},{ky})"
        return problem, {
            "image": image, "kx": kx, "ky": ky,
            "terms": terms, "real": real_part, "imag": imag_part,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"F(kx,ky) = sum f(x,y)*exp(-2pi*i*(kx*x+ky*y)/N)"]
        steps.extend(sd["terms"])
        steps.append(f"F({sd['kx']},{sd['ky']}) = {sd['real']} + {sd['imag']}i")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Complex k-space value as a string.
        """
        return f"{sd['real']}+{sd['imag']}i"


@register
class SNRCalculationGenerator(StepGenerator):
    """Compute signal-to-noise ratio from signal and noise measurements.

    SNR = mean(signal) / std(noise). Given a set of signal measurements
    and noise measurements, compute both statistics and the ratio.

    Difficulty scaling:
        Difficulty 1-3: 3 measurements each.
        Difficulty 4-6: 4-5 measurements each.
        Difficulty 7-8: 6 measurements with outlier noise.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "snr_calculation"

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
            Task description string.
        """
        return "compute SNR from signal and noise measurements"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an SNR problem.

        Args:
            difficulty: Controls number of measurements.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            n = 3
        elif difficulty <= 6:
            n = self._rng.randint(4, 5)
        else:
            n = 6

        signal = [_r4(self._rng.uniform(50.0, 200.0)) for _ in range(n)]
        noise = [_r4(self._rng.uniform(-5.0, 5.0)) for _ in range(n)]

        sig_mean = _r4(sum(signal) / n)
        noise_mean = _r4(sum(noise) / n)
        noise_var = _r4(sum((x - noise_mean) ** 2 for x in noise) / n)
        noise_std = _r4(math.sqrt(noise_var)) if noise_var > 0 else 0.0001

        snr = _r4(sig_mean / noise_std) if noise_std != 0 else 0.0

        problem = f"signal={signal}, noise={noise}"
        return problem, {
            "signal": signal, "noise": noise,
            "sig_mean": sig_mean, "noise_mean": noise_mean,
            "noise_std": noise_std, "snr": snr, "n": n,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"mean(signal) = {sd['sig_mean']}",
            f"std(noise) = {sd['noise_std']}",
            f"SNR = {sd['sig_mean']} / {sd['noise_std']} = {sd['snr']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            SNR value as a string.
        """
        return str(sd["snr"])


@register
class HounsfieldUnitGenerator(StepGenerator):
    """Convert linear attenuation coefficient to Hounsfield Units.

    HU = 1000 * (mu - mu_water) / (mu_water - mu_air). Standard
    reference values: mu_water ~ 0.206 cm^-1, mu_air ~ 0.0004 cm^-1.

    Difficulty scaling:
        Difficulty 1-3: single tissue conversion.
        Difficulty 4-6: compare two tissues.
        Difficulty 7-8: identify tissue type from HU range.
    """

    _TISSUE_HU_RANGES = {
        "bone": (300, 2000),
        "muscle": (35, 55),
        "fat": (-120, -60),
        "lung": (-900, -500),
        "liver": (40, 70),
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "hounsfield_unit"

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
            Task description string.
        """
        return "convert attenuation coefficient to Hounsfield Units"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Hounsfield unit problem.

        Args:
            difficulty: Controls problem complexity.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mu_water = 0.206
        mu_air = 0.0004

        mu = _r4(self._rng.uniform(0.01, 0.5))
        hu = _r4(1000.0 * (mu - mu_water) / (mu_water - mu_air))

        # Classify tissue
        tissue = "unknown"
        for name, (lo, hi) in self._TISSUE_HU_RANGES.items():
            if lo <= hu <= hi:
                tissue = name
                break

        if difficulty <= 3:
            problem = f"mu={mu} cm^-1, mu_water={mu_water}, mu_air={mu_air}"
            return problem, {
                "mu": mu, "mu_water": mu_water, "mu_air": mu_air,
                "hu": hu, "tissue": tissue, "compare": False,
            }

        # Compare two tissues
        mu2 = _r4(self._rng.uniform(0.01, 0.5))
        hu2 = _r4(1000.0 * (mu2 - mu_water) / (mu_water - mu_air))
        tissue2 = "unknown"
        for name, (lo, hi) in self._TISSUE_HU_RANGES.items():
            if lo <= hu2 <= hi:
                tissue2 = name
                break

        problem = (
            f"mu_1={mu}, mu_2={mu2}, mu_water={mu_water}, mu_air={mu_air}"
        )
        return problem, {
            "mu": mu, "mu2": mu2, "mu_water": mu_water, "mu_air": mu_air,
            "hu": hu, "hu2": hu2, "tissue": tissue, "tissue2": tissue2,
            "compare": True,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        denom = _r4(sd["mu_water"] - sd["mu_air"])
        steps = [
            "HU = 1000 * (mu - mu_water) / (mu_water - mu_air)",
            f"denom = {sd['mu_water']} - {sd['mu_air']} = {denom}",
            f"HU_1 = 1000 * ({sd['mu']} - {sd['mu_water']}) / {denom} = {sd['hu']}",
        ]
        if sd["compare"]:
            steps.append(
                f"HU_2 = 1000 * ({sd['mu2']} - {sd['mu_water']}) / {denom} = {sd['hu2']}"
            )
        if sd["tissue"] != "unknown":
            steps.append(f"tissue type: {sd['tissue']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Hounsfield Unit value as a string.
        """
        if sd["compare"]:
            return f"HU_1={sd['hu']}, HU_2={sd['hu2']}"
        return f"HU={sd['hu']}"
