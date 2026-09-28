#!/bin/bash
FILE=/root/lab/risk_register.md
[ -f "$FILE" ] || exit 1
ROWS=$(grep -E '^\|' "$FILE" | tail -n +3 | grep -civ 'TODO')
if [ "$ROWS" -ge 5 ]; then
  exit 0
fi
exit 1
