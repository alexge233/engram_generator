"""Extended networking task generators.

6 generators across tiers 4-5 covering IP subnetting, ARP resolution,
DNS resolution, TCP congestion control, internet checksum computation,
and sliding window (Go-back-N) protocol.
"""

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. IP Subnetting (tier 4)
# ---------------------------------------------------------------------------

@register
class IPSubnettingGenerator(StepGenerator):
    """Compute network address, broadcast, and host count from IP and mask.

    Given an IP address and subnet mask (or CIDR prefix), compute the
    network address, broadcast address, and number of usable hosts.
    VLSM calculations at higher difficulty.

    Difficulty scaling:
        Difficulty 1-3: /24 or /16 subnets, class C.
        Difficulty 4-6: /20 to /28 subnets.
        Difficulty 7-8: /29 to /30 subnets (small), VLSM.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "ip_subnetting"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "compute subnet details for small VLSM subnet"
        return "compute network address, broadcast, and host count"

    def _ip_to_int(self, octets: list[int]) -> int:
        """Convert IP octets to 32-bit integer.

        Args:
            octets: List of 4 octets (0-255 each).

        Returns:
            32-bit integer representation.
        """
        return (octets[0] << 24) | (octets[1] << 16) | (octets[2] << 8) | octets[3]

    def _int_to_ip(self, val: int) -> str:
        """Convert 32-bit integer to dotted-decimal IP.

        Args:
            val: 32-bit integer.

        Returns:
            Dotted-decimal string.
        """
        return f"{(val >> 24) & 0xFF}.{(val >> 16) & 0xFF}.{(val >> 8) & 0xFF}.{val & 0xFF}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an IP subnetting problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            prefix = self._rng.choice([16, 24])
            octets = [
                self._rng.randint(10, 192),
                self._rng.randint(0, 255),
                self._rng.randint(0, 255),
                self._rng.randint(1, 254),
            ]
        elif difficulty <= 6:
            prefix = self._rng.choice([20, 22, 24, 26, 28])
            octets = [
                self._rng.randint(10, 223),
                self._rng.randint(0, 255),
                self._rng.randint(0, 255),
                self._rng.randint(1, 254),
            ]
        else:
            prefix = self._rng.choice([29, 30])
            octets = [
                self._rng.randint(10, 223),
                self._rng.randint(0, 255),
                self._rng.randint(0, 255),
                self._rng.randint(1, 254),
            ]

        ip_int = self._ip_to_int(octets)
        mask_int = (0xFFFFFFFF << (32 - prefix)) & 0xFFFFFFFF
        network_int = ip_int & mask_int
        broadcast_int = network_int | (~mask_int & 0xFFFFFFFF)
        host_bits = 32 - prefix
        num_hosts = max(0, (2 ** host_bits) - 2)

        ip_str = self._int_to_ip(ip_int)
        mask_str = self._int_to_ip(mask_int)
        network_str = self._int_to_ip(network_int)
        broadcast_str = self._int_to_ip(broadcast_int)

        return (
            f"IP: {ip_str}/{prefix}",
            {"ip": ip_str, "prefix": prefix, "mask": mask_str,
             "network": network_str, "broadcast": broadcast_str,
             "num_hosts": num_hosts, "host_bits": host_bits},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for IP subnetting.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing mask, network, broadcast, and host count.
        """
        return [
            f"subnet mask: /{data['prefix']} = {data['mask']}",
            f"network: {data['ip']} AND {data['mask']} = {data['network']}",
            f"broadcast: {data['network']} OR NOT({data['mask']}) = {data['broadcast']}",
            f"host bits: {data['host_bits']}, usable hosts: 2^{data['host_bits']}-2 = {data['num_hosts']}",
        ]

    def _create_answer(self, data: dict) -> str:
        """Return the subnet details.

        Args:
            data: Solution data dict.

        Returns:
            Network, broadcast, and host count as a string.
        """
        return f"net={data['network']}, bcast={data['broadcast']}, hosts={data['num_hosts']}"


# ---------------------------------------------------------------------------
# 2. ARP Resolution (tier 4)
# ---------------------------------------------------------------------------

@register
class ARPResolutionGenerator(StepGenerator):
    """Simulate ARP table lookup and broadcast request/reply.

    Given an IP address and an ARP cache, determine if a MAC address
    is cached. If not, show the ARP broadcast request and unicast reply.
    Template-based with small ARP tables.

    Difficulty scaling:
        Difficulty 1-3: 3-entry ARP table, target is cached.
        Difficulty 4-6: 4-entry table, target may not be cached.
        Difficulty 7-8: 5-entry table, target not cached, show full exchange.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "arp_resolution"

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
            Short task description.
        """
        return "resolve IP to MAC address using ARP"

    def _random_mac(self) -> str:
        """Generate a random MAC address string.

        Returns:
            MAC address in colon-separated hex format.
        """
        octets = [self._rng.randint(0, 255) for _ in range(6)]
        return ":".join(f"{o:02x}" for o in octets)

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an ARP resolution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            table_size = 3
            cached = True
        elif difficulty <= 6:
            table_size = 4
            cached = self._rng.choice([True, False])
        else:
            table_size = 5
            cached = False

        base_ip = f"192.168.1."
        arp_table = {}
        for i in range(table_size):
            ip = f"{base_ip}{10 + i}"
            arp_table[ip] = self._random_mac()

        if cached:
            target_ip = self._rng.choice(list(arp_table.keys()))
            target_mac = arp_table[target_ip]
            action = "cache hit"
        else:
            target_ip = f"{base_ip}{10 + table_size}"
            target_mac = self._random_mac()
            action = "broadcast ARP request"

        sender_ip = f"{base_ip}{10 + table_size + 1}"
        sender_mac = self._random_mac()

        table_str = ", ".join(f"{ip}->{mac}" for ip, mac in arp_table.items())

        return (
            f"ARP: resolve {target_ip}, table=[{table_str}]",
            {"target_ip": target_ip, "target_mac": target_mac,
             "sender_ip": sender_ip, "sender_mac": sender_mac,
             "arp_table": arp_table, "cached": cached, "action": action},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for ARP resolution.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing lookup, request, and reply.
        """
        steps = [f"lookup {data['target_ip']} in ARP cache"]
        if data["cached"]:
            steps.append(f"cache hit: {data['target_ip']} -> {data['target_mac']}")
        else:
            steps.append(f"cache miss: {data['target_ip']} not found")
            steps.append(
                f"broadcast: who-has {data['target_ip']}? tell {data['sender_ip']}"
            )
            steps.append(
                f"reply: {data['target_ip']} is-at {data['target_mac']}"
            )
            steps.append(f"update cache: {data['target_ip']} -> {data['target_mac']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the resolved MAC address.

        Args:
            data: Solution data dict.

        Returns:
            IP to MAC mapping as a string.
        """
        return f"{data['target_ip']} -> {data['target_mac']} ({data['action']})"


# ---------------------------------------------------------------------------
# 3. DNS Resolution (tier 4)
# ---------------------------------------------------------------------------

@register
class DNSResolutionGenerator(StepGenerator):
    """Simulate iterative DNS resolution query chain.

    Show the query path: local resolver -> root server -> TLD server
    -> authoritative server for a domain name. Template-based.

    Difficulty scaling:
        Difficulty 1-3: 2-level domain (example.com).
        Difficulty 4-6: 3-level domain (sub.example.com).
        Difficulty 7-8: 4-level domain with CNAME.

    Prerequisites:
        comparison.
    """

    _TLDS = ["com", "org", "net", "edu", "io"]
    _DOMAINS = ["example", "alpha", "beta", "gamma", "delta",
                "omega", "sigma", "lambda", "kappa"]
    _SUBS = ["www", "mail", "api", "cdn", "dev", "app"]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "dns_resolution"

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
            Short task description.
        """
        return "trace iterative DNS resolution for domain name"

    def _random_ip(self) -> str:
        """Generate a random public IP address.

        Returns:
            Dotted-decimal IP string.
        """
        return f"{self._rng.randint(1, 223)}.{self._rng.randint(0, 255)}.{self._rng.randint(0, 255)}.{self._rng.randint(1, 254)}"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a DNS resolution problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        tld = self._rng.choice(self._TLDS)
        domain = self._rng.choice(self._DOMAINS)

        if difficulty <= 3:
            fqdn = f"{domain}.{tld}"
            levels = 2
        elif difficulty <= 6:
            sub = self._rng.choice(self._SUBS)
            fqdn = f"{sub}.{domain}.{tld}"
            levels = 3
        else:
            sub = self._rng.choice(self._SUBS)
            sub2 = self._rng.choice([s for s in self._SUBS if s != sub])
            fqdn = f"{sub2}.{sub}.{domain}.{tld}"
            levels = 4

        # Generate IP addresses for each server
        root_ip = self._random_ip()
        tld_ip = self._random_ip()
        auth_ip = self._random_ip()
        final_ip = self._random_ip()

        chain = [
            {"query": f"query root for {fqdn}", "server": f"root ({root_ip})",
             "response": f"refer to .{tld} server at {tld_ip}"},
            {"query": f"query .{tld} for {fqdn}", "server": f".{tld} ({tld_ip})",
             "response": f"refer to {domain}.{tld} server at {auth_ip}"},
            {"query": f"query {domain}.{tld} for {fqdn}",
             "server": f"auth ({auth_ip})",
             "response": f"A record: {fqdn} -> {final_ip}"},
        ]

        return (
            f"DNS resolve: {fqdn}",
            {"fqdn": fqdn, "levels": levels, "final_ip": final_ip,
             "chain": chain, "root_ip": root_ip, "tld_ip": tld_ip,
             "auth_ip": auth_ip},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for DNS resolution.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the query chain.
        """
        steps = []
        for entry in data["chain"]:
            steps.append(f"{entry['query']} -> {entry['server']}: {entry['response']}")
        steps.append(f"resolved: {data['fqdn']} = {data['final_ip']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the resolved IP address.

        Args:
            data: Solution data dict.

        Returns:
            FQDN to IP mapping as a string.
        """
        return f"{data['fqdn']} -> {data['final_ip']}"


# ---------------------------------------------------------------------------
# 4. TCP Congestion Control (tier 5)
# ---------------------------------------------------------------------------

@register
class TCPCongestionGenerator(StepGenerator):
    """Compute TCP congestion window evolution over time.

    Slow start: cwnd doubles each RTT until reaching ssthresh.
    Congestion avoidance: cwnd increases by 1 MSS each RTT.
    Given ssthresh and number of RTTs, compute cwnd at each step.

    Difficulty scaling:
        Difficulty 1-3: 4-6 RTTs, ssthresh 8-16.
        Difficulty 4-6: 6-10 RTTs, ssthresh 16-32.
        Difficulty 7-8: 10-15 RTTs, ssthresh 32-64, with loss event.

    Prerequisites:
        multiplication.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "tcp_congestion"

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
            Short task description.
        """
        if difficulty >= 7:
            return "compute TCP cwnd evolution with loss event"
        return "compute TCP congestion window over RTTs"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a TCP congestion control problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_rtts = self._rng.randint(4, 6)
            ssthresh = self._rng.choice([8, 16])
            has_loss = False
        elif difficulty <= 6:
            n_rtts = self._rng.randint(6, 10)
            ssthresh = self._rng.choice([16, 32])
            has_loss = False
        else:
            n_rtts = self._rng.randint(10, 15)
            ssthresh = self._rng.choice([32, 64])
            has_loss = True

        # Simulate cwnd evolution
        cwnd = 1  # start at 1 MSS
        phase = "slow_start"
        history = [{"rtt": 0, "cwnd": cwnd, "phase": phase}]

        loss_rtt = self._rng.randint(n_rtts // 2, n_rtts - 2) if has_loss else -1

        for rtt in range(1, n_rtts + 1):
            if has_loss and rtt == loss_rtt:
                # Multiplicative decrease
                ssthresh = max(2, cwnd // 2)
                cwnd = 1
                phase = "slow_start"
                history.append({"rtt": rtt, "cwnd": cwnd,
                                "phase": f"loss! ssthresh={ssthresh}"})
                continue

            if phase == "slow_start":
                cwnd = cwnd * 2
                if cwnd >= ssthresh:
                    cwnd = ssthresh
                    phase = "congestion_avoidance"
            else:
                cwnd += 1

            history.append({"rtt": rtt, "cwnd": cwnd, "phase": phase})

        final_cwnd = cwnd

        return (
            f"TCP: ssthresh={ssthresh}, {n_rtts} RTTs" +
            (f", loss at RTT {loss_rtt}" if has_loss else ""),
            {"ssthresh": ssthresh, "n_rtts": n_rtts,
             "history": history, "final_cwnd": final_cwnd,
             "has_loss": has_loss, "loss_rtt": loss_rtt},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for TCP congestion.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing cwnd at each RTT.
        """
        steps = []
        # Show up to 8 history entries to keep under 512 chars
        shown = data["history"][:8]
        for entry in shown:
            steps.append(f"RTT {entry['rtt']}: cwnd={entry['cwnd']} ({entry['phase']})")
        if len(data["history"]) > 8:
            steps.append(f"... final cwnd={data['final_cwnd']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the final congestion window.

        Args:
            data: Solution data dict.

        Returns:
            Final cwnd as a string.
        """
        return f"cwnd={data['final_cwnd']}"


# ---------------------------------------------------------------------------
# 5. Checksum Compute (tier 4)
# ---------------------------------------------------------------------------

@register
class ChecksumComputeGenerator(StepGenerator):
    """Compute internet checksum (one's complement sum).

    Sum 16-bit words, fold any carry bits back, take one's complement.
    Used in IP, TCP, and UDP headers for error detection.

    Difficulty scaling:
        Difficulty 1-3: 2-3 words, small values.
        Difficulty 4-6: 3-4 words, values up to 0xFFFF.
        Difficulty 7-8: 4-6 words, verify received packet.

    Prerequisites:
        binary_arithmetic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "checksum_compute"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["binary_arithmetic"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Short task description.
        """
        if difficulty >= 7:
            return "verify internet checksum of received packet"
        return "compute internet checksum of 16-bit words"

    def _ones_complement_add(self, a: int, b: int) -> int:
        """Add two 16-bit values with one's complement wraparound.

        Args:
            a: First 16-bit value.
            b: Second 16-bit value.

        Returns:
            One's complement sum (16-bit).
        """
        s = a + b
        while s > 0xFFFF:
            s = (s & 0xFFFF) + (s >> 16)
        return s

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an internet checksum problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            n_words = self._rng.randint(2, 3)
            cap = 0x00FF
        elif difficulty <= 6:
            n_words = self._rng.randint(3, 4)
            cap = 0xFFFF
        else:
            n_words = self._rng.randint(4, 6)
            cap = 0xFFFF

        words = [self._rng.randint(0, cap) for _ in range(n_words)]

        # Compute checksum
        total = 0
        partial_sums = []
        for w in words:
            total = self._ones_complement_add(total, w)
            partial_sums.append(total)

        checksum = (~total) & 0xFFFF

        # For verification mode (high difficulty): include checksum in words
        verify_mode = difficulty >= 7
        if verify_mode:
            verify_words = words + [checksum]
            verify_total = 0
            for w in verify_words:
                verify_total = self._ones_complement_add(verify_total, w)
            verify_result = (~verify_total) & 0xFFFF  # should be 0
        else:
            verify_words = []
            verify_result = -1

        words_hex = [f"0x{w:04X}" for w in words]

        return (
            f"Checksum: words={words_hex}",
            {"words": words, "words_hex": words_hex,
             "partial_sums": partial_sums, "total": total,
             "checksum": checksum,
             "verify_mode": verify_mode,
             "verify_words": verify_words,
             "verify_result": verify_result},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for checksum computation.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing partial sums and final checksum.
        """
        steps = []
        running = 0
        for i, (w, ps) in enumerate(zip(data["words"], data["partial_sums"])):
            steps.append(f"add 0x{w:04X}: sum=0x{ps:04X}")
            running = ps

        steps.append(f"one's complement: ~0x{data['total']:04X} = 0x{data['checksum']:04X}")

        if data["verify_mode"]:
            steps.append(f"verify: sum with checksum -> 0x{data['verify_result']:04X}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the checksum.

        Args:
            data: Solution data dict.

        Returns:
            Checksum in hex as a string.
        """
        return f"checksum=0x{data['checksum']:04X}"


# ---------------------------------------------------------------------------
# 6. Sliding Window (Go-back-N) (tier 5)
# ---------------------------------------------------------------------------

@register
class SlidingWindowGenerator(StepGenerator):
    """Simulate Go-back-N sliding window protocol.

    Given window size W and a sequence of ACKs and timeouts, determine
    which packets are transmitted and retransmitted.

    Difficulty scaling:
        Difficulty 1-3: W=3, 4-6 events, no losses.
        Difficulty 4-6: W=4, 6-8 events, one loss.
        Difficulty 7-8: W=4-6, 8-10 events, multiple losses.

    Prerequisites:
        comparison.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "sliding_window"

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
            Short task description.
        """
        return "simulate Go-back-N sliding window protocol"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Go-back-N sliding window problem.

        Args:
            difficulty: Difficulty level (1-8).

        Returns:
            Tuple of (latex_problem, solution_data).
        """
        if difficulty <= 3:
            window = 3
            total_packets = self._rng.randint(4, 6)
            n_losses = 0
        elif difficulty <= 6:
            window = 4
            total_packets = self._rng.randint(6, 8)
            n_losses = 1
        else:
            window = self._rng.randint(4, 6)
            total_packets = self._rng.randint(8, 10)
            n_losses = self._rng.randint(1, 2)

        # Select which packets get lost
        loss_packets = set()
        if n_losses > 0:
            candidates = list(range(1, total_packets))
            loss_packets = set(self._rng.sample(candidates, min(n_losses, len(candidates))))

        # Simulate
        base = 0  # oldest unACKed packet
        next_seq = 0  # next packet to send
        events = []
        retransmitted = []
        transmitted = []

        max_events = 20  # safety limit
        event_count = 0

        while base < total_packets and event_count < max_events:
            event_count += 1

            # Send packets within window
            while next_seq < min(base + window, total_packets):
                transmitted.append(next_seq)
                events.append(f"send pkt {next_seq}")
                next_seq += 1

            # Simulate ACK/loss for base packet
            if base in loss_packets:
                events.append(f"pkt {base} lost -> timeout")
                # Go back N: retransmit from base
                retransmit_from = base
                retransmit_to = next_seq
                next_seq = base
                for pkt in range(retransmit_from, retransmit_to):
                    retransmitted.append(pkt)
                events.append(f"retransmit pkts {retransmit_from}-{retransmit_to - 1}")
                loss_packets.discard(base)  # loss only happens once
                # Re-send
                while next_seq < min(base + window, total_packets):
                    transmitted.append(next_seq)
                    next_seq += 1
                # Now the base packet is ACKed on retry
                events.append(f"ACK {base}")
                base += 1
            else:
                events.append(f"ACK {base}")
                base += 1

        # Limit events shown
        shown_events = events[:10]

        return (
            f"Go-back-N: W={window}, {total_packets} packets, losses={sorted(loss_packets) if loss_packets else 'none'}",
            {"window": window, "total_packets": total_packets,
             "events": shown_events, "retransmitted": retransmitted,
             "transmitted": transmitted, "n_losses": n_losses,
             "total_transmissions": len(transmitted)},
        )

    def _create_steps(self, data: dict) -> list[str]:
        """Generate solution steps for Go-back-N.

        Args:
            data: Solution data dict.

        Returns:
            Steps showing the protocol events.
        """
        steps = [f"window size W={data['window']}"]
        # Show up to 6 events to keep under 512 chars
        for event in data["events"][:6]:
            steps.append(event)
        if data["retransmitted"]:
            retrans = sorted(set(data["retransmitted"]))
            steps.append(f"retransmitted packets: {retrans}")
        steps.append(f"total transmissions: {data['total_transmissions']}")
        return steps

    def _create_answer(self, data: dict) -> str:
        """Return the retransmission summary.

        Args:
            data: Solution data dict.

        Returns:
            Retransmission count and list as a string.
        """
        retrans = sorted(set(data["retransmitted"]))
        return f"retransmitted={retrans}, total_sends={data['total_transmissions']}"
