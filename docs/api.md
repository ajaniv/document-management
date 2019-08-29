# Overview
* The  snippets below show the minimal set of required parameters.  Additional header parameters
  may be required for optimization and compliance with best practices.
* Each of the resources supports POST, PUT, PATCH, GET, and DELETE operations.
* For the `association` operations, the referenced resources have to be created
  prior to the creation of the association (i.e. DocumentTag, DocumentAnnotation)

# Implementation decisions
* Version management will be added as part of content type, and will not require
   url changes.
* Initial authentication implementation is using basic auth to obtain a Token required per API request.
* Django login is not being called, and there is no session management.
* Custom API header has been defined which includes API version, status, and error information.
* On POST and PUT requests minimal set of fields are returned including resource id,
  creation and modification time, and uuid.

# Authentication
* Login is required to the api to obtain a token, which then has to be used
  in all subsequent requests.  The token expires as per configuration setting
  after N hours (i.e. 12), and it then deleted.
* Login is using basic auth, and user id and password are required.
* Per login a new token is created, and the old token if it exists is deleted.
* On logout, the token is deleted.
* Upon successful login last_login time is updated.


# Authorization
* Django model based authorization is being used by default, and  permissions
  have to be granted explicitly in order to perform CRUD operations per
  type.
* End user is not defined as 'staff' member, and cannot log in to the admin site.
* Explicit permission have to be defined for the group to which the user belogns.
* End user can only see objects for  which he/she is authorized.
* User is associated with a Client, either a well defined one or a System Client for
  individual users.
* For both types of clients (actual, system), the associated users have to be added to a Group, to which
  the relevant permissions have been added (i.e. Document add, change, view, delete)
* Permissions should not be managed at the individual user level making it a challenge to manage.



# User admin API
* Designed for login, logout, and change password actions.
## login
### command
``` bash
> curl -X POST   http://localhost:8000/api/user-admin/login/   -H 'Content-Type: application/json' -d '{"username": "client_1_user_1","password": "ondalear123"}' | python3 -m json.tool
```

### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Successfully logged in."
    },
    "detail": {
        "email": "client_1_user_1@gmail.com",
        "token": "7afee96b63de4996519d43914a1c5c76c7227f65",
        "first_name": "Client_1_user_1_first",
        "last_name": "Client_1_user_1_last"
    }
}
```
## logout
### command
``` bash
> curl -X POST   http://localhost:8000/api/user-admin/logout/  -H 'Authorization: Token 7afee96b63de4996519d43914a1c5c76c7227f65' | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Successfully logged out."
    },
    "detail": {}
}
    
```

### command curl no authorization
`> curl -X POST   http://localhost:8000/api/user-admin/logout/ | python3 -m json.tool` 
### command curl no authorization output
``` bash
{
    "header": {
        "user": "*unknown*",
        "api_version": 1,
        "api_status": "ERROR",
        "msg": "Failed to log out."
    },
    "detail": {}
}
```

## change password 
### command
``` bash
> curl -X POST   http://localhost:8000/api/user-admin/password/change/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'   -d '{ "new_password1": "ondalear123","new_password2": "ondalear123"}' | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "New password has been saved."
    },
    "detail": {}
}
```

# Site admin API
* Designed for user, group, client, and client user actions.
* Limited for retrieve and list operations.

## fetch users
### command
``` bash
> curl  http://localhost:8000/api/site-admin/users/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 1,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "id": 5,
            "username": "staff",
            "email": "staff@gmail.com",
            "groups": [
                4
            ]
        }
    ]
}
```
## fetch the specified user
### command
``` bash
> curl  http://localhost:8000/api/site-admin/users/1/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Retrieve request successfully processed."
    },
    "detail": {
        "id": 1,
        "username": "admin",
        "email": "admin@ondalear.com",
        "groups": []
    }
}
```
## fetch groups
### command
``` bash
> curl  http://localhost:8000/api/site-admin/groups/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 1,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "id": 1,
            "name": "ClientOneGroup"
        }
    ]
}
```
## fetch the specified group
### command
``` bash
> curl  http://localhost:8000/api/site-admin/groups/1/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Retrieve request successfully processed."
    },
    "detail": {
        "id": 1,
        "name": "ClientOneGroup"
    }
}
```

## fetch clients
### command
``` bash
> curl  http://localhost:8000/api/site-admin/clients/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 1,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "id": 1,
            "client_id": "client_one",
            "name": "Client One LLC",
            "email": null,
            "phone": null,
            "description": ""
        }
    ]
}
```
## fetch the specified client
### command
``` bash
> curl  http://localhost:8000/api/site-admin/clients/1/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Retrieve request successfully processed."
    },
    "detail": {
        "id": 1,
        "client_id": "client_one",
        "name": "Client One LLC",
        "email": null,
        "phone": null,
        "description": ""
    }
}
```
## fetch client users
### command
``` bash
> curl  http://localhost:8000/api/site-admin/client-users/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 1,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "id": 1,
            "client": 1,
            "user": 2,
            "phone": null,
            "description": ""
        }
    ]
}
```
## fetch the specified client user
### command
``` bash
> curl  http://localhost:8000/api/site-admin/client-users/1/  -H 'Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689'   -H 'Content-Type: application/json'  | python3 -m json.tool
```
### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Retrieve request successfully processed."
    },
    "detail": {
        "id": 1,
        "client": 1,
        "user": 2,
        "phone": null,
        "description": ""
    }
}
```

# Document Management (docmgmt) API

## Tags
### Create tag instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/tags/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"description\": \"curl crated tag\", \"domain\": \"general\", \"name\": \"curl tag 1\", \"target\": \"reference\"}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
}
```
### Fetch tag hierarcy
#### command
``` bash
> curl  "http://127.0.0.1:8000/api/docmgmt/tags-hiearchy/" -H "accept: application/json" -H "Authorization: Token cce1a474b062cf94f5a41fec007942ab60d7e0d1" -H "Content-Type: application/json"  | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Hierarchy request successfully processed."
    },
    "detail": {
        "Client One LLC": [
            {
                "reference": [
                    {
                        "name": "root_tag",
                        "children": [
                            {
                                "name": "curl child tag",
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```
## Categories
### Create category instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/categories/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"description\": \"curl crated category\", \"domain\": \"general\", \"name\": \"curl category 1\", \"target\": \"reference\"}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
```
### Fetch category hierarchy
#### command
``` bash
> curl  "http://127.0.0.1:8000/api/docmgmt/categories-hiearchy/" -H "accept: application/json" -H "Authorization: Token cce1a474b062cf94f5a41fec007942ab60d7e0d1" -H "Content-Type: application/json"  | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Hierarchy request successfully processed."
    },
    "detail": {
        "Client One LLC": [
            {
                "reference": [
                    {
                        "name": "root_category",
                        "children": [
                            {
                                "name": "child category 1",
                                "children": []
                            }
                        ]
                    }
                ]
            }
        ]
    }
}
```
## Annotations
### Create annotation instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/annotations/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"description\": \"curl crated annotation\", \"annotation\": \"some annotation\", \"name\": \"curl annotation 1\"}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
}
```
## Reference Document
* Creates the reference document and the underlying document
* Separate api requests are required to associate the document
  with annotations, tags, and linked documents.
* Contents may be embedded or uploaded with a text file.
### Create reference document with embeded contents
#### Command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/reference-documents/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json" -d "{ \"content_type\": \"txt\", \"description\": \"curl created reference document\", \"name\": \"curl reference document\", \"title\": \"curl source document title\", \"content\": \"curl reference document contents\"}" | python3 -m json.tool
```
#### Output
```bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Create request successfully processed."
    },
    "detail": {
        "id": 6,
        "uuid":"6d9fca88-db3c-4b0a-bc55-bc7a1a6181ef",
        "creation_time": "2019-07-27T18:36:42.432597Z",
        "version":1
    }
}
```
### Create reference document with file upload
#### command using json
``` bash
> curl \
 -X POST  "http://127.0.0.1:8000/api/docmgmt/reference-documents/" \
 -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" \
 -H "Accept: application/json" \
 -H "Content-Type: multipart/form-data" \
 -F "document={ \"content_type\": \"txt\", \"description\": \"curl created reference document\", \"name\": \"api.md\", \"title\": \"Curl reference uploaed document title\"};type=application/json}" \
 -F "upload=@docs/api.md;type=text/plain" | python3 -m json.tool

```
#### Output
```bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Create request successfully processed."
    },
    "detail": {
        "id": 6,
        "uuid":"6d9fca88-db3c-4b0a-bc55-bc7a1a6181ef",
        "creation_time": "2019-07-27T18:36:42.432597Z",
        "version":1
    }
}
```
#### command using multi part form
``` bash
> curl \
 -X POST  "http://127.0.0.1:8000/api/docmgmt/reference-documents/" \
 -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" \
 -H "Accept: application/json" \
 -H "Content-Type: multipart/form-data" \
 -F "description=curl created source document" \
 -F "name=api.md" \
 -F "title=Curl source document title" \
 -F "upload=@docs/api.md;type=text/plain" | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Create request successfully processed."
    },
    "detail": {
        "id": 6,
        "uuid":"6d9fca88-db3c-4b0a-bc55-bc7a1a6181ef",
        "creation_time": "2019-07-27T18:36:42.432597Z",
        "version":1
    }
}
```
### Fetch reference document list
#### Command
``` bash
> curl "http://127.0.0.1:8000/api/docmgmt/reference-documents/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json" | python3 -m json.tool
```
#### Output
```bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 2,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "content": null,
            "dir_path": null,
            "upload": "http://127.0.0.1:8000/media/client_one/client_1_user_1/api.md",
            "file_contents": "# Overview\n* ....",
            "creation_time": "2019-08-27T20:36:26.036483Z",
            "creation_user": 2,
            "is_deleted": false,
            "is_enabled": true,
            "effective_user": 2,
            "id": 9,
            "site": 1,
            "update_user": 2,
            "update_time": "2019-08-27T20:36:26.057937Z",
            "uuid": "65abed40-4d8a-4f77-a647-9b00bdee5bd1",
            "version": 2,
            "annotations": [],
            "client": 1,
            "category": null,
            "description": "curl created reference document",
            "documents": [],
            "document_type": "reference",
            "language": "en-us",
            "mime_type": "application/octet-stream",
            "name": "api.md",
            "tags": [],
            "title": "Curl reference uploaded document title"
        },
        {
            "content": "curl reference document contents",
            "dir_path": null,
            "upload": null,
            "file_contents": null,
            "creation_time": "2019-08-27T20:32:17.810371Z",
            "creation_user": 2,
            "is_deleted": false,
            "is_enabled": true,
            "effective_user": 2,
            "id": 8,
            "site": 1,
            "update_user": 2,
            "update_time": "2019-08-27T20:32:17.825788Z",
            "uuid": "2691ce33-63c7-4043-907c-82eca9d7980a",
            "version": 2,
            "annotations": [],
            "client": 1,
            "category": null,
            "description": "curl created reference document",
            "documents": [],
            "document_type": "reference",
            "language": "en-us",
            "mime_type": "text/plain",
            "name": "curl reference document",
            "tags": [],
            "title": "curl source document title"
        }
    ]
}
```
## Auxiliary documents
### Create auxiliary document
* Creates the auxiliary document and the underlying document
* Separate api requests are required to associate the document
  with annotations and tags.
* Contents may be embedded or uploaded with a text file.
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/auxiliary-documents/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"content_type\": \"txt\", \"description\": \"curl created auxiliary document\", \"document_type\": \"auxiliary\", \"name\": \"curl auxiliary document\", \"title\": \"Curl auxiliary document title\", \"content\": \"curl auxiliary document contents\"}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T15:08:30.872824Z",
    "id": 3,
    "uuid": "b07eaad7-e66d-41ff-9944-2c471fc455f8",
    "version":1
  }
}
```
## Document tags
* Create document tag association
* Requires prior creation of reference or auxiliary document and the tag
* This association makes the document searchable by the tag
### Create document tag instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-tag/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"document\": 9, \"tag\": 1}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
}
```
### fetch list of document tags user is authorized to see
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/document-tag/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "List request successfully processed.",
    "pagination": {
      "count": 1,
      "next": null,
      "previous": null
    }
  },
  "detail": [
    {
      "creation_time": "2019-07-27T15:08:30.888306Z",
      "creation_user": 2,
      "is_deleted": false,
      "is_enabled": true,
      "effective_user": 2,
      "id": 2,
      "site": 1,
      "update_user": 2,
      "update_time": "2019-07-27T15:08:30.888332Z",
      "uuid": "bcbb9474-0680-42ab-b800-eea378c25a00",
      "version": 1,
      "client": 1,
      "document": 3,
      "tag": 2
    }
  ]
}
```
### Delete set of document tags user is authorized to see
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-tag-delete-many/" -H "accept: application/json" -H "Authorization: Token 565dadc6de02c8659cb2d3cf089ef5e337ccd6bf" -H "Content-Type: application/json"  -d "[10]" | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Delete request successfully processed."
    },
    "detail": {
        "count_deleted": 1
    }
}
```
## Document annotations
* Allows the association of a document with 1->N annotations.
* Requires the prior creation of a reference or auxiliary document and the annotation.
### Create document annotation instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-annotations/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"document\": 9, \"annotation\": 4}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
}
```
### fetch list of document annotations user is authorized to see
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/document-annotation/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "List request successfully processed.",
    "pagination": {
      "count": 1,
      "next": null,
      "previous": null
    }
  },
  "detail": [
    {
      "creation_time": "2019-07-27T15:08:30.888306Z",
      "creation_user": 2,
      "is_deleted": false,
      "is_enabled": true,
      "effective_user": 2,
      "id": 2,
      "site": 1,
      "update_user": 2,
      "update_time": "2019-07-27T15:08:30.888332Z",
      "uuid": "bcbb9474-0680-42ab-b800-eea378c25a00",
      "version": 1,
      "client": 1,
      "document": 3,
      "annotation": 2
    }
  ]
}
```
### Delete set of document annotations
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-annotation-delete-many/" -H "accept: application/json" -H "Authorization: Token 565dadc6de02c8659cb2d3cf089ef5e337ccd6bf" -H "Content-Type: application/json"  -d "[5]" | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Delete request successfully processed."
    },
    "detail": {
        "count_deleted": 1
    }
}
```
## Document association (links)
* Establishes an association between a reference (from document) and auxiliary (to document) document for the given purpose.
### Create document association instance
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-association/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" -H "Content-Type: application/json"  -d "{ \"from_document\": 9, \"to_document\": 7, \"purpose\": \"question\"}" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "Create request successfully processed."
  },
  "detail": {
    "creation_time": "2019-07-27T14:52:15.362879Z",
    "id": 2,
    "uuid": "91824c7f-9106-4e12-959a-938871c6fc65",
    "version":1
  }
}
```
### fetch list of document association (links) user is authorized to see
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/document-association/" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
``` bash
{
  "header": {
    "user": "client_1_user_1",
    "api_version": 1,
    "api_status": "OK",
    "msg": "List request successfully processed.",
    "pagination": {
      "count": 1,
      "next": null,
      "previous": null
    }
  },
  "detail": [
    {
      "creation_time": "2019-07-27T15:08:30.888306Z",
      "creation_user": 2,
      "is_deleted": false,
      "is_enabled": true,
      "effective_user": 2,
      "id": 2,
      "site": 1,
      "update_user": 2,
      "update_time": "2019-07-27T15:08:30.888332Z",
      "uuid": "bcbb9474-0680-42ab-b800-eea378c25a00",
      "version": 1,
      "client": 1,
      "from_document": 3,
      "to_document": 2,
      "purpose": "question"
    }
  ]
}
```
### Delete set of document association
#### command
``` bash
> curl -X POST "http://127.0.0.1:8000/api/docmgmt/document-association-delete-many/" -H "accept: application/json" -H "Authorization: Token 565dadc6de02c8659cb2d3cf089ef5e337ccd6bf" -H "Content-Type: application/json"  -d "[9]" | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "Delete request successfully processed."
    },
    "detail": {
        "count_deleted": 1
    }
}
```
## Document queries
* These are intended to support filtering by name|names, date ranges, tag|tags, and category|categories
### fetch list of documents based on a tag list
* Tag queries support in and exact match.
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/reference-documents/?document__tags__in=1" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
``` bash
{
    "header": {
        "user": "client_1_user_1",
        "api_version": 1,
        "api_status": "OK",
        "msg": "List request successfully processed.",
        "pagination": {
            "count": 1,
            "next": null,
            "previous": null
        }
    },
    "detail": [
        {
            "content": null,
            "dir_path": null,
            "upload": "http://127.0.0.1:8000/media/client_one/client_1_user_1/api.md",
            "file_contents": ".....",
            "creation_time": "2019-08-27T20:36:26.036483Z",
            "creation_user": 2,
            "is_deleted": false,
            "is_enabled": true,
            "effective_user": 2,
            "id": 9,
            "site": 1,
            "update_user": 2,
            "update_time": "2019-08-27T20:36:26.057937Z",
            "uuid": "65abed40-4d8a-4f77-a647-9b00bdee5bd1",
            "version": 2,
            "annotations": [
                4
            ],
            "client": 1,
            "category": null,
            "description": "curl created reference document",
            "documents": [
                7
            ],
            "document_type": "reference",
            "language": "en-us",
            "mime_type": "application/octet-stream",
            "name": "api.md",
            "tags": [
                1
            ],
            "title": "Curl reference uploaed document title"
        }
    ]
}
```
### fetch list of documents based on exact match with  document name
* The document name can be part of a list of names (in clause), exact match, or starts witch
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/reference-documents/?document__name=api.md" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
* see above

### fetch list of documents based on exact match with category  name
* The category name can be part of a list of names(in clause) or exact match
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/reference-documents/?document__category_name=curl%20category%201" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
* see above
### fetch list of documents based on update time
* The update time can be specified as greater than, less than, and within a range
#### command
``` bash
> curl -X GET "http://127.0.0.1:8000/api/docmgmt/reference-documents/?document__update_time__gte=2019-08-27+19:33:19" -H "accept: application/json" -H "Authorization: Token 305078cfe62d75e09384bb8a83e7fc464b669689" | python3 -m json.tool
```
#### output
* see above

# Issues
* Review request parameters and header parameters, verify correctness
* Returning the resource id, which is an object id stored in the db.  Exposing internal data
  through the API
* Consider having separate api for file upload, retrieval
* Reveiw the approach to support both file upload and content.  Files should be served by the web server
  not the application server.