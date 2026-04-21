#!/usr/bin/env bash
# publish.sh — git add / commit / push を一気に実行(モノレポ対応)
#
# Usage (essays/ ディレクトリから実行):
#   bash scripts/publish.sh <slug> <commit-message>
#
# Example:
#   bash scripts/publish.sh civil-vs-common-law "essays: 法の二大系統を公開"

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: bash scripts/publish.sh <slug> <commit-message>"
  echo "  Run this from the essays/ directory of the monorepo."
  exit 1
fi

SLUG="$1"
MSG="$2"

ESSAYS_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
MONOREPO_ROOT="$(cd "$ESSAYS_ROOT/.." && pwd)"
ARTICLE_DIR="$ESSAYS_ROOT/articles/$SLUG"

if [ ! -d "$ARTICLE_DIR" ]; then
  echo "✗ Article not found: $ARTICLE_DIR"
  exit 1
fi

echo "Running pre-publish check ..."
if ! bash "$ESSAYS_ROOT/scripts/check.sh" "$ARTICLE_DIR/index.html"; then
  echo ""
  echo "✗ Pre-publish check failed. Please fix the issues above before publishing."
  exit 1
fi

cd "$MONOREPO_ROOT"
BRANCH=$(git symbolic-ref --short HEAD 2>/dev/null || echo "main")

echo ""
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"
echo "  Publishing to branch: $BRANCH"
echo "━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━"

git add "essays/articles/$SLUG/" "essays/index.html"

if git diff --cached --quiet; then
  echo "⚠ No changes staged. Nothing to commit."
  exit 0
fi

echo ""
echo "Files to commit:"
git diff --cached --name-only | sed 's/^/  /'
echo ""
echo "Commit message: $MSG"
echo ""

git commit -m "$MSG"

echo ""
echo "Pushing to origin/$BRANCH ..."
git push origin "$BRANCH"

echo ""
echo "✓ Published successfully"
REMOTE_URL=$(git remote get-url origin)
PAGES_URL=$(echo "$REMOTE_URL" | sed -E 's|.*github\.com[:/]([^/]+)/([^.]+)(\.git)?|https://\1.github.io/\2|')
echo "  View at: $PAGES_URL/essays/articles/$SLUG/"
