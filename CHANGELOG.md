# Changelog

All notable changes to the rule set. Versions follow `ruleset.yaml`.

## Site - 2026-11-25

Not a rule change (the rule set stays at 2.0.0). The Rule Set page template (`site/ruleset.html`) gets the current vibe-dashboard page patches, so the GitHub Pages site and the Claude copy keep them on every rebuild: a **hide TOC** button, a **back to top** button, separate **expand all** and **collapse all** buttons, an expand/collapse button on each section header that has collapsible parts, house-style tooltips instead of the browser's own, the bright silver colour for the Glossary and References badges, and the plumbing for diagram tooltips and the Source Document view.

## Tests - 2026-11-22

Not a rule change. Adds `tests/prompts/` (a test question and pass check for every active rule, plus three live tests on a Fusion design), the results format in `tests/results/`, a **Test result** issue form, and test kits for each AI (`tests/test-kit-<ai>.md` on the site). The build now warns about rules without a test and works out, from recorded results, which rules are backed as Proven.

## [2.0.0] - 2026-11-22

Adds Izzy's Symmetry & Mirror rules, first proposed as #29 to #29D (candidates C-2026-11-01 to 05), in a new category, **Symmetry & Mirror**. 39 active rules. A major version because a rule is retired and two change meaning.

- **Added** R36 Symmetry-First Modeling & Origin Body Mirroring (Must), R37 Exception Protocol for near-symmetrical parts (Should), R38 Full-Width Parameters & Half-Sketch Dimensioning (Must), R39 Multi-Component Mirroring & Handed Parts (Should), R40 Fillet Sequencing Across Mirror Planes (Should). All Untested until Phase 4 tests.
- **Deprecated** R17 Model symmetric parts as halves: R36 replaces it.
- **Changed** R06: on a symmetric part, the body mirror comes after the whole shared core. R18: on a symmetric part, intersect the half body before the mirror, never the full part. R38 (from Izzy's #29B): half-sketch dimensions use a Centerline or a half parameter defined in the user table, so R08 and R09 stay as they are. R35: example updated to the new count and version.

Review record: `sources/2026-11-21-izzy-symmetry-candidates.md`.

## Site - 2026-11-22

Not a rule change (the rule set stays at 1.0.0). The Rule Set page is now built from this repository and published on GitHub Pages: the same cards, Export Builder and how-tos, plus ready-made files for every AI, a clear *local draft* banner and tags for edits made in the browser, a *Propose on GitHub* button that turns those edits into a proposal, and a link from each card to its rule file and history.

## [1.0.0] - 2026-11-20

First release: 35 rules (R01 to R35) in 9 categories, drawn from the snow-thrower key sessions with Izzy on Thu Nov 19, 2026. Moved into this repository on 2026-11-22 from the Rule Set dashboard, unchanged.

Pending review (not part of the rule set): Izzy's Symmetry & Mirror candidates #29 to #29D, held as `C-2026-11-01` to `C-2026-11-05` (proposed IDs R36 to R40). See `candidates/2026-11-izzy-symmetry/`.
