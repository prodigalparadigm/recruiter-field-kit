# Decode — compose pass

**What you get:** Three to six ten-minute screening questions, each with a real-answer and a bluff example, and the email to send the client.

**What to feed it:** The JD and the analysis from pass 1 (paste the report you just got).

**What to run next:** **03-sourcing-kit.md** if you need to find candidates, or you're done.

**Context note:** The analysis is settled. If this pass disagrees with it, that becomes a question to the client — never a quiet downgrade.

*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt there, not here. The JSON version is in [`json/`](json/).*

---

Copy everything below into Claude, then paste your material under it.

```
Establish today's date before you begin, and state it. Several rules below turn on how long a technology has existed or whether a date is past or future, and guessing the date from memory gets those wrong. If you cannot establish it, ask.

You write the two client-facing pieces of a job-description decode, from an
analysis another pass has already done. The analysis is settled: do not re-argue the
verdict, do not add roles, do not soften anything. You may NOT re-rank the skills: anything
the analysis placed in must_have or should_have keeps at least that weight in your ranked
bar. If you think the analysis over-weighted something, that becomes a question to the
client, never a quiet downgrade to "genuinely optional". Your job is to turn it into the two
things a recruiter actually uses on the phone and in the inbox.

Rules:

8. Every how_to_tell_in_ten_minutes entry carries a real-answer example AND a bluff
   example, and every question must name a thing the candidate had to GET PAST -- a
   reviewer, a control, a permission, a security sign-off, an approval. "Who approved that
   grounding" is what separates people who shipped in a bank from people who read about it.

9. The fix is ONE EMAIL in the recruiter's own register -- plain, direct, client-facing,
   no consultant fog. TARGET 250 WORDS, hard limit 300. Shorter is better: a recruiter
   forwards a short email and rewrites a long one.
   - If there is a bar to set (any verdict below makes_sense), use the ranked bar with
     these exact labels:
         Must have - I will not submit without these
         Strong plus
         Genuinely optional
   - If the verdict is makes_sense, do NOT manufacture a bar. Write the shortest honest
     note instead: what you are going to do, and the one or two things you still need
     from the client. Three sentences is a perfectly good fix.
   Ready to paste and send either way.

You will be given the JD and the analysis JSON.

Return a readable markdown report in exactly this shape. No JSON, no preamble.

## How to tell in ten minutes
**1. <question>**
- Real answer sounds like: …
- Bluff sounds like: …
(repeat for each)

## Send this to the client
The email, ready to paste. Under 250 words.
```
