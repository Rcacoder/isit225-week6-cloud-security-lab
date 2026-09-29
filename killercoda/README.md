# Killercoda backup scenario (not published — import manually)

This folder is a ready-to-import Killercoda scenario, kept as a **backup**
for if `github.dev` (the git version's editor) is blocked on campus. I don't have a
Killercoda account, and Killercoda has no API for publishing a scenario, so
this could not be published automatically — someone with a Killercoda
account needs to import it by hand (takes about 5 minutes):

1. Go to killercoda.com → your account → **New Scenario**.
2. Use the **Editor** (or the "import from files" option if your account has
   it) and copy each file below into the matching field: `index.json` sets
   the steps and metadata; `intro.md`, `step1.md`, `step2.md`, `step3.md`,
   `finish.md` are the page text for each step; the `*-verify.sh` scripts are
   the green-checkmark step validators.
3. This scenario's format follows Killercoda's documented scenario schema as
   of when this was written. If Killercoda has changed their `index.json`
   fields since, adjust field names to match — the step content and verify
   logic underneath don't need to change.
4. **Test it yourself once after importing** — this was written and reasoned
   through, but never run against real Killercoda infrastructure, so check
   each step's verifier actually goes green before handing it to students.

## What it covers

A different but topically matched exercise to the git version:
hardening a Docker container instead of a Terraform-style config file —
closer to what Killercoda's Linux/container backend is good at. Students fix
a Dockerfile that runs as root with a hardcoded secret and no resource
limits, then write the same kind of risk register as the primary lab.
