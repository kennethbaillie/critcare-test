# Useful commands

## Find/replace

grep -rl --exclude-dir .git --exclude-dir .jekyll* --exclude-dir _site "pattern" ./
grep -rl --exclude-dir .git --exclude-dir .jekyll* --exclude-dir _site "Link" ./

## to enable auto update of submodule

subl .gitmodules
add 'branch=main'
git submodule update --remote
