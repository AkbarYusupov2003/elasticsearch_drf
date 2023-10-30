from django_elasticsearch_dsl_drf.serializers import DocumentSerializer

from search import documents


class ContentDocumentSerializer(DocumentSerializer):
    class Meta:
        document = documents.ContentDocument
        fields = (
            "title_ru",
            "description_ru"
        )
