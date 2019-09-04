# Busines Object Model Overview
## Model common fields
* creation time
* udpate time
* creation user
* update user
* uuid
* id


## User
* Requires registration by site admin
### Key properties
* user id
* password
* group or groups

## Group
* Defines the permissions which a user associated with the group would have

## Client
* Requires registration by site admin prior to user creation.
* Logically a tenant

### Key properties
* Client id.  Used to associate end user with a tenant.
* Client name. 

## ClientUser
* Requires registration of client prior to user registration.
* Requires registration by site admin prior usage of API.
* Logically an extension of Django User abstraction.

### Key properties
* Client id to associate user with tenant.

## Document
* Separate classes and tables are created for reference and auxiliary documents, using an abstract
  base class and inheritance.
* Document table is being referenced by reference and auxiliary documents usine one-to-one relationship.
* Document contents is being validated by `python-ftfy` from https://github.com/LuminosoInsight/python-ftfy
  Significant more work is required to define the validation rules and implement them to avoid
  allowing bad data into the system.
* Document size is constrained to 1 MB
* File size is constrained to 10 MB.  There is no validation of file contents at this time; this
  clearly needs to be revisited.
* A document can be associated with 0 or more other documents.  For instance, a `reference document` can be
  associated with an `auxiliary document` with a specified `purpose`


### Key properties
* annotations.  Optional set of associated annotations.
* client.
* description.
* documents.  Optional set of associated documents.
* language.  Defaults to Englishe
* name.  Needs to be unique per client.
* category.  Document may be associated with a category.
* mime_type.  (i.e. text/plain)
* document_type.  (i.e. auxiliary, reference)
* tags.  Optional set of associated tags.
* title.  Optional title.

## Tag
* Tag has an optional parent tag link supporting a hierarchical representation.
* Tag has client foreign key, which can be both to a system client and end user client
* Document is associated with 0 or more tags, both leaf and intermediate if so desired, but not      recommended.
* After creating  a document, one can associate it with one or more tags by tag id
* One can make a request to fetch tag hierarchy, which will return a tree of tags, one system, one   client
* When making a document query, one can associate the query with one or more tags.  These should  be the tag id’s of the selected node and its children, if any.
* When changing the tag hierarchy, a leaf tag could become a parent or intermediate tag, with document linked to it.  This will not be an issue, as when making a query, one need to provide the tag tree branch tag  set.
* There is a many-2-many table with document id’s and tags.
* A document deletion results in the table entry being removed, similarly when a tag is removed, at which point the document will not have the tag.
* When a client is deleted, all its tags and documents are deleted.
* Tag may be associated with both auxiliary and reference documents.

### Key properties
* name
* parent
* target.  Determines whether the tag target space (i.e. referene or auxiliary document).
* domain.  Determines the domain space (i.e. insurance, finance)

## Category
* Designed as another means to  classify documents.
* Document may be associated with category.
* Has a similar hierarchical structure as tag.
* A document may be associated with 0..N categories.
* Category may be associated with both auxiliary and reference documents.

### Key properties
* name
* parent
* target
* domain

## Annotation
* Designed to support association of a document with 0..N
  annotations, allowing end user to capture time sensitive notes
  durint document lifecycle.
* Annotation may be associated with both auxiliary and reference documents.
* The same annotation may be associated with multiple documents.

### Key properties
* name
* annotation


## DocumentAnnotation
* Designed to support the association of a document with an annotation instance.
* Deletion of document or annotation results in the deletion of the association.

### Key properties
* document
* annotation

## DocumentTag
* Designed to support the association of a document with a tag instance.
* Deletion of document or annotation results in the deletion of the association.

### Key properties
* document
* tag

## DocumentAssocation
* Designed to support the association of a document with another document.
* Loosely constrained to have a reference document link to an auxiliary document.
* Deletion of either documents results in the deletion of the association.

### Key properties
* from_document
* to_document
* purpose

# Issues
* Need to determine whether detailed address field breakdown is required for client/tenant, client user,
  and whether multiple addresses, address type are to be supported.  Address breakdown is region, country specific.
* Need to determine whether multiple phone numbers, number type (work, cell) are required per client/tenant, client user
* Category and tag hierarchy organization should include domain,
  other considerations.
