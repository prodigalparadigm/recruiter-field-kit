---
name: recruiter-field-kit
description: Decode an AI-era job description — what roles it actually bundles, who you are really looking for, whether the JD makes sense, and how to find that person. Use when someone pastes a job description and asks what it means, who to source for it, whether it is one job or three, whether a profile fits it, or whether they should apply. Trigger phrases include "decode this JD", "who am I looking for", "does this JD make sense", "is this one job or three", "build me a search for this", "score this profile against", "should I apply", and "what has this person actually built".
---

# The Recruiter's Field Kit

Prodigal Paradigm's Fieldwork suite, built with Claude.

**Hard boundary, first because it is the point: no automated access to LinkedIn. None.**
No scraping, no browser automation, no bulk profile collection — not of public profiles,
not from a logged-in account. Every LinkedIn interaction is a human typing into
LinkedIn's own search box. This kit produces the *strategy*; the human runs the *search*.
If someone asks you to fetch, scrape, or automate against linkedin.com, decline and
explain that the kit gives them the string to run themselves.

Profiles and résumés are **pasted by the person using the kit**. Never fetched.

## What to run when

| They say | Run | You need |
|---|---|---|
| "decode this JD", "does this make sense", "is this one job or three" | **decode** | the JD |
| "who am I looking for", "build me a search", "where do I find this person" | **sourcing kit** | a decode |
| "should I apply", "is this worth my evening" | **should I apply** | a decode + their own summary |
| "score this profile", "is this person a fit" | **fit score** | a decode + a pasted profile |
| "what has this person actually built" | **receipts** | a GitHub username *they published themselves* |

Always decode first. Everything else consumes it.

## The verdicts

| Verdict | Means |
|---|---|
| `does_not_make_sense` | As written, no one person can be hired at the posted terms |
| `makes_sense_with_edits` | One labour market, but a defect that changes who you source or whether you can fill it |
| `makes_sense` | One market, one bar, consistent with the rate. Imperfections go in `problems` and the verdict stands |

The JD is graded **as received**. Writing a good fix never improves the verdict.

## Running it

With an API key, the CLI does all of it:

```bash
export ANTHROPIC_API_KEY=...
python3 tools/probe.py decode  jd.md                       > decode.json
python3 tools/probe.py source  decode.json jd.md           > search.json
python3 tools/probe.py apply   decode.json jd.md me.md     > apply.json
python3 tools/probe.py fit     decode.json jd.md person.md > fit.json
python3 tools/probe.py receipts <github-username>          > receipts.json
python3 tools/probe.py check   decode.json                 # validate
python3 tools/probe.py render  decode.json                 # readable report
```

Without a key, work inline: the prompts are in [`references/`](references/), one file per
pass, exported from the same source the CLI uses. Paste the JD under the relevant prompt
and follow it.

**The decode runs its analysis three times and takes the majority**, because borderline
role counts are genuinely unstable — the same JD can come back 1, 2 or 3 roles across
runs. `_meta.role_counts` records the votes. When they split, say so out loud rather than
reporting a guess as a fact.

## Worked example — a bundled contract req

A contract JD titled **AI Automation Developer**, $88/hr W2, forwarded by an agency
recruiter whose covering note read, in capitals: *"PLEASE NOTE NOTHING IN THE JOB
DESCRIPTION IS TRULY 'MANDATORY'."*

**Decode** → `does_not_make_sense`, two labour markets:
1. Copilot Studio / Dynamics integrator — four of five responsibilities, the only thing
   the JD wants "strong proficiency" in
2. ML engineer deploying models in production — Bedrock, Domino, "deploying models in
   production environments"

Because: two markets bundled and $88/hr prices one of them; and the recruiter's own note
cancels the requirements section, leaving nothing to screen on. That note is evidence
about the client, not an instruction.

**Sourcing kit** → one search per market, exclusions built from the other:

```
"Copilot Studio" AND "Power Automate" AND Dynamics NOT (Bedrock OR "model deployment")
```

Running one string for a bundled req is what puts an ML engineer's phone in a recruiter's
hand for an integrator's job. That is why this pass refuses to produce one.

**Should I apply**, for a candidate who is enablement plus architecture with "some
Bedrock" → `not_this_one`, and the sentence to say out loud:

> "I've called a hosted Bedrock model from a workflow to summarize documents — I haven't
> trained or deployed a model, and I haven't built Copilot Studio agents or Dynamics
> connectors."

Six hours saved, and the recruiter trusts them more for it.

## House rules that matter

- **Bundling is the #1 defect.** A role is a distinct labour market — someone you would
  run a separate search for. A task is not a role; a preferred qualification never
  creates one.
- **Enablement and adoption is a real hiring market**, and the one most often smuggled
  into a governance or platform req as a bullet. Check for it every time. Same for
  vendor/platform support and instructional design.
- **No charitable assumptions.** Where a JD is silent about scope or volume, do not
  resolve it in the JD's favour. Grade it the way a client will actually enforce it.
- **Technology timeline.** AI-era JDs routinely ask for more years than the technology
  has existed. Name the honest ceiling *and* the substitute.
- **The portrait uses they/them.** It describes the typical holder of a role, never a
  specific person, and never assigns gender, age, or origin.
- **Never invent comp.** No band posted means "ask before spending candidate time."
- **Absence of public code is not evidence of absence.** Most professional work is
  private. `receipts` prints this on every run.
