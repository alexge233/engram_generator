"""Networking task generators.

4 generators covering TCP window throughput, routing table longest
prefix match, CRC polynomial check, and network delay computation.
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
# 1. TCP Window Throughput (tier 5)
# ===================================================================

@register
class TcpWindowGenerator(StepGenerator):
    """Compute TCP throughput from window size and RTT.

    Throughput = window_size / RTT. With packet loss at high difficulty:
    W = sqrt(1.5 / loss_rate) * MSS, then throughput = W / RTT.

    Difficulty scaling:
        Difficulty 1-3: simple W (bytes) and RTT (ms), direct division.
        Difficulty 4-6: larger window, convert to Mbps.
        Difficulty 7-8: given loss rate, compute effective window first.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tcp_window"

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
            return "compute TCP throughput with packet loss"
        return "compute TCP throughput from window size and RTT"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate TCP parameters and compute throughput.

        Args:
            difficulty: Controls parameter ranges and variant.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            w_bytes = self._rng.choice([4096, 8192, 16384, 32768])
            rtt_ms = float(self._rng.randint(10, 100))
            mode = "direct"
            loss_rate = 0.0
            mss = 0
        elif difficulty <= 6:
            w_bytes = self._rng.choice([32768, 65536, 131072, 262144])
            rtt_ms = round(self._rng.uniform(5, 200), 1)
            mode = "mbps"
            loss_rate = 0.0
            mss = 0
        else:
            mss = self._rng.choice([536, 1460])
            loss_rate = round(self._rng.uniform(0.0001, 0.01), 4)
            w_bytes = round(math.sqrt(1.5 / loss_rate) * mss, 4)
            rtt_ms = round(self._rng.uniform(10, 200), 1)
            mode = "loss"

        rtt_s = round(rtt_ms / 1000.0, 6)
        throughput_bps = round(w_bytes / rtt_s, 4) if rtt_s > 0 else 0.0
        throughput_mbps = round(throughput_bps * 8.0 / 1e6, 4)

        if mode == "direct":
            problem = (
                f"\\text{{TCP}}: W={w_bytes} B, "
                f"RTT={_f(rtt_ms)} ms"
            )
        elif mode == "mbps":
            problem = (
                f"\\text{{TCP}}: W={w_bytes} B, "
                f"RTT={_f(rtt_ms)} ms"
            )
        else:
            problem = (
                f"\\text{{TCP}}: MSS={mss} B, "
                f"loss={loss_rate}, RTT={_f(rtt_ms)} ms"
            )

        return problem, {
            "w_bytes": w_bytes, "rtt_ms": rtt_ms, "rtt_s": rtt_s,
            "throughput_bps": throughput_bps,
            "throughput_mbps": throughput_mbps,
            "mode": mode, "loss_rate": loss_rate, "mss": mss,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate TCP throughput computation steps.

        Args:
            data: Solution data with TCP parameters.

        Returns:
            List of step strings.
        """
        steps = []
        if data["mode"] == "loss":
            steps.append(f"MSS = {data['mss']} B, loss = {data['loss_rate']}")
            steps.append(
                f"W = sqrt(1.5/{data['loss_rate']})*{data['mss']} "
                f"= {_f(data['w_bytes'])} B"
            )
        else:
            steps.append(f"W = {_f(data['w_bytes'])} B")
        steps.append(f"RTT = {_f(data['rtt_ms'])} ms = {data['rtt_s']} s")
        steps.append(
            f"throughput = {_f(data['w_bytes'])}/{data['rtt_s']} "
            f"= {_f(data['throughput_bps'])} B/s"
        )
        steps.append(
            f"throughput = {_f(data['throughput_bps'])}*8/1e6 "
            f"= {_f(data['throughput_mbps'])} Mbps"
        )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the throughput.

        Args:
            data: Solution data.

        Returns:
            Throughput in Mbps.
        """
        return f"throughput = {_f(data['throughput_mbps'])} Mbps"


# ===================================================================
# 2. Routing Table (tier 4)
# ===================================================================

@register
class RoutingTableGenerator(StepGenerator):
    """Determine next hop by longest prefix match on a routing table.

    Given a routing table with destination/mask/next_hop entries and
    a target IP, find the matching entry with the longest prefix.

    Difficulty scaling:
        Difficulty 1-3: 2 routes, /8 and /16 masks.
        Difficulty 4-6: 3 routes, /16 and /24 masks.
        Difficulty 7-8: 4 routes, /24 and /28 masks.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "routing_table"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        return "find next hop using longest prefix match"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate routing table and target IP.

        Args:
            difficulty: Controls number of routes and mask lengths.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            routes = [
                {"dest": "10.0.0.0", "mask": 8, "hop": "R1"},
                {"dest": "10.1.0.0", "mask": 16, "hop": "R2"},
            ]
            target = f"10.1.{self._rng.randint(0, 255)}.{self._rng.randint(1, 254)}"
            best_hop = "R2"
            best_mask = 16
        elif difficulty <= 6:
            octet2 = self._rng.randint(0, 255)
            routes = [
                {"dest": "192.168.0.0", "mask": 16, "hop": "R1"},
                {"dest": f"192.168.{octet2}.0", "mask": 24, "hop": "R2"},
                {"dest": "0.0.0.0", "mask": 0, "hop": "R3"},
            ]
            target = f"192.168.{octet2}.{self._rng.randint(1, 254)}"
            best_hop = "R2"
            best_mask = 24
        else:
            octet2 = self._rng.randint(0, 255)
            octet3 = self._rng.randint(1, 15) * 16
            routes = [
                {"dest": "172.16.0.0", "mask": 12, "hop": "R1"},
                {"dest": f"172.16.{octet2}.0", "mask": 24, "hop": "R2"},
                {"dest": f"172.16.{octet2}.{octet3}", "mask": 28, "hop": "R3"},
                {"dest": "0.0.0.0", "mask": 0, "hop": "R4"},
            ]
            host = octet3 + self._rng.randint(1, 14)
            target = f"172.16.{octet2}.{host}"
            best_hop = "R3"
            best_mask = 28

        route_strs = [
            f"{r['dest']}/{r['mask']}->{r['hop']}" for r in routes
        ]
        problem = (
            f"\\text{{Route table}}: [{', '.join(route_strs)}], "
            f"IP={target}"
        )
        return problem, {
            "routes": routes, "target": target,
            "best_hop": best_hop, "best_mask": best_mask,
        }

    def _create_steps(self, data: dict) -> list[str]:
        """Generate routing lookup steps.

        Args:
            data: Solution data with routing table.

        Returns:
            List of step strings.
        """
        steps = [f"target IP = {data['target']}"]
        for r in data["routes"]:
            match = self._check_match(data["target"], r["dest"], r["mask"])
            status = "MATCH" if match else "no match"
            steps.append(
                f"{r['dest']}/{r['mask']} -> {status}"
            )
        steps.append(
            f"longest prefix = /{data['best_mask']} -> {data['best_hop']}"
        )
        return steps

    def _check_match(self, target: str, dest: str, mask: int) -> bool:
        """Check if target IP matches destination with given mask.

        Args:
            target: Target IP address string.
            dest: Destination network address string.
            mask: CIDR prefix length.

        Returns:
            True if target matches the route.
        """
        target_int = self._ip_to_int(target)
        dest_int = self._ip_to_int(dest)
        if mask == 0:
            return True
        mask_int = (0xFFFFFFFF << (32 - mask)) & 0xFFFFFFFF
        return (target_int & mask_int) == (dest_int & mask_int)

    def _ip_to_int(self, ip: str) -> int:
        """Convert dotted IP string to integer.

        Args:
            ip: IP address in dotted notation.

        Returns:
            32-bit integer representation.
        """
        parts = [int(x) for x in ip.split(".")]
        return (parts[0] << 24) | (parts[1] << 16) | (parts[2] << 8) | parts[3]

    def _create_answer(self, data: dict) -> str:
        """Return the selected next hop.

        Args:
            data: Solution data.

        Returns:
            Next hop identifier.
        """
        return f"next_hop = {data['best_hop']} (/{data['best_mask']})"


# ===================================================================
# 3. CRC Check (tier 5)
# ===================================================================

@register
class CrcCheckGenerator(StepGenerator):
    """Compute CRC by polynomial division mod 2.

    Given data bits and a generator polynomial, append zeros and
    perform XOR-based polynomial long division to find the remainder.
    Verify a received message by checking if the remainder is zero.

    Difficulty scaling:
        Difficulty 1-3: 4-bit data, 3-bit generator.
        Difficulty 4-6: 6-bit data, 4-bit generator.
        Difficulty 7-8: 8-bit data, 5-bit generator, verify received.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crc_check"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite tasks."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute CRC and verify received message"
        return "compute CRC remainder using polynomial division"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate data and generator polynomial for CRC.

        Args:
            difficulty: Controls bit lengths.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        if difficulty <= 3:
            data_len = 4
            gen_len = 3
        elif difficulty <= 6:
            data_len = 6
            gen_len = 4
        else:
            data_len = 8
            gen_len = 5

        data_bits = [self._rng.randint(0, 1) for _ in range(data_len)]
        if all(b == 0 for b in data_bits):
            data_bits[0] = 1
        gen_bits = [1] + [self._rng.randint(0, 1) for _ in range(gen_len - 2)] + [1]

        remainder = self._compute_crc(data_bits, gen_bits)
        codeword = data_bits + remainder

        data_str = "".join(str(b) for b in data_bits)
        gen_str = "".join(str(b) for b in gen_bits)
        rem_str = "".join(str(b) for b in remainder)
        code_str = "".join(str(b) for b in codeword)

        problem = f"\\text{{CRC}}: data={data_str}, gen={gen_str}"

        return problem, {
            "data_bits": data_bits, "gen_bits": gen_bits,
            "remainder": remainder, "codeword": codeword,
            "data_str": data_str, "gen_str": gen_str,
            "rem_str": rem_str, "code_str": code_str,
            "verify": difficulty >= 7,
        }

    def _compute_crc(self, data: list[int], gen: list[int]) -> list[int]:
        """Compute CRC remainder by XOR polynomial division.

        Args:
            data: Data bits.
            gen: Generator polynomial bits.

        Returns:
            Remainder bits.
        """
        r = len(gen) - 1
        padded = data + [0] * r
        work = list(padded)

        for i in range(len(data)):
            if work[i] == 1:
                for j in range(len(gen)):
                    work[i + j] ^= gen[j]

        return work[len(data):]

    def _create_steps(self, data: dict) -> list[str]:
        """Generate CRC computation steps.

        Args:
            data: Solution data with bits and remainder.

        Returns:
            List of step strings.
        """
        r = len(data["gen_bits"]) - 1
        steps = [
            f"data = {data['data_str']}",
            f"generator = {data['gen_str']} (degree {r})",
            f"append {r} zeros: {data['data_str']}{'0'*r}",
            f"XOR division mod 2",
            f"remainder = {data['rem_str']}",
            f"codeword = {data['code_str']}",
        ]
        if data["verify"]:
            verify_rem = self._compute_crc(data["codeword"], data["gen_bits"])
            verify_str = "".join(str(b) for b in verify_rem)
            is_valid = all(b == 0 for b in verify_rem)
            steps.append(
                f"verify: remainder of codeword = {verify_str} "
                f"({'valid' if is_valid else 'error'})"
            )
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the CRC remainder and codeword.

        Args:
            data: Solution data.

        Returns:
            CRC remainder string.
        """
        return f"CRC = {data['rem_str']}, codeword = {data['code_str']}"


# ===================================================================
# 4. Network Delay (tier 4)
# ===================================================================

@register
class NetworkDelayGenerator(StepGenerator):
    """Compute total network delay from its components.

    Total delay = transmission (L/R) + propagation (d/s) + queuing
    + processing. Given packet size L, link rate R, distance d, and
    propagation speed s, compute each component and the total.

    Difficulty scaling:
        Difficulty 1-3: only transmission + propagation, simple values.
        Difficulty 4-6: all four components, realistic values.
        Difficulty 7-8: compare delays for two different packet sizes.

    Prerequisites:
        division.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "network_delay"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

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
            return "compare network delays for different packet sizes"
        return "compute total network delay"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate network parameters and compute delays.

        Args:
            difficulty: Controls which delay components are included.

        Returns:
            Tuple of (latex_formula, solution_data).
        """
        l_bits = self._rng.choice([500, 1000, 1500, 4000, 8000]) * 8
        r_bps = self._rng.choice([1e6, 10e6, 100e6, 1e9])
        d_km = float(self._rng.randint(1, 5000))
        s_mps = 2e8

        transmission = round(l_bits / r_bps, 6)
        propagation = round((d_km * 1000) / s_mps, 6)

        if difficulty <= 3:
            queuing = 0.0
            processing = 0.0
        else:
            queuing = round(self._rng.uniform(0.0001, 0.005), 6)
            processing = round(self._rng.uniform(0.00001, 0.001), 6)

        total = round(transmission + propagation + queuing + processing, 6)
        total_ms = round(total * 1000, 4)

        r_label = self._format_rate(r_bps)
        problem = (
            f"\\text{{Delay}}: L={l_bits} bits, "
            f"R={r_label}, d={_f(d_km)} km"
        )
        if difficulty >= 4:
            problem += (
                f", q={round(queuing*1000, 4)} ms, "
                f"p={round(processing*1000, 4)} ms"
            )

        return problem, {
            "l_bits": l_bits, "r_bps": r_bps, "d_km": d_km,
            "transmission": transmission, "propagation": propagation,
            "queuing": queuing, "processing": processing,
            "total": total, "total_ms": total_ms,
            "r_label": r_label,
        }

    def _format_rate(self, r_bps: float) -> str:
        """Format link rate with appropriate unit.

        Args:
            r_bps: Rate in bits per second.

        Returns:
            Human-readable rate string.
        """
        if r_bps >= 1e9:
            return f"{_f(r_bps/1e9)} Gbps"
        if r_bps >= 1e6:
            return f"{_f(r_bps/1e6)} Mbps"
        return f"{_f(r_bps/1e3)} Kbps"

    def _create_steps(self, data: dict) -> list[str]:
        """Generate delay component computation steps.

        Args:
            data: Solution data with network parameters.

        Returns:
            List of step strings.
        """
        trans_ms = round(data["transmission"] * 1000, 4)
        prop_ms = round(data["propagation"] * 1000, 4)
        steps = [
            f"L = {data['l_bits']} bits, R = {data['r_label']}",
            f"transmission = L/R = {data['l_bits']}/{_f(data['r_bps'])} = {_f(trans_ms)} ms",
            f"propagation = d/s = {_f(data['d_km']*1000)}/{_f(2e8)} = {_f(prop_ms)} ms",
        ]
        if data["queuing"] > 0 or data["processing"] > 0:
            steps.append(f"queuing = {_f(round(data['queuing']*1000, 4))} ms")
            steps.append(f"processing = {_f(round(data['processing']*1000, 4))} ms")
        steps.append(f"total = {_f(data['total_ms'])} ms")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the total delay.

        Args:
            data: Solution data.

        Returns:
            Total delay in ms.
        """
        return f"total delay = {_f(data['total_ms'])} ms"
