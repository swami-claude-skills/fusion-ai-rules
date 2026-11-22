# Fusion AI Rules

Good-practice rules to give an AI **before it models in Autodesk Fusion** ("vibe modeling"): naming, timeline, parameters, sketches, features, robustness, reporting, and how to work with the AI. One rule set, exported in the right format for **Autodesk Assistant, Claude, ChatGPT and Gemini**.

- **Download the rules (no account needed):** https://swami-claude-skills.github.io/fusion-ai-rules/
- **Latest release:** see [Releases](../../releases); every file is stamped with the rule-set version.
- **Rule Set dashboard (cards, filters, Export Builder):** https://claude.ai/artifact/L3KyH8YpFuRxALRsjo4qQp

## Use the rules in your AI

| AI | Where the rules go | File |
|---|---|---|
| Autodesk Assistant (in Fusion) | Paste as the first message of each new chat | `targets/aa-chat/fusion-rules-autodesk-assistant.txt` |
| Claude (claude.ai, Desktop) | Upload as a skill, or add to a project's knowledge | `skill/fusion-modeling-rules/SKILL.md` or `fusion-modeling-rules.md` |
| Claude Code | `CLAUDE.md` in your add-in or script folder | `CLAUDE.md` |
| ChatGPT | A Project file, a custom GPT, or (short version) custom instructions | `fusion-modeling-rules.md`, `targets/gpt-ci/...` |
| ChatGPT Codex | `AGENTS.md` in the repository root | `AGENTS.md` |
| Gemini app | A Gemini skill file, or (short version) Saved info | `fusion-modeling-rules.md`, `targets/gem-saved/...` |
| Gemini CLI | `GEMINI.md` in the project folder | `GEMINI.md` |
| Any API | System prompt | `fusion-modeling-rules.txt` or `.json` |

Every target in [`targets.yaml`](targets.yaml) gets its own file under `targets/` in each release, trimmed to fit that place's size limit. After loading the rules, ask the AI *"Which Fusion modeling rule-set version do you have?"* to confirm it took.

## How this repository works

| Path | Holds |
|---|---|
| `rules/` | One YAML file per accepted rule (`R01-...yaml`). IDs are permanent and never reused. |
| `candidates/` | Proposed rules waiting for review (`C-YYYY-MM-NN`), one folder per batch. |
| `categories.yaml`, `targets.yaml`, `ruleset.yaml` | Categories, export targets and selections, rule-set name and version. |
| `schema/rule.schema.json` | What a rule file must contain. Checked on every pull request. |
| `build/build.py` | Validates everything and writes every export (`python3 build/build.py build`). |
| `tests/` | Test prompts and recorded results per AI. |
| `sources/` | Short notes on the sessions and chats the rules came from. |

On every merge to `main`, a GitHub Action validates the rules, builds the exports, publishes the download page, and, if `ruleset.yaml` has a new version, creates a release.

### Rule fields

`id`, `title`, `category`, `priority` (Must, Should, Nice to have), `status` (Proven, Failed once, Untested, Candidate, Deprecated), `rule`, `why`, `good`, `avoid`, `works` (per AI: 2 applies, 1 only when the AI is connected to the live Fusion model or writing a script, 0 does not apply), `scope`, `conflicts_with`, `supersedes`, `related`, `source`, `authors`, `reviewers`, `added_in`, `changed_in`, `tests`.

### Versions

`ruleset.yaml` holds the version. Patch = wording fix; minor = new rule or target; major = a rule removed, its meaning changed, or raised to Must.

## Contributing

Propose a rule or report one failing with the [issue forms](../../issues/new/choose), or open a pull request. See [CONTRIBUTING.md](CONTRIBUTING.md).

## Licence

Rules and documentation: [CC BY 4.0](LICENSE-CONTENT.md). Code: [MIT](LICENSE). Credit: Swami and contributors.
