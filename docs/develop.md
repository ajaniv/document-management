## pylint
### run pylint on a file from the project directory
`> pylint --rcfile=.pylintrc <file path>`


## vscode
### change terminal name on Mac
* launch vscode command mode: `cmd + shift + p`
* rename terminal command: `Terminal:Rename`


## Python path
`> export PYTHONPATH=<project path>/src`

`> export PYTHONPATH=~/projects/document_management_dev/document_management/src`
## Running selected unit test in non-django package
```
import unittest
def create_suite():
    """create test suite"""
    suite = unittest.TestSuite()
    suite.addTest(SourceDocumentModelCRUDTests("test_crud"))
    return suite

if __name__ == "__main__":
    runner = unittest.TextTestRunner()
    runner.run(create_suite())

```
## coverage
### run the coverage command
`> coverage run --source ondalear setup.py test`
### run the coverage report
`> coverage report -m`

### sample output
``` bash
> coverage report -m
Name                                                                        Stmts   Miss  Cover   Missing
---------------------------------------------------------------------------------------------------------
ondalear/__init__.py                                                            1      0   100%
ondalear/backend/__init__.py                                                    6      0   100%
ondalear/backend/api/__init__.py                                                0      0   100%
ondalear/backend/api/auto_token.py                                             12     12     0%   7-24
ondalear/back
...
...
...
```

## check manifest
`> check-manifest -v`

## Requires installation of libmagic
### Macos
`> brew install libmagic`