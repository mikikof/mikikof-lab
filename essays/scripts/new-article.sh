#!/usr/bin/env bash
# new-article.sh — 新しいコラムをスキャフォールドする
#
# Usage:
#   bash scripts/new-article.sh "civil-vs-common-law" "法の二大系統"
#
# Creates:
#   articles/{slug}/index.html  (templates/base.html からコピー、タイトル置換)

set -euo pipefail

if [ $# -lt 2 ]; then
  echo "Usage: bash scripts/new-article.sh <slug> <title>"
  echo "  <slug>  : lowercase, hyphen-separated, ≤40 chars (e.g. civil-vs-common-law)"
  echo "  <title> : article title in Japanese (e.g. 法の二大系統)"
  exit 1
fi

SLUG="$1"
TITLE="$2"
REPO_ROOT="$(cd "$(dirname "$0")/.." && pwd)"
TARGET_DIR="$REPO_ROOT/articles/$SLUG"
TARGET_FILE="$TARGET_DIR/index.html"
TEMPLATE_FILE="$REPO_ROOT/templates/base.html"

# Validate slug format
if [[ ! "$SLUG" =~ ^[a-z0-9-]+$ ]]; then
  echo "Error: slug must contain only lowercase letters, digits, and hyphens"
  exit 1
fi
if [ ${#SLUG} -gt 40 ]; then
  echo "Error: slug must be ≤40 characters"
  exit 1
fi

# Check template exists
if [ ! -f "$TEMPLATE_FILE" ]; then
  echo "Error: template not found at $TEMPLATE_FILE"
  exit 1
fi

# Check duplicate
if [ -d "$TARGET_DIR" ]; then
  echo "Error: article '$SLUG' already exists at $TARGET_DIR"
  echo "  Use a different slug, or delete the existing directory first."
  exit 1
fi

# Create directory and copy
mkdir -p "$TARGET_DIR"
cp "$TEMPLATE_FILE" "$TARGET_FILE"

# Replace placeholders (title only — other placeholders are for Claude to fill)
# Use a portable sed-in-place pattern
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s/{{ARTICLE_TITLE}}/$TITLE/g" "$TARGET_FILE"
else
  sed -i "s/{{ARTICLE_TITLE}}/$TITLE/g" "$TARGET_FILE"
fi

echo "✓ Created: $TARGET_FILE"
echo ""
echo "Next steps for Claude:"
echo "  1. Read the source materials provided by the user"
echo "  2. Decide on chapter count (3 / 5 / 7)"
echo "  3. Choose a color palette from templates/palettes.md"
echo "  4. Fill in all {{PLACEHOLDER}} markers in $TARGET_FILE"
echo "  5. Add chapter sections, visual elements, and references"
echo "  6. Update index.html with the new article card"
echo "  7. Run: bash scripts/check.sh $TARGET_FILE"
echo "  8. Run: bash scripts/publish.sh \"$SLUG\" \"Add article: $TITLE\""
