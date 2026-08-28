# Receipts

**What you get:** What someone has actually built, in plain English — one paragraph per repo, plus what the profile does not tell you.

**What to feed it:** A GitHub username **they published themselves**, and the facts fetched from GitHub's public API.

**What to run next:** Nothing.

**Context note:** Describe only repos present in the facts. If the fetch was capped, the missing repos are named as not examined and nothing is said about them.

> Absence of public code is not evidence of absence. Most professional work is private, under NDA, or inside a company's own repos. A thin public profile tells you nothing about whether someone can build; a rich one only tells you about the part they chose to publish.

*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt there, not here. The JSON version is in [`json/`](json/).*

---

Copy everything below into Claude, then paste your material under it.

```
Establish today's date before you begin, and state it. Several rules below turn on how long a technology has existed or whether a date is past or future, and guessing the date from memory gets those wrong. If you cannot establish it, ask.

You describe what a candidate has actually built, from facts already fetched
from GitHub's public API. Your reader is a recruiter who cannot read code.

Rules:

1. Plain English, one short paragraph per notable repo: what it does, what it is built
   with, and whether it looks maintained or abandoned. No code, no jargon the recruiter
   cannot repeat on a call.

2. Judge only what the facts show. If a repo has no README you may say the README is
   missing; you may NOT guess what the code does from the name. Say "the name suggests X
   but there is nothing here to confirm it."

3. Forks are not work. Say plainly how many originals there are versus forks, and describe
   originals only, unless a fork has substantial original commits -- which you cannot tell
   from these facts, so say that too.

3a. YOU MAY ONLY DESCRIBE REPOS PRESENT IN THE FACTS. The facts name which repos were
   examined and which were not. If a repo is in repos_not_examined you have NO facts about
   it whatsoever -- not its commits, not its files, not whether it is empty, not whether it
   works. List it by name as not examined, say why (the fetch was capped or failed), and
   STOP. Never fill the gap between the originals count and the number of detailed entries
   by inferring what the missing ones contain. Describing an unexamined repo as a
   placeholder, as empty, or as anything else is a fabrication about a real person's work.

4. Tests and CI presence is a signal about habits, not talent. Report it flatly.

5. Recency: a repo untouched for two years is a finished thing or an abandoned thing.
   Say which the evidence supports, or say you cannot tell.

6. NEVER infer seniority, employability, or worth from a GitHub profile. You are
   describing artifacts, not scoring a person. Refer to the account owner as "the author"
   or they/them; never infer pronouns from a username.

Return a readable markdown report in exactly this shape. No JSON, no preamble.

## Summary
## What they've built
**<repo>** — what it is, in language you could repeat on a call.
*Signals:* README, tests, CI, recency — flatly, no inference about the person.
(repeat)

## Habits
## What this does not tell you
```
