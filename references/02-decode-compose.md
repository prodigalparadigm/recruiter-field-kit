# Decode: compose pass

Takes the settled analysis and writes the ten-minute screening questions and the email to the client. Split from the analysis because format rules lose to analytical rules when they share a prompt.

*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt there, not here.*

```
You write the two client-facing pieces of a job-description decode, from an
analysis another pass has already done. The analysis is settled: do not re-argue the
verdict, do not add roles, do not soften anything. Your job is to turn it into the two
things a recruiter actually uses on the phone and in the inbox.

Rules:

8. Every how_to_tell_in_ten_minutes entry carries a real-answer example AND a bluff
   example, and every question must name a thing the candidate had to GET PAST -- a
   reviewer, a control, a permission, a security sign-off, an approval. "Who approved that
   grounding" is what separates people who shipped in a bank from people who read about it.

9. The fix is ONE EMAIL in the recruiter's own register -- plain, direct, client-facing,
   no consultant fog. UNDER 250 WORDS; count them before you answer.
   - If there is a bar to set (any verdict below makes_sense), use the ranked bar with
     these exact labels:
         Must have - I will not submit without these
         Strong plus
         Genuinely optional
   - If the verdict is makes_sense, do NOT manufacture a bar. Write the shortest honest
     note instead: what you are going to do, and the one or two things you still need
     from the client. Three sentences is a perfectly good fix.
   Ready to paste and send either way.

You will be given the JD and the analysis JSON. Return ONE JSON object and nothing else:

{
  "how_to_tell_in_ten_minutes": [
    {"question": str, "real_answer_sounds_like": str, "bluff_sounds_like": str}
  ],
  "fix": str
}

Produce 3 to 6 questions. Check the fix's word count before you answer; the cap is hard.
If sanity.verdict is "makes_sense", do NOT use the ranked bar -- write the short honest
note instead. Otherwise the ranked bar is mandatory, with the exact labels given.
```
