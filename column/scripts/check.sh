#!/usr/bin/env bash
# check.sh — 公開前の自動点検
#
# Usage:
#   bash scripts/check.sh articles/civil-vs-common-law/index.html
#
# Checks:
#   - HTML tag balance
#   - Forbidden AI-style expressions
#   - All です・ます endings (non-ending だ/である outside quotes)
#   - References section exists with at least 2 entries
#   - No unresolved {{PLACEHOLDER}} markers
#   - Article linked from top-level index.html

set -u

if [ $# -lt 1 ]; then
  echo "Usage: bash scripts/check.sh <path/to/article.html>"
  exit 1
fi

FILE="$1"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
ROOT_INDEX="$REPO_ROOT/index.html"

if [ ! -f "$FILE" ]; then
  echo "✗ File not found: $FILE"
  exit 1
fi

ERRORS=0
WARNINGS=0

echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Pre-publish check: $FILE"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

# ============ CHECK 1: unresolved placeholders ============
echo ""
echo "[1/6] Unresolved {{PLACEHOLDER}} markers ..."
PLACEHOLDERS=$(grep -o '{{[A-Z_0-9]*}}' "$FILE" | sort -u || true)
if [ -n "$PLACEHOLDERS" ]; then
  echo "  ✗ Found unresolved placeholders:"
  echo "$PLACEHOLDERS" | sed 's/^/    /'
  ERRORS=$((ERRORS + 1))
else
  echo "  ✓ All placeholders resolved"
fi

# ============ CHECK 2: HTML tag balance ============
echo ""
echo "[2/6] HTML tag balance ..."
python3 - "$FILE" << 'PYEOF'
import sys, re
with open(sys.argv[1]) as f: content = f.read()
issues = 0
for tag in ['html', 'head', 'body', 'section', 'div', 'nav', 'footer', 'p', 'h1', 'h2', 'h3', 'h4', 'h5', 'ol', 'ul', 'li', 'aside', 'blockquote', 'style', 'script']:
    o = len(re.findall(rf'<{tag}[\s>]', content))
    c = len(re.findall(rf'</{tag}>', content))
    if o != c:
        print(f'  ✗ <{tag}>: {o} open / {c} close'); issues += 1
sys.exit(1 if issues else 0)
PYEOF
if [ $? -ne 0 ]; then ERRORS=$((ERRORS + 1)); else echo "  ✓ Tags balanced"; fi

# ============ CHECK 3: Forbidden AI-style expressions ============
echo ""
echo "[3/6] Forbidden AI-style expressions ..."
# Strip HTML tags first, then grep
TMPFILE=$(mktemp)
python3 -c "
import re, sys
with open('$FILE') as f: c = f.read()
text = re.sub(r'<[^>]+>', ' ', c)
text = re.sub(r'\s+', ' ', text)
print(text)
" > "$TMPFILE"

FORBIDDEN='していきます|ていきます|てきます(?!。)|のぞきこむ|のぞいてみる|見えてきます|浮かび上がってきます|というタイプ|ということです|というわけです|となります(?!。$)|ユニーク|ピッタリ|バッチリ|ちゃぶ台|ブチ切|ベタ褒|わけです|まさに.*まさに'
HITS=$(grep -oE "(していきます|てきます|のぞきこむ|のぞいてみる|見えてきます|浮かび上がってきます|というタイプ|ということです|というわけです|ユニーク|ピッタリ|バッチリ|ちゃぶ台|ブチ切|ベタ褒|わけです)" "$TMPFILE" | sort | uniq -c || true)
if [ -n "$HITS" ]; then
  echo "  ✗ Forbidden expressions found:"
  echo "$HITS" | sed 's/^/    /'
  ERRORS=$((ERRORS + 1))
else
  echo "  ✓ No forbidden expressions"
fi
rm -f "$TMPFILE"

# ============ CHECK 4: sentence endings ============
echo ""
echo "[4/6] Sentence endings (です・ます form) ..."
python3 - "$FILE" << 'PYEOF'
import sys, re
with open(sys.argv[1]) as f: c = f.read()
text = re.sub(r'<[^>]+>', ' ', c)
# Find sentences ending in plain form markers
patterns = ['である。', 'のだ。', 'なのだ。']
flagged = []
for p in patterns:
    count = text.count(p)
    if count > 0:
        flagged.append(f'{p}: {count} times')
if flagged:
    print('  ✗ Plain-form endings detected:')
    for f in flagged:
        print('    ' + f)
    sys.exit(1)
else:
    print('  ✓ All sentence endings are in です・ます form')
PYEOF
if [ $? -ne 0 ]; then ERRORS=$((ERRORS + 1)); fi

# ============ CHECK 5: References section exists ============
echo ""
echo "[5/6] References section ..."
if ! grep -q 'class="refs"' "$FILE"; then
  echo "  ✗ <section class=\"refs\"> not found"
  ERRORS=$((ERRORS + 1))
else
  REF_COUNT=$(grep -c '<li>' "$FILE" || true)
  # crude: count <li> items inside refs-list
  REF_ITEMS=$(python3 -c "
import re
with open('$FILE') as f: c = f.read()
m = re.search(r'<ol[^>]*class=\"[^\"]*refs-list[^\"]*\"[^>]*>(.*?)</ol>', c, re.DOTALL)
if m:
    print(len(re.findall(r'<li\b', m.group(1))))
else:
    print(0)
")
  if [ "$REF_ITEMS" -lt 2 ]; then
    echo "  ✗ References list has $REF_ITEMS items (minimum 2 required)"
    ERRORS=$((ERRORS + 1))
  else
    echo "  ✓ References section present with $REF_ITEMS entries"
  fi
fi

# ============ CHECK 6: Linked from index ============
echo ""
echo "[6/6] Top-level index.html link ..."
SLUG=$(basename "$(dirname "$FILE")")
if [ ! -f "$ROOT_INDEX" ]; then
  echo "  ⚠ Top index.html not found at $ROOT_INDEX (skipping)"
  WARNINGS=$((WARNINGS + 1))
elif ! grep -q "articles/$SLUG/" "$ROOT_INDEX"; then
  echo "  ✗ Article '$SLUG' is not linked from $ROOT_INDEX"
  echo "    Please add a card for this article to the top page."
  ERRORS=$((ERRORS + 1))
else
  echo "  ✓ Article linked from top index"
fi

# ============ SUMMARY ============
echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
if [ $ERRORS -eq 0 ] && [ $WARNINGS -eq 0 ]; then
  echo "  ✓ All checks passed"
  exit 0
elif [ $ERRORS -eq 0 ]; then
  echo "  ✓ Passed with $WARNINGS warning(s)"
  exit 0
else
  echo "  ✗ Failed: $ERRORS error(s), $WARNINGS warning(s)"
  exit 1
fi
