#!/usr/bin/env bash
# Build the full review hub into a directory and, optionally, commit it to a local orphan gh-pages branch.
#
#   build/pages.sh                         # build into tools/review-hub/out/site and validate it
#   build/pages.sh --commit                # ... then commit the site to the local gh-pages branch (separate worktree)
#   build/pages.sh --skip-build --commit   # only publish what is already in the output directory
#
# This script NEVER pushes. After --commit it prints the one command that would publish.
#
# Options
#   --out DIR         site output directory (default tools/review-hub/out/site)
#   --cache DIR       build cache (default tools/review-hub/build/cache)
#   --commit          commit the built site to the gh-pages branch, in its own worktree
#   --branch NAME     branch to commit to (default gh-pages; created as an orphan branch if it does not exist)
#   --worktree DIR    where the gh-pages worktree lives (default <repo>-gh-pages, next to the checkout)
#   --skip-build      do not build; use what is in --out
#   --rev ID          build only this revision (repeatable); partial sites are meant for testing
#   --fetch-models    download KiCad's 3D models first (done automatically when the cache has none)
#   --force           rebuild every stage, ignoring the build cache
#
# The published tree is the site without the *.glb files: the viewer loads only the .gltf.json twins that
# publish_prep.py writes next to them, which also works on plain static hosts.
set -euo pipefail

HERE=$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)
HUB=$(dirname "$HERE")
REPO=$(git -C "$HUB" rev-parse --show-toplevel)

OUT="$HUB/out/site"
CACHE="$HERE/cache"
BRANCH=gh-pages
WT="${REPO}-gh-pages"
COMMIT=0
SKIP_BUILD=0
FETCH=0
BUILD_ARGS=()

usage() { awk 'NR > 1 && /^#/ {sub(/^# ?/, ""); print; next} NR > 1 {exit}' "${BASH_SOURCE[0]}"; }

while [ $# -gt 0 ]; do
  case "$1" in
    --out) mkdir -p "$2"; OUT=$(cd "$2" && pwd); shift 2;;
    --cache) CACHE=$2; shift 2;;
    --commit) COMMIT=1; shift;;
    --branch) BRANCH=$2; shift 2;;
    --worktree) WT=$2; shift 2;;
    --skip-build) SKIP_BUILD=1; shift;;
    --rev) BUILD_ARGS+=(--rev "$2"); shift 2;;
    --fetch-models) FETCH=1; shift;;
    --force) BUILD_ARGS+=(--force); shift;;
    -h|--help) usage; exit 0;;
    *) echo "unknown option: $1" >&2; usage >&2; exit 2;;
  esac
done

if [ "$SKIP_BUILD" -eq 0 ]; then
  if [ "$FETCH" -eq 1 ] || [ ! -f "$CACHE/packages3D/MANIFEST.json" ]; then
    BUILD_ARGS+=(--fetch-models)
  fi
  python3 "$HERE/build.py" --out "$OUT" --cache "$CACHE" ${BUILD_ARGS[@]+"${BUILD_ARGS[@]}"}
fi

[ -f "$OUT/index.html" ] && [ -f "$OUT/data/revisions.json" ] || { echo "no built site in $OUT" >&2; exit 1; }
python3 "$HERE/validate.py" "$OUT"

# Size of what would be published (no .glb).
python3 - "$OUT" <<'PY'
import sys
from pathlib import Path
fs = [f for f in Path(sys.argv[1]).rglob('*') if f.is_file() and f.suffix != '.glb']
print(f'publishable (no .glb): {len(fs)} files, {sum(f.stat().st_size for f in fs) / 1e6:.1f} MB')
PY

if [ "$COMMIT" -eq 0 ]; then
  echo "site ready in $OUT (serve it with: python3 -m http.server -d '$OUT')"
  exit 0
fi

# ---- local gh-pages commit (separate worktree; the current checkout is not touched) ----
SRC=$(git -C "$REPO" rev-parse --short HEAD)
case "$WT" in "$REPO"|"$REPO"/*) echo "worktree $WT must be outside the repository checkout" >&2; exit 1;; esac

if [ ! -e "$WT/.git" ]; then
  if git -C "$REPO" show-ref --verify --quiet "refs/heads/$BRANCH"; then
    git -C "$REPO" worktree add "$WT" "$BRANCH"
  else
    git -C "$REPO" worktree add --detach "$WT"
    git -C "$WT" checkout --orphan "$BRANCH"
    git -C "$WT" rm -rf -q --ignore-unmatch .
    git -C "$WT" clean -fdxq
  fi
fi
[ "$(git -C "$WT" symbolic-ref --short HEAD)" = "$BRANCH" ] || { echo "$WT is not on branch $BRANCH" >&2; exit 1; }

rsync -a --delete --exclude '.git' --exclude '*.glb' "$OUT"/ "$WT"/
touch "$WT/.nojekyll"

# The worktree holds only the generated site, so staging everything (including deletions) is what we want here.
git -C "$WT" add --all .
if git -C "$WT" diff --cached --quiet; then
  echo "gh-pages already matches this build; nothing to commit"
else
  git -C "$WT" commit -q -F - <<EOF
Publish the review hub built from $SRC

Why: update the static review hub that GitHub Pages (or any static host) serves.
What: the full site from tools/review-hub (viewer, data/, docs/) built from
commit $SRC of $(git -C "$REPO" rev-parse --abbrev-ref HEAD), without the .glb files
(the viewer loads the .gltf.json twins). Verified with build/validate.py
before committing.
EOF
  echo "committed to $BRANCH in $WT: $(git -C "$WT" log -1 --format='%h %s')"
fi
echo "Nothing was pushed. To publish: git -C '$WT' push origin $BRANCH"
