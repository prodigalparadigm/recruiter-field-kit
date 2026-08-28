#!/usr/bin/env bash
# Validate every recorded decode against the schema and its fixture's expectations.
# No network: CI has no API key. Live decodes are recorded under tests/recorded/ by
#   tools/probe.py run <fixture> <model>
# and committed, so CI checks the last known-good output of the prompt.
set -uo pipefail
cd "$(dirname "$0")/.."
fail=0; n=0

shopt -s nullglob
for out in tests/recorded/*.json; do
  base=$(basename "$out" .json)            # e.g. finserv_ai_automation_developer.claude-opus-5
  fixture=${base%%.*}
  exp="tests/fixtures/${fixture}.expected.json"
  n=$((n+1))
  if [ ! -f "$exp" ]; then
    echo "FAIL: $out has no sidecar at $exp"; fail=1; continue
  fi
  echo "--- $base"
  python3 tools/probe.py check "$out" "$exp" || fail=1
done

if [ "$n" -eq 0 ]; then echo "FAIL: no recorded decodes to check"; exit 1; fi
[ "$fail" -eq 0 ] && echo "PASS: $n recorded decode(s) valid."
exit $fail
