"""Deep networking generators.

8 generators across tiers 4-5 covering TCP three-way handshake,
congestion avoidance, BGP routing, NAT translation, DHCP process,
WiFi throughput (Shannon), load balancing, and packet loss
retransmission.
"""
from __future__ import annotations

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


# ---------------------------------------------------------------------------
# 1. TCP Three-Way Handshake (tier 4)
# ---------------------------------------------------------------------------

@register
class TcpHandshakeGenerator(StepGenerator):
    """Trace the TCP three-way handshake sequence numbers.

    SYN(seq=x) -> SYN-ACK(seq=y, ack=x+1) -> ACK(seq=x+1, ack=y+1).
    Show the full sequence number exchange.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tcp_handshake"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace TCP three-way handshake sequence numbers"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a TCP handshake problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        max_seq = 1000 if difficulty <= 3 else 100000
        client_isn = self._rng.randint(100, max_seq)
        server_isn = self._rng.randint(100, max_seq)

        syn_seq = client_isn
        syn_ack_seq = server_isn
        syn_ack_ack = client_isn + 1
        ack_seq = client_isn + 1
        ack_ack = server_isn + 1

        steps = [
            f"1. Client -> SYN: seq={syn_seq}",
            f"2. Server -> SYN-ACK: seq={syn_ack_seq}, ack={syn_ack_ack}",
            f"3. Client -> ACK: seq={ack_seq}, ack={ack_ack}",
        ]

        if difficulty >= 5:
            data_len = self._rng.randint(100, 500)
            data_seq = ack_seq
            data_ack_num = data_seq + data_len
            steps.append(
                f"4. Client -> DATA: seq={data_seq}, len={data_len}"
            )
            steps.append(f"5. Server -> ACK: ack={data_ack_num}")

        problem = f"TCP handshake: client_ISN={client_isn}, server_ISN={server_isn}"
        return problem, {
            "steps": steps,
            "client_isn": client_isn,
            "server_isn": server_isn,
            "final_client_seq": ack_seq,
            "final_server_ack": ack_ack,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the handshake steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the final sequence state.

        Args:
            solution_data: All computed solution information.

        Returns:
            Sequence number summary string.
        """
        d = solution_data
        return (
            f"client_seq={d['final_client_seq']}, "
            f"server_ack={d['final_server_ack']}"
        )


# ---------------------------------------------------------------------------
# 2. Congestion Avoidance (tier 5)
# ---------------------------------------------------------------------------

@register
class CongestionAvoidanceGenerator(StepGenerator):
    """Simulate TCP AIMD congestion avoidance.

    Additive increase: cwnd += MSS/cwnd per ACK (approximately +1 MSS
    per RTT). After loss: cwnd = cwnd / 2. Show cwnd evolution over
    several rounds.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "congestion_avoidance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["division"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "simulate TCP AIMD congestion window over rounds"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a congestion avoidance problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        mss = self._rng.choice([1, 2])
        initial_cwnd = self._rng.randint(1, 4) * mss
        n_rounds = min(5 + difficulty, 10)
        loss_rounds = set()
        n_losses = min(1 + difficulty // 3, 3)
        for _ in range(n_losses):
            loss_rounds.add(self._rng.randint(2, n_rounds - 1))

        cwnd = float(initial_cwnd)
        steps = [f"MSS={mss}, initial cwnd={initial_cwnd}"]
        history = []

        for rnd in range(1, n_rounds + 1):
            if rnd in loss_rounds:
                old_cwnd = cwnd
                cwnd = round(cwnd / 2, 4)
                cwnd = max(cwnd, mss)
                steps.append(
                    f"round {rnd}: LOSS cwnd {_f(old_cwnd)}->{_f(cwnd)}"
                )
            else:
                cwnd = round(cwnd + mss, 4)
                steps.append(f"round {rnd}: cwnd={_f(cwnd)}")
            history.append({"round": rnd, "cwnd": cwnd})

        problem = (
            f"AIMD: MSS={mss}, cwnd0={initial_cwnd}, "
            f"loss_at={sorted(loss_rounds)}"
        )
        return problem, {
            "steps": steps,
            "history": history,
            "final_cwnd": cwnd,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the cwnd evolution steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the final congestion window.

        Args:
            solution_data: All computed solution information.

        Returns:
            Final cwnd string.
        """
        return f"final cwnd={_f(solution_data['final_cwnd'])}"


# ---------------------------------------------------------------------------
# 3. BGP Routing (tier 5)
# ---------------------------------------------------------------------------

@register
class BgpRoutingGenerator(StepGenerator):
    """Select the best BGP route from path attributes.

    Given multiple routes to a destination with AS-path length and
    local preference, apply BGP decision process to select the best.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "bgp_routing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "select best BGP route from path attributes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a BGP route selection problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_routes = min(2 + difficulty // 2, 5)
        routes = []
        for i in range(n_routes):
            local_pref = self._rng.choice([80, 100, 120, 150, 200])
            as_path_len = self._rng.randint(1, 5)
            as_path = [self._rng.randint(100, 999) for _ in range(as_path_len)]
            med = self._rng.randint(0, 200)
            routes.append({
                "id": f"R{i}",
                "local_pref": local_pref,
                "as_path": as_path,
                "as_path_len": as_path_len,
                "med": med,
            })

        steps = []
        for r in routes:
            steps.append(
                f"{r['id']}: LP={r['local_pref']}, "
                f"AS-path={r['as_path']}(len={r['as_path_len']}), "
                f"MED={r['med']}"
            )

        best = max(routes, key=lambda r: r["local_pref"])
        tied = [r for r in routes if r["local_pref"] == best["local_pref"]]
        if len(tied) > 1:
            best = min(tied, key=lambda r: r["as_path_len"])
            steps.append(f"tie on LP={best['local_pref']}, use shortest AS-path")

        steps.append(f"best route: {best['id']}")

        routes_str = "; ".join(
            f"{r['id']}(LP={r['local_pref']},ASlen={r['as_path_len']})"
            for r in routes
        )
        problem = f"BGP: [{routes_str}]"
        return problem, {
            "steps": steps,
            "best": best["id"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the BGP decision steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the selected route.

        Args:
            solution_data: All computed solution information.

        Returns:
            Best route identifier.
        """
        return f"best={solution_data['best']}"


# ---------------------------------------------------------------------------
# 4. NAT Translation (tier 4)
# ---------------------------------------------------------------------------

@register
class NatTranslationGenerator(StepGenerator):
    """Translate internal IP:port to external via NAT table.

    Given internal address, NAT table mappings, and external pool,
    show the address translation and reverse translation.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "nat_translation"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "translate internal address through NAT table"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a NAT translation problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        ext_ip = f"203.0.113.{self._rng.randint(1, 254)}"
        n_entries = min(2 + difficulty // 2, 5)
        nat_table: list[dict] = []
        used_ext_ports: set[int] = set()

        for i in range(n_entries):
            int_ip = f"192.168.1.{10 + i}"
            int_port = self._rng.randint(1024, 65000)
            ext_port = self._rng.randint(10000, 60000)
            while ext_port in used_ext_ports:
                ext_port = self._rng.randint(10000, 60000)
            used_ext_ports.add(ext_port)
            nat_table.append({
                "int_ip": int_ip,
                "int_port": int_port,
                "ext_ip": ext_ip,
                "ext_port": ext_port,
            })

        query_idx = self._rng.randint(0, len(nat_table) - 1)
        query = nat_table[query_idx]

        steps = [f"NAT external IP: {ext_ip}"]
        for entry in nat_table:
            steps.append(
                f"{entry['int_ip']}:{entry['int_port']} <-> "
                f"{entry['ext_ip']}:{entry['ext_port']}"
            )

        steps.append(
            f"outgoing from {query['int_ip']}:{query['int_port']} -> "
            f"{query['ext_ip']}:{query['ext_port']}"
        )
        steps.append(
            f"incoming to {query['ext_ip']}:{query['ext_port']} -> "
            f"{query['int_ip']}:{query['int_port']}"
        )

        problem = (
            f"NAT: query {query['int_ip']}:{query['int_port']}, "
            f"ext={ext_ip}"
        )
        return problem, {
            "steps": steps,
            "ext_addr": f"{query['ext_ip']}:{query['ext_port']}",
            "int_addr": f"{query['int_ip']}:{query['int_port']}",
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the NAT translation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the translated address.

        Args:
            solution_data: All computed solution information.

        Returns:
            NAT mapping string.
        """
        d = solution_data
        return f"{d['int_addr']} <-> {d['ext_addr']}"


# ---------------------------------------------------------------------------
# 5. DHCP Process (tier 4)
# ---------------------------------------------------------------------------

@register
class DhcpProcessGenerator(StepGenerator):
    """Trace the DHCP DORA process.

    Discover -> Offer -> Request -> Acknowledge. Given a server
    pool and client MAC, show the address allocation steps.
    """

    _TEMPLATES = [
        {
            "server_ip": "10.0.0.1",
            "pool_start": "10.0.0.100",
            "pool_end": "10.0.0.200",
            "subnet": "255.255.255.0",
            "lease": 3600,
            "gateway": "10.0.0.1",
            "dns": "8.8.8.8",
        },
        {
            "server_ip": "192.168.1.1",
            "pool_start": "192.168.1.50",
            "pool_end": "192.168.1.150",
            "subnet": "255.255.255.0",
            "lease": 7200,
            "gateway": "192.168.1.1",
            "dns": "1.1.1.1",
        },
        {
            "server_ip": "172.16.0.1",
            "pool_start": "172.16.0.10",
            "pool_end": "172.16.0.50",
            "subnet": "255.255.0.0",
            "lease": 1800,
            "gateway": "172.16.0.1",
            "dns": "8.8.4.4",
        },
        {
            "server_ip": "10.10.10.1",
            "pool_start": "10.10.10.100",
            "pool_end": "10.10.10.200",
            "subnet": "255.255.255.0",
            "lease": 86400,
            "gateway": "10.10.10.1",
            "dns": "9.9.9.9",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dhcp_process"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["comparison"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace DHCP DORA address allocation"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DHCP process trace problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]

        mac_parts = [
            f"{self._rng.randint(0, 255):02x}" for _ in range(6)
        ]
        client_mac = ":".join(mac_parts)

        pool_start_parts = [int(x) for x in tmpl["pool_start"].split(".")]
        offset = self._rng.randint(0, 20)
        offered_ip_parts = list(pool_start_parts)
        offered_ip_parts[3] += offset
        offered_ip = ".".join(str(x) for x in offered_ip_parts)

        steps = [
            f"1. DISCOVER: client {client_mac} broadcasts",
            f"2. OFFER: server {tmpl['server_ip']} offers {offered_ip}",
            f"   subnet={tmpl['subnet']}, gw={tmpl['gateway']}, dns={tmpl['dns']}",
            f"3. REQUEST: client requests {offered_ip}",
            f"4. ACK: server confirms {offered_ip}, lease={tmpl['lease']}s",
        ]

        problem = f"DHCP: client={client_mac}, server={tmpl['server_ip']}"
        return problem, {
            "steps": steps,
            "offered_ip": offered_ip,
            "lease": tmpl["lease"],
            "client_mac": client_mac,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the DORA steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the allocated address.

        Args:
            solution_data: All computed solution information.

        Returns:
            DHCP allocation result.
        """
        d = solution_data
        return f"assigned {d['offered_ip']}, lease={d['lease']}s"


# ---------------------------------------------------------------------------
# 6. WiFi Throughput - Shannon (tier 5)
# ---------------------------------------------------------------------------

@register
class WifiThroughputGenerator(StepGenerator):
    """Compute WiFi throughput using the Shannon capacity formula.

    C = B * log2(1 + SNR). Given bandwidth B and signal-to-noise
    ratio (or distance-based path loss), compute channel capacity.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "wifi_throughput"

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
            Task instruction string.
        """
        return "compute WiFi throughput using Shannon capacity"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a WiFi throughput problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        bw_mhz = self._rng.choice([20, 40, 80, 160])
        bw_hz = bw_mhz * 1e6

        if difficulty >= 5:
            distance_m = self._rng.randint(5, 50)
            freq_ghz = self._rng.choice([2.4, 5.0])
            path_loss_db = round(
                20 * math.log10(distance_m)
                + 20 * math.log10(freq_ghz * 1e9)
                - 147.55,
                4
            )
            tx_power_dbm = self._rng.choice([20, 23, 27])
            noise_dbm = -90
            signal_dbm = round(tx_power_dbm - path_loss_db, 4)
            snr_db = round(signal_dbm - noise_dbm, 4)
            snr_linear = round(10 ** (snr_db / 10), 4)

            steps = [
                f"B={bw_mhz} MHz, freq={freq_ghz} GHz, dist={distance_m}m",
                f"path_loss={_f(path_loss_db)} dB",
                f"signal={tx_power_dbm}-{_f(path_loss_db)}={_f(signal_dbm)} dBm",
                f"SNR={_f(signal_dbm)}-({noise_dbm})={_f(snr_db)} dB",
                f"SNR_linear={_f(snr_linear)}",
            ]
        else:
            snr_db = self._rng.choice([10, 15, 20, 25, 30])
            snr_linear = round(10 ** (snr_db / 10), 4)
            steps = [
                f"B={bw_mhz} MHz, SNR={snr_db} dB",
                f"SNR_linear={_f(snr_linear)}",
            ]

        capacity_bps = round(bw_hz * math.log2(1 + snr_linear), 4)
        capacity_mbps = round(capacity_bps / 1e6, 4)

        steps.append(
            f"C = {bw_mhz}e6 * log2(1+{_f(snr_linear)}) = {_f(capacity_mbps)} Mbps"
        )

        problem = f"Shannon: B={bw_mhz}MHz, SNR={_f(snr_db)}dB"
        return problem, {
            "steps": steps,
            "capacity_mbps": capacity_mbps,
            "snr_db": snr_db,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the Shannon computation steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the channel capacity.

        Args:
            solution_data: All computed solution information.

        Returns:
            Capacity in Mbps.
        """
        return f"capacity={_f(solution_data['capacity_mbps'])} Mbps"


# ---------------------------------------------------------------------------
# 7. Load Balancing (tier 4)
# ---------------------------------------------------------------------------

@register
class LoadBalancingGenerator(StepGenerator):
    """Distribute requests across servers using balancing algorithms.

    Round-robin, weighted round-robin, and least connections.
    Given server weights and request sequence, show distribution.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "load_balancing"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "distribute requests using load balancing algorithm"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a load balancing problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_servers = min(2 + difficulty // 2, 5)
        n_requests = min(6 + difficulty, 12)
        algo = self._rng.choice(["round-robin", "weighted-rr", "least-conn"])

        weights = [self._rng.randint(1, 5) for _ in range(n_servers)]
        servers = [f"S{i}" for i in range(n_servers)]
        counts = {s: 0 for s in servers}
        assignments = []
        steps = [f"algo={algo}, servers={servers}"]

        if algo == "round-robin":
            for req in range(n_requests):
                target = servers[req % n_servers]
                counts[target] += 1
                assignments.append(target)
                steps.append(f"req{req}: -> {target}")

        elif algo == "weighted-rr":
            steps.append(f"weights={weights}")
            expanded = []
            for i, s in enumerate(servers):
                expanded.extend([s] * weights[i])
            idx = 0
            for req in range(n_requests):
                target = expanded[idx % len(expanded)]
                counts[target] += 1
                assignments.append(target)
                steps.append(f"req{req}: -> {target}")
                idx += 1

        else:
            active = {s: 0 for s in servers}
            for req in range(n_requests):
                target = min(servers, key=lambda s: active[s])
                active[target] += 1
                counts[target] += 1
                assignments.append(target)
                steps.append(f"req{req}: -> {target} (active={active[target]})")
                if self._rng.random() < 0.3 and any(v > 0 for v in active.values()):
                    done_server = self._rng.choice(
                        [s for s in servers if active[s] > 0]
                    )
                    active[done_server] -= 1

        steps.append(f"distribution: {dict(counts)}")

        problem = f"{algo}: {n_servers} servers, {n_requests} requests"
        return problem, {
            "steps": steps,
            "counts": counts,
            "assignments": assignments,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the distribution steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the load distribution.

        Args:
            solution_data: All computed solution information.

        Returns:
            Server count distribution string.
        """
        parts = [f"{s}={c}" for s, c in solution_data["counts"].items()]
        return ", ".join(parts)


# ---------------------------------------------------------------------------
# 8. Packet Loss Retransmission (tier 5)
# ---------------------------------------------------------------------------

@register
class PacketLossRetransmitGenerator(StepGenerator):
    """Compare Go-Back-N and Selective Repeat retransmission.

    Go-Back-N: one loss triggers retransmission of N packets from
    the lost one. Selective Repeat: only the lost packet is
    retransmitted. Compare total transmissions and throughput.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "packet_loss_retransmit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compare Go-Back-N and Selective Repeat retransmission"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a retransmission comparison problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        window_size = self._rng.randint(4, min(4 + difficulty * 2, 16))
        total_packets = self._rng.randint(window_size + 2, window_size * 3)
        n_losses = self._rng.randint(1, min(1 + difficulty // 2, 3))
        loss_positions = sorted(
            self._rng.sample(range(total_packets), n_losses)
        )

        gbn_total = total_packets
        for loss_pos in loss_positions:
            remaining_in_window = min(window_size, total_packets - loss_pos)
            gbn_total += remaining_in_window

        sr_total = total_packets + n_losses

        gbn_efficiency = round(total_packets / gbn_total, 4)
        sr_efficiency = round(total_packets / sr_total, 4)

        steps = [
            f"window={window_size}, packets={total_packets}, losses at {loss_positions}",
        ]
        steps.append(
            f"Go-Back-N: retransmit window from each loss, "
            f"total={gbn_total} transmissions"
        )
        steps.append(
            f"Selective Repeat: retransmit only lost, "
            f"total={sr_total} transmissions"
        )
        steps.append(f"GBN efficiency={_f(gbn_efficiency)}")
        steps.append(f"SR efficiency={_f(sr_efficiency)}")

        problem = (
            f"retransmit: W={window_size}, "
            f"packets={total_packets}, loss={loss_positions}"
        )
        return problem, {
            "steps": steps,
            "gbn_total": gbn_total,
            "sr_total": sr_total,
            "gbn_efficiency": gbn_efficiency,
            "sr_efficiency": sr_efficiency,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the retransmission comparison steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the efficiency comparison.

        Args:
            solution_data: All computed solution information.

        Returns:
            Efficiency comparison string.
        """
        d = solution_data
        return (
            f"GBN: {d['gbn_total']} tx (eff={_f(d['gbn_efficiency'])}), "
            f"SR: {d['sr_total']} tx (eff={_f(d['sr_efficiency'])})"
        )
