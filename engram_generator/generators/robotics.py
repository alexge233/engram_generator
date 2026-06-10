"""Robotics task generators.

6 generators across tiers 5-6 covering forward kinematics, inverse
kinematics, A* path planning, PID control, Kalman filter update,
and MDP value iteration.
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


# ===================================================================
# 1. Forward Kinematics (tier 5)
# ===================================================================

@register
class ForwardKinematicsGenerator(StepGenerator):
    """Compute end-effector position from 2 joint angles via DH parameters.

    For a 2-link planar robot with link lengths L1 and L2 and joint
    angles theta1 and theta2:
        x = L1*cos(theta1) + L2*cos(theta1 + theta2)
        y = L1*sin(theta1) + L2*sin(theta1 + theta2)

    Difficulty scaling:
        Difficulty 1-3: 90-degree angles, integer link lengths.
        Difficulty 4-6: 45-degree increments, decimal link lengths.
        Difficulty 7-8: arbitrary angles, compute Jacobian entries.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "forward_kinematics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute end-effector position and Jacobian"
        return "compute 2-link robot end-effector position"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate link lengths and joint angles.

        Args:
            difficulty: Controls angle precision and variants.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            l1 = float(self._rng.randint(1, 5))
            l2 = float(self._rng.randint(1, 5))
            theta1_deg = self._rng.choice([0, 90, 180, 270])
            theta2_deg = self._rng.choice([0, 90, 180, 270])
        elif difficulty <= 6:
            l1 = round(self._rng.uniform(0.5, 5.0), 2)
            l2 = round(self._rng.uniform(0.5, 5.0), 2)
            theta1_deg = self._rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
            theta2_deg = self._rng.choice([0, 45, 90, 135, 180, 225, 270, 315])
        else:
            l1 = round(self._rng.uniform(0.5, 5.0), 2)
            l2 = round(self._rng.uniform(0.5, 5.0), 2)
            theta1_deg = self._rng.randint(0, 359)
            theta2_deg = self._rng.randint(0, 359)

        t1 = math.radians(theta1_deg)
        t2 = math.radians(theta2_deg)
        t12 = t1 + t2

        x = round(l1 * math.cos(t1) + l2 * math.cos(t12), 4)
        y = round(l1 * math.sin(t1) + l2 * math.sin(t12), 4)

        # Jacobian: dx/dt1, dx/dt2, dy/dt1, dy/dt2
        j11 = round(-l1 * math.sin(t1) - l2 * math.sin(t12), 4)
        j12 = round(-l2 * math.sin(t12), 4)
        j21 = round(l1 * math.cos(t1) + l2 * math.cos(t12), 4)
        j22 = round(l2 * math.cos(t12), 4)

        return ("x = L_1 \\cos\\theta_1 + L_2 \\cos(\\theta_1+\\theta_2), \\quad"
                " y = L_1 \\sin\\theta_1 + L_2 \\sin(\\theta_1+\\theta_2)"), {
            "L1": l1, "L2": l2,
            "theta1": theta1_deg, "theta2": theta2_deg,
            "x": x, "y": y,
            "J": [[j11, j12], [j21, j22]],
            "show_jacobian": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate forward kinematics computation steps.

        Args:
            data: Solution data with link lengths, angles, and position.

        Returns:
            List of step strings.
        """
        steps = [
            f"L1={_f(data['L1'])}, L2={_f(data['L2'])}",
            f"theta1={data['theta1']}deg, theta2={data['theta2']}deg",
            f"x = {_f(data['L1'])}*cos({data['theta1']}) + {_f(data['L2'])}*cos({data['theta1']}+{data['theta2']})",
            f"y = {_f(data['L1'])}*sin({data['theta1']}) + {_f(data['L2'])}*sin({data['theta1']}+{data['theta2']})",
        ]
        if data["show_jacobian"]:
            j = data["J"]
            steps.append(f"J = [[{_f(j[0][0])}, {_f(j[0][1])}], [{_f(j[1][0])}, {_f(j[1][1])}]]")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the end-effector position.

        Args:
            data: Solution data.

        Returns:
            End-effector (x, y) coordinates.
        """
        return f"({_f(data['x'])}, {_f(data['y'])})"


# ===================================================================
# 2. Inverse Kinematics (tier 6)
# ===================================================================

@register
class InverseKinematicsGenerator(StepGenerator):
    """Solve 2-link planar IK: find theta1, theta2 for target (x, y).

    Geometric approach:
        cos(theta2) = (x^2 + y^2 - L1^2 - L2^2) / (2*L1*L2)
        theta2 = acos(c2)
        theta1 = atan2(y, x) - atan2(L2*sin(theta2), L1 + L2*cos(theta2))

    Difficulty scaling:
        Difficulty 1-3: target on reachable integer grid.
        Difficulty 4-6: decimal target, check reachability.
        Difficulty 7-8: both elbow-up and elbow-down solutions.

    Prerequisites:
        system_equations.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "inverse_kinematics"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["system_equations"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "solve 2-link planar inverse kinematics"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate link lengths and target position.

        Args:
            difficulty: Controls parameter ranges and solutions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        l1 = round(self._rng.uniform(2, 5), 2) if difficulty > 3 else float(self._rng.randint(2, 5))
        l2 = round(self._rng.uniform(2, 5), 2) if difficulty > 3 else float(self._rng.randint(2, 5))

        # Generate reachable target
        max_reach = l1 + l2
        min_reach = abs(l1 - l2)
        r = round(self._rng.uniform(min_reach + 0.1, max_reach - 0.1), 4)
        angle = math.radians(self._rng.randint(0, 359))
        tx = round(r * math.cos(angle), 4)
        ty = round(r * math.sin(angle), 4)

        dist_sq = tx ** 2 + ty ** 2
        c2 = round((dist_sq - l1 ** 2 - l2 ** 2) / (2 * l1 * l2), 4)
        c2 = max(-1.0, min(1.0, c2))

        theta2_up = round(math.degrees(math.acos(c2)), 4)
        theta2_down = round(-theta2_up, 4)

        s2_up = round(math.sin(math.radians(theta2_up)), 4)
        theta1_up = round(math.degrees(
            math.atan2(ty, tx) - math.atan2(l2 * s2_up, l1 + l2 * c2)
        ), 4)

        s2_down = round(math.sin(math.radians(theta2_down)), 4)
        theta1_down = round(math.degrees(
            math.atan2(ty, tx) - math.atan2(l2 * s2_down, l1 + l2 * c2)
        ), 4)

        reachable = (min_reach <= r <= max_reach)

        return ("\\cos\\theta_2 = \\frac{x^2+y^2-L_1^2-L_2^2}{2 L_1 L_2}"), {
            "L1": l1, "L2": l2,
            "tx": tx, "ty": ty,
            "c2": c2,
            "theta2_up": theta2_up, "theta1_up": theta1_up,
            "theta2_down": theta2_down, "theta1_down": theta1_down,
            "reachable": reachable,
            "both_solutions": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate inverse kinematics computation steps.

        Args:
            data: Solution data with joint angles.

        Returns:
            List of step strings.
        """
        steps = [
            f"L1={_f(data['L1'])}, L2={_f(data['L2'])}",
            f"target = ({_f(data['tx'])}, {_f(data['ty'])})",
            f"cos(theta2) = {_f(data['c2'])}",
            f"theta2 = {_f(data['theta2_up'])}deg",
            f"theta1 = {_f(data['theta1_up'])}deg",
        ]
        if data["both_solutions"]:
            steps.append(f"elbow-down: t1={_f(data['theta1_down'])}deg, t2={_f(data['theta2_down'])}deg")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the joint angles.

        Args:
            data: Solution data.

        Returns:
            Joint angle solution(s).
        """
        ans = f"theta1 = {_f(data['theta1_up'])}deg, theta2 = {_f(data['theta2_up'])}deg"
        if data["both_solutions"]:
            ans += (f" | theta1 = {_f(data['theta1_down'])}deg,"
                    f" theta2 = {_f(data['theta2_down'])}deg")
        return ans


# ===================================================================
# 3. Path Planning (A*) (tier 5)
# ===================================================================

@register
class PathPlanningGenerator(StepGenerator):
    """A* pathfinding on a 5x5 grid with obstacles.

    Uses Manhattan distance heuristic. Shows open list, closed list,
    and final path from start to goal.

    Difficulty scaling:
        Difficulty 1-3: 0-2 obstacles, start=(0,0), goal=(4,4).
        Difficulty 4-6: 3-5 obstacles, varied start/goal.
        Difficulty 7-8: 6-8 obstacles, may be unsolvable.

    Prerequisites:
        shortest_path.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "path_planning"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["shortest_path"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find shortest path using A* on a grid"

    def _manhattan(self, a: tuple[int, int], b: tuple[int, int]) -> int:
        """Compute Manhattan distance between two grid cells.

        Args:
            a: First cell (row, col).
            b: Second cell (row, col).

        Returns:
            Manhattan distance.
        """
        return abs(a[0] - b[0]) + abs(a[1] - b[1])

    def _astar(self, grid: list[list[int]], start: tuple[int, int],
               goal: tuple[int, int]) -> list[tuple[int, int]] | None:
        """Run A* on a grid and return the path.

        Args:
            grid: 5x5 grid where 1 = obstacle.
            start: Start cell.
            goal: Goal cell.

        Returns:
            Path as list of (row, col) or None if no path.
        """
        rows = len(grid)
        cols = len(grid[0])
        open_set = {start}
        came_from: dict[tuple[int, int], tuple[int, int]] = {}
        g_score: dict[tuple[int, int], int] = {start: 0}
        f_score: dict[tuple[int, int], int] = {start: self._manhattan(start, goal)}

        while open_set:
            current = min(open_set, key=lambda n: f_score.get(n, 9999))
            if current == goal:
                path = [current]
                while current in came_from:
                    current = came_from[current]
                    path.append(current)
                return list(reversed(path))

            open_set.remove(current)
            for dr, dc in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
                nr, nc = current[0] + dr, current[1] + dc
                neighbor = (nr, nc)
                if not (0 <= nr < rows and 0 <= nc < cols):
                    continue
                if grid[nr][nc] == 1:
                    continue
                tentative_g = g_score[current] + 1
                if tentative_g < g_score.get(neighbor, 9999):
                    came_from[neighbor] = current
                    g_score[neighbor] = tentative_g
                    f_score[neighbor] = tentative_g + self._manhattan(neighbor, goal)
                    open_set.add(neighbor)

        return None

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 5x5 grid with obstacles, start, and goal.

        Args:
            difficulty: Controls obstacle count and positions.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        size = 5
        grid = [[0] * size for _ in range(size)]

        if difficulty <= 3:
            n_obs = self._rng.randint(0, 2)
            start = (0, 0)
            goal = (4, 4)
        elif difficulty <= 6:
            n_obs = self._rng.randint(3, 5)
            start = (self._rng.randint(0, 1), self._rng.randint(0, 1))
            goal = (self._rng.randint(3, 4), self._rng.randint(3, 4))
        else:
            n_obs = self._rng.randint(6, 8)
            start = (self._rng.randint(0, 1), self._rng.randint(0, 1))
            goal = (self._rng.randint(3, 4), self._rng.randint(3, 4))

        # Place obstacles avoiding start and goal
        placed = 0
        attempts = 0
        while placed < n_obs and attempts < 50:
            r = self._rng.randint(0, size - 1)
            c = self._rng.randint(0, size - 1)
            if (r, c) != start and (r, c) != goal and grid[r][c] == 0:
                grid[r][c] = 1
                placed += 1
            attempts += 1

        path = self._astar(grid, start, goal)
        obstacles = [(r, c) for r in range(size) for c in range(size) if grid[r][c] == 1]

        return "A^* on 5 \\times 5 grid", {
            "grid": grid,
            "start": start,
            "goal": goal,
            "obstacles": obstacles,
            "path": path,
            "path_len": len(path) - 1 if path else -1,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate A* pathfinding steps.

        Args:
            data: Solution data with grid, path, and lists.

        Returns:
            List of step strings.
        """
        steps = [
            f"start={data['start']}, goal={data['goal']}",
            f"obstacles: {data['obstacles']}",
        ]
        if data["path"] is not None:
            path_str = " -> ".join(str(p) for p in data["path"])
            steps.append(f"path: {path_str}")
            steps.append(f"cost = {data['path_len']}")
        else:
            steps.append("no path found")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the path or no-path result.

        Args:
            data: Solution data.

        Returns:
            Path length or unreachable.
        """
        if data["path"] is not None:
            return f"cost = {data['path_len']}"
        return "unreachable"


# ===================================================================
# 4. PID Control for Robot Joint (tier 5)
# ===================================================================

@register
class PidControlRobotGenerator(StepGenerator):
    """Compute PID output: u = Kp*e + Ki*sum(e)*dt + Kd*(e - e_prev)/dt.

    Given PID gains, current error, previous error, integral
    accumulator, and time step, compute the control signal.

    Difficulty scaling:
        Difficulty 1-3: P-only or PD, integer gains.
        Difficulty 4-6: full PID, decimal gains.
        Difficulty 7-8: simulate 3 time steps of PID loop.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "pid_control_robot"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "simulate PID control loop for 3 steps"
        return "compute PID control output for robot joint"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate PID parameters and compute control output.

        Args:
            difficulty: Controls PID complexity and simulation depth.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        dt = round(self._rng.choice([0.01, 0.02, 0.05, 0.1]), 4)

        if difficulty <= 3:
            kp = float(self._rng.randint(1, 10))
            ki = 0.0
            kd = float(self._rng.randint(0, 3))
            e = round(self._rng.uniform(-5, 5), 2)
            e_prev = round(self._rng.uniform(-5, 5), 2)
            e_sum = 0.0
        elif difficulty <= 6:
            kp = round(self._rng.uniform(0.5, 10), 2)
            ki = round(self._rng.uniform(0.01, 2.0), 3)
            kd = round(self._rng.uniform(0.01, 5.0), 3)
            e = round(self._rng.uniform(-5, 5), 2)
            e_prev = round(self._rng.uniform(-5, 5), 2)
            e_sum = round(self._rng.uniform(-10, 10), 2)
        else:
            kp = round(self._rng.uniform(1, 8), 2)
            ki = round(self._rng.uniform(0.1, 1.5), 3)
            kd = round(self._rng.uniform(0.1, 3.0), 3)
            e = round(self._rng.uniform(-5, 5), 2)
            e_prev = round(self._rng.uniform(-5, 5), 2)
            e_sum = 0.0

        # Single step
        e_sum_new = round(e_sum + e * dt, 4)
        p_term = round(kp * e, 4)
        i_term = round(ki * e_sum_new, 4)
        d_term = round(kd * (e - e_prev) / dt, 4)
        u = round(p_term + i_term + d_term, 4)

        # Multi-step simulation for difficulty >= 7
        sim_steps = []
        if difficulty >= 7:
            cur_e = e
            cur_e_prev = e_prev
            cur_e_sum = e_sum
            for step_i in range(3):
                cur_e_sum = round(cur_e_sum + cur_e * dt, 4)
                p = round(kp * cur_e, 4)
                i = round(ki * cur_e_sum, 4)
                d = round(kd * (cur_e - cur_e_prev) / dt, 4)
                u_step = round(p + i + d, 4)
                sim_steps.append({
                    "step": step_i, "e": cur_e,
                    "p": p, "i": i, "d": d, "u": u_step,
                })
                cur_e_prev = cur_e
                # Simulate simple plant: error reduces by 10-30%
                cur_e = round(cur_e * self._rng.uniform(0.5, 0.9), 4)

        return "u = K_p e + K_i \\sum e \\cdot dt + K_d \\frac{e - e_{\\text{prev}}}{dt}", {
            "Kp": kp, "Ki": ki, "Kd": kd, "dt": dt,
            "e": e, "e_prev": e_prev, "e_sum": e_sum,
            "p_term": p_term, "i_term": i_term, "d_term": d_term,
            "u": u,
            "sim_steps": sim_steps,
            "multi_step": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate PID computation steps.

        Args:
            data: Solution data with gains, errors, and output.

        Returns:
            List of step strings.
        """
        steps = [
            f"Kp={_f(data['Kp'])}, Ki={_f(data['Ki'])}, Kd={_f(data['Kd'])}, dt={data['dt']}",
            f"e={_f(data['e'])}, e_prev={_f(data['e_prev'])}",
            f"P = {_f(data['p_term'])}",
            f"I = {_f(data['i_term'])}",
            f"D = {_f(data['d_term'])}",
        ]
        if data["multi_step"]:
            for s in data["sim_steps"]:
                steps.append(f"step{s['step']}: e={_f(s['e'])}, u={_f(s['u'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the PID output.

        Args:
            data: Solution data.

        Returns:
            Control signal u.
        """
        if data["multi_step"] and data["sim_steps"]:
            last = data["sim_steps"][-1]
            return f"u = {_f(last['u'])}"
        return f"u = {_f(data['u'])}"


# ===================================================================
# 5. Kalman Update (tier 6)
# ===================================================================

@register
class KalmanUpdateGenerator(StepGenerator):
    """One-dimensional Kalman filter predict-update cycle.

    Predict: x' = F*x + B*u, P' = F*P*F + Q.
    Update: K = P'*H / (H*P'*H + R), x = x' + K*(z - H*x'), P = (1-K*H)*P'.

    Difficulty scaling:
        Difficulty 1-3: F=1, H=1, B=0 (random walk), integer noise.
        Difficulty 4-6: F, H as decimals, nonzero B*u.
        Difficulty 7-8: 2 consecutive predict-update cycles.

    Prerequisites:
        matrix_multiply.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "kalman_update"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["matrix_multiply"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "run 2-cycle 1D Kalman filter"
        return "compute one Kalman filter predict-update step"

    def _kalman_step(self, x: float, p: float, f: float, b: float,
                     u: float, q: float, h: float, r: float,
                     z: float) -> dict:
        """Run one Kalman predict-update cycle.

        Args:
            x: Current state estimate.
            p: Current estimate covariance.
            f: State transition factor.
            b: Control input factor.
            u: Control input.
            q: Process noise variance.
            h: Observation model factor.
            r: Measurement noise variance.
            z: Measurement.

        Returns:
            Dict with predicted and updated values.
        """
        x_pred = round(f * x + b * u, 4)
        p_pred = round(f * p * f + q, 4)
        denom = round(h * p_pred * h + r, 4)
        k = round(p_pred * h / denom, 4) if denom != 0 else 0.0
        x_upd = round(x_pred + k * (z - h * x_pred), 4)
        p_upd = round((1 - k * h) * p_pred, 4)
        return {
            "x_pred": x_pred, "p_pred": p_pred,
            "K": k, "x_upd": x_upd, "p_upd": p_upd,
            "z": z,
        }

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate Kalman filter parameters and measurements.

        Args:
            difficulty: Controls parameter complexity and cycles.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            f_val = 1.0
            h_val = 1.0
            b_val = 0.0
            u_val = 0.0
            q = float(self._rng.randint(1, 5))
            r = float(self._rng.randint(1, 10))
            x0 = float(self._rng.randint(0, 20))
            p0 = float(self._rng.randint(1, 10))
            z1 = float(self._rng.randint(0, 25))
            z2 = float(self._rng.randint(0, 25))
        elif difficulty <= 6:
            f_val = round(self._rng.uniform(0.8, 1.2), 2)
            h_val = round(self._rng.uniform(0.5, 1.5), 2)
            b_val = round(self._rng.uniform(0.1, 1.0), 2)
            u_val = round(self._rng.uniform(-2, 2), 2)
            q = round(self._rng.uniform(0.1, 3.0), 2)
            r = round(self._rng.uniform(0.5, 5.0), 2)
            x0 = round(self._rng.uniform(0, 20), 2)
            p0 = round(self._rng.uniform(1, 10), 2)
            z1 = round(self._rng.uniform(0, 25), 2)
            z2 = round(self._rng.uniform(0, 25), 2)
        else:
            f_val = round(self._rng.uniform(0.9, 1.1), 3)
            h_val = round(self._rng.uniform(0.8, 1.2), 3)
            b_val = round(self._rng.uniform(0.1, 0.5), 3)
            u_val = round(self._rng.uniform(-1, 3), 2)
            q = round(self._rng.uniform(0.1, 2.0), 3)
            r = round(self._rng.uniform(0.5, 3.0), 3)
            x0 = round(self._rng.uniform(0, 15), 2)
            p0 = round(self._rng.uniform(1, 5), 2)
            z1 = round(self._rng.uniform(0, 20), 2)
            z2 = round(self._rng.uniform(0, 20), 2)

        step1 = self._kalman_step(x0, p0, f_val, b_val, u_val, q, h_val, r, z1)
        step2 = None
        if difficulty >= 7:
            step2 = self._kalman_step(
                step1["x_upd"], step1["p_upd"],
                f_val, b_val, u_val, q, h_val, r, z2,
            )

        return ("x' = Fx + Bu, \\quad P' = FPF + Q, \\quad"
                " K = P'H/(HP'H+R)"), {
            "F": f_val, "H": h_val, "B": b_val, "u": u_val,
            "Q": q, "R": r,
            "x0": x0, "P0": p0,
            "z1": z1, "z2": z2,
            "step1": step1, "step2": step2,
            "two_cycles": difficulty >= 7,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate Kalman filter computation steps.

        Args:
            data: Solution data with predictions and updates.

        Returns:
            List of step strings.
        """
        s1 = data["step1"]
        steps = [
            f"x0={_f(data['x0'])}, P0={_f(data['P0'])}",
            f"predict: x'={_f(s1['x_pred'])}, P'={_f(s1['p_pred'])}",
            f"K = {_f(s1['K'])}",
            f"update: x={_f(s1['x_upd'])}, P={_f(s1['p_upd'])}",
        ]
        if data["two_cycles"] and data["step2"]:
            s2 = data["step2"]
            steps.append(f"cycle2: x'={_f(s2['x_pred'])}, K={_f(s2['K'])}")
            steps.append(f"x={_f(s2['x_upd'])}, P={_f(s2['p_upd'])}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final state estimate.

        Args:
            data: Solution data.

        Returns:
            Updated state and covariance.
        """
        if data["two_cycles"] and data["step2"]:
            s = data["step2"]
            return f"x = {_f(s['x_upd'])}, P = {_f(s['p_upd'])}"
        s = data["step1"]
        return f"x = {_f(s['x_upd'])}, P = {_f(s['p_upd'])}"


# ===================================================================
# 6. MDP Policy (Value Iteration) (tier 6)
# ===================================================================

@register
class MdpPolicyGenerator(StepGenerator):
    """Compute optimal policy for a small MDP via value iteration.

    V(s) = max_a [R(s,a) + gamma * sum P(s'|s,a)*V(s')].
    Uses 3-4 states, 2 actions, and deterministic or simple stochastic
    transitions.

    Difficulty scaling:
        Difficulty 1-3: 3 states, deterministic transitions, gamma = 0.9.
        Difficulty 4-6: 3 states, stochastic transitions.
        Difficulty 7-8: 4 states, stochastic transitions.

    Prerequisites:
        bellman_equation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "mdp_policy"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["bellman_equation"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "compute optimal policy via value iteration"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a small MDP and run value iteration.

        Args:
            difficulty: Controls state count and transition type.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        n_states = 3 if difficulty <= 6 else 4
        n_actions = 2
        gamma = 0.9

        # Generate rewards R(s, a)
        rewards = {}
        for s in range(n_states):
            for a in range(n_actions):
                rewards[(s, a)] = round(self._rng.uniform(-2, 10), 2)

        # Generate transition probabilities P(s'|s, a)
        transitions: dict[tuple[int, int], dict[int, float]] = {}
        for s in range(n_states):
            for a in range(n_actions):
                if difficulty <= 3:
                    # Deterministic
                    next_s = self._rng.randint(0, n_states - 1)
                    probs = {ns: 0.0 for ns in range(n_states)}
                    probs[next_s] = 1.0
                else:
                    # Stochastic: split probability among 2 states
                    s1 = self._rng.randint(0, n_states - 1)
                    s2 = self._rng.randint(0, n_states - 1)
                    p1 = round(self._rng.uniform(0.3, 0.9), 2)
                    p2 = round(1.0 - p1, 2)
                    probs = {ns: 0.0 for ns in range(n_states)}
                    probs[s1] = round(probs[s1] + p1, 4)
                    probs[s2] = round(probs[s2] + p2, 4)
                transitions[(s, a)] = probs

        # Value iteration (limited iterations for compact output)
        v = [0.0] * n_states
        n_iter = 5
        iteration_log = []
        for it in range(n_iter):
            v_new = [0.0] * n_states
            for s in range(n_states):
                best_val = float("-inf")
                for a in range(n_actions):
                    q_val = rewards[(s, a)]
                    for s_prime in range(n_states):
                        q_val += gamma * transitions[(s, a)].get(s_prime, 0) * v[s_prime]
                    q_val = round(q_val, 4)
                    if q_val > best_val:
                        best_val = q_val
                v_new[s] = round(best_val, 4)
            v = v_new
            iteration_log.append(list(v))

        # Extract policy
        policy = []
        for s in range(n_states):
            best_a = 0
            best_val = float("-inf")
            for a in range(n_actions):
                q_val = rewards[(s, a)]
                for s_prime in range(n_states):
                    q_val += gamma * transitions[(s, a)].get(s_prime, 0) * v[s_prime]
                q_val = round(q_val, 4)
                if q_val > best_val:
                    best_val = q_val
                    best_a = a
            policy.append(best_a)

        return "V(s) = \\max_a \\left[R(s,a) + \\gamma \\sum P(s'|s,a) V(s')\\right]", {
            "n_states": n_states,
            "gamma": gamma,
            "rewards": {f"({s},{a})": rewards[(s, a)]
                        for s in range(n_states) for a in range(n_actions)},
            "V": [round(v_s, 4) for v_s in v],
            "policy": policy,
            "n_iter": n_iter,
            "last_iter": iteration_log[-1] if iteration_log else v,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate value iteration steps.

        Args:
            data: Solution data with value function and policy.

        Returns:
            List of step strings.
        """
        steps = [
            f"{data['n_states']} states, 2 actions, gamma={data['gamma']}",
            f"rewards: {data['rewards']}",
            f"after {data['n_iter']} iterations:",
            f"V = {[_f(v) for v in data['V']]}",
        ]
        policy_str = ", ".join(f"s{s}->a{data['policy'][s]}"
                               for s in range(data["n_states"]))
        steps.append(f"policy: {policy_str}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the optimal policy and value function.

        Args:
            data: Solution data.

        Returns:
            Policy mapping and converged values.
        """
        policy_str = ", ".join(f"s{s}:a{data['policy'][s]}"
                               for s in range(data["n_states"]))
        return f"policy = {{{policy_str}}}"
