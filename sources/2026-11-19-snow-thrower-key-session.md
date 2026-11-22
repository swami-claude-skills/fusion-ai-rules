# Snow-thrower key session (Thu Nov 19, 2026)

A three-hour session in which Swami and Izzy graded a 3D-printable snow-thrower ignition key that
the Autodesk Assistant had built in Fusion from a spec written with Gemini, then used the Assistant
to audit and clean up its parameters. Rules R01 to R35 (rule set v1.0.0) were drawn from it.

## What the AI got wrong, and the rules it led to

| What happened | Why | Rule |
|---|---|---|
| Guessed that the timeline count fell from 32 to 5 because "you may have switched documents" | Collapsed timeline groups appear as single items; the AI filled the gap with a plausible story instead of checking | R24 Check, don't guess; R30 Look inside timeline groups |
| Linked three 24 mm dimensions to `handle_length` because the numbers matched | Matching values is cheap; checking what a dimension measures needs a look at the sketch | R12 Link by meaning, not by value |
| First cleanup covered only the sketch dimensions; fillet radii and extrude distances kept literals | Its plan said "sketch dimensions" and nobody asked for features | R10 Parameterize features too; R29 Ask about scope |
| Reported driven (reference) dimensions as values it "couldn't identify", three times | It did not open the sketch to see they were driven | R25 Say when a dimension is driven |
| Flagged material and missing joints on a single-part model | The audit prompt asked for everything critical, with no context about use | R31 Skip what doesn't apply |
| Every dimension named, yet changing the handle length only thickened one wall | Names are not relationships; dependent features were not tied to their drivers | R20 Tie dependents to drivers; R14 Dimension design intent |
| Asked for "close to 22" features but never reported the count | Nobody asked it to report | R23 Report what you did |

## Habits that worked

- Say "don't take any actions till I say so" before an analysis, and ask for the plan first (R26).
- Apply the safest, geometry-neutral changes first, in batches (R27), and check an invariant such as volume after every batch (R28).
- Comment every parameter while the conversation is still in context (R07).
- Flex-test the key drivers by hand and watch what moves.

## Not in this repository

The recording, the Fusion file and the full chat exports stay private. This note keeps only what
the rules need.
