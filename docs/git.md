# Strategy
* Subset of git flow

## Workflow
* Master branch is the offical latest working version.
* Work in feature branches off dev branch
* Merge feature branch into dev when ready
* Periodically merge dev into master
* Label master for a given release

## create a new repository on the command line 
echo "# <app name>" >> README.md
git init
git add README.md
git commit -m "first commit"
git remote add origin <https repository url>
git push -u origin master

## push an existing repository from the command line
git remote add origin <https repository url>
git push -u origin master

## Clone
`git clone https://github.com/ondalear/<repository> <project>`

## Branching

### Create any  branch
`> git checkout -b <branch name>`

### Create "dev" branch
`> git checkout -b dev`

### Create feature branch
`> git checkout -b feature_xyz`

##Push
## Push branch
`> git push -u origin dev`