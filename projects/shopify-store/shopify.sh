#!/usr/bin/env bash
# Shopify Admin GraphQL helper. Credentials come from ~/.zshrc, never this file.
#   SHOPIFY_STORE, SHOPIFY_CLIENT_ID, SHOPIFY_CLIENT_SECRET
# Usage: ./shopify.sh '{ shop { name } }'            (query string)
#        ./shopify.sh -f query.graphql [vars.json]  (query file + optional variables)
#        STORE=bebita ./shopify.sh ...              (Bebita Lifestyle: uses BEBITA_* vars)
set -euo pipefail
if [[ "${STORE:-}" == "bebita" ]]; then
  SHOPIFY_STORE="${BEBITA_STORE:?}" SHOPIFY_CLIENT_ID="${BEBITA_CLIENT_ID:?}" SHOPIFY_CLIENT_SECRET="${BEBITA_CLIENT_SECRET:?}"
fi
: "${SHOPIFY_STORE:?set in ~/.zshrc}" "${SHOPIFY_CLIENT_ID:?}" "${SHOPIFY_CLIENT_SECRET:?}"
API_VERSION="${SHOPIFY_API_VERSION:-2026-07}"
CACHE="${TMPDIR:-/tmp}/shopify-token-${SHOPIFY_STORE}"

token() {
  # Client-credentials tokens are short-lived; reuse for 20h, then refresh.
  if [[ -f "$CACHE" && $(( $(date +%s) - $(stat -f %m "$CACHE") )) -lt 72000 ]]; then
    cat "$CACHE"; return
  fi
  local resp
  resp=$(curl -sS -X POST "https://${SHOPIFY_STORE}/admin/oauth/access_token" \
    -H 'Content-Type: application/x-www-form-urlencoded' \
    --data-urlencode "grant_type=client_credentials" \
    --data-urlencode "client_id=${SHOPIFY_CLIENT_ID}" \
    --data-urlencode "client_secret=${SHOPIFY_CLIENT_SECRET}")
  local t; t=$(printf '%s' "$resp" | python3 -c 'import sys,json; print(json.load(sys.stdin).get("access_token",""))' 2>/dev/null || true)
  [[ -n "$t" ]] || { echo "token fetch failed: $resp" >&2; exit 1; }
  umask 077; printf '%s' "$t" > "$CACHE"; printf '%s' "$t"
}

if [[ "${1:-}" == "-f" ]]; then q=$(cat "$2"); v=$( [[ -n "${3:-}" ]] && cat "$3" || echo '{}'); else q="$1"; v='{}'; fi
body=$(python3 -c 'import sys,json; print(json.dumps({"query":sys.argv[1],"variables":json.loads(sys.argv[2])}))' "$q" "$v")
curl -sS -X POST "https://${SHOPIFY_STORE}/admin/api/${API_VERSION}/graphql.json" \
  -H 'Content-Type: application/json' -H "X-Shopify-Access-Token: $(token)" \
  -d "$body" | python3 -m json.tool
