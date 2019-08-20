## API
### core
* Determine if uploaded file exists in file system so that user can be provided heads up before clobbering file
* Provide end point for hierarchical tag and category fetch
* Determine if effective user is required

### Authenticaiton
* Only simple token based authentication is supported.  Extend to JWT, google, etc

### Site Admin
* Responsibility is not clear at this time, and whether a separate UI tool (non django admin) is required for the
  CRUD operations.  Current implementation only supports fetch operations, requiring staff authorization.
* Review whether read-only access is sufficient for non-staff users

### General
* Log client amount of usage time per computation
* Capture amount of time has user has been logged in

## Analytics
* Provide high level model, customized model plug in

## Models
* Determine if there is a need for custom User model or whether ClientUser is sufficient

## Unit test
* It is not clear whether all database instances created are being deleted by underlying Django test framework.
  With sqlite it is not an issue, as the database is an in-memory instance deleted after test run.
  Separately, non-model unit tests track the instances created and delete them.  This may be redundant.
  Review the approach when using postgres as the back end.
