"""How dc-jerry is packaged as a Claude Code plugin.

dc-jerry is installed as a plugin: Claude reads its skills and agents from the plugin root and
runs the CLI from the user's project. These tests pin what that needs.
"""

from __future__ import annotations

import json
import re
import shutil
import subprocess
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent.parent
PLUGIN = json.loads((ROOT / ".claude-plugin" / "plugin.json").read_text())
MARKETPLACE = json.loads((ROOT / ".claude-plugin" / "marketplace.json").read_text())
HOOKS = json.loads((ROOT / "hooks" / "hooks.json").read_text())["hooks"]
CLI = 'uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry'


def _instruction_files() -> list[Path]:
    return sorted([*ROOT.glob("skills/**/*.md"), *ROOT.glob("commands/*.md")])


def test_every_cli_call_runs_from_the_users_project() -> None:
    """`--project` keeps the working directory, so a relative path to a project file resolves;
    `--directory` would move into the plugin root, and a bare `uv run jerry` only works inside
    a dc-jerry checkout. The root is quoted because plugin paths can contain spaces."""
    wrong = re.compile(r"uv run --directory \$\{CLAUDE_PLUGIN_ROOT\}|uv run jerry\b")
    offenders = [
        f"{path.relative_to(ROOT)}:{n}"
        for path in _instruction_files()
        for n, line in enumerate(path.read_text().splitlines(), 1)
        if wrong.search(line)
    ]
    assert offenders == []
    assert any(CLI in path.read_text() for path in _instruction_files())


def test_cli_reads_a_relative_path_from_another_project_without_warnings(tmp_path: Path) -> None:
    shutil.copy2(ROOT / "tests" / "fixtures" / "ast" / "ST-001-jerry-document.md", tmp_path / "story.md")
    result = subprocess.run(
        ["uv", "run", "--project", str(ROOT), "jerry", "ast", "frontmatter", "story.md"],
        cwd=tmp_path,
        capture_output=True,
        text=True,
        timeout=120,
    )
    assert result.returncode == 0, result.stderr
    assert json.loads(result.stdout)["Type"] == "story"
    assert "Failed to load patterns" not in result.stderr


def test_skills_are_invoked_under_the_plugin_name() -> None:
    offenders = [str(p.relative_to(ROOT)) for p in _instruction_files() if "/jerry:" in p.read_text()]
    assert offenders == []


def test_plugin_lists_exactly_the_agents_on_disk() -> None:
    on_disk = sorted(f"./{p.relative_to(ROOT)}" for p in ROOT.glob("skills/*/agents/*.md"))
    assert PLUGIN["name"] == "dc-jerry"
    assert sorted(PLUGIN["agents"]) == on_disk
    assert PLUGIN["commands"] == ["./commands/architect.md"]


def test_only_a_session_start_hook_that_starts_no_process() -> None:
    assert list(HOOKS) == ["SessionStart"]
    commands = [hook["command"] for entry in HOOKS["SessionStart"] for hook in entry["hooks"]]
    assert len(commands) == 1
    assert commands[0].startswith("echo ")
    assert "${CLAUDE_PLUGIN_ROOT}" in commands[0]


def test_marketplace_serves_this_plugin_from_the_repository_root() -> None:
    assert MARKETPLACE["name"] == "dc-jerry"
    [entry] = MARKETPLACE["plugins"]
    assert entry["name"] == PLUGIN["name"]
    assert entry["source"] == "./"
    assert entry["version"] == PLUGIN["version"]
