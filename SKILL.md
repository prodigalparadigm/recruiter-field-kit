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

## How to run this skill

**Read the reference file for the pass you need, and follow it exactly as written.** The
house rules further down are orientation for choosing a pass — they are a summary, not the
pass. The real rules live in the reference files and they are much longer than what is in
this document. Never work a pass from memory or from the summary below.

| They say | Read and follow | You need |
|---|---|---|
| "decode this JD", "does this make sense", "is this one job or three" | `references/01-decode-analysis.md`, then `references/02-decode-compose.md` | the JD |
| "who am I looking for", "build me a search", "where do I find this person" | `references/03-sourcing-kit.md` | the JD + a decode |
| "should I apply", "is this worth my evening" | `references/04-should-i-apply.md` | a decode + their own summary |
| "score this profile", "is this person a fit" | `references/05-fit-score.md` | a decode + a pasted profile |
| "what has this person actually built" | `references/06-receipts.md` | a GitHub username *they published themselves* |

Always decode first — everything else consumes a decode. A decode is two passes: run 01,
then feed its output to 02. Do not stop after 01 and present it as a finished decode.

`references/json/` holds the same passes with a JSON output contract, for wiring into code.
For a person, use the markdown versions.

## Say when you are guessing

The CLI runs the analysis three times and takes the majority, because borderline role
counts are genuinely unstable — the same JD came back 1, 2 and 3 roles across runs of an
identical prompt. **You cannot reproduce that by sampling yourself three times in one
context; that is correlated, not independent, and it would be theatre.**

Do this instead: when a role count is borderline — when you seriously considered a
different answer, or the merge and delete tests disagreed — say so in the output. "This
reads as two markets, but the enablement strand is arguable as a third" is worth more to a
recruiter than a confident number. The votes were never the point; knowing when it is a
coin flip was.

## Context hygiene

- **Decode and fit score must see only what they are given** — the JD, the decode, the
  pasted profile. If memory surfaces the user's own background during a decode or a fit
  score, ignore it. A decode contaminated by the reader's history describes the reader.
- **Should I apply is the exception**: there, recalling the user's own background is the
  whole point.
- **Never fetch a profile or résumé.** The person pastes it, or you do not have it.

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
- **Pronouns are never inferred.** Use the pronouns a person's own document states;
  where none are stated, use they/them. This holds in every pass that describes a
  person, and it matters most in the sentence a recruiter forwards to a client. The
  decode's portrait is always they/them — it describes the typical holder of a role,
  not a person, and never assigns gender, age, or origin.
- **Never describe a repo nobody fetched.** If receipts was capped, the missing repos
  are named as unexamined and nothing is said about their contents.
- **Never invent comp.** No band posted means "ask before spending candidate time."
- **Absence of public code is not evidence of absence.** Most professional work is
  private. `receipts` prints this on every run.
