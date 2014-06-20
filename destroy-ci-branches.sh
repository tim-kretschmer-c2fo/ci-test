#! /bin/bash

if [ -z "$1" ]
  then
    echo "This script will destroy local and remote branches."
    echo "If you want that to happen, then run it with any argument"
    echo ""
    echo "ie: ./destroy-ci-branches.sh dangerzone"
    exit
fi

git branch | grep -E stable/ | xargs -I % git branch -D %
git branch | grep dev/ | xargs -I % git branch -D %
git branch -r | grep dev/ | sed "s/origin\///" | xargs -I % git push origin :%
git branch -r | grep stable/ | sed "s/origin\///" | xargs -I % git push origin :%
git remote prune origin
