"""Extended robotics task generators.

8 generators across tiers 4-6 covering Denavit-Hartenberg transforms,
robot Jacobian, workspace analysis, trajectory planning, potential
field navigation, sensor fusion, odometry, and reward shaping.
"""
import math

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


def _f(value: float, decimals: int = 4) -> str:
    """Format a numeric value, stripping unnecessary trailing zeros.

    Args:
        value: Number to format.
        decimals: Maximum decimal places.

    Returns:
        Clean string representation.
    """
    rounded = round(value, decimals)
    if rounded == int(rounded):
        return str(int(rounded))
    return str(rounded)


def _fv(vec: list[float]) -> str:
    """Format a vector as a compact string.

    Args:
        vec: List of floats.

    Returns:
        Bracket-enclosed comma-separated string.
    """
    return "[" + ",".join(_f(v) for v in vec) + "]"


# ===================================================================
# 1. DH Transform (tier 5)
# ===================================================================

@register
class DhTransformGenerator(StepGenerator):
    """Compute Denavit-Hartenberg 4x4 transform matrix for one joint.

    DH parameters (theta, d, a, alpha) produce:
        T = [[ct, -st*ca, st*sa, a*ct],
             [st, ct*ca, -ct*sa, a*st],
             [0, sa, ca, d],
             [0, 0, 0, 1]]
    where ct=cos(theta), st=sin(theta), ca=cos(alpha), sa=sin(alpha).

    Difficulty scaling:
        Difficulty 1-3: 90-degree angles, integer d and a.
        Difficulty 4-6: 45-degree angles, decimal parameters.
        Difficulty 7-8: arbitrary angles, verify orthogonality.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dh_transform"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls angle precision.

        Returns:
            Short task description.
        """
        return "compute DH transform matrix for one robot joint"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate DH parameters and compute the 4x4 transform.

        Args:
            difficulty: Controls angle and parameter precision.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            theta_deg = self._rng.choice([0, 90, 180, 270])
            alpha_deg = self._rng.choice([0, 90, 180, 270])
            d = float(self._rng.randint(0, 5))
            a = float(self._rng.randint(0, 5))
        elif difficulty <= 6:
            theta_deg = self._rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
            alpha_deg = self._rng.choice([0, 45, 90, 135, 180, 270])
            d = round(self._rng.uniform(0, 3.0), 2)
            a = round(self._rng.uniform(0, 3.0), 2)
        else:
            theta_deg = self._rng.randint(0, 359)
            alpha_deg = self._rng.randint(0, 359)
            d = round(self._rng.uniform(0, 3.0), 2)
            a = round(self._rng.uniform(0, 3.0), 2)

        theta = math.radians(theta_deg)
        alpha = math.radians(alpha_deg)

        ct = round(math.cos(theta), 4)
        st = round(math.sin(theta), 4)
        ca = round(math.cos(alpha), 4)
        sa = round(math.sin(alpha), 4)

        t_matrix = [
            [ct, round(-st * ca, 4), round(st * sa, 4), round(a * ct, 4)],
            [st, round(ct * ca, 4), round(-ct * sa, 4), round(a * st, 4)],
            [0.0, sa, ca, d],
            [0.0, 0.0, 0.0, 1.0],
        ]

        problem = (
            f"DH(\\theta={theta_deg}^\\circ, d={_f(d)}, "
            f"a={_f(a)}, \\alpha={alpha_deg}^\\circ)"
        )
        return problem, {
            "theta_deg": theta_deg, "alpha_deg": alpha_deg,
            "d": d, "a": a,
            "ct": ct, "st": st, "ca": ca, "sa": sa,
            "T": t_matrix,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate DH transform computation steps.

        Args:
            data: Solution data with trig values and matrix.

        Returns:
            Steps showing trig evaluations and matrix rows.
        """
        steps: list[str] = [
            f"cos({data['theta_deg']})={data['ct']}, "
            f"sin({data['theta_deg']})={data['st']}",
            f"cos({data['alpha_deg']})={data['ca']}, "
            f"sin({data['alpha_deg']})={data['sa']}",
        ]
        for i, row in enumerate(data["T"]):
            row_str = ",".join(_f(v) for v in row)
            steps.append(f"T[{i}]=[{row_str}]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the 4x4 transform matrix.

        Args:
            data: Solution data.

        Returns:
            Compact string representation of the matrix.
        """
        rows = [",".join(_f(v) for v in row) for row in data["T"]]
        return "[" + ";".join(rows) + "]"


# ===================================================================
# 2. Jacobian Robot (tier 6)
# ===================================================================

@register
class JacobianRobotGenerator(StepGenerator):
    """Compute the 2x2 Jacobian for a 2-link planar robot.

    J = [[-L1*sin(t1)-L2*sin(t1+t2), -L2*sin(t1+t2)],
         [L1*cos(t1)+L2*cos(t1+t2),  L2*cos(t1+t2)]].

    Difficulty scaling:
        Difficulty 1-3: 90-degree angles, integer link lengths.
        Difficulty 4-6: 45-degree angles, decimal link lengths.
        Difficulty 7-8: arbitrary angles, compute determinant.

    Prerequisites:
        derivative.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "jacobian_robot"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["derivative"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls angle precision.

        Returns:
            Short task description.
        """
        return "compute Jacobian for 2-link planar robot"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate link lengths and angles, compute Jacobian.

        Args:
            difficulty: Controls angle and length precision.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            l1 = float(self._rng.randint(1, 5))
            l2 = float(self._rng.randint(1, 5))
            t1_deg = self._rng.choice([0, 90, 180, 270])
            t2_deg = self._rng.choice([0, 90, 180, 270])
        elif difficulty <= 6:
            l1 = round(self._rng.uniform(1.0, 5.0), 2)
            l2 = round(self._rng.uniform(1.0, 5.0), 2)
            t1_deg = self._rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
            t2_deg = self._rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
        else:
            l1 = round(self._rng.uniform(1.0, 5.0), 2)
            l2 = round(self._rng.uniform(1.0, 5.0), 2)
            t1_deg = self._rng.randint(0, 359)
            t2_deg = self._rng.randint(0, 359)

        t1 = math.radians(t1_deg)
        t2 = math.radians(t2_deg)
        t12 = t1 + t2

        j11 = round(-l1 * math.sin(t1) - l2 * math.sin(t12), 4)
        j12 = round(-l2 * math.sin(t12), 4)
        j21 = round(l1 * math.cos(t1) + l2 * math.cos(t12), 4)
        j22 = round(l2 * math.cos(t12), 4)

        det = round(j11 * j22 - j12 * j21, 4)

        problem = (
            f"J(L1={_f(l1)}, L2={_f(l2)}, "
            f"\\theta_1={t1_deg}^\\circ, \\theta_2={t2_deg}^\\circ)"
        )
        return problem, {
            "l1": l1, "l2": l2, "t1_deg": t1_deg, "t2_deg": t2_deg,
            "J": [[j11, j12], [j21, j22]], "det": det,
            "show_det": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Jacobian computation steps.

        Args:
            data: Solution data with Jacobian entries.

        Returns:
            Steps showing each Jacobian entry.
        """
        j = data["J"]
        steps: list[str] = [
            f"L1={_f(data['l1'])}, L2={_f(data['l2'])}",
            f"t1={data['t1_deg']}deg, t2={data['t2_deg']}deg",
            f"J[0,0]={_f(j[0][0])}, J[0,1]={_f(j[0][1])}",
            f"J[1,0]={_f(j[1][0])}, J[1,1]={_f(j[1][1])}",
        ]
        if data["show_det"]:
            steps.append(f"det(J)={_f(data['det'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the Jacobian matrix.

        Args:
            data: Solution data.

        Returns:
            Compact string representation of the Jacobian.
        """
        j = data["J"]
        return f"[[{_f(j[0][0])},{_f(j[0][1])}],[{_f(j[1][0])},{_f(j[1][1])}]]"


# ===================================================================
# 3. Workspace Analysis (tier 5)
# ===================================================================

@register
class WorkspaceAnalysisGenerator(StepGenerator):
    """Analyse reachable workspace of a 2-link planar robot.

    Reachable region is an annulus: r_min = |L1 - L2|, r_max = L1 + L2.
    Check if a target point (x, y) is reachable.

    Difficulty scaling:
        Difficulty 1-3: integer link lengths, 1 test point.
        Difficulty 4-6: decimal link lengths, 2 test points.
        Difficulty 7-8: decimal link lengths, 3 test points.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "workspace_analysis"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of test points.

        Returns:
            Short task description.
        """
        return "analyse 2-link robot workspace reachability"

    def _n_points(self, difficulty: int) -> int:
        """Map difficulty to number of test points.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of test points (1-3).
        """
        if difficulty <= 3:
            return 1
        if difficulty <= 6:
            return 2
        return 3

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate link lengths and test points.

        Args:
            difficulty: Controls precision and number of points.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            l1 = float(self._rng.randint(2, 6))
            l2 = float(self._rng.randint(2, 6))
        else:
            l1 = round(self._rng.uniform(1.5, 6.0), 2)
            l2 = round(self._rng.uniform(1.5, 6.0), 2)

        r_min = round(abs(l1 - l2), 4)
        r_max = round(l1 + l2, 4)

        n = self._n_points(difficulty)
        points = []
        for _ in range(n):
            px = round(self._rng.uniform(-r_max - 1, r_max + 1), 2)
            py = round(self._rng.uniform(-r_max - 1, r_max + 1), 2)
            dist = round(math.sqrt(px ** 2 + py ** 2), 4)
            reachable = r_min <= dist <= r_max
            points.append({"x": px, "y": py, "dist": dist, "reachable": reachable})

        pts_str = ", ".join(f"({p['x']},{p['y']})" for p in points)
        problem = (
            f"workspace L1={_f(l1)}, L2={_f(l2)}, points={pts_str}"
        )
        return problem, {
            "l1": l1, "l2": l2, "r_min": r_min, "r_max": r_max,
            "points": points,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate workspace analysis steps.

        Args:
            data: Solution data with boundaries and test points.

        Returns:
            Steps showing annulus bounds and each point check.
        """
        steps: list[str] = [
            f"r_min=|{_f(data['l1'])}-{_f(data['l2'])}|={_f(data['r_min'])}",
            f"r_max={_f(data['l1'])}+{_f(data['l2'])}={_f(data['r_max'])}",
        ]
        for i, p in enumerate(data["points"]):
            status = "reachable" if p["reachable"] else "unreachable"
            steps.append(
                f"P{i}=({p['x']},{p['y']}): "
                f"dist={_f(p['dist'])}, {status}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return reachability results.

        Args:
            data: Solution data.

        Returns:
            String with each point's reachability.
        """
        parts = []
        for i, p in enumerate(data["points"]):
            status = "reachable" if p["reachable"] else "unreachable"
            parts.append(f"P{i}:{status}")
        return ", ".join(parts)


# ===================================================================
# 4. Trajectory Planning (tier 5)
# ===================================================================

@register
class TrajectoryPlanningGenerator(StepGenerator):
    """Plan cubic polynomial trajectory between two joint positions.

    q(t) = a0 + a1*t + a2*t^2 + a3*t^3. Given boundary conditions
    q(0), q(T), q_dot(0), q_dot(T), solve for a0..a3.

    Difficulty scaling:
        Difficulty 1-3: T=1, zero velocities at endpoints.
        Difficulty 4-6: T=2, non-zero velocities.
        Difficulty 7-8: T varies, evaluate at midpoint.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "trajectory_planning"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls trajectory complexity.

        Returns:
            Short task description.
        """
        return "plan cubic polynomial joint trajectory"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate boundary conditions and solve for coefficients.

        Args:
            difficulty: Controls duration and velocities.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            t_f = 1.0
            q0 = round(self._rng.uniform(0, 90), 2)
            q_f = round(self._rng.uniform(0, 90), 2)
            v0 = 0.0
            v_f = 0.0
        elif difficulty <= 6:
            t_f = 2.0
            q0 = round(self._rng.uniform(0, 90), 2)
            q_f = round(self._rng.uniform(0, 90), 2)
            v0 = round(self._rng.uniform(-10, 10), 2)
            v_f = round(self._rng.uniform(-10, 10), 2)
        else:
            t_f = round(self._rng.uniform(1.0, 4.0), 1)
            q0 = round(self._rng.uniform(0, 180), 2)
            q_f = round(self._rng.uniform(0, 180), 2)
            v0 = round(self._rng.uniform(-20, 20), 2)
            v_f = round(self._rng.uniform(-20, 20), 2)

        # Solve: a0=q0, a1=v0
        # a2 = (3*(qf-q0)/T^2) - (2*v0 + vf)/T
        # a3 = (-2*(qf-q0)/T^3) + (v0 + vf)/T^2
        a0 = q0
        a1 = v0
        a2 = round(3 * (q_f - q0) / t_f ** 2 - (2 * v0 + v_f) / t_f, 4)
        a3 = round(-2 * (q_f - q0) / t_f ** 3 + (v0 + v_f) / t_f ** 2, 4)

        # Evaluate at midpoint for high difficulty
        t_mid = round(t_f / 2, 4)
        q_mid = round(
            a0 + a1 * t_mid + a2 * t_mid ** 2 + a3 * t_mid ** 3, 4
        )

        problem = (
            f"cubic traj: q(0)={_f(q0)}, q({_f(t_f)})={_f(q_f)}, "
            f"v(0)={_f(v0)}, v({_f(t_f)})={_f(v_f)}"
        )
        return problem, {
            "t_f": t_f, "q0": q0, "q_f": q_f, "v0": v0, "v_f": v_f,
            "a0": a0, "a1": a1, "a2": a2, "a3": a3,
            "t_mid": t_mid, "q_mid": q_mid,
            "show_mid": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate coefficient computation steps.

        Args:
            data: Solution data with boundary conditions and coefficients.

        Returns:
            Steps showing each coefficient computation.
        """
        steps: list[str] = [
            f"a0=q(0)={_f(data['a0'])}",
            f"a1=v(0)={_f(data['a1'])}",
            f"a2={_f(data['a2'])}",
            f"a3={_f(data['a3'])}",
        ]
        if data["show_mid"]:
            steps.append(
                f"q({_f(data['t_mid'])})={_f(data['q_mid'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the trajectory coefficients.

        Args:
            data: Solution data.

        Returns:
            String with a0..a3 coefficients.
        """
        return (
            f"a0={_f(data['a0'])}, a1={_f(data['a1'])}, "
            f"a2={_f(data['a2'])}, a3={_f(data['a3'])}"
        )


# ===================================================================
# 5. Potential Field (tier 5)
# ===================================================================

@register
class PotentialFieldGenerator(StepGenerator):
    """Compute potential field forces for robot navigation.

    Attractive: F_att = -k_att * (q - q_goal).
    Repulsive: F_rep = k_rep * (1/d - 1/d0) * (1/d^2) * grad(d)
    when d < d0, else 0. Net force: F = F_att + F_rep.

    Difficulty scaling:
        Difficulty 1-3: 2D, one obstacle, d >= d0 (no repulsion).
        Difficulty 4-6: 2D, one obstacle, d < d0 (with repulsion).
        Difficulty 7-8: 2D, two obstacles.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "potential_field"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of obstacles.

        Returns:
            Short task description.
        """
        return "compute potential field navigation forces"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate robot position, goal, obstacles, and compute forces.

        Args:
            difficulty: Controls obstacle scenario.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        k_att = round(self._rng.uniform(0.5, 2.0), 2)
        k_rep = round(self._rng.uniform(1.0, 5.0), 2)
        d0 = round(self._rng.uniform(2.0, 5.0), 2)

        qx = round(self._rng.uniform(-5, 5), 2)
        qy = round(self._rng.uniform(-5, 5), 2)
        gx = round(self._rng.uniform(-5, 5), 2)
        gy = round(self._rng.uniform(-5, 5), 2)

        # Attractive force
        f_att_x = round(-k_att * (qx - gx), 4)
        f_att_y = round(-k_att * (qy - gy), 4)

        if difficulty <= 3:
            # Obstacle far away
            n_obs = 1
            ox = qx + self._rng.choice([-1, 1]) * (d0 + self._rng.uniform(1, 3))
            oy = qy + self._rng.choice([-1, 1]) * (d0 + self._rng.uniform(1, 3))
            obstacles = [(round(ox, 2), round(oy, 2))]
        elif difficulty <= 6:
            n_obs = 1
            direction = self._rng.uniform(0, 2 * math.pi)
            close_d = self._rng.uniform(0.5, d0 - 0.1)
            ox = round(qx + close_d * math.cos(direction), 2)
            oy = round(qy + close_d * math.sin(direction), 2)
            obstacles = [(ox, oy)]
        else:
            n_obs = 2
            obstacles = []
            for _ in range(n_obs):
                direction = self._rng.uniform(0, 2 * math.pi)
                close_d = self._rng.uniform(0.5, d0 - 0.1)
                ox = round(qx + close_d * math.cos(direction), 2)
                oy = round(qy + close_d * math.sin(direction), 2)
                obstacles.append((ox, oy))

        # Compute repulsive forces
        f_rep_x = 0.0
        f_rep_y = 0.0
        obs_details = []
        for ox, oy in obstacles:
            dx = qx - ox
            dy = qy - oy
            d = round(math.sqrt(dx ** 2 + dy ** 2), 4)
            if d < 0.01:
                d = 0.01
            if d < d0:
                grad_x = round(dx / d, 4)
                grad_y = round(dy / d, 4)
                mag = round(k_rep * (1.0 / d - 1.0 / d0) * (1.0 / d ** 2), 4)
                frx = round(mag * grad_x, 4)
                fry = round(mag * grad_y, 4)
                f_rep_x += frx
                f_rep_y += fry
                obs_details.append({
                    "pos": (ox, oy), "d": d, "mag": mag,
                    "frx": frx, "fry": fry, "active": True,
                })
            else:
                obs_details.append({
                    "pos": (ox, oy), "d": d, "mag": 0.0,
                    "frx": 0.0, "fry": 0.0, "active": False,
                })

        f_rep_x = round(f_rep_x, 4)
        f_rep_y = round(f_rep_y, 4)
        f_net_x = round(f_att_x + f_rep_x, 4)
        f_net_y = round(f_att_y + f_rep_y, 4)

        problem = (
            f"PF: q=({qx},{qy}), goal=({gx},{gy}), "
            f"k_att={k_att}, k_rep={k_rep}, d0={d0}"
        )
        return problem, {
            "q": (qx, qy), "goal": (gx, gy),
            "k_att": k_att, "k_rep": k_rep, "d0": d0,
            "f_att": (f_att_x, f_att_y),
            "f_rep": (f_rep_x, f_rep_y),
            "f_net": (f_net_x, f_net_y),
            "obs_details": obs_details,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate force computation steps.

        Args:
            data: Solution data with forces and obstacle details.

        Returns:
            Steps showing attractive, repulsive, and net forces.
        """
        steps: list[str] = [
            f"F_att=({_f(data['f_att'][0])},{_f(data['f_att'][1])})"
        ]
        for i, obs in enumerate(data["obs_details"]):
            if obs["active"]:
                steps.append(
                    f"obs{i}: d={_f(obs['d'])}<{_f(data['d0'])}, "
                    f"F_rep=({_f(obs['frx'])},{_f(obs['fry'])})"
                )
            else:
                steps.append(
                    f"obs{i}: d={_f(obs['d'])}>={_f(data['d0'])}, no repulsion"
                )
        steps.append(
            f"F_net=({_f(data['f_net'][0])},{_f(data['f_net'][1])})"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the net force.

        Args:
            data: Solution data.

        Returns:
            String representation of net force vector.
        """
        return f"({_f(data['f_net'][0])},{_f(data['f_net'][1])})"


# ===================================================================
# 6. Sensor Fusion (tier 5)
# ===================================================================

@register
class SensorFusionGenerator(StepGenerator):
    """Fuse two Gaussian sensor estimates into one.

    mu = (mu1*sigma2^2 + mu2*sigma1^2) / (sigma1^2 + sigma2^2).
    sigma^2 = sigma1^2*sigma2^2 / (sigma1^2 + sigma2^2).

    Difficulty scaling:
        Difficulty 1-3: integer means and variances, 2 sensors.
        Difficulty 4-6: decimal values, 2 sensors.
        Difficulty 7-8: decimal values, 3 sensors (sequential fusion).

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sensor_fusion"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of sensors.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "fuse three Gaussian sensor estimates sequentially"
        return "fuse two Gaussian sensor estimates"

    def _fuse_two(self, mu1: float, s1_sq: float,
                  mu2: float, s2_sq: float) -> tuple[float, float]:
        """Fuse two Gaussian estimates.

        Args:
            mu1: Mean of first estimate.
            s1_sq: Variance of first estimate.
            mu2: Mean of second estimate.
            s2_sq: Variance of second estimate.

        Returns:
            Tuple of (fused_mean, fused_variance).
        """
        denom = s1_sq + s2_sq
        mu_f = round((mu1 * s2_sq + mu2 * s1_sq) / denom, 4)
        s_f_sq = round(s1_sq * s2_sq / denom, 4)
        return mu_f, s_f_sq

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate sensor estimates and fuse them.

        Args:
            difficulty: Controls number of sensors and precision.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            mu1 = float(self._rng.randint(1, 20))
            s1 = float(self._rng.randint(1, 5))
            mu2 = float(self._rng.randint(1, 20))
            s2 = float(self._rng.randint(1, 5))
        else:
            mu1 = round(self._rng.uniform(1, 20), 2)
            s1 = round(self._rng.uniform(0.5, 5.0), 2)
            mu2 = round(self._rng.uniform(1, 20), 2)
            s2 = round(self._rng.uniform(0.5, 5.0), 2)

        s1_sq = round(s1 ** 2, 4)
        s2_sq = round(s2 ** 2, 4)
        mu_f, sf_sq = self._fuse_two(mu1, s1_sq, mu2, s2_sq)

        fusion_steps_data = [{
            "mu1": mu1, "s1_sq": s1_sq, "mu2": mu2, "s2_sq": s2_sq,
            "mu_f": mu_f, "sf_sq": sf_sq,
        }]

        if difficulty >= 7:
            mu3 = round(self._rng.uniform(1, 20), 2)
            s3 = round(self._rng.uniform(0.5, 5.0), 2)
            s3_sq = round(s3 ** 2, 4)
            mu_f2, sf_sq2 = self._fuse_two(mu_f, sf_sq, mu3, s3_sq)
            fusion_steps_data.append({
                "mu1": mu_f, "s1_sq": sf_sq, "mu2": mu3, "s2_sq": s3_sq,
                "mu_f": mu_f2, "sf_sq": sf_sq2,
            })
            mu_final = mu_f2
            sf_final = sf_sq2
        else:
            mu3 = None
            mu_final = mu_f
            sf_final = sf_sq

        problem = (
            f"fuse: (\\mu_1={_f(mu1)},\\sigma_1={_f(s1)}), "
            f"(\\mu_2={_f(mu2)},\\sigma_2={_f(s2)})"
        )
        if mu3 is not None:
            problem += f", (\\mu_3={_f(mu3)},\\sigma_3={_f(s3)})"

        return problem, {
            "fusion_steps": fusion_steps_data,
            "mu_final": mu_final, "sf_final": sf_final,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate fusion computation steps.

        Args:
            data: Solution data with fusion intermediates.

        Returns:
            Steps showing each fusion computation.
        """
        steps: list[str] = []
        for i, fs in enumerate(data["fusion_steps"]):
            label = f"fuse{i+1}" if len(data["fusion_steps"]) > 1 else "fuse"
            steps.append(
                f"{label}: mu=({_f(fs['mu1'])}*{_f(fs['s2_sq'])}+"
                f"{_f(fs['mu2'])}*{_f(fs['s1_sq'])})"
                f"/({_f(fs['s1_sq'])}+{_f(fs['s2_sq'])})={_f(fs['mu_f'])}"
            )
            steps.append(
                f"{label}: var={_f(fs['s1_sq'])}*{_f(fs['s2_sq'])}"
                f"/({_f(fs['s1_sq'])}+{_f(fs['s2_sq'])})={_f(fs['sf_sq'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the fused estimate.

        Args:
            data: Solution data.

        Returns:
            String with fused mean and variance.
        """
        return f"mu={_f(data['mu_final'])}, var={_f(data['sf_final'])}"


# ===================================================================
# 7. Odometry (tier 4)
# ===================================================================

@register
class OdometryGenerator(StepGenerator):
    """Compute differential drive odometry over several time steps.

    dx = v * cos(theta) * dt, dy = v * sin(theta) * dt,
    dtheta = omega * dt. Integrates 3-5 steps.

    Difficulty scaling:
        Difficulty 1-3: 3 steps, constant v and omega.
        Difficulty 4-6: 4 steps, varying v.
        Difficulty 7-8: 5 steps, varying v and omega.

    Prerequisites:
        sin_cos_eval.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "odometry"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["sin_cos_eval"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls number of steps.

        Returns:
            Short task description.
        """
        return "compute differential drive odometry"

    def _n_steps(self, difficulty: int) -> int:
        """Map difficulty to number of integration steps.

        Args:
            difficulty: Difficulty level.

        Returns:
            Number of steps (3-5).
        """
        if difficulty <= 3:
            return 3
        if difficulty <= 6:
            return 4
        return 5

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate velocity commands and integrate odometry.

        Args:
            difficulty: Controls step count and variability.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        n = self._n_steps(difficulty)
        dt = round(self._rng.choice([0.1, 0.2, 0.5]), 2)

        if difficulty <= 3:
            v_base = round(self._rng.uniform(0.5, 2.0), 2)
            w_base = round(self._rng.uniform(-0.5, 0.5), 2)
            commands = [(v_base, w_base)] * n
        elif difficulty <= 6:
            w_base = round(self._rng.uniform(-0.5, 0.5), 2)
            commands = [
                (round(self._rng.uniform(0.5, 2.0), 2), w_base)
                for _ in range(n)
            ]
        else:
            commands = [
                (round(self._rng.uniform(0.5, 2.0), 2),
                 round(self._rng.uniform(-0.5, 0.5), 2))
                for _ in range(n)
            ]

        x, y, theta = 0.0, 0.0, 0.0
        trace = []
        for v, w in commands:
            dx = round(v * math.cos(theta) * dt, 4)
            dy = round(v * math.sin(theta) * dt, 4)
            dtheta = round(w * dt, 4)
            x = round(x + dx, 4)
            y = round(y + dy, 4)
            theta = round(theta + dtheta, 4)
            trace.append({
                "v": v, "w": w, "dx": dx, "dy": dy,
                "dtheta": dtheta, "x": x, "y": y, "theta": theta,
            })

        cmd_str = ", ".join(f"(v={c[0]},w={c[1]})" for c in commands)
        problem = f"odometry dt={dt}, cmds=[{cmd_str}]"
        return problem, {
            "dt": dt, "trace": trace,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate per-step odometry integration steps.

        Args:
            data: Solution data with position trace.

        Returns:
            Steps showing each integration step.
        """
        steps: list[str] = []
        for i, t in enumerate(data["trace"]):
            steps.append(
                f"t{i}: v={_f(t['v'])},w={_f(t['w'])}: "
                f"({_f(t['x'])},{_f(t['y'])},{_f(t['theta'])})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final pose.

        Args:
            data: Solution data.

        Returns:
            String with final (x, y, theta).
        """
        last = data["trace"][-1]
        return f"({_f(last['x'])},{_f(last['y'])},{_f(last['theta'])})"


# ===================================================================
# 8. Reward Shaping (tier 6)
# ===================================================================

@register
class RewardShapingGenerator(StepGenerator):
    """Compute potential-based reward shaping.

    R'(s, a, s') = R(s, a, s') + gamma * Phi(s') - Phi(s).
    Shows that this preserves the optimal policy by demonstrating
    the shaped return equals original return plus a telescoping sum.

    Difficulty scaling:
        Difficulty 1-3: 3 states, 2 transitions, integer values.
        Difficulty 4-6: 4 states, 3 transitions, decimal values.
        Difficulty 7-8: 4 states, 4 transitions, show telescoping proof.

    Prerequisites:
        bellman_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "reward_shaping"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bellman_equation"]

    def task_description(self, difficulty: int) -> str:
        """Generate a natural language task description.

        Args:
            difficulty: Controls trajectory length.

        Returns:
            Short task description.
        """
        return "compute potential-based reward shaping"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate state sequence, rewards, potentials, and shaped rewards.

        Args:
            difficulty: Controls number of states and transitions.

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        gamma = self._rng.choice([0.9, 0.95, 0.99])

        if difficulty <= 3:
            n_states = 3
            n_trans = 2
        elif difficulty <= 6:
            n_states = 4
            n_trans = 3
        else:
            n_states = 4
            n_trans = 4

        # Generate potentials for each state
        if difficulty <= 3:
            phi = [float(self._rng.randint(-5, 10)) for _ in range(n_states)]
        else:
            phi = [round(self._rng.uniform(-5, 10), 2) for _ in range(n_states)]

        # Generate trajectory: sequence of states
        states = [self._rng.randint(0, n_states - 1)]
        for _ in range(n_trans):
            states.append(self._rng.randint(0, n_states - 1))

        # Generate original rewards for each transition
        if difficulty <= 3:
            rewards = [float(self._rng.randint(-2, 10)) for _ in range(n_trans)]
        else:
            rewards = [round(self._rng.uniform(-2, 10), 2) for _ in range(n_trans)]

        # Compute shaped rewards
        shaped = []
        for i in range(n_trans):
            s = states[i]
            s_next = states[i + 1]
            r_shaped = round(
                rewards[i] + gamma * phi[s_next] - phi[s], 4
            )
            shaped.append(r_shaped)

        # Telescoping: sum of shaped returns = sum of original returns
        # + gamma^n * Phi(s_n) - Phi(s_0)
        orig_return = round(
            sum(rewards[i] * gamma ** i for i in range(n_trans)), 4
        )
        shaped_return = round(
            sum(shaped[i] * gamma ** i for i in range(n_trans)), 4
        )
        telescope = round(
            gamma ** n_trans * phi[states[-1]] - phi[states[0]], 4
        )

        problem = (
            f"shaping: states={states}, R={rewards}, "
            f"\\Phi={[_f(p) for p in phi]}, \\gamma={gamma}"
        )
        return problem, {
            "states": states, "rewards": rewards, "phi": phi,
            "gamma": gamma, "shaped": shaped,
            "orig_return": orig_return, "shaped_return": shaped_return,
            "telescope": telescope,
            "show_telescope": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate reward shaping computation steps.

        Args:
            data: Solution data with original and shaped rewards.

        Returns:
            Steps showing each shaped reward and telescoping.
        """
        steps: list[str] = []
        for i in range(len(data["shaped"])):
            s = data["states"][i]
            s_next = data["states"][i + 1]
            steps.append(
                f"R'(s{s},s{s_next})={_f(data['rewards'][i])}+"
                f"{data['gamma']}*{_f(data['phi'][s_next])}"
                f"-{_f(data['phi'][s])}={_f(data['shaped'][i])}"
            )
        if data["show_telescope"]:
            steps.append(
                f"telescope: shaped_return-orig_return="
                f"{_f(data['telescope'])}"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the shaped rewards.

        Args:
            data: Solution data.

        Returns:
            String with shaped reward values.
        """
        parts = [_f(r) for r in data["shaped"]]
        return f"R'=[{','.join(parts)}]"
