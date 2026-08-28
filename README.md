# The Recruiter's Field Kit

**Prodigal Paradigm's Fieldwork suite, built with Claude.** A decoder for technical
recruiters reading AI-era job descriptions. **Hard boundary, stated first because it is
the point: this kit makes no automated access to LinkedIn. None.** No scraping, no browser
automation, no bulk profile collection — not even of public profiles, not even from a
logged-in account. It breaches the LinkedIn User Agreement and it is what accounts get
restricted for. Every LinkedIn interaction in this kit is a human typing into LinkedIn's
own search box: the kit produces the *strategy*, the human runs the *search*. The only
network calls it makes are to the Anthropic API and to GitHub's public API. CI enforces
this on every push — see [`tools/check_no_linkedin.sh`](tools/check_no_linkedin.sh).

## The problem

Recruiters are handed AI-era JDs written by people who don't know what they're asking for,
and sent to people who don't know how to read them. Then "some Bedrock, I've touched AWS"
turns up on the phone and there's no way to know whether that's a yes. Nobody has handed
them a decoder. Meanwhile the candidate on the other end can't tell whether the JD is one
job or three.

## What's here today

`jd_decode` — the core. Paste in a JD, get back a structured read: every role the JD
bundles, which one the day-to-day actually is, skills sorted by how the JD *uses* them,
a portrait of the person who holds this job, ten-minute screening questions with a
real-answer and a bluff example for each, and a blunt sanity verdict with a fix you can
send to the client.

The verdict is graded on the JD **as received** — the existence of a fix never upgrades it:

| Verdict | Means |
|---|---|
| `does_not_make_sense` | As written, no one person can be hired at the posted terms |
| `makes_sense_with_edits` | One labour market, fixable defects |
| `makes_sense` | One labour market, one bar, consistent with the rate |

Still to come, in order: `should_i_apply` (the same decode addressed to the candidate),
`sourcing_kit` (Boolean strings, x-ray strings, adjacent-title map, screen script),
`fit_score` (paste-in profile scoring), `receipts` (GitHub public API).

## Using it

```bash
export ANTHROPIC_API_KEY=...
python3 tools/probe.py run tests/fixtures/finserv_ai_automation_developer.md claude-sonnet-5 > out.json
python3 tools/probe.py check out.json tests/fixtures/finserv_ai_automation_developer.expected.json
python3 tools/probe.py render out.json
```

`tools/probe.py` is the tuning harness, not a throwaway: it holds the prompt, validates
against the schema, and mechanically enforces the rules that are easy to regress —
the 250-word cap on the fix, the ranked-bar structure, the they/them portrait, and the
requirement that every screening question names something the candidate had to get past.

## Fixtures

Fixtures are fed **verbatim**. Expectations live in a sidecar `<fixture>.expected.json`,
never inside the fixture — a fixture that states its own answers grades its own homework.

Live decodes are recorded to `tests/recorded/<fixture>.<model>.json` and committed, so CI
can validate the prompt's last known-good output without an API key. Tune on Sonnet for
speed, confirm on Opus; **both must pass** before a prompt change is kept.

## Design notes

- **Bundling is the #1 defect.** A role is a distinct labour market — a person you would
  run a separate search for. A task is not a role, a hat is not a role, and a preferred
  qualification never creates one.
- **The portrait uses they/them** and never assigns gender, age, or origin. It describes
  the typical holder of a role, not a person. In a sourcing tool, a gendered portrait
  primes the recruiter before they open a single profile.
- **Absence of public code is not evidence of absence.** Most professional work is
  private. `receipts` prints this every time it runs.

## Licence

MIT. See [LICENSE](LICENSE).
