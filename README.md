# dc-jerry

A Claude Code plugin for project-based work: work tracking, structured problem-solving,
architecture decisions, NASA-style systems engineering, multi-agent orchestration and adversarial
review. It is a trimmed fork of the [Jerry Framework](https://github.com/geekatron/jerry); see
`UPSTREAM.md` for what was kept and changed.

## Requirements

- [Claude Code](https://code.claude.com/docs)
- [`uv`](https://docs.astral.sh/uv/) on `PATH` (`brew install uv`, or `winget install astral-sh.uv`).
  The first CLI call creates `.venv` in the plugin folder and installs its packages from PyPI.

## Install

```sh
claude plugin marketplace add puneetsharma2791/dc-jerry
claude plugin install dc-jerry@dc-jerry
```

A repository can offer it to everyone who opens it, in its committed `.claude/settings.json`:

```json
{
  "extraKnownMarketplaces": {
    "dc-jerry": { "source": { "source": "github", "repo": "puneetsharma2791/dc-jerry" } }
  },
  "enabledPlugins": { "dc-jerry@dc-jerry": true },
  "env": { "JERRY_PROJECT": "PROJ-001-your-project" }
}
```

## Skills

| Skill | Use |
|-------|-----|
| `/dc-jerry:worktracker` | Epics, features, stories, tasks, enablers and bugs in `projects/<id>/WORKTRACKER.md` |
| `/dc-jerry:problem-solving` | Research, analysis, root cause, review and synthesis through nine agents |
| `/dc-jerry:architecture` | Hexagonal, DDD and CQRS guidance, ADRs and diagrams |
| `/dc-jerry:adversary` | Adversarial review and quality scoring of a finished deliverable |
| `/dc-jerry:nasa-se` | Requirements, V&V, risk, trade studies and technical reviews |
| `/dc-jerry:orchestration` | Multi-phase, multi-agent workflows with state across sessions |
| `/dc-jerry:ast` | Read, validate and modify the frontmatter of work-item files |
| `/dc-jerry:architect` | Command: write a plan into the project before implementing |

Projects live in the repository that uses the plugin, under `projects/<PROJ-NNN-slug>/`;
`JERRY_PROJECT` names the active one.

## CLI

Claude runs the CLI from the project as `uv run --project "<plugin root>" jerry <command>`; a
session-start hook prints the plugin root. From a terminal, use the path of a clone:

```sh
uv run --project ~/src/dc-jerry jerry ast frontmatter projects/PROJ-001-x/WORKTRACKER.md
uv run --project ~/src/dc-jerry jerry ast validate <file> --schema story
```

## Development

```sh
uv run pytest
```

## Licence

Apache-2.0. See `LICENSE`, `NOTICE` and `UPSTREAM.md`.
