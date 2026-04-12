#!/usr/bin/env bash
# examples/curl_requests.sh
#
# Curl examples for the PPT Generator API.
# Demonstrates all available endpoints.
#
# Usage:
#   chmod +x examples/curl_requests.sh
#   ./examples/curl_requests.sh
#
# Requirements:
#   - curl
#   - jq (optional, for pretty-printing JSON)
#
# Set PPT_API_URL to override the default server address:
#   PPT_API_URL=http://my-server:8000 ./examples/curl_requests.sh

BASE_URL="${PPT_API_URL:-http://localhost:8000}"

# Pretty-print JSON if jq is available, otherwise use cat
json_print() {
  if command -v jq &>/dev/null; then
    jq .
  else
    cat
  fi
}

echo "======================================================"
echo " PPT Generator API - curl examples"
echo " Base URL: $BASE_URL"
echo "======================================================"
echo ""

# ── 1. Health check ────────────────────────────────────────────────────────────
echo ">>> 1. Health check"
echo "    GET $BASE_URL/health"
curl -s "$BASE_URL/health" | json_print
echo ""
echo ""

# ── 2. Generate a presentation ────────────────────────────────────────────────
echo ">>> 2. Generate a presentation"
echo "    POST $BASE_URL/api/v1/generate"
GENERATE_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/generate" \
  -H "Content-Type: application/json" \
  -d '{
    "prompt": "Create a 5-slide presentation about the benefits of renewable energy sources",
    "slide_count": 5,
    "theme": "default"
  }')
echo "$GENERATE_RESPONSE" | json_print
echo ""

# Extract the presentation ID for use in the next step
PRESENTATION_ID=$(echo "$GENERATE_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo ""

# ── 3. Get a presentation by ID ───────────────────────────────────────────────
if [ -n "$PRESENTATION_ID" ]; then
  echo ">>> 3. Get presentation by ID: $PRESENTATION_ID"
  echo "    GET $BASE_URL/api/v1/presentation/$PRESENTATION_ID"
  curl -s "$BASE_URL/api/v1/presentation/$PRESENTATION_ID" | json_print
  echo ""
  echo ""
else
  echo ">>> 3. Get presentation by ID (skipped — no ID returned from step 2)"
  echo ""
fi

# ── 4. List all templates ──────────────────────────────────────────────────────
echo ">>> 4. List all templates"
echo "    GET $BASE_URL/api/v1/templates"
curl -s "$BASE_URL/api/v1/templates" | json_print
echo ""
echo ""

# ── 5. Upload a JSON template definition ──────────────────────────────────────
echo ">>> 5. Upload a JSON template definition"
echo "    POST $BASE_URL/api/v1/upload-template"

# Create a temporary JSON template file
TEMPLATE_FILE=$(mktemp /tmp/template_XXXXXX.json)
cat > "$TEMPLATE_FILE" <<'EOF'
{
  "name": "Example Business Template",
  "description": "A simple business presentation template",
  "theme": "corporate",
  "slides": [
    { "title": "Title Slide", "layout": "title" },
    { "title": "Agenda",      "layout": "content" },
    { "title": "Key Points",  "layout": "content" },
    { "title": "Summary",     "layout": "content" },
    { "title": "Thank You",   "layout": "title" }
  ]
}
EOF

UPLOAD_RESPONSE=$(curl -s -X POST "$BASE_URL/api/v1/upload-template" \
  -F "file=@$TEMPLATE_FILE")
echo "$UPLOAD_RESPONSE" | json_print
rm -f "$TEMPLATE_FILE"
echo ""

# Extract the template ID for use in the next step
TEMPLATE_ID=$(echo "$UPLOAD_RESPONSE" | grep -o '"id":"[^"]*"' | head -1 | cut -d'"' -f4)
echo ""

# ── 6. Generate a presentation using the uploaded template ─────────────────────
if [ -n "$TEMPLATE_ID" ]; then
  echo ">>> 6. Generate a presentation using template ID: $TEMPLATE_ID"
  echo "    POST $BASE_URL/api/v1/generate"
  curl -s -X POST "$BASE_URL/api/v1/generate" \
    -H "Content-Type: application/json" \
    -d "{
      \"prompt\": \"Create a quarterly business review with key highlights\",
      \"slide_count\": 5,
      \"template_id\": \"$TEMPLATE_ID\"
    }" | json_print
  echo ""
  echo ""
else
  echo ">>> 6. Generate using template (skipped — no template ID returned from step 5)"
  echo ""
fi

# ── 7. Transform a .pptx file into a template ─────────────────────────────────
# This step requires a .pptx file to upload. Uncomment and update the path below.
#
# echo ">>> 7. Transform a .pptx file into a template"
# echo "    POST $BASE_URL/api/v1/transform"
# curl -s -X POST "$BASE_URL/api/v1/transform" \
#   -F "file=@/path/to/your_presentation.pptx" \
#   -F "name=My Uploaded Template" \
#   -F "description=Converted from existing presentation" | json_print
# echo ""

echo "======================================================"
echo " All examples complete!"
echo "======================================================"
