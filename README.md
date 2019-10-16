# document-management
* Primarily intended to provide a document management platform for text based NLP.
* This is a multi-phase project:
  - Text document management backend and API layer.
  - Text analytics layer using AllenNLP, Pythorch, and similar frameworks.
  - Front end using React.
  - Cloud and on-premise hosting.
* Can be leveraged as a foundation for building a commercial product as well as a learning tool.

## Document management

### Key document management features
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

## NLP

### Key NLP features
* Ability to select model family and implementation.
* perform reading comprehension analysis using AllenNLP using BDAF and BDAFNAQNAET.

### Key technical features
* Ability to cache and save to db the analysis results.


# links
* [API](./docs/api.md)
* [Business Object Model](./docs/bom.md)
* [Development](./docs/develop.md)
* [DevOps](./docs/devops.md)
* [Django](./docs/django.md)
* [Git](./docs/git.md)
* [Swagger](./docs/swagger.md)
* [Todo](./docs/todo.md)