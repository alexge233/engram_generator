"""Music theory generators.

6 generators across tiers 3-5 covering intervals, chord construction,
chord progressions, voice leading, frequency ratios, and rhythm subdivision.
"""
from engram_generator.base import StepGenerator
from engram_generator.curriculum.registry import register


# ===================================================================
# HELPER CONSTANTS
# ===================================================================

_NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F",
               "F#", "G", "G#", "A", "A#", "B"]

_INTERVAL_NAMES = {
    0: "P1", 1: "m2", 2: "M2", 3: "m3", 4: "M3", 5: "P4",
    6: "TT", 7: "P5", 8: "m6", 9: "M6", 10: "m7", 11: "M7", 12: "P8",
}

_CHORD_TYPES = {
    "major": (0, 4, 7),
    "minor": (0, 3, 7),
    "dim": (0, 3, 6),
    "aug": (0, 4, 8),
}

# Major scale intervals from root (in semitones)
_MAJOR_SCALE = [0, 2, 4, 5, 7, 9, 11]

# Roman numeral chord qualities in major key
_ROMAN_QUALITY = {
    1: ("I", "major"),
    2: ("ii", "minor"),
    3: ("iii", "minor"),
    4: ("IV", "major"),
    5: ("V", "major"),
    6: ("vi", "minor"),
    7: ("vii", "dim"),
}


# ===================================================================
# HELPER UTILITIES
# ===================================================================

def _round4(x: float) -> float:
    """Round a float to 4 decimal places.

    Args:
        x: Value to round.

    Returns:
        Rounded value.
    """
    return round(x, 4)


def _note_name(pitch_class: int) -> str:
    """Convert a pitch class (0-11) to note name.

    Args:
        pitch_class: Integer 0-11.

    Returns:
        Note name string.
    """
    return _NOTE_NAMES[pitch_class % 12]


# ===================================================================
# 1. INTERVAL IDENTIFICATION (tier 3)
# ===================================================================

@register
class IntervalIdentifyGenerator(StepGenerator):
    """Identify the musical interval between two notes.

    Given two notes as pitch classes (C=0 through B=11), compute
    the interval in semitones and name it.

    Difficulty scaling:
        Difficulty 1-3: simple intervals (P1 through P5).
        Difficulty 4-6: any interval within octave.
        Difficulty 7-8: compound intervals (add octave).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "interval_identify"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["modular"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "identify the interval between two notes"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate an interval identification problem.

        Args:
            difficulty: Controls interval range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        note1 = self._rng.randint(0, 11)
        if difficulty <= 3:
            interval = self._rng.randint(0, 7)
        elif difficulty <= 6:
            interval = self._rng.randint(0, 12)
        else:
            interval = self._rng.randint(0, 12)

        note2 = (note1 + interval) % 12
        semitones = (note2 - note1) % 12

        name1 = _note_name(note1)
        name2 = _note_name(note2)
        interval_name = _INTERVAL_NAMES.get(semitones, f"{semitones}st")

        problem = f"interval from {name1} to {name2}"
        return problem, {
            "note1": name1, "note2": name2,
            "semitones": semitones,
            "interval_name": interval_name,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        return [
            f"{sd['note1']} to {sd['note2']}",
            f"semitones = {sd['semitones']}",
            f"interval = {sd['interval_name']}",
        ]

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Interval name and semitone count.
        """
        return f"{sd['interval_name']} ({sd['semitones']} semitones)"


# ===================================================================
# 2. CHORD CONSTRUCTION (tier 4)
# ===================================================================

@register
class ChordConstructGenerator(StepGenerator):
    """Build a chord from a root note and chord type.

    Major = (0,4,7), minor = (0,3,7), dim = (0,3,6), aug = (0,4,8).

    Difficulty scaling:
        Difficulty 1-3: major or minor only.
        Difficulty 4-6: all four chord types.
        Difficulty 7-8: all types with sharps/flats.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chord_construct"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["interval_identify"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "construct a chord from root and quality"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chord construction problem.

        Args:
            difficulty: Controls chord type variety and root range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        root = self._rng.randint(0, 11)

        if difficulty <= 3:
            chord_type = self._rng.choice(["major", "minor"])
        else:
            chord_type = self._rng.choice(
                ["major", "minor", "dim", "aug"])

        intervals = _CHORD_TYPES[chord_type]
        notes = [(root + iv) % 12 for iv in intervals]
        note_names = [_note_name(n) for n in notes]
        root_name = _note_name(root)

        problem = f"build {root_name} {chord_type} chord"
        return problem, {
            "root": root_name,
            "chord_type": chord_type,
            "intervals": intervals,
            "notes": notes,
            "note_names": note_names,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"root: {sd['root']}, type: {sd['chord_type']}"]
        steps.append(f"intervals: {sd['intervals']}")
        for iv, name in zip(sd["intervals"], sd["note_names"]):
            steps.append(f"+{iv} semitones = {name}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Chord notes as a string.
        """
        return f"{sd['root']} {sd['chord_type']}: {'-'.join(sd['note_names'])}"


# ===================================================================
# 3. CHORD PROGRESSION (tier 5)
# ===================================================================

@register
class ChordProgressionGenerator(StepGenerator):
    """Analyze a Roman numeral chord progression in a major key.

    Given a key and a sequence of Roman numerals, identify each
    chord's root and notes.

    Difficulty scaling:
        Difficulty 1-3: 3 chords, I/IV/V only.
        Difficulty 4-6: 4 chords, I through vi.
        Difficulty 7-8: 4-5 chords, all diatonic.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "chord_progression"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["chord_construct"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "analyze chord progression in major key"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a chord progression analysis problem.

        Args:
            difficulty: Controls progression length and chord variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        key_root = self._rng.randint(0, 11)
        key_name = _note_name(key_root)

        if difficulty <= 3:
            n_chords = 3
            degrees = self._rng.sample([1, 4, 5], 3)
        elif difficulty <= 6:
            n_chords = 4
            pool = [1, 2, 3, 4, 5, 6]
            degrees = [self._rng.choice(pool) for _ in range(n_chords)]
        else:
            n_chords = self._rng.randint(4, 5)
            pool = [1, 2, 3, 4, 5, 6, 7]
            degrees = [self._rng.choice(pool) for _ in range(n_chords)]

        chords = []
        for deg in degrees:
            roman, quality = _ROMAN_QUALITY[deg]
            root_pc = (key_root + _MAJOR_SCALE[deg - 1]) % 12
            intervals = _CHORD_TYPES[quality]
            notes = [_note_name((root_pc + iv) % 12) for iv in intervals]
            chords.append({
                "degree": deg,
                "roman": roman,
                "quality": quality,
                "root": _note_name(root_pc),
                "notes": notes,
            })

        roman_str = "-".join(c["roman"] for c in chords)
        problem = f"key: {key_name} major, progression: {roman_str}"

        return problem, {
            "key": key_name,
            "chords": chords,
            "roman_str": roman_str,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"key: {sd['key']} major"]
        for c in sd["chords"]:
            steps.append(
                f"{c['roman']} ({c['quality']}): "
                f"root={c['root']}, notes={'-'.join(c['notes'])}"
            )
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Progression with note names.
        """
        parts = [f"{c['roman']}={'-'.join(c['notes'])}" for c in sd["chords"]]
        return ", ".join(parts)


# ===================================================================
# 4. VOICE LEADING (tier 5)
# ===================================================================

@register
class VoiceLeadingGenerator(StepGenerator):
    """Find minimal voice leading between two chords.

    Given two chords (as pitch class sets), find the assignment of
    voices that minimizes total semitone movement.

    Difficulty scaling:
        Difficulty 1-3: triads (3 notes).
        Difficulty 4-6: triads with different types.
        Difficulty 7-8: seventh chords (4 notes).
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "voice_leading"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 5

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["chord_construct"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "find minimal voice leading between two chords"

    def _semitone_distance(self, a: int, b: int) -> int:
        """Compute minimum semitone distance between two pitch classes.

        Args:
            a: First pitch class (0-11).
            b: Second pitch class (0-11).

        Returns:
            Minimum distance in semitones.
        """
        diff = abs(a - b)
        return min(diff, 12 - diff)

    def _minimal_voice_leading(self, chord1: list[int],
                               chord2: list[int]) -> tuple[int, list]:
        """Find minimal total voice movement via brute-force permutation.

        Args:
            chord1: List of pitch classes for first chord.
            chord2: List of pitch classes for second chord.

        Returns:
            Tuple of (total_movement, best_assignment).
        """
        from itertools import permutations
        n = len(chord1)
        best_cost = float("inf")
        best_assign = list(range(n))
        for perm in permutations(range(n)):
            cost = sum(
                self._semitone_distance(chord1[i], chord2[perm[i]])
                for i in range(n)
            )
            if cost < best_cost:
                best_cost = cost
                best_assign = list(perm)
        return best_cost, best_assign

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a voice leading problem.

        Args:
            difficulty: Controls chord sizes.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        root1 = self._rng.randint(0, 11)
        root2 = self._rng.randint(0, 11)

        if difficulty <= 6:
            type1 = self._rng.choice(["major", "minor"])
            type2 = self._rng.choice(["major", "minor"])
            chord1 = [(root1 + iv) % 12 for iv in _CHORD_TYPES[type1]]
            chord2 = [(root2 + iv) % 12 for iv in _CHORD_TYPES[type2]]
        else:
            type1 = self._rng.choice(["major", "minor"])
            type2 = self._rng.choice(["major", "minor"])
            # Add 7th: major 7th or minor 7th
            seventh1 = 11 if type1 == "major" else 10
            seventh2 = 11 if type2 == "major" else 10
            chord1 = [(root1 + iv) % 12
                      for iv in list(_CHORD_TYPES[type1]) + [seventh1]]
            chord2 = [(root2 + iv) % 12
                      for iv in list(_CHORD_TYPES[type2]) + [seventh2]]

        names1 = [_note_name(pc) for pc in chord1]
        names2 = [_note_name(pc) for pc in chord2]

        total, assignment = self._minimal_voice_leading(chord1, chord2)

        movements = []
        for i in range(len(chord1)):
            j = assignment[i]
            dist = self._semitone_distance(chord1[i], chord2[j])
            movements.append(
                f"{names1[i]}->{names2[j]} ({dist}st)"
            )

        problem = (f"chord1: {'-'.join(names1)}, "
                   f"chord2: {'-'.join(names2)}")

        return problem, {
            "chord1": names1,
            "chord2": names2,
            "total": total,
            "movements": movements,
            "assignment": assignment,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"chord1: {'-'.join(sd['chord1'])}",
            f"chord2: {'-'.join(sd['chord2'])}",
        ]
        steps.extend(sd["movements"])
        steps.append(f"total movement = {sd['total']} semitones")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Total movement as a string.
        """
        return f"{sd['total']} semitones"


# ===================================================================
# 5. FREQUENCY RATIO (tier 4)
# ===================================================================

@register
class FrequencyRatioGenerator(StepGenerator):
    """Compute note frequency using equal temperament.

    f = f_0 * 2^(n/12) where f_0 = 440 Hz (A4) and n is the
    number of semitones from A4.

    Difficulty scaling:
        Difficulty 1-3: notes within one octave of A4.
        Difficulty 4-6: notes within two octaves.
        Difficulty 7-8: arbitrary notes, compute ratio between two.
    """

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "frequency_ratio"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 4

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["multiplication"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "compute frequency using equal temperament"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a frequency ratio problem.

        Args:
            difficulty: Controls semitone range.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        f0 = 440.0  # A4

        if difficulty <= 3:
            n = self._rng.randint(-12, 12)
        elif difficulty <= 6:
            n = self._rng.randint(-24, 24)
        else:
            n = self._rng.randint(-36, 36)

        freq = _round4(f0 * (2 ** (n / 12)))

        # Determine note name and octave
        # A4 is pitch class 9, MIDI 69
        midi = 69 + n
        octave = (midi // 12) - 1
        pc = midi % 12
        note_name = _NOTE_NAMES[pc]

        if difficulty >= 7:
            # Also compute ratio between two notes
            n2 = self._rng.randint(-24, 24)
            freq2 = _round4(f0 * (2 ** (n2 / 12)))
            ratio = _round4(freq / freq2) if freq2 != 0 else 0
            problem = (f"compute frequencies: n1={n} and n2={n2}"
                       f" semitones from A4=440Hz")
            return problem, {
                "n": n, "freq": freq, "note": f"{note_name}{octave}",
                "n2": n2, "freq2": freq2, "ratio": ratio,
                "two_notes": True,
            }

        problem = f"note {n} semitones from A4 (440 Hz)"
        return problem, {
            "n": n, "freq": freq, "note": f"{note_name}{octave}",
            "two_notes": False,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [
            f"f = 440 * 2^({sd['n']}/12)",
            f"f = {sd['freq']} Hz ({sd['note']})",
        ]
        if sd["two_notes"]:
            steps.append(f"f2 = 440 * 2^({sd['n2']}/12) = {sd['freq2']} Hz")
            steps.append(f"ratio = {sd['freq']}/{sd['freq2']}"
                         f" = {sd['ratio']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Frequency (and ratio if applicable) as a string.
        """
        if sd["two_notes"]:
            return f"f1={sd['freq']}Hz, f2={sd['freq2']}Hz, ratio={sd['ratio']}"
        return f"{sd['freq']} Hz"


# ===================================================================
# 6. RHYTHM SUBDIVISION (tier 3)
# ===================================================================

@register
class RhythmSubdivisionGenerator(StepGenerator):
    """Check whether note values complete a bar in a given time signature.

    Given a time signature and a sequence of note values, compute
    the total beats and determine if the bar is complete.

    Difficulty scaling:
        Difficulty 1-3: 4/4 time, simple note values.
        Difficulty 4-6: 3/4 or 6/8 time.
        Difficulty 7-8: mixed time signatures, dotted notes.
    """

    _NOTE_VALUES = {
        "whole": 4.0,
        "half": 2.0,
        "quarter": 1.0,
        "eighth": 0.5,
        "sixteenth": 0.25,
        "dotted_half": 3.0,
        "dotted_quarter": 1.5,
        "dotted_eighth": 0.75,
    }

    @property
    def task_name(self) -> str:
        """Return the unique task identifier."""
        return "rhythm_subdivision"

    @property
    def tier(self) -> int:
        """Return the skill tree tier."""
        return 3

    @property
    def prerequisites(self) -> list[str]:
        """Return required prerequisite task names."""
        return ["addition"]

    def task_description(self, difficulty: int) -> str:
        """Return a natural language task description.

        Args:
            difficulty: Current difficulty level.

        Returns:
            Task description string.
        """
        return "check if note values complete a bar"

    def _create_problem(self, difficulty: int) -> tuple[str, dict]:
        """Generate a rhythm subdivision problem.

        Args:
            difficulty: Controls time signature and note variety.

        Returns:
            Tuple of (problem_text, solution_data).
        """
        if difficulty <= 3:
            num, denom = 4, 4
            pool = ["whole", "half", "quarter", "eighth"]
        elif difficulty <= 6:
            num, denom = self._rng.choice([(3, 4), (6, 8)])
            pool = ["half", "quarter", "eighth", "sixteenth"]
        else:
            num, denom = self._rng.choice([(4, 4), (3, 4), (6, 8)])
            pool = ["half", "quarter", "eighth", "sixteenth",
                    "dotted_half", "dotted_quarter", "dotted_eighth"]

        # Beats per bar
        if denom == 4:
            beats_per_bar = float(num)
        else:  # denom == 8
            beats_per_bar = num * 0.5

        # Generate note sequence
        n_notes = self._rng.randint(2, min(5, 2 + difficulty))
        notes = [self._rng.choice(pool) for _ in range(n_notes)]
        beat_values = [self._NOTE_VALUES[n] for n in notes]
        total_beats = _round4(sum(beat_values))
        complete = abs(total_beats - beats_per_bar) < 0.001

        notes_str = ", ".join(notes)
        problem = f"time sig: {num}/{denom}; notes: {notes_str}"

        return problem, {
            "time_sig": f"{num}/{denom}",
            "beats_per_bar": beats_per_bar,
            "notes": notes,
            "beat_values": beat_values,
            "total_beats": total_beats,
            "complete": complete,
        }

    def _create_steps(self, sd: dict) -> list[str]:
        """Generate solution steps.

        Args:
            sd: Solution data.

        Returns:
            List of step strings.
        """
        steps = [f"time signature: {sd['time_sig']}"
                 f" ({sd['beats_per_bar']} beats/bar)"]
        for note, val in zip(sd["notes"], sd["beat_values"]):
            steps.append(f"{note} = {val} beats")
        steps.append(f"total = {sd['total_beats']} beats")
        steps.append(f"bar complete: {sd['complete']}")
        return steps

    def _create_answer(self, sd: dict) -> str:
        """Return the final answer.

        Args:
            sd: Solution data.

        Returns:
            Total beats and completeness.
        """
        status = "COMPLETE" if sd["complete"] else "INCOMPLETE"
        return f"{sd['total_beats']} beats, {status}"
