### API
* Determine if uploaded file exists in file system so that user can be provided heads up before clobbering file
* Determine if effective user is required
* Determine if uuid is required, adding value
* Delete request does not return count of objects deleted, not consistent with delete-many.
* Delete many request takes a simple list.  It does not take a dict with object ids as a key.
* Associations do not support put and patch requests.  It is expected that they are deleted
  and re-created.  This needs to be visited.
* Should file upload have separate end point, to avoid multi-part form limitation of handling
  nested structures?
* Document fetch retrieves the contents of a file, including when it was uploaded and not
  only when it is embedded.  This needs to be revisited, and consider the web
  server serving the file using a separate api end point.

### Authentication
* Only simple DRF token based authentication is supported.  Extend to JWT, oath2(i.e google), etc

### Site Admin
* Responsibility is not clear at this time, and whether a separate UI tool (non django admin) is required for the
  CRUD operations.  Current implementation only supports fetch operations, requiring staff authorization.
* Review whether read-only access is sufficient for non-staff users

### Usage analytics
* Log client amount of usage time per computation
* Capture amount of time has user has been logged in

### Analytics
* Provide high level model, customized model plug in

### Models
* Determine if there is a need for custom User model or whether ClientUser is sufficient
* Database queries have not been optimized.

### Unit test
* It is not clear whether all database instances created are being deleted by underlying Django test framework.
  With sqlite it is not an issue, as the database is an in-memory instance deleted after test run.
  Separately, non-model unit tests track the instances created and delete them.  This may be redundant.
  Review the approach when using postgres as the back end.

### Persistence
* Optimize queries
* Explore using alternative tenant implementation approaches (i.e Postgres Schema)
  as per https://django-tenant-schemas.readthedocs.io/en/latest/use.html