# document-management
* Primarily intended to provide a document management platform for text based NLP.
* This is a multi-phase project:
  - Text document management backend and API.
  - AllenNLP based text analysis back end and API.
  - Front end using react.
  - Cloud and on-premise hosting.
* Can be leveraged as a foundation for building a commercial product as well as a learning tool.

## Document management backed end and API

### Key functionalal features
* Create/update/delete/fetch of text documents, both embeded and file based.
* Document search using date range, name, category, and tag criteria applying 'in', exact match, and range criteria.
* Association of document with tags and category for classification and search.
* Annotation of document.
* Linking of documents.
* Support for user, group, client, and client user abstractions which govern
  document access.

### Key technical features
* Token based authentication.
* Group based access authorization to documents and other abstractions.
* Basic administration portal.
* Auto-generated OpenAPI compliant API.


# links
* [API](./docs/api.md)
* [Business Object Model](./docs/bom.md)
* [Development](./docs/develop.md)
* [DevOps](./docs/devops.md)
* [Django](./docs/django.md)
* [Git](./docs/git.md)
* [Swagger](./docs/swagger.md)
* [Todo](./docs/todo.md)