"""Distributed systems generators.

8 generators across tiers 5-6 covering Lamport clocks, vector clock
comparison, consensus rounds, CAP theorem classification, consistent
hash rebalancing, two-phase commit, Raft elections, and CRDT merges.
"""
from __future__ import annotations

from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ---------------------------------------------------------------------------
# 1. Lamport Clock (tier 5)
# ---------------------------------------------------------------------------

@register
class LamportClockGenerator(StepGenerator):
    """Update Lamport timestamps across distributed processes.

    Generates event sequences (local, send, receive) for 2-3 processes
    and applies Lamport clock rules: increment on event, increment on
    send, max(local, received)+1 on receive.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "lamport_clock"

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
        return "update Lamport timestamps for event sequence"

    def _generate_events(self, difficulty: int) -> tuple[int, list[dict]]:
        """Generate an event sequence across processes.

        Args:
            difficulty: Controls number of processes and events.

        Returns:
            Tuple of (n_processes, event_list).
        """
        n_procs = 2 if difficulty <= 4 else 3
        n_events = min(4 + difficulty, 8)
        events = []
        pending_sends: list[dict] = []

        for _ in range(n_events):
            proc = self._rng.randint(0, n_procs - 1)
            kind = self._rng.choice(["local", "send", "receive"])

            if kind == "send":
                dest = self._rng.choice(
                    [p for p in range(n_procs) if p != proc]
                )
                evt = {"proc": proc, "type": "send", "dest": dest}
                events.append(evt)
                pending_sends.append(evt)
            elif kind == "receive" and pending_sends:
                # Find a send destined for this process
                matching = [
                    s for s in pending_sends if s["dest"] == proc
                ]
                if matching:
                    sender_evt = matching[0]
                    pending_sends.remove(sender_evt)
                    events.append({
                        "proc": proc, "type": "receive",
                        "from_proc": sender_evt["proc"],
                        "sender_idx": events.index(sender_evt),
                    })
                else:
                    events.append({"proc": proc, "type": "local"})
            else:
                events.append({"proc": proc, "type": "local"})

        return n_procs, events

    def _simulate(self, n_procs: int,
                  events: list[dict]) -> tuple[list[str], list[int]]:
        """Simulate Lamport clock updates.

        Args:
            n_procs: Number of processes.
            events: Event sequence.

        Returns:
            Tuple of (steps, final_clock_per_event).
        """
        clocks = [0] * n_procs
        steps = []
        timestamps = []

        for i, evt in enumerate(events):
            p = evt["proc"]
            if evt["type"] == "local":
                clocks[p] += 1
                steps.append(f"e{i}: P{p} local LC={clocks[p]}")
            elif evt["type"] == "send":
                clocks[p] += 1
                evt["send_ts"] = clocks[p]
                steps.append(
                    f"e{i}: P{p} send(->P{evt['dest']}) LC={clocks[p]}"
                )
            elif evt["type"] == "receive":
                sender_ts = events[evt["sender_idx"]].get("send_ts", 0)
                clocks[p] = max(clocks[p], sender_ts) + 1
                steps.append(
                    f"e{i}: P{p} recv(P{evt['from_proc']},ts={sender_ts}) "
                    f"LC={clocks[p]}"
                )
            timestamps.append(clocks[p])

        return steps, timestamps

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Lamport clock problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_procs, events = self._generate_events(difficulty)
        steps, timestamps = self._simulate(n_procs, events)

        evt_str = "; ".join(
            f"e{i}:P{e['proc']},{e['type']}" for i, e in enumerate(events)
        )
        problem = f"{n_procs} procs, events: {evt_str}"

        return problem, {
            "steps": steps,
            "timestamps": timestamps,
            "final_clocks": timestamps[-1] if timestamps else 0,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the Lamport clock update steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the final timestamps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Timestamp list string.
        """
        ts = solution_data["timestamps"]
        return f"timestamps={ts}"


# ---------------------------------------------------------------------------
# 2. Vector Clock Compare (tier 5)
# ---------------------------------------------------------------------------

@register
class VectorClockCompareGenerator(StepGenerator):
    """Compare two vector clocks to determine causal ordering.

    VC1 <= VC2 iff all components of VC1 are <= VC2. Determines
    whether events are causally related or concurrent.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "vector_clock_compare"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vector_clock_update"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compare vector clocks to determine causal ordering"

    def _generate_clocks(self, difficulty: int) -> tuple[list[int], list[int]]:
        """Generate two vector clocks for comparison.

        Args:
            difficulty: Controls number of processes and values.

        Returns:
            Tuple of (vc1, vc2).
        """
        n_procs = 2 if difficulty <= 3 else 3
        max_val = min(3 + difficulty, 10)

        # Choose relationship type
        rel = self._rng.choice(["causal", "concurrent", "equal"])

        if rel == "causal":
            vc1 = [self._rng.randint(0, max_val) for _ in range(n_procs)]
            vc2 = [v + self._rng.randint(1, 3) for v in vc1]
        elif rel == "concurrent":
            vc1 = [self._rng.randint(1, max_val) for _ in range(n_procs)]
            vc2 = list(vc1)
            # Make at least one component greater and one less
            idx_a = self._rng.randint(0, n_procs - 1)
            idx_b = (idx_a + 1) % n_procs
            vc2[idx_a] = vc1[idx_a] + self._rng.randint(1, 3)
            vc2[idx_b] = max(0, vc1[idx_b] - self._rng.randint(1, 3))
        else:
            vc1 = [self._rng.randint(0, max_val) for _ in range(n_procs)]
            vc2 = list(vc1)

        return vc1, vc2

    def _compare(self, vc1: list[int], vc2: list[int]) -> str:
        """Compare two vector clocks.

        Args:
            vc1: First vector clock.
            vc2: Second vector clock.

        Returns:
            Ordering result string.
        """
        leq_12 = all(a <= b for a, b in zip(vc1, vc2))
        leq_21 = all(b <= a for a, b in zip(vc1, vc2))

        if vc1 == vc2:
            return "VC1 = VC2 (same logical time)"
        if leq_12:
            return "VC1 -> VC2 (VC1 happens-before VC2)"
        if leq_21:
            return "VC2 -> VC1 (VC2 happens-before VC1)"
        return "VC1 || VC2 (concurrent)"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a vector clock comparison problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        vc1, vc2 = self._generate_clocks(difficulty)
        ordering = self._compare(vc1, vc2)

        # Component-wise comparison details
        comparisons = []
        for i, (a, b) in enumerate(zip(vc1, vc2)):
            if a < b:
                comparisons.append(f"P{i}: {a}<{b}")
            elif a > b:
                comparisons.append(f"P{i}: {a}>{b}")
            else:
                comparisons.append(f"P{i}: {a}={b}")

        problem = f"VC1={vc1}, VC2={vc2}"
        return problem, {
            "vc1": vc1,
            "vc2": vc2,
            "comparisons": comparisons,
            "ordering": ordering,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate vector clock comparison steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        steps = [f"VC1={d['vc1']}, VC2={d['vc2']}"]
        steps.extend(d["comparisons"])
        return steps

    def _create_answer(self, solution_data: dict) -> str:
        """Return the causal ordering.

        Args:
            solution_data: All computed solution information.

        Returns:
            Ordering verdict string.
        """
        return solution_data["ordering"]


# ---------------------------------------------------------------------------
# 3. Consensus Round (tier 6)
# ---------------------------------------------------------------------------

@register
class ConsensusRoundGenerator(StepGenerator):
    """Simulate one round of simplified Paxos consensus.

    Generates a scenario with a proposer, acceptors, and a proposed
    value. Shows the prepare-promise-accept message sequence and
    determines whether consensus is reached.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "consensus_round"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["vector_clock_compare"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "simulate one round of Paxos consensus"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a consensus round problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_acceptors = 3 if difficulty <= 4 else 5
        majority = n_acceptors // 2 + 1
        proposal_num = self._rng.randint(1, 10)
        value = self._rng.choice(["A", "B", "C", "X", "Y"])

        # Each acceptor may have a previous promise
        acceptors = []
        for i in range(n_acceptors):
            prev_promise = self._rng.choice([0, 0, 0, proposal_num - 1])
            prev_accepted = None
            if prev_promise > 0 and self._rng.random() > 0.5:
                prev_accepted = self._rng.choice(["A", "B", "C"])
            acceptors.append({
                "id": f"A{i}",
                "prev_promise": prev_promise,
                "prev_accepted": prev_accepted,
            })

        # Phase 1: Prepare and Promise
        promises = []
        for acc in acceptors:
            if proposal_num > acc["prev_promise"]:
                promises.append(acc)

        got_majority = len(promises) >= majority

        # Phase 2: Accept (if majority promised)
        if got_majority:
            # Check if any promise had an accepted value
            accepted_vals = [
                a["prev_accepted"] for a in promises
                if a["prev_accepted"] is not None
            ]
            if accepted_vals:
                # Must use the value from highest-numbered accepted
                final_value = accepted_vals[-1]
            else:
                final_value = value
            outcome = f"COMMIT {final_value}"
        else:
            final_value = None
            outcome = "ABORT (no majority)"

        steps = [
            f"proposer sends PREPARE(n={proposal_num})",
            f"{len(promises)}/{n_acceptors} promise (need {majority})",
        ]
        if got_majority:
            steps.append(f"proposer sends ACCEPT(n={proposal_num}, v={final_value})")
            steps.append(f"majority accepts => COMMIT")
        else:
            steps.append("insufficient promises => ABORT")

        acc_str = ", ".join(
            f"{a['id']}(prom={a['prev_promise']})" for a in acceptors
        )
        problem = (
            f"Paxos: n={proposal_num}, val={value}, "
            f"acceptors=[{acc_str}]"
        )

        return problem, {
            "steps": steps,
            "outcome": outcome,
            "proposal_num": proposal_num,
            "n_promises": len(promises),
            "majority": majority,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the consensus round steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the consensus outcome.

        Args:
            solution_data: All computed solution information.

        Returns:
            COMMIT or ABORT string.
        """
        return solution_data["outcome"]


# ---------------------------------------------------------------------------
# 4. CAP Theorem (tier 5)
# ---------------------------------------------------------------------------

@register
class CAPTheoremGenerator(StepGenerator):
    """Classify a distributed system under the CAP theorem.

    Given a system description, identify which of Consistency,
    Availability, or Partition tolerance is sacrificed and classify
    the system as CP, AP, or CA.
    """

    _TEMPLATES: list[dict] = [
        {
            "system": "single-leader replicated DB, sync replication",
            "sacrificed": "Availability",
            "classification": "CP",
            "reason": "sync writes block during partition, sacrificing A",
        },
        {
            "system": "multi-leader DB with async replication",
            "sacrificed": "Consistency",
            "classification": "AP",
            "reason": "async replication allows stale reads during partition",
        },
        {
            "system": "single-node relational DB (no replication)",
            "sacrificed": "Partition tolerance",
            "classification": "CA",
            "reason": "no network partition possible with single node",
        },
        {
            "system": "distributed cache with eventual consistency",
            "sacrificed": "Consistency",
            "classification": "AP",
            "reason": "eventual consistency means stale data during partition",
        },
        {
            "system": "ZooKeeper (majority quorum reads/writes)",
            "sacrificed": "Availability",
            "classification": "CP",
            "reason": "minority partition cannot serve requests",
        },
        {
            "system": "Cassandra (tunable consistency, default ONE)",
            "sacrificed": "Consistency",
            "classification": "AP",
            "reason": "ONE consistency allows reads from stale replicas",
        },
        {
            "system": "etcd / Raft-based key-value store",
            "sacrificed": "Availability",
            "classification": "CP",
            "reason": "Raft requires majority for writes, blocks in minority",
        },
        {
            "system": "DNS with caching and TTL",
            "sacrificed": "Consistency",
            "classification": "AP",
            "reason": "cached entries may be stale during partition/TTL window",
        },
    ]

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "cap_theorem"

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
        return "classify system under CAP theorem"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CAP theorem classification problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        idx = difficulty % len(self._TEMPLATES)
        tmpl = self._TEMPLATES[idx]
        problem = f"system: {tmpl['system']}"
        return problem, {
            "system": tmpl["system"],
            "sacrificed": tmpl["sacrificed"],
            "classification": tmpl["classification"],
            "reason": tmpl["reason"],
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Generate CAP analysis steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        d = solution_data
        return [
            f"system: {d['system']}",
            f"sacrificed: {d['sacrificed']}",
            d["reason"],
        ]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the CAP classification.

        Args:
            solution_data: All computed solution information.

        Returns:
            Classification string (CP, AP, or CA).
        """
        return solution_data["classification"]


# ---------------------------------------------------------------------------
# 5. Consistent Hash Rebalance (tier 5)
# ---------------------------------------------------------------------------

@register
class ConsistentHashRebalanceGenerator(StepGenerator):
    """Compute key migration when adding or removing a node from a hash ring.

    Places nodes on a hash ring, assigns keys, then adds or removes
    a node and determines which keys must be migrated.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "consistent_hash_rebalance"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["hash_table_ops"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "compute key migration on hash ring add/remove"

    def _find_owner(self, ring: dict[str, int],
                    key_hash: int) -> str:
        """Find the node owning a key on the hash ring.

        Args:
            ring: Node name to position mapping.
            key_hash: Hash value of the key.

        Returns:
            Name of the owning node.
        """
        sorted_nodes = sorted(ring.items(), key=lambda x: x[1])
        for name, pos in sorted_nodes:
            if pos >= key_hash:
                return name
        return sorted_nodes[0][0]

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a consistent hash rebalance problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_nodes = min(3 + difficulty // 2, 6)
        positions = sorted(self._rng.sample(range(0, 360, 10), n_nodes))
        ring = {f"N{i}": positions[i] for i in range(n_nodes)}

        n_keys = min(3 + difficulty, 8)
        keys = {
            f"k{j}": self._rng.randint(0, 359)
            for j in range(n_keys)
        }

        # Before operation: assign keys
        before = {k: self._find_owner(ring, h) for k, h in keys.items()}

        op = self._rng.choice(["add", "remove"])
        if op == "add":
            available = [p for p in range(0, 360, 10) if p not in ring.values()]
            new_pos = self._rng.choice(available)
            new_name = f"N{n_nodes}"
            ring_after = dict(ring)
            ring_after[new_name] = new_pos
            op_desc = f"add {new_name}@{new_pos}"
        else:
            rm_name = self._rng.choice(list(ring.keys()))
            ring_after = {n: p for n, p in ring.items() if n != rm_name}
            op_desc = f"remove {rm_name}"

        after = {k: self._find_owner(ring_after, h) for k, h in keys.items()}

        # Keys that moved
        moved = {k: (before[k], after[k]) for k in keys if before[k] != after[k]}

        ring_str = " ".join(
            f"{n}@{p}" for n, p in sorted(ring.items(), key=lambda x: x[1])
        )
        keys_str = " ".join(f"{k}={h}" for k, h in keys.items())
        problem = f"ring=[{ring_str}], keys=[{keys_str}], op={op_desc}"

        steps = [f"before: {before}"]
        steps.append(f"operation: {op_desc}")
        steps.append(f"after: {after}")

        return problem, {
            "steps": steps,
            "moved": moved,
            "n_moved": len(moved),
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the rebalance steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the moved keys.

        Args:
            solution_data: All computed solution information.

        Returns:
            Key migration summary.
        """
        d = solution_data
        if d["moved"]:
            parts = [f"{k}:{fr}->{to}" for k, (fr, to) in d["moved"].items()]
            return f"moved={', '.join(parts)}"
        return "moved=none"


# ---------------------------------------------------------------------------
# 6. Two-Phase Commit (tier 6)
# ---------------------------------------------------------------------------

@register
class TwoPhaseCommitGenerator(StepGenerator):
    """Trace the two-phase commit (2PC) protocol.

    Simulates coordinator sending PREPARE, participants voting
    YES/NO, and coordinator deciding COMMIT or ABORT. Handles
    participant failure scenarios.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "two_phase_commit"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["consensus_round"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "trace two-phase commit protocol"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a 2PC protocol trace problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_participants = min(2 + difficulty // 2, 5)
        participants = [f"P{i}" for i in range(n_participants)]

        # Each participant votes YES or NO, or may fail (timeout)
        votes = {}
        for p in participants:
            if difficulty >= 5 and self._rng.random() < 0.15:
                votes[p] = "TIMEOUT"
            elif self._rng.random() < 0.8:
                votes[p] = "YES"
            else:
                votes[p] = "NO"

        all_yes = all(v == "YES" for v in votes.values())
        any_timeout = any(v == "TIMEOUT" for v in votes.values())

        if all_yes:
            decision = "COMMIT"
        elif any_timeout:
            decision = "ABORT (timeout)"
        else:
            decision = "ABORT"

        steps = [
            f"coordinator sends PREPARE to {participants}",
        ]
        for p in participants:
            steps.append(f"{p} votes {votes[p]}")

        if all_yes:
            steps.append("all YES => coordinator sends COMMIT")
        else:
            no_list = [p for p, v in votes.items() if v != "YES"]
            steps.append(f"{no_list} not YES => coordinator sends ABORT")

        votes_str = ", ".join(f"{p}={v}" for p, v in votes.items())
        problem = f"2PC: participants={participants}, votes=[{votes_str}]"

        return problem, {
            "steps": steps,
            "decision": decision,
            "votes": votes,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the 2PC protocol trace steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the commit/abort decision.

        Args:
            solution_data: All computed solution information.

        Returns:
            Decision string.
        """
        return solution_data["decision"]


# ---------------------------------------------------------------------------
# 7. Raft Election (tier 6)
# ---------------------------------------------------------------------------

@register
class RaftElectionGenerator(StepGenerator):
    """Simulate a Raft leader election round.

    A candidate increments its term, requests votes from peers. Nodes
    vote for the candidate if the candidate's term is higher than their
    current term and they have not already voted in this term.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "raft_election"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 6

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["consensus_round"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "simulate Raft leader election"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a Raft election problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_nodes = 3 if difficulty <= 3 else 5
        majority = n_nodes // 2 + 1

        # Pick candidate
        candidate = self._rng.randint(0, n_nodes - 1)
        candidate_term = self._rng.randint(2, 5 + difficulty)

        # Each other node has a current term and possibly already voted
        peers = []
        for i in range(n_nodes):
            if i == candidate:
                continue
            peer_term = self._rng.randint(
                max(1, candidate_term - 2),
                candidate_term + 1
            )
            already_voted = (
                peer_term == candidate_term and self._rng.random() < 0.3
            )
            peers.append({
                "id": f"N{i}",
                "term": peer_term,
                "voted": already_voted,
            })

        # Count votes (candidate votes for itself)
        votes = 1
        vote_results = []
        for peer in peers:
            if candidate_term > peer["term"]:
                votes += 1
                vote_results.append(f"{peer['id']}(term={peer['term']}): YES")
            elif candidate_term == peer["term"] and not peer["voted"]:
                votes += 1
                vote_results.append(f"{peer['id']}(term={peer['term']}): YES")
            else:
                reason = "already voted" if peer["voted"] else "higher term"
                vote_results.append(
                    f"{peer['id']}(term={peer['term']}): NO ({reason})"
                )

        elected = votes >= majority
        outcome = f"ELECTED (votes={votes}/{n_nodes})" if elected else f"FAILED (votes={votes}/{n_nodes})"

        steps = [
            f"N{candidate} starts election, term={candidate_term}",
        ]
        steps.extend(vote_results)
        steps.append(f"total votes={votes}, need {majority}")

        peers_str = ", ".join(
            f"{p['id']}(t={p['term']},voted={p['voted']})" for p in peers
        )
        problem = (
            f"Raft: candidate=N{candidate}, term={candidate_term}, "
            f"peers=[{peers_str}]"
        )

        return problem, {
            "steps": steps,
            "outcome": outcome,
            "votes": votes,
            "majority": majority,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the Raft election steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the election outcome.

        Args:
            solution_data: All computed solution information.

        Returns:
            ELECTED or FAILED string.
        """
        return solution_data["outcome"]


# ---------------------------------------------------------------------------
# 8. CRDT Merge (tier 5)
# ---------------------------------------------------------------------------

@register
class CRDTMergeGenerator(StepGenerator):
    """Merge conflict-free replicated data type (CRDT) states.

    G-Counter merge: take component-wise max. PN-Counter: merge
    P (positive) and N (negative) counters separately, value = P - N.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "crdt_merge"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task instruction string.
        """
        return "merge CRDT states across replicas"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a CRDT merge problem.

        Args:
            difficulty: Difficulty level.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        n_nodes = 2 if difficulty <= 3 else 3
        crdt_type = self._rng.choice(["G-Counter", "PN-Counter"])

        if crdt_type == "G-Counter":
            # Each replica has a vector of counts
            replica_a = [
                self._rng.randint(0, 5 + difficulty) for _ in range(n_nodes)
            ]
            replica_b = [
                self._rng.randint(0, 5 + difficulty) for _ in range(n_nodes)
            ]
            merged = [max(a, b) for a, b in zip(replica_a, replica_b)]
            value = sum(merged)

            steps = [
                f"A={replica_a}",
                f"B={replica_b}",
                f"merge: max component-wise = {merged}",
                f"value = sum({merged}) = {value}",
            ]
            problem = f"G-Counter: A={replica_a}, B={replica_b}"
        else:
            # PN-Counter: separate P and N vectors
            p_a = [self._rng.randint(0, 5 + difficulty) for _ in range(n_nodes)]
            n_a = [self._rng.randint(0, 3) for _ in range(n_nodes)]
            p_b = [self._rng.randint(0, 5 + difficulty) for _ in range(n_nodes)]
            n_b = [self._rng.randint(0, 3) for _ in range(n_nodes)]

            p_merged = [max(a, b) for a, b in zip(p_a, p_b)]
            n_merged = [max(a, b) for a, b in zip(n_a, n_b)]
            value = sum(p_merged) - sum(n_merged)

            steps = [
                f"P_A={p_a}, N_A={n_a}",
                f"P_B={p_b}, N_B={n_b}",
                f"P_merge={p_merged}, N_merge={n_merged}",
                f"value = {sum(p_merged)}-{sum(n_merged)} = {value}",
            ]
            problem = (
                f"PN-Counter: P_A={p_a}, N_A={n_a}, "
                f"P_B={p_b}, N_B={n_b}"
            )

        return problem, {
            "steps": steps,
            "crdt_type": crdt_type,
            "value": value,
        }

    def _create_steps(self, solution_data: dict) -> list[str]:
        """Return the CRDT merge steps.

        Args:
            solution_data: All computed solution information.

        Returns:
            Step strings in execution order.
        """
        return solution_data["steps"]

    def _create_answer(self, solution_data: dict) -> str:
        """Return the merged CRDT value.

        Args:
            solution_data: All computed solution information.

        Returns:
            Merged value string.
        """
        d = solution_data
        return f"{d['crdt_type']}: value={d['value']}"
