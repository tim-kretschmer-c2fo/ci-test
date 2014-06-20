#! /bin/bash
git branch | grep -E stable/ | xargs -I % git branch -D %
git branch | grep dev/ | xargs -I % git branch -D %
git branch -r | grep dev/ | sed "s/origin\///" | xargs -I % git push origin :%
git branch -r | grep stable/ | sed "s/origin\///" | xargs -I % git push origin :%