"""
.. module::  ondalear.backend.api.docmgmt.serializers.derived_document
   :synopsis:  ondalear docmgmt derived document serializers module.

"""
import logging
import json
from django.http import QueryDict
from rest_framework.utils import json
from rest_framework.serializers import (FileField,
                                        ModelSerializer,
                                        SerializerMethodField)

from ondalear.backend.docmgmt.models import (constants,
                                             AuxiliaryDocument,
                                             DocumentAssociation,
                                             Document,
                                             DocumentTag,
                                             ReferenceDocument,
                                             Tag)
from ondalear.backend.api.base_serializers import RequestContextMixin
from ondalear.backend.api.docmgmt.serializers.document import DocumentSerializer


_logger = logging.getLogger(__name__)

# pylint: disable=too-many-ancestors


class AbstractDerivedDocumentModelSerializer(RequestContextMixin, ModelSerializer):
    """Base document serializer class.
    """
    document = DocumentSerializer(many=False, read_only=False)
    upload = FileField(allow_empty_file=False, validators=[],
                       required=False, allow_null=True,
                       max_length=constants.UPLOAD_FIELD_MAX_FILE_SIZE)

    file_contents = SerializerMethodField()

    class Meta:
        """Meta class"""
        fields = ('content', 'document', 'dir_path', 'upload', 'file_contents')

    def get_file_contents(self, instance):  # pylint: disable=no-self-use
        """get file contents if file has been uploaded"""
        data = None
        if instance.upload:
            try:
                with open(instance.upload.path) as input_file:
                    data = input_file.read()
            except IOError as ex:
                _logger.error('invalid file %s exc %s', instance.upload.path, ex)
        return data

    def _document_type(self):
        """get document type"""
        # pylint: disable=no-member
        if self.Meta.model is AuxiliaryDocument:
            document_type = constants.DOCUMENT_TYPE_AUXILIARY
        elif self.Meta.model is ReferenceDocument:
            document_type = constants.DOCUMENT_TYPE_REFERENCE
        else:
            document_type = constants.DOCUMENT_TYPE_UNKNOWN
        return document_type

    def is_valid(self, raise_exception=False):
        """validate the underlying data"""
        # need to massage the request data to pass validation
        # the request data is flat, while we have a nested document model
        doc_fields = DocumentSerializer.field_names()
        initial_data = self.initial_data.copy()
        if isinstance(initial_data, (QueryDict,)):
            # @TODO: this is required for multi part request - cannot handle QueryDict
            initial_data = initial_data.dict()
        
        document_data = initial_data.pop('document', None)
        if document_data and isinstance(document_data, (str,)):
            document_data = json.loads(document_data)
        else:
            document_data = {name: initial_data.pop(name, None)
                             for name in doc_fields if name in initial_data}
        initial_data['document'] = document_data
        self.initial_data = initial_data

        super(AbstractDerivedDocumentModelSerializer, self).is_valid(
            raise_exception=raise_exception)

    def _create_document_tags(self, document, tags, create_context=None):
        """create document tag association"""
        if tags:
            create_context = create_context or self.build_request_context()
            for tag_id in tags:
                # assert tag exists
                try:
                    tag = Tag.objects.get(pk=tag_id)
                    DocumentTag.objects.create(document=document, tag=tag, **create_context)
                except Tag.DoesNotExist:  # pylint: disable=no-member
                    _logger.error('tag does not exist: %s', tag_id)

    def _delete_document_tags(self, document):   # pylint: disable=no-self-use
        """delete the tags associated with the document"""
        DocumentTag.objects.filter(document=document).delete()

    def _create_document_associations(self, from_document, documents, create_context=None):
        """create document->document association"""
        if documents:
            # when using multi part for file upload, underlying framework
            #  is using QueryDict, and the 'documents' value  is converted to stirng.
            if isinstance(documents, (str,)):
                replaced = documents.replace("'", "\"")
                documents = [json.loads(replaced)]

            create_context = create_context or self.build_request_context()
            for document_id, purpose in documents:
                # assert document exists
                try:
                    to_document = Document.objects.get(pk=document_id)
                    DocumentAssociation.objects.create(from_document=from_document,
                                                       to_document=to_document,
                                                       purpose=purpose,
                                                       **create_context)
                except Document.DoesNotExist:  # pylint: disable=no-member
                    _logger.error('document does not exist: %s', document_id)

    def _delete_document_associations(self, document):   # pylint: disable=no-self-use
        """delete the document associations"""
        DocumentAssociation.objects.filter(from_document=document).delete()

    def to_representation(self, instance):      # pylint: disable=arguments-differ
        """Move fields from document to derived document representation."""

        representation = super(
            AbstractDerivedDocumentModelSerializer, self).to_representation(instance)
        document_representation = representation.pop('document')
        representation.update(document_representation)
        return representation

    def create(self, validated_data):
        """create derived instance"""
        # extract document data
        document_data = validated_data.pop('document')
        create_context = self.build_request_context()
        document_data.update(create_context)

        # set document type
        document_type = self._document_type()
        document_data['document_type'] = document_type

        # create document instance
        document = Document.objects.create(**document_data)

        # create derived instance
        validated_data['document'] = document
        derived_document = self.Meta.model.objects.create(**validated_data)  # pylint: disable=no-member

        # @TODO would have expected to have a beter way of getting tag handles
        tags = self.context['request'].data.get('tags')
        self._create_document_tags(document, tags, create_context)

        documents = self.context['request'].data.get('documents')
        self._create_document_associations(document, documents, create_context)

        return derived_document

    def _update_tag_associations(self, document):
        """update tag associations"""
        # @TODO would have expected to have a beter way of getting tag handles
        tags = self.context['request'].data.get('tags')
        if tags:
            # need to get existing list of tags
            existing_tags = [item.tag_id for item
                             in list(DocumentTag.objects.filter(document=document).only('tag_id'))]

            # if the existing list is not the same, need to update
            if sorted(tags) != sorted(existing_tags):
                # delete existing tag associations
                self._delete_document_tags(document)
                # create new tag associations
                self._create_document_tags(document, tags)

    def _update_document_associations(self, document):
        """update document association"""
        documents = self.context['request'].data.get('documents')
        if documents:
            # need to get existing list of document links
            existing_documents = [
                [item.to_document.id, item.purpose] for item
                in list(DocumentAssociation.objects.filter(
                    from_document=document).only('to_document', 'purpose'))]
            # if the existing list is not the same, need to update
            def take_first(elem):
                return elem[0]
            if sorted(documents, key=take_first) != sorted(existing_documents, key=take_first):
                # delete existing document association
                self._delete_document_associations(document)
                # create new document association
                self._create_document_associations(document, documents)

    def update(self, instance, validated_data):
        """update the instance"""
        document_data = validated_data.pop('document')
        document = instance.document
        # update the document
        for key, value in document_data.items():
            setattr(document, key, value)
        # update the derived document
        for key, value in validated_data.items():
            setattr(instance, key, value)

        # save changes
        document.save()
        instance.save()

        self._update_tag_associations(document)
        self._update_document_associations(document)

        return instance


class AuxiliaryDocumentSerializer(AbstractDerivedDocumentModelSerializer):
    """Auxiliary document serializer class"""

    class Meta(AbstractDerivedDocumentModelSerializer.Meta):
        """Meta class"""
        model = AuxiliaryDocument


class ReferenceDocumentSerializer(AbstractDerivedDocumentModelSerializer):
    """Reference document serializer class"""

    class Meta(AbstractDerivedDocumentModelSerializer.Meta):
        """Meta class"""
        model = ReferenceDocument
