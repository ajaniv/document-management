## Django unit test
### run all unit tests
`> python manage.py test`
### unit test a specific module
`> python manage.py test ondalear.backend.tests.docmgmt.models.test_client`
### unit test a specify class
`> python manage.py test ondalear.backend.tests.docmgmt.models.ClientModelCRUDTests`
### unit test a specific test method
`> python manage.py test ondalear.backend.tests.docmgmt.models.test_client.ClientModelCRUDTests.test_crud`

## Django admin
### create super user
`> python manage.py createsuperuser`
### change admin password
`> python manage.py changepassword admin`
### Clear session data
`> python manage.py clearsessions`

## Schema
### Make schema migration and assign it a name
`> python manage.py makemigrations -n contact docmgmt`
### Migrate
`> python manage.py migrate`

## Fixtures
### dump database content
```> python manage.py dumpdata --natural-foreign --natural-primary --indent 2 --format json --exclude auth.permission --exclude contenttypes --exclude admin.logentry --exclude sessions > db.json```

### load the database from a prior dump
`python manage.py loaddata db.json`

## turn DEBUG on decorator during using test
`from django.test.utils import override_settings`
`@override_settings(DEBUG=True)`

# Issues
* Cannot have migrations for data for initializing the database with complex objects
  It can handle simple things like adding a user, but an object with foreign key
  references fails on wrong foreign key referene with __fake__ prefixed to class name