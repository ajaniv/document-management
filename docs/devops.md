## local fresh install
### Clone repository from github
`> git clone https://github.com/ondalear/<repository> <project>`
### Set PYTHONPATH
`> export PYTHONPATH=<project path>/src`
### Create a python virtual env
```> python3 -m venv venv/python3.7```
### Activate the python interpreter
```> source venv/python3.7/bin/activate```
### Change directory to project directory
```> cd src/backend```
### Install the python packages
```> LDFLAGS="-L/usr/local/opt/openssl/lib" pip install -r requirements.txt```
### Run schema migrations
```> python manage.py migrate```
### Verify unit tests
```> python manage.py test```
### Load fixtures used for development
```> python manage.py loaddata fixtures/db.json```
### Run the dev python server
```> python manage.py runserver```