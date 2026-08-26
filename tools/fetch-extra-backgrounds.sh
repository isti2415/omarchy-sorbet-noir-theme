#!/usr/bin/env bash
# Optional: fetch four community wallpapers from Wallhaven that pair well with
# Sorbet Noir. They are NOT redistributed in this repo — they are third-party
# uploads with their own rights holders, so you download them yourself here.
#
#   ./tools/fetch-extra-backgrounds.sh [DEST]
#
# Default DEST is the installed theme's background directory.
set -euo pipefail

DEST="${1:-$HOME/.config/omarchy/themes/sorbet-noir/backgrounds}"
mkdir -p "$DEST"

# id | filename | source page
ENTRIES=(
  "4xz98z|5-aqua-orb.jpg|https://wallhaven.cc/w/4xz98z"
  "573kd1|6-lilac-vortex.jpg|https://wallhaven.cc/w/573kd1"
  "k88m2m|7-rose-nebula.jpg|https://wallhaven.cc/w/k88m2m"
  "ymxr2d|8-constellation.png|https://wallhaven.cc/w/ymxr2d"
)

for entry in "${ENTRIES[@]}"; do
  IFS='|' read -r id name page <<<"$entry"
  ext="${name##*.}"
  url="https://w.wallhaven.cc/full/${id:0:2}/wallhaven-${id}.${ext}"
  echo "→ $name   ($page)"
  curl -fsSL -H "Referer: https://wallhaven.cc/" -o "$DEST/$name" "$url" \
    || echo "  ! failed — the upload may have been removed; see $page"
done

echo
echo "Done. Cycle them with:  omarchy theme bg next"
