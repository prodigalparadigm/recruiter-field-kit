#!/usr/bin/env python3
"""Export the prompts from probe.py into references/ as usable markdown.

probe.py is the single source of truth. Two variants are written:

  references/*.md        HUMAN — asks for a readable markdown report. This is what a
                         recruiter pastes into Claude, and what SKILL.md tells Claude
                         to read. JSON is a machine format; handing it to a recruiter
                         is a failure at the last inch.
  references/json/*.md   MACHINE — the original JSON contract, for wiring into code.

Each rules constant ends with "Return ONE JSON object", which is the split point: the
rules are shared, only the output contract differs.

    python3 tools/export_references.py           # write
    python3 tools/export_references.py --check   # verify in sync, write nothing
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe

SPLIT = "Return ONE JSON object"
HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")
GPT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..",
                   "distribution", "custom-gpt", "knowledge")
ONE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "distribution", "one-paste")

# (file, title, rules, gives, feed, next_step, context, report)
PASSES = [
 ("01-decode-analysis.md", "Decode — analysis pass", probe.ANALYSE_RULES,
  "Every role the JD bundles, the skills sorted by how the JD uses them, the seniority read, "
  "a portrait of the person, the red flags, and the verdict.",
  "The job description, verbatim. Include any covering note the recruiter sent with it — "
  "that note is often the highest-signal line in the packet.",
  "**02-decode-compose.md**, which turns this into screening questions and an email to the "
  "client. This pass deliberately does not produce those.",
  "This pass should see the JD and nothing else. If your Claude has memory on and starts "
  "recalling your own background, tell it to ignore that — a decode contaminated by the "
  "reader's history describes the reader, not the job.",
  """# <Title as posted> — decoded
**Verdict:** <verdict, in plain words>

## This is <one job / two jobs / three jobs>
For each labour market: what it is, and the JD's own words as evidence.
Then: **the one the day-to-day actually is**, and why.

## Skills
**Must have** / **Should have** / **Nice to have** / **Decorative — ignore**
Each with the one-line reason it sits there.

## Seniority
## Who this person is
The portrait, as prose. Not a checklist.

## Red flags
## Problems
## Ask the client"""),

 ("02-decode-compose.md", "Decode — compose pass", probe.COMPOSE_RULES,
  "Three to six ten-minute screening questions, each with a real-answer and a bluff example, "
  "and the email to send the client.",
  "The JD and the analysis from pass 1 (paste the report you just got).",
  "**03-sourcing-kit.md** if you need to find candidates, or you're done.",
  "The analysis is settled. If this pass disagrees with it, that becomes a question to the "
  "client — never a quiet downgrade.",
  """## How to tell in ten minutes
**1. <question>**
- Real answer sounds like: …
- Bluff sounds like: …
(repeat for each)

## Send this to the client
The email, ready to paste. Under 250 words."""),

 ("03-sourcing-kit.md", "Sourcing kit", probe.SOURCE_RULES,
  "One Boolean search per labour market — tight, wide, and an exclusion clause — plus x-ray "
  "strings, the same title at three company sizes, and where these people are besides a profile search.",
  "The JD and the decode.",
  "Nothing — run the searches yourself. Every string here is for you to type.",
  "Check each string before you run it: balanced parentheses, AND/OR/NOT in capitals, "
  "multi-word phrases in quotes. A string that doesn't parse wastes a search you can't get back.",
  """## Fill first
Which market to search first, and why.

## <Market name> <(core)>
- **Tight:** <string>
- **Wide:** <string>
- **Exclude:** NOT (…)  — and why these exclusions, in one line
- **X-ray:** site:linkedin.com/in …
- **Same person is called:** at an enterprise / at a mid-size / at a startup
- **Where else they are:** the communities, with why

(repeat per market)

## Warnings"""),

 ("04-should-i-apply.md", "Should I apply — mirror mode", probe.MIRROR_RULES,
  "Whether this is one job or several, which of them you actually are, the honest sentence to "
  "say about the gap, what to ask before applying, and a verdict.",
  "The JD, the decode, and your own summary in your own words.",
  "Nothing. Decide.",
  "This is the one pass where your Claude's memory of your background **helps** — it can only "
  "tell you which role you are if it knows what you've done. Let it recall.",
  """## This is <one job / three jobs>
## Which of them you are
## Evidence you fit  /  Evidence you don't
## The honest sentence
> The sentence, in your own voice, ready to say out loud.

## Ask before you apply
## Verdict — and why"""),

 ("05-fit-score.md", "Fit score", probe.FIT_RULES,
  "Evidence for and against, gaps, over-claims, under-claims, questions for this specific "
  "person, and the sentence to send the client.",
  "The JD, the decode, and a profile **you pasted**. Never fetched.",
  "**06-receipts.md** if they published a GitHub username and you want to see what they built.",
  "This pass must see the JD, the decode and the pasted profile **and nothing else**. If your "
  "Claude recalls your own background here, it will score the candidate against you.",
  """## Evidence for  /  Evidence against  /  Gaps
## Over-claims
A tool named with no project behind it.
## Under-claims
A project described without naming the tool it obviously took. These are the ones worth chasing.
## Ask this person
## Honesty read
## Verdict
## Send this to the client
> One sentence, defensible if the client pushes back."""),

 ("06-receipts.md", "Receipts", probe.RECEIPTS_RULES,
  "What someone has actually built, in plain English — one paragraph per repo, plus what the "
  "profile does not tell you.",
  "A GitHub username **they published themselves**, and the facts fetched from GitHub's public API.",
  "Nothing.",
  "Describe only repos present in the facts. If the fetch was capped, the missing repos are "
  "named as not examined and nothing is said about them.\n\n> " + probe.CAVEAT,
  """## Summary
## What they've built
**<repo>** — what it is, in language you could repeat on a call.
*Signals:* README, tests, CI, recency — flatly, no inference about the person.
(repeat)

## Habits
## What this does not tell you"""),
]


def human(title, rules, gives, feed, nxt, context, report):
    body = rules.split(SPLIT)[0].rstrip()
    return (f"# {title}\n\n"
            f"**What you get:** {gives}\n\n"
            f"**What to feed it:** {feed}\n\n"
            f"**What to run next:** {nxt}\n\n"
            f"**Context note:** {context}\n\n"
            f"*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt "
            f"there, not here. The JSON version is in [`json/`](json/).*\n\n"
            f"---\n\nCopy everything below into Claude, then paste your material under it.\n\n"
            f"```\nEstablish today's date before you begin, and state it. Several rules below turn on "
            f"how long a technology has existed or whether a date is past or future, and guessing the "
            f"date from memory gets those wrong. If you cannot establish it, ask.\n\n{body}\n\nReturn a readable markdown report in exactly this shape. "
            f"No JSON, no preamble.\n\n{report}\n```\n")


def knowledge(title, rules, report, nxt):
    """Knowledge-file variant for a Custom GPT. Same rules, no human-paste framing: the
    GPT is the reader, so 'copy everything below into Claude' would be nonsense."""
    body = rules.split(SPLIT)[0].rstrip()
    return (f"# {title}\n\n*Generated from `tools/probe.py`. Do not edit here.*\n\n"
            f"Follow these rules exactly. Next step after this pass: {nxt}\n\n"
            f"{body}\n\nReturn a readable markdown report in exactly this shape. "
            f"No JSON, no preamble.\n\n{report}\n")


def machine(title, rules):
    return (f"# {title} — JSON contract\n\nMachine-readable variant, for wiring into code. "
            f"Humans want [`../{'':s}`](..) instead.\n\n"
            f"*Generated from `tools/probe.py` — do not edit here.*\n\n```\n{rules}\n```\n")


REPORT = """# <Title as posted> — decoded
**Verdict:** <verdict, in plain words>

## This is <one job / two jobs / three jobs>
Each labour market, with the JD's own words as evidence. Then the one the day-to-day
actually is, and why.

## Skills
**Must have** / **Should have** / **Nice to have** / **Decorative — ignore**, each with the
one-line reason it sits there.

## Seniority

## Who this person is
The portrait, as prose. Not a checklist. They/them.

## How to tell in ten minutes
**1. <question>**
- Real answer sounds like: …
- Bluff sounds like: …
(three to six of these)

## Red flags

## Problems

## Send this to the client
The email, ready to paste.

## Ask the client
"""


def one_paste():
    body = probe.combined_rules().split("Return ONE JSON object")[0].rstrip()
    return ("# The Recruiter's Field Kit — one-paste decoder\n\n"
            "*Generated from `tools/probe.py`. Do not edit here.*\n\n"
            "Copy everything inside the fence, paste it into any AI assistant, then paste a "
            "job description underneath it in the same message.\n\n"
            "```\n" + body +
            "\n\nEstablish today's date before you begin and state it; several rules above turn "
            "on how long a technology has existed. If you cannot, ask.\n\n"
            "Return a readable markdown report in exactly this shape. No JSON, no preamble.\n\n"
            + REPORT + "```\n")


def main():
    check = "--check" in sys.argv
    os.makedirs(os.path.join(HERE, "json"), exist_ok=True)
    os.makedirs(GPT, exist_ok=True)
    os.makedirs(ONE, exist_ok=True)
    stale = []
    op = os.path.join(ONE, "PROMPT.md")
    want_one = one_paste()
    if (open(op).read() if os.path.exists(op) else None) != want_one:
        stale.append("distribution/one-paste/PROMPT.md")
        if not check:
            open(op, "w").write(want_one)
    for fn, title, rules, gives, feed, nxt, context, report in PASSES:
        for path, want in ((os.path.join(HERE, fn), human(title, rules, gives, feed, nxt, context, report)),
                           (os.path.join(HERE, "json", fn), machine(title, rules)),
                           (os.path.join(GPT, fn), knowledge(title, rules, report, nxt))):
            have = open(path).read() if os.path.exists(path) else None
            if want != have:
                stale.append(os.path.relpath(path, os.path.join(HERE, "..")))
                if not check:
                    open(path, "w").write(want)
    if check:
        if stale:
            print("FAIL: references/ is stale, re-run tools/export_references.py:")
            for f in stale: print("  -", f)
            return 1
        print(f"PASS: prompts in sync across all surfaces ({len(PASSES) * 3 + 1} files).")
    else:
        print(f"wrote {len(PASSES) * 3 + 1} files" + (f" ({len(stale)} changed)" if stale else ""))
    return 0


if __name__ == "__main__":
    sys.exit(main())
