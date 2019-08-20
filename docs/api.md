# Overview
* The  snippets below show the minimal set of required parameters.  Additional header parameters
  may be required for optimization and compliance with best practices.

# Implementation decisions
* Version management will be added as part of content type, and will not require
   url changes.
* Initial authentication implementation is using basic auth
* Django login is not being called, and there is no session management

# Authentication
* Login is required to the api to obtain a token, which then has to be used
  in all subsequent requets.
* Login is using basic auth, and user id and password are required.
* On logout, the token is deleted.
* Upon successful login last_login time is updated.


# Authorization
* End user is not a staff member, and cannot log in to the admin site.
* Explicit permission have to be defined for the group to which the user belogns.
* End user can only see objects for  which he/she is authorized.
* User is associated with a Client, either a well defined one or a System Client for
  individual users.
* For both types of clients (actual, system), associated users have to be added to a Group, to which
  the relevant permissions have been added (i.e. Document add, change, view, delete)
* Permissions should not be managed at the individual user level.



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

# Issues
* Review request parameters and header parameters, verify correctness
* Returning the resource id, which is an object id stored in the db.  Exposing internal data
  through the API
* Consider having separate api for file upload, retrieval
* Reveiw the approach to support both file upload and content.  Files should be served by the web server
  not the application server.