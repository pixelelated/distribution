#!/bin/bash
# scripts/get_git 36's cache check, lifted verbatim, over a fixture clone whose
# HEAD is an older commit than its remote branch (#652).
#   sb-get-git-head.sh <empty scratch dir>
SB=${1:?usage: sb-get-git-head.sh <empty scratch dir>}; mkdir "$SB" || exit 2; cd "$SB" || exit 2
export GIT_CONFIG_GLOBAL=/dev/null GIT_AUTHOR_NAME=fixture GIT_AUTHOR_EMAIL=fixture@invalid GIT_COMMITTER_NAME=fixture GIT_COMMITTER_EMAIL=fixture@invalid
git init -q -b main upstream && git -C upstream commit -q --allow-empty -m B && B=$(git -C upstream rev-parse HEAD)
git -C upstream commit -q --allow-empty -m A && A=$(git -C upstream rev-parse HEAD)
git clone -q upstream cache && git -C cache reset -q --hard "$B"      # the cache as a build left it, pinned at B
cd cache
for PKG_VERSION in "$B" "$A"; do
  if git ls-remote . | grep -q -m1 "^${PKG_VERSION}"; then v=accepted; else v=refused; fi
  echo "PKG_VERSION=${PKG_VERSION:0:7}: the cache is $v; HEAD is $(git rev-parse --short HEAD) (B=${B:0:7}, A=${A:0:7})"
done
git ls-remote . | awk '{print substr($1,1,7), $2}'
