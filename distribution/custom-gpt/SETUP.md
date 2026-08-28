# Publishing the Field Kit as a Custom GPT

Fifteen minutes, no code. The point is that a recruiter clicks a link, pastes a job
description, and gets a report — no install, no API key, no reference files, no idea that
any of this exists.

## Why it is split in two

ChatGPT caps a Custom GPT's Instructions field at **8,000 characters**. The analysis prompt
alone is over 10,000. So the instructions are a *router* — what to run when, the hard
boundary, and the rules that must hold even if something fails to load — and the six passes
are uploaded as **Knowledge** files it reads on demand.

That is the same architecture as `SKILL.md`, and it has the same failure mode: a router
that merely *describes* the passes will produce a plausible imitation instead of running
them. Both documents say, in as many words, *read the file and follow it exactly; do not
work from the summary.* Keep that line if you edit anything.

## Steps

1. **chatgpt.com → Explore GPTs → Create**, then open the **Configure** tab. Skip the
   conversational builder; it will rewrite what you paste.

2. **Name:** `The Recruiter's Field Kit`
   **Description:** `Decodes AI-era job descriptions: what the req actually contains, who to look for, and whether it makes sense. Built by Prodigal Paradigm.`

3. **Instructions:** paste the entire contents of [`INSTRUCTIONS.md`](INSTRUCTIONS.md).

4. **Knowledge:** upload all six files from [`knowledge/`](knowledge/). Filenames matter —
   the instructions route by name.

5. **Capabilities:** turn **Web Browsing OFF**. This is not optional. The kit's hard
   boundary is that it never fetches profiles or touches LinkedIn, and leaving browsing on
   invites exactly that. Code Interpreter off. DALL·E off.

6. **Conversation starters:**
   - `Decode this JD for me`
   - `Is this one job or three?`
   - `Who am I actually looking for?`
   - `Should I apply to this?`

7. **Save → Anyone with the link** while you test. Publish publicly only once you have run
   the checks below.

## Before you publish it publicly

Run `tests/fixtures/finserv_ai_automation_developer.md` through the GPT and check four
things against `tests/fixtures/finserv_ai_automation_developer.expected.json`:

- **2 labour markets**, not 1 and not 4
- **`does_not_make_sense`**, and it names the rate covering only one of them
- The client email uses the ranked bar — *Must have / Strong plus / Genuinely optional*
- The portrait uses **they/them**

Then the boundary, which matters more than any of them: ask it to *"find me candidates on
LinkedIn for this."* **It must decline and hand you a search string to run yourself.** If it
offers to browse, browsing is still on.

Also worth a run: `saas_platform_support_engineer.md`, which should come back
`makes_sense`. If everything returns a problem, the floor rule has been lost in
translation and the GPT will be useless by its third use.

## Keeping it honest

The knowledge files are generated from `tools/probe.py` by `tools/export_references.py`,
and CI fails if they drift. **When you change a prompt, re-run the exporter and re-upload
the knowledge files** — otherwise the GPT quietly runs last month's rules while the repo
claims this month's.

The GPT has no validator. Everything the repo enforces mechanically — the word cap, the
ranked-bar labels, they/them, no describing unfetched repos — is unchecked once a recruiter
is running it. The CLI stays the reference implementation. Re-run the fixture checks above
after any prompt change, the same way the repo confirms on two models before keeping one.
