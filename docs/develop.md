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

## Requires installation of libmagic
### Macos
`> brew install libmagic`