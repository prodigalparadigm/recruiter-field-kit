#!/usr/bin/env bash
# Hard boundary check. The kit produces LinkedIn search STRATEGY for a human to run by
# hand; it never touches linkedin.com over the network. Prose may name LinkedIn. Code
# may not reference linkedin.com at all, and nothing anywhere may build a URL to it.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0

# 1. any linkedin.com reference inside executable files
hits=$(grep -rInE 'linkedin\.com' \
  --include='*.py' --include='*.sh' --include='*.js' --include='*.ts' \
  --include='*.yml' --include='*.yaml' --include='*.toml' --include='*.json' \
  . 2>/dev/null | grep -v '^\./tools/check_no_linkedin\.sh:' || true)
if [ -n "$hits" ]; then
  echo "FAIL: linkedin.com referenced in executable/config files:"; echo "$hits"; fail=1
fi

# 2. any URL to linkedin, in any file type including docs
urls=$(grep -rInE '(https?://|//)([a-z0-9.-]*\.)?linkedin\.com' . 2>/dev/null \
  | grep -v '^\./tools/check_no_linkedin\.sh:' || true)
if [ -n "$urls" ]; then
  echo "FAIL: a linkedin.com URL appears in the repo:"; echo "$urls"; fail=1
fi

# 3. browser automation / scraping libraries have no business here
libs=$(grep -rInE '\b(selenium|playwright|puppeteer|scrapy|mechanize|linkedin_api|staffspy)\b' \
  --include='*.py' --include='*.txt' --include='*.toml' --include='*.cfg' . 2>/dev/null \
  | grep -v '^\./tools/check_no_linkedin\.sh:' || true)
if [ -n "$libs" ]; then
  echo "FAIL: browser-automation/scraping dependency present:"; echo "$libs"; fail=1
fi

[ "$fail" -eq 0 ] && echo "PASS: hard boundary intact — no linkedin.com network surface."
exit $fail
