#!/usr/bin/env python3
"""Contract for the quality-gates mutation-testing org hub README."""

from __future__ import annotations

import re
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
README = (ROOT / "README.md").read_text(encoding="utf-8")

REQUIRED_HEADINGS = [
    "# Mutation testing",
    "## Why you need it",
    "## Pain points it hits",
    "## Language map",
    "## Start here",
    "## Manual mutation",
    "## Related quality gates",
]

LANGUAGE_ROWS = [
    ("Go", "https://github.com/quality-gates/mutago", "mutago"),
    ("Rust", "https://github.com/quality-gates/mutarust", "mutarust"),
    ("Haskell", "https://github.com/quality-gates/mutaskell", "mutaskell"),
]

START_COMMANDS = [
    "go install github.com/quality-gates/mutago/v2/cmd/mutago@latest",
    "cargo install mutarust",
    "cabal run mutaskell",
]

AI_SLOP_MARKERS = [
    "AI",
    "slop",
    "passing tests",
]


class HubContractTest(unittest.TestCase):
    def test_required_headings_in_order(self) -> None:
        positions = []
        for heading in REQUIRED_HEADINGS:
            pos = README.find(heading)
            self.assertGreaterEqual(pos, 0, f"missing heading: {heading}")
            positions.append(pos)
        self.assertEqual(positions, sorted(positions), "headings must stay in hub order")

    def test_ai_slop_message_is_front_and_center(self) -> None:
        why = self._section("## Why you need it", "## Pain points it hits")
        for marker in AI_SLOP_MARKERS:
            self.assertIn(marker, why)
        # Keep the core claim near the top of the page.
        self.assertLess(README.find("## Why you need it"), 800)

    def test_language_map_lists_org_tools(self) -> None:
        section = self._section("## Language map", "## Start here")
        for language, url, tool in LANGUAGE_ROWS:
            self.assertRegex(
                section,
                rf"\|\s*{re.escape(language)}\s*\|",
                f"language map must include {language}",
            )
            self.assertIn(url, section, f"language map must link {url}")
            self.assertIn(tool, section, f"language map must name {tool}")

    def test_start_here_has_real_install_commands(self) -> None:
        section = self._section("## Start here", "## Manual mutation")
        for command in START_COMMANDS:
            self.assertIn(command, section)

    def test_no_first_person_blog_voice(self) -> None:
        banned = [
            r"\bI should\b",
            r"\bin my opinion\b",
            r"\bI've found\b",
            r"\blet's step back\b",
        ]
        for pattern in banned:
            self.assertIsNone(
                re.search(pattern, README, flags=re.IGNORECASE),
                f"hub should not use blog voice: {pattern}",
            )

    def test_related_gates_point_at_mess_family(self) -> None:
        section = self._section("## Related quality gates", None)
        for name in ("messgo", "messrust", "messpy", "messcript", "messharp", "messfsharp"):
            self.assertIn(f"quality-gates/{name}", section)

    def _section(self, start: str, end: str | None) -> str:
        start_pos = README.find(start)
        self.assertGreaterEqual(start_pos, 0, f"missing section {start}")
        if end is None:
            return README[start_pos:]
        end_pos = README.find(end, start_pos + 1)
        self.assertGreaterEqual(end_pos, 0, f"missing section end {end}")
        return README[start_pos:end_pos]


if __name__ == "__main__":
    suite = unittest.defaultTestLoader.loadTestsFromTestCase(HubContractTest)
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    sys.exit(0 if result.wasSuccessful() else 1)
