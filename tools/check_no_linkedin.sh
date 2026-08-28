#!/usr/bin/env bash
# Hard boundary. The kit produces LinkedIn search STRATEGY for a human to run by hand; it
# never makes a network call to LinkedIn. The invariant is about NETWORK ACCESS, not about
# the word appearing: the x-ray feature legitimately contains the search operator
# "site:linkedin.com/in", which is text a recruiter types into a search engine.
#
# Fails on:  a linkedin URL with a scheme, linkedin.com near any HTTP-calling code, or a
#            browser-automation / scraping dependency.
# Allows:    the bare x-ray operator, and prints every occurrence so the allowance is
#            visible in CI output rather than silent.
set -uo pipefail
cd "$(dirname "$0")/.."
SELF='^\./tools/check_no_linkedin\.sh:'
fail=0

# 1. a scheme-qualified LinkedIn URL anywhere, in any file type
urls=$(grep -rInE '(https?:)?//([a-z0-9.-]*\.)?linkedin\.com' . 2>/dev/null | grep -vE "$SELF" || true)
if [ -n "$urls" ]; then
  echo "FAIL: a linkedin.com URL appears in the repo:"; echo "$urls"; fail=1
fi

# 2. linkedin.com on the same line as anything that makes an HTTP request
calls=$(grep -rInE 'linkedin\.com' --include='*.py' --include='*.sh' --include='*.js' \
        --include='*.ts' --include='*.yml' --include='*.yaml' . 2>/dev/null \
        | grep -vE "$SELF" \
        | grep -iE 'requests\.|httpx|urllib|aiohttp|fetch\(|axios|curl |wget |webbrowser|open_url' || true)
if [ -n "$calls" ]; then
  echo "FAIL: linkedin.com used in something that makes a request:"; echo "$calls"; fail=1
fi

# 3. browser automation / scraping dependencies have no business here
libs=$(grep -rInE '\b(selenium|playwright|puppeteer|scrapy|mechanize|linkedin_api|staffspy)\b' \
       --include='*.py' --include='*.txt' --include='*.toml' --include='*.cfg' --include='*.yml' . 2>/dev/null \
       | grep -vE "$SELF" || true)
if [ -n "$libs" ]; then
  echo "FAIL: browser-automation/scraping dependency present:"; echo "$libs"; fail=1
fi

if [ "$fail" -eq 0 ]; then
  echo "PASS: hard boundary intact — no network path to LinkedIn."
  allowed=$(grep -rIn 'site:linkedin\.com/in' . 2>/dev/null | grep -vE "$SELF" || true)
  if [ -n "$allowed" ]; then
    echo "  allowed (x-ray search operator, human-typed, not a URL):"
    echo "$allowed" | sed 's/^/    /'
  fi
fi
exit $fail
