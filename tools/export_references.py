#!/usr/bin/env python3
"""Export the prompts from probe.py into references/ as readable markdown.

probe.py is the single source of truth. These files exist so a recruiter's Claude can
run the kit inline -- no API key, no CLI -- and so the prompts are reviewable without
reading Python. CI re-runs this and fails if the exports have drifted.

    python3 tools/export_references.py           # write
    python3 tools/export_references.py --check   # verify in sync, write nothing
"""
import os, sys
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import probe

EXPORTS = {
    "01-decode-analysis.md": ("Decode: analysis pass", probe.ANALYSE_RULES,
        "Paste a JD. This pass names the labour markets, sorts the skills, reads the "
        "seniority, and grades the JD as received."),
    "02-decode-compose.md": ("Decode: compose pass", probe.COMPOSE_RULES,
        "Takes the settled analysis and writes the ten-minute screening questions and "
        "the email to the client. Split from the analysis because format rules lose to "
        "analytical rules when they share a prompt."),
    "03-sourcing-kit.md": ("Sourcing kit", probe.SOURCE_RULES,
        "One Boolean search per labour market, with each market's exclusions built from "
        "the others. Every string is for a human to type."),
    "04-should-i-apply.md": ("Should I apply (mirror mode)", probe.MIRROR_RULES,
        "The same decode addressed to the candidate. The deliverable is the honest "
        "sentence."),
    "05-fit-score.md": ("Fit score", probe.FIT_RULES,
        "Scores one pasted profile against the core role. Never fetched."),
    "06-receipts.md": ("Receipts", probe.RECEIPTS_RULES,
        "Describes what someone has actually built, from GitHub's public API. The "
        "caveat below is printed on every run, including errors.\n\n> " + probe.CAVEAT),
}

HERE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "references")


def body(title, rules, blurb):
    return f"# {title}\n\n{blurb}\n\n*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt there, not here.*\n\n```\n{rules}\n```\n"


def main():
    check = "--check" in sys.argv
    stale = []
    for fn, (title, rules, blurb) in EXPORTS.items():
        path = os.path.join(HERE, fn)
        want = body(title, rules, blurb)
        have = open(path).read() if os.path.exists(path) else None
        if want != have:
            stale.append(fn)
            if not check:
                open(path, "w").write(want)
    if check:
        if stale:
            print("FAIL: references/ is stale, re-run tools/export_references.py:")
            for f in stale: print("  -", f)
            return 1
        print(f"PASS: references/ in sync with the prompts ({len(EXPORTS)} files).")
    else:
        print(f"wrote {len(EXPORTS)} reference files" + (f" ({len(stale)} changed)" if stale else " (no changes)"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
