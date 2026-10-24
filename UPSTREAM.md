# Upstream

dc-jerry is a modified copy of the Jerry Framework, https://github.com/geekatron/jerry, licensed
under the Apache License, Version 2.0 (see `LICENSE` and `NOTICE`). It is not affiliated with or
endorsed by the upstream project.

- Imported from tag `v0.31.9`, commit `4aff242854ebb1bc74208991901b88c559be5a19`.
- The first commit of this repository holds the imported files byte-identical to that tag; every
  later change is in the history after it.

## Not imported

The skills other than worktracker, problem-solving, adversary, architecture, ast, nasa-se and
orchestration (and `skills/shared`), with their agents; upstream's own `projects/`; `docs/` except
`docs/governance/JERRY_CONSTITUTION.md` and `docs/schemas/`; the documentation site (`mkdocs.yml`,
`overrides/`, `CNAME`, `.nojekyll`); `.github/`; `.claude/`; `runbooks/`; `commands/release.md`;
`AGENTS.md`, `CLAUDE.md`, `CHANGELOG.md`, `CODE_OF_CONDUCT.md`, `CONTRIBUTING.md`,
`GOVERNANCE.md`, `SECURITY.md`, `SOUNDTRACK.md` and `TOOL_REGISTRY.yaml`.

## Changes

This list is the notice of modification that section 4(b) of the licence requires; the files
below have been changed from geekatron/jerry v0.31.9.

- **Plugin name and manifests:** the plugin and its marketplace are named `dc-jerry`, version
  0.1.0, listing only the kept agents and `commands/architect.md`:
  `.claude-plugin/plugin.json`, `.claude-plugin/marketplace.json`.
- **Hooks:** the six upstream hooks, which start `uv` at session start, on every prompt, before
  every tool call, before compaction, after subagents and at stop, are replaced by one
  SessionStart `echo` that names the plugin root and the CLI form: `hooks/hooks.json`. The six
  wrapper scripts in `hooks/` are removed.
- **CLI calls:** `uv run --directory ${CLAUDE_PLUGIN_ROOT} jerry ...` and `uv run jerry ...`
  become `uv run --project "${CLAUDE_PLUGIN_ROOT}" jerry ...`, so the CLI runs from the user's
  project and relative paths resolve; `/jerry:` skill names become `/dc-jerry:`:
  `skills/ast/SKILL.md`, `skills/worktracker/SKILL.md`,
  `skills/adversary/agents/adv-executor.md`, `skills/adversary/agents/adv-scorer.md`,
  `skills/nasa-se/agents/nse-requirements.md`, `skills/nasa-se/agents/nse-reviewer.md`,
  `skills/problem-solving/agents/ps-critic.md`, `skills/problem-solving/agents/ps-reviewer.md`,
  `skills/problem-solving/agents/ps-validator.md`, `skills/worktracker/agents/wt-auditor.md`,
  `skills/worktracker/agents/wt-verifier.md`, `skills/worktracker/agents/wt-visualizer.md`,
  `skills/worktracker/composition/wt-auditor.prompt.md`,
  `skills/worktracker/composition/wt-verifier.prompt.md`,
  `skills/worktracker/composition/wt-visualizer.prompt.md`.
- **Pattern library path:** the CLI looked for its own `scripts/patterns/patterns.yaml` under the
  project it runs in, so every call from a user's project logged "Failed to load patterns"; it now
  reads the file from its own folder: `src/bootstrap.py`.
- **Tests:** tests that covered only what was not imported, or the removed hook scripts, are
  removed; tests that read upstream's `CLAUDE.md`, `AGENTS.md`, `.claude/` or CI are cut; the
  markdown discovery floor drops from 2500 files to 150 and `UPSTREAM.md` joins its list of
  unclassified files; the AST CLI tests read their story from
  `tests/fixtures/ast/` (moved unchanged from upstream's `projects/PROJ-005-markdown-ast/`); an
  allowlist test whose sample entry expired on 2026-08-30 now uses 2099 dates; the CLI-form test
  expects `--project`; the keyword test looks up `dc-jerry`:
  `tests/architecture/test_ast_enforcement.py`,
  `tests/architecture/test_session_hook_architecture.py`,
  `tests/contract/test_plugin_manifest_validation.py`,
  `tests/e2e/test_adversary_templates_e2e.py`,
  `tests/e2e/test_progressive_disclosure_crossrefs.py`,
  `tests/e2e/test_quality_framework_e2e.py`, `tests/integration/cli/test_ast_subprocess.py`,
  `tests/integration/test_document_type_regression.py`,
  `tests/schemas/test_frontmatter_schemas.py`, `tests/security/test_audit_allowlist.py`.
- **New:** `tests/architecture/test_plugin_packaging.py`, `UPSTREAM.md`; `README.md` is
  rewritten and `NOTICE` gains a line for these modifications.
