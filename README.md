# The Recruiter's Field Kit

**Prodigal Paradigm's Fieldwork suite, built with Claude.** A decoder for technical
recruiters reading AI-era job descriptions. **Hard boundary, stated first because it is
the point: this kit makes no automated access to LinkedIn. None.** No scraping, no browser
automation, no bulk profile collection — not of public profiles, not from a logged-in
account. It breaches the LinkedIn User Agreement and it is what accounts get restricted
for. Every LinkedIn interaction here is a human typing into LinkedIn's own search box: the
kit produces the *strategy*, the human runs the *search*. Profiles and résumés are pasted
by the person using the kit, never fetched. The only network calls it makes are to the
Anthropic API and to GitHub's public API — CI enforces that on every push.

## The problem

Recruiters are handed AI-era JDs written by people who don't know what they're asking for,
and sent to people who don't know how to read them. Then "some Bedrock, I've touched AWS"
turns up on the phone and there's no way to know whether that's a yes. Meanwhile the
candidate on the other end can't tell whether the JD is one job or three.

---

## How to use it

### 1. Paste a prompt into Claude — no install, no key, no terminal

**This is the way most people should use this.** Everything the kit does is a prompt.
Open [`references/01-decode-analysis.md`](references/01-decode-analysis.md), copy the
block inside the code fence, paste it into Claude, then paste the job description under
it. You get the decode back as JSON.

The other five passes work the same way, and each one tells you what to feed it:

| File | Does | Feed it |
|---|---|---|
| [`01-decode-analysis.md`](references/01-decode-analysis.md) | roles, skills, seniority, verdict | the JD |
| [`02-decode-compose.md`](references/02-decode-compose.md) | screening questions + the client email | the JD + the analysis |
| [`03-sourcing-kit.md`](references/03-sourcing-kit.md) | Boolean strings, one per market | the JD + the decode |
| [`04-should-i-apply.md`](references/04-should-i-apply.md) | the candidate's answer | the decode + your own summary |
| [`05-fit-score.md`](references/05-fit-score.md) | one profile scored | the decode + a pasted profile |
| [`06-receipts.md`](references/06-receipts.md) | what someone has actually built | GitHub facts |

### 2. Install it as a Claude Skill

Put this repo where your Claude reads skills from and [`SKILL.md`](SKILL.md) wires up all
six tools with trigger phrases — "decode this JD", "is this one job or three", "build me a
search for this", "should I apply". Claude picks the right pass itself instead of you
choosing a file.

### 3. Run the CLI

For batch work, tuning, or testing against fixtures. Needs Python 3.12 and an Anthropic
API key.

```bash
export ANTHROPIC_API_KEY=...
pip install anthropic

python3 tools/probe.py decode   jd.md                       > decode.json
python3 tools/probe.py source   decode.json jd.md           > search.json
python3 tools/probe.py apply    decode.json jd.md me.md     > apply.json
python3 tools/probe.py fit      decode.json jd.md person.md > fit.json
python3 tools/probe.py receipts <github-username>           > receipts.json

python3 tools/probe.py check    decode.json   # validate against the schema
python3 tools/probe.py render   decode.json   # readable markdown report
```

`receipts` uses GitHub's public API unauthenticated (60 requests/hour); set `GITHUB_TOKEN`
for 5,000.

---

## What the decode tells you

Every role the JD bundles, which one the day-to-day actually is, skills sorted by how the
JD *uses* them, a portrait of the person who holds this job, ten-minute screening
questions with a real-answer and a bluff example for each, and a blunt verdict with a fix
you can send to the client.

| Verdict | Means |
|---|---|
| `does_not_make_sense` | As written, no one person can be hired at the posted terms |
| `makes_sense_with_edits` | One labour market, but a defect that changes who you source or whether you can fill it |
| `makes_sense` | One market, one bar, consistent with the rate |

The JD is graded **as received** — writing a good fix never improves the verdict. And
`makes_sense` is reachable on purpose: wide scope, an admitted backlog, optimistic
nice-to-haves and a weak title are `problems`, not demotions. A demanding job is not a
broken job.

## How the decode is built

**Two passes.** The analysis pass decides roles, skills, seniority and verdict. A second,
short pass writes the questions and the client email from that analysis. They are split
because eleven analytical rules and two formatting rules in one prompt meant the
formatting rules kept losing — ranked-bar compliance went from 8/10 to 10/10 on the split.

**Three votes.** Borderline role counts are genuinely unstable: the same JD came back 1, 2
and 3 roles across runs of an identical prompt. The analysis runs three times and the
majority wins, on the count and then on the verdict. `_meta.role_counts` records the
votes, and `check` prints `[split vote …]` when they disagreed — the tool says when it is
guessing.

## The sourcing kit refuses to give you one search

A bundled req run as one Boolean string is why an ML engineer's phone rings about an
integrator's job. So the sourcing pass emits one search **per labour market**, and builds
each market's exclusions from the *other* markets in the same JD:

```
"Copilot Studio" AND "Power Automate" AND Dynamics NOT (Bedrock OR "model deployment")
```

Every string is checked before you see it — balanced parentheses, uppercase operators,
quoted phrases, term count against free-tier truncation, no dangling operators — and
failures are fed back for correction rather than handed over broken. A string that doesn't
parse wastes a search you can't get back.

## What this is calibrated against

The decode is tuned to **one practitioner's judgment** — an agency-side recruiter and AI
adoption consultant who rated ten real job descriptions before seeing the tool's answers.
On role counts it agrees with that reading 8 times out of 10, up from 2 out of 6 when the
comparison started.

That is worth stating plainly rather than implying general calibration it doesn't have.
Every house rule below came out of a disagreement with that reader, which means the rules
encode how one experienced recruiter reads a req — not a consensus, and not a survey. If
your read differs, the rules are in `tools/probe.py` in plain English and the fixtures are
in `tests/`; disagreeing with them is a matter of editing a paragraph and a sidecar.

Role counts on genuinely bundled reqs also vary run to run. The CLI runs the analysis three
times and takes the majority; `_meta.role_counts` records the votes and `check` prints
`[split vote …]` when they disagreed. On the skill path there is no voting, and Claude is
told to say when a count is a coin flip rather than report a guess as a fact.

## Fixtures

Fixtures are fed **verbatim**. Expectations live in a sidecar `<fixture>.expected.json`,
never inside the fixture — a fixture that states its own answers grades its own homework.

Live decodes are recorded to `tests/recorded/` and committed so CI validates the prompt's
last known-good output without an API key. Tune on Sonnet for speed.


**Each fixture defends one rule** — it exists because it is the case that taught the rule,
and its sidecar asserts the thing that would break if the rule eroded:

| Fixture | Defends |
|---|---|
| `finserv_ai_automation_developer` | bundling: two markets at a rate that prices one |
| `healthinsurer_ai_governance_lead` | enablement is its own labour market |
| `oem_enablement_program_lead` | capacity is not skill adjacency |
| `enterprise_ai_training_specialist` | technology timeline: name the ceiling *and* the substitute |
| `consultancy_ai_architect` | authority mismatch, as distinct from bundling |
| `saas_platform_support_engineer` | the floor under `makes_sense` (synthetic control) |

Assertions are scoped to where the rule says the reasoning belongs. A rule that says "put
it in problems" is checked in `problems` — a document-wide search passes on incidental
mentions and defends nothing. Every one of these was verified by deliberately eroding the
rule and confirming the fixture fails.

## House rules that took a session to learn

- **Bundling is the #1 defect.** A role is a distinct labour market — someone you would
  run a separate search for. A task is not a role, a hat is not a role, and a preferred
  qualification never creates one. Test it three ways: would one person commonly hold
  both; delete this section and is it still the same hire; could one person carry all of
  it at the posted terms.
- **Enablement and adoption is a real hiring market** — and the one most often smuggled
  into a governance or platform req as a bullet, because whoever wrote the req doesn't
  think of it as a job. Same for vendor support and instructional design.
- **No charitable assumptions.** Where a JD is silent about scope or volume, don't resolve
  it in the JD's favour. Grade it the way a client will actually enforce it. The recruiter
  is the one who pays for the optimistic reading.
- **Technology timeline.** AI-era JDs routinely ask for more years than the technology has
  existed. Name the honest ceiling *and* the substitute.
- **Authority mismatch** is its own defect, separate from bundling: some roles need
  standing that a short cheap contract cannot confer, however coherent the role is.
- **The portrait uses they/them**, describes the typical holder of a role rather than a
  person, and never assigns gender, age, or origin. In a sourcing tool, a gendered
  portrait primes the recruiter before they open a single profile.
- **Never invent comp.** No band posted means "ask before spending candidate time."
- **Absence of public code is not evidence of absence.** Most professional work is
  private. `receipts` prints that on every run, errors included.

## Licence

MIT. See [LICENSE](LICENSE).
