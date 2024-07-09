#!/bin/bash

#
# Creating limitless git repo
#
git init
git add .
git commit -m "Initial commit"
# git remote add origin git@github.com:thinknimble/limitless.git
gh repo create thinknimble/limitless --private -y
git push origin main
printf "\033[0;32mRepo https://github.com/thinknimble/limitless/\033[0m \n"
