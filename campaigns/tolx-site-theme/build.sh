#!/bin/bash
# Rebuild tolx/style.min.css from tolx/style.css (run after every style.css edit).
# Needs Node: npx downloads lightningcss-cli on first run.
set -e
cd "$(dirname "$0")/tolx"
npx --yes lightningcss-cli --minify --targets '>= 0.5%' style.css -o style.min.css
echo "style.min.css: $(wc -c < style.min.css) bytes (style.css: $(wc -c < style.css))"
