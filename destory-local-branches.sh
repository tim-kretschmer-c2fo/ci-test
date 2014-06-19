#! /bin/bash
git branch -D `git branch | grep -E 'stable//*'`
git branch -D `git branch | grep -E 'dev//*'`
