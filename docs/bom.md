# Busines Object Model Overview
## Model common fields
* creation time
* udpate time
* creation user
* update user
* id
* pk


## User
* Requires registration
### Key properties
* user id
* password
* group or groups

## Group
* Defines the permissions which a user associated with the group would have

## Client
* Requires registration prior to user creation.
* Logically a tenant

### Key properties
* Client id.  Used to associate end user with a tenant.
* Client name. 

## ClientUser
* Requires registration of client prior to user registration.
* Requires registration prior usage of API.

### Key properties

* Client id to associate user with tenant.

## Document
* Separate classes and tables are created for reference and auxiliary documents, using an abstract
  base class and inheritance.
* Document table is being referenced by reference and auxiliary documents.
* Document contents is being validated by `python-ftfy` from https://github.com/LuminosoInsight/python-ftfy
  Significant more work is required to define the validation rules and implement them to avoid
  allowing bad data into the system.
* Document size is constrained to 1 MB
* File size is constrained to 10 MB.  There is no validation of file contents at this time; this
  clearly needs to be revisited.
* A document can be associated with 0 or more other documents.  For instance, a `reference document` can be
  associated with an `auxiliary document` with a specified `purpose`


### Key properties

## Tag
* Tag has a parent tag link
* Tag has client foreign key, which can be both to a system client and end user client
* Document is associated with 0 or more tags, both leaf and intermediate if so desired, but not      recommended.
* When creating or updating  a document, one can associate it with one or more tags by tag id
* One can make a request to fetch tag hierarchy, which will return a tree of tags, one system, one   client
* When making a document query, one can associate the query with one or more tags.  These should     be the tag id’s of the selected node and its children, if any.
* When changing the tag hierarchy, a leaf tag could become a parent or intermediate tag, with        document linked to it.  This will not be an issue, as when making a query, one need to provide     the tag tree branch tag  set.
* There is a many-2-many table with document id’s and tags.
* A document deletion should result in the table entry being removed, similarly when a tag is        removed, at which point the document will not have the tag.
* When a client is deleted, all its tags and documents are deleted.
* There are separate tag tables for Criteria and Source document.  The desire was to leave
  the two tag namespaces separate.
### Key properties
* name
* parent

## Category
* Document may be associated with category.

### Key properties
* name
* parent

# Issues
* Need to determine whether detailed address field breakdown is required for client/tenant, client user,
  and whether multiple addresses, address type are to be supported.  Address breakdown is region, country specific.
* Need to determine whether multiple phone numbers, number type (work, cell) are required per client/tenant, client user
