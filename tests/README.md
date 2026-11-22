# Tests

How rules are tested against each AI (Phase 4 of the plan fills this in).

- `prompts/` - one YAML file per test: `id` (e.g. `T-R17-01`), `rule`, `prompt` (what to ask the AI with the rules loaded), `good_answer` (what a passing answer contains), `needs_fusion` (true if the AI must be connected to a live Fusion model).
- `results/` - one YAML file per test run: `test`, `ai`, `model`, `fusion_version`, `ruleset_version`, `date`, `result` (pass, fail, n/a), `notes`.
- `parts/` - benchmark parts (the snow-thrower key first) with a checklist of what a correct model looks like.

A rule's `status` follows its results: Proven after a pass in each AI it applies to, Failed once after any failure that a person had to catch.
