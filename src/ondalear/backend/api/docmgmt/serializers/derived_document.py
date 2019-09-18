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
                                             Document,
                                             ReferenceDocument)
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
        return instance.get_file_contents()

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

        return derived_document


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
