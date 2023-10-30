from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from search import models
from search import analyzers
from elasticsearch_dsl import analyzer, tokenizer


@registry.register_document
class ContentDocument(Document):
    
    title_ru = fields.TextField(
        analyzer=analyzers.edge_ngram_analyzer,
        #search_analyzer='standard',
        attr='title_ru',
        fields={
            'raw': fields.KeywordField(required=True, ),
            'suggest': fields.CompletionField(),
        }
    )
    
    class Index:
        name = "contents"

    class Django:
        model = models.Content
        fields = []
