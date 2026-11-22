# Tests

How each rule is tested in each AI. The build checks these files and turns them into test kits and a results matrix.

- `prompts/` - one YAML file per test: `id` (`T-R08-01`, or `T-LIVE-01` for tests on a live Fusion design), `rules` (the rule IDs it checks), `prompt` (what to ask the AI with the rules loaded), `good_answer` (what a passing answer says), `needs_fusion` (true if the AI must be working on an open Fusion design).
- `results/` - one YAML file per test session, named `YYYY-MM-DD-<ai>-<tester>.yaml`: `date`, `ai` (`aa`, `gpt`, `claude`, `gem`), `surface`, `model`, `ruleset_version`, `tester`, and `results`, a list of `test`, `result` (`pass`, `fail`, `partial`, `n/a`) and `notes`.
- `parts/` - benchmark parts with a checklist of what a correct model looks like (to come).

## Running a test

Download the test kit for your AI (`tests/test-kit-<ai>.md`, linked from the Rule Set page's Test Your AI section and in each release), load the rules, ask each question, and report the filled-in results block with the **Test result** issue form. A maintainer saves it in `results/`.

## How results set a rule's status

For each rule and AI, the latest result of any test that covers the rule counts. A rule is backed as **Proven** when every AI it applies to has a recorded pass, and **Failed once** after any failure. The Rules Admin page lists every rule whose `status` doesn't match its results, so the status can be updated in a pull request.
