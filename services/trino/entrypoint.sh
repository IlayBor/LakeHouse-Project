#!/bin/bash
# Renders *.properties.tmpl -> *.properties using current env vars, then starts
# Trino. envsubst isn't in the image, so we use a pure-bash substitution that
# only expands variables we explicitly pass. This keeps all credentials in the
# single root .env instead of hardcoded in iceberg.properties.
set -euo pipefail

CATALOG_DIR=/etc/trino/catalog
for tmpl in "$CATALOG_DIR"/*.properties.tmpl; do
    [ -e "$tmpl" ] || continue
    out="${tmpl%.tmpl}"
    rendered="$(cat "$tmpl")"
    for var in CATALOG_URI CATALOG_WAREHOUSE S3_REGION S3_ENDPOINT_URL AWS_ACCESS_KEY_ID AWS_SECRET_ACCESS_KEY; do
        val="${!var-}"
        rendered="${rendered//\$\{$var\}/$val}"
    done
    printf '%s\n' "$rendered" > "$out"
done

exec /usr/lib/trino/bin/run-trino
