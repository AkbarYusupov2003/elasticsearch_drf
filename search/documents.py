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
    # description_ru = fields.TextField(
    #     analyzer=analyzers.autocomplete_analyzer,
    #     attr='description_ru',
    #     fields={
    #         'raw': fields.KeywordField(required=True, ),
    #         'suggest': fields.CompletionField(),
    #     }
    # )
    
    class Index:
        name = "contents"
        # settings = {
        #     # "number_of_shards": 1,
        #     # "number_of_replicas": 0,
        #     'max_ngram_diff': 20 
        # }

    class Django:
        model = models.Content
        fields = []
