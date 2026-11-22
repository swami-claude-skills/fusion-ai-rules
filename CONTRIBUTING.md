# Contributing

Thanks for helping make AI modeling in Fusion more reliable.

## Ways to contribute

1. **Propose a rule**: use the "Propose a rule" issue form. Swami (or Claude, on his behalf) turns accepted proposals into candidate files.
2. **Report a rule failing**: use "A rule failed in an AI". These reports drive each rule's status (Proven, Failed once).
3. **Pull request**: add a file to `candidates/<YYYY-MM-short-name>/` named `C-YYYY-MM-NN-short-title.yaml`, following `schema/rule.schema.json`. Do not add files to `rules/` directly; accepted candidates move there with a new R number during review.

## Review

Candidates are reviewed in batches. Each batch gets a review page (verbatim text, how it maps to existing rules, conflicts and gaps). A candidate that conflicts with an existing rule cannot be accepted until the conflict is resolved: one rule is reworded, or the old rule is deprecated or superseded.

Only the repository owner merges to `main` (see `.github/CODEOWNERS`).

## Rules for rule files

- One rule per file. Keep `rule` short enough to paste into a chat; put the reasoning in `why`.
- IDs are never reused. Removing a rule means `status: Deprecated` plus `deprecated_in`.
- Run `pip install pyyaml jsonschema && python3 build/build.py check` before opening a pull request.
- Nothing confidential: no client names, private files or NDA material in rules, sources or tests.

## Licence of contributions

By contributing you agree that your contribution is published under CC BY 4.0 (rules and text) or MIT (code), with credit in the rule's `authors` field.
