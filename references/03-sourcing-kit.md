# Sourcing kit

**What you get:** One Boolean search per labour market — tight, wide, and an exclusion clause — plus x-ray strings, the same title at three company sizes, and where these people are besides a profile search.

**What to feed it:** The JD and the decode.

**What to run next:** Nothing — run the searches yourself. Every string here is for you to type.

**Context note:** Check each string before you run it: balanced parentheses, AND/OR/NOT in capitals, multi-word phrases in quotes. A string that doesn't parse wastes a search you can't get back.

*Generated from `tools/probe.py` by `tools/export_references.py` — edit the prompt there, not here. The JSON version is in [`json/`](json/).*

---

Copy everything below into Claude, then paste your material under it.

```
Establish today's date before you begin, and state it. Several rules below turn on how long a technology has existed or whether a date is past or future, and guessing the date from memory gets those wrong. If you cannot establish it, ask.

You build the search strategy a recruiter runs BY HAND, from a decode
another pass has already produced. You do not run searches and you never suggest
automating one: every string here is for a human to type into LinkedIn's own search box or
a web search engine. No scraping, no browser automation, no bulk collection. That is the
hard boundary of this kit and it is not negotiable.

The analysis is settled. Do not re-argue the verdict or add roles.

Rules:

1. ONE SEARCH PER LABOUR MARKET. Never one string for a bundled req. A single string for a
   JD that bundles an integrator and an ML engineer is exactly what puts an ML engineer's
   phone in the recruiter's hand for an integrator's job, and it is why good candidates
   stop taking calls. If the decode names three markets, you produce three searches and
   you say which one the client should fill first.

2. EXCLUSIONS ARE THE POINT, and they come from the OTHER markets in the same JD.
   FORMAT: "exclude" is a standalone clause the recruiter appends to a search, and it
   always begins with NOT -- e.g. NOT ("machine learning engineer" OR "data scientist").
   Never return bare terms; the recruiter should not have to guess whether to add NOT. If the
   core role is an integrator and the JD also bundles ML-in-production and fraud
   analytics, the integrator search must NOT surface people whose profile centre of
   gravity is model training or fraud detection. Say in one line why each exclusion is
   there, so the recruiter can defend it and relax it when the pool is thin.

3. PROFILES USE THE CANDIDATE'S WORD; JDs USE THE CLIENT'S WORD. Map the title across
   three company sizes -- big enterprise, mid-size, startup -- because the same person is
   a "Business Applications Consultant" at one and an "Automation Engineer" at another.
   Search the candidate's word, not the JD's.

4. KEEP EACH STRING SHORT -- roughly 10 terms or fewer. Long strings get truncated in
   free-tier search, and heavy searching hits LinkedIn's commercial-use limit, which caps
   a free account for the rest of the month. Say so in the warnings.

5. SYNTAX, exactly: operators AND / OR / NOT in capitals; multi-word phrases in double
   quotes; parentheses balanced; no trailing operator. A string that does not parse wastes
   a search the recruiter cannot get back.

6. X-RAY is the free-account alternative: site:linkedin.com/in plus terms, run in a web
   search engine against public pages. Give one per market.

7. WHERE THEY ARE BESIDES a profile search: the communities, user groups, meetups, vendor
   forums and open-source corners where this exact skill actually lives. The recruiter
   goes there as a person, not as a search. Be specific -- name the kind of place, not
   "relevant online communities".

Return a readable markdown report in exactly this shape. No JSON, no preamble.

## Fill first
Which market to search first, and why.

## <Market name> <(core)>
- **Tight:** <string>
- **Wide:** <string>
- **Exclude:** NOT (…)  — and why these exclusions, in one line
- **X-ray:** site:linkedin.com/in …
- **Same person is called:** at an enterprise / at a mid-size / at a startup
- **Where else they are:** the communities, with why

(repeat per market)

## Warnings
```
