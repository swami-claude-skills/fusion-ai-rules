# Izzy's Symmetry & Mirror candidates (#29 to #29D)

Submitted Sat Nov 21, 2026. Reviewed in Phase 3 and accepted into rule set 2.0.0 as R36 to R40 (see Decisions below).
Izzy's own numbers clash with existing rule IDs (R29 already exists), so they carry C- IDs here,
keep Izzy's label under `source.author_label`, and show the R number they would get under `proposed_id`.


## Conflicts to resolve before accepting

### Feature mirrors vs. body mirrors

Candidates R36 vs rules R06, R17.

Izzy's #29 and its checklist allow only Mirror (Bodies, Join) across an origin plane, after the whole shared core, and never Features. R17 allows "the feature or body", and R06 places a mirror right after each feature it mirrors.

Options: Reword R06 and R17 to match #29; Leave R17 out (R36 replaces it).

### Intersect cuts

Candidates R36 vs rules R18.

Izzy's #29 says never carve a full symmetric part with "duplicate or intersect cuts". R18 recommends one intersect over several cuts when the intent is to keep a shape.

Options: Scope R18 to the half body; Leave R18 out.

### Math in half-sketch dimensions

Candidates R38 vs rules R08, R09.

Izzy's #29B allows a half-span sketch dimension of <param_name> / 2. R08 says never put math in a model (d###) parameter expression, and R09 keeps all arithmetic in the user parameter table.

Options: Centerline only (edit R38); Allow / 2 (edit R08 and R09).

## Decisions (Sun Nov 22, 2026)

| Candidate | Izzy's label | Became | Notes |
|---|---|---|---|
| C-2026-11-01 | #29 | R36 (Must) | Supersedes R17, which is deprecated. |
| C-2026-11-02 | #29A | R37 (Should) | Unchanged. |
| C-2026-11-03 | #29B | R38 (Must) | Half-sketch dimensions use a Centerline, or a derived user parameter; no `/ 2` typed into a sketch. |
| C-2026-11-04 | #29C | R39 (Should) | Unchanged. |
| C-2026-11-05 | #29D | R40 (Should) | Unchanged. |

Conflicts resolved:

- **Feature mirrors vs. body mirrors:** R17 is deprecated (R36 replaces it). R06 now says that on a symmetric part the body mirror comes after the whole shared core.
- **Intersect cuts:** R18 is scoped: on a symmetric part, intersect the half body before the mirror, never the full part.
- **Math in half-sketch dimensions:** R38 now uses a Centerline, or a half parameter defined in the user table as a formula of the full width. R08 and R09 are unchanged.

Izzy agreed on Sun Nov 22, 2026 to publish the five rules under CC BY 4.0, with credit as author.

All five are a new category, Symmetry & Mirror, with status Untested until tested in each AI (Phase 4).
