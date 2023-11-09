from django_elasticsearch_dsl import Document, fields
from django_elasticsearch_dsl.registries import registry

from content import models
from content import analyzers


@registry.register_document
class ContentDocument(Document):
    title_ru = fields.TextField(
        attr="title_ru",
        fields={
            "multiple_words_ngram": fields.TextField(analyzer=analyzers.multiple_words_analyzer),
            "strict_edge": fields.TextField(analyzer=analyzers.strict_edge_ngram_analyzer),
            "medium_edge": fields.TextField(analyzer=analyzers.medium_edge_ngram_analyzer),
            "soft_edge": fields.TextField(analyzer=analyzers.soft_edge_ngram_analyzer),
            "very_soft_edge": fields.TextField(analyzer=analyzers.very_soft_edge_ngram_analyzer),
            "strict_ngram": fields.TextField(analyzer=analyzers.strict_ngram_analyzer),
            "medium_ngram": fields.TextField(analyzer=analyzers.medium_ngram_analyzer),
        }
    )
    title_uz = fields.TextField(
        attr="title_uz",
        fields={
            "multiple_words_ngram": fields.TextField(analyzer=analyzers.multiple_words_analyzer),
            "strict_edge": fields.TextField(analyzer=analyzers.strict_edge_ngram_analyzer),
            "medium_edge": fields.TextField(analyzer=analyzers.medium_edge_ngram_analyzer),
            "soft_edge": fields.TextField(analyzer=analyzers.soft_edge_ngram_analyzer),
            "very_soft_edge": fields.TextField(analyzer=analyzers.very_soft_edge_ngram_analyzer),
            "strict_ngram": fields.TextField(analyzer=analyzers.strict_ngram_analyzer),
            "medium_ngram": fields.TextField(analyzer=analyzers.medium_ngram_analyzer),
        }
    )
    # -------------------------------------------------------------------------------------------
    age_restrictions = fields.IntegerField(
        attr="age_restrictions"
    )
    allowed_countries = fields.ObjectField(
        attr="allowed_countries",
        properties={
            "country_code": fields.TextField(),
            "country_name": fields.TextField(),
        }
    )
    # -------------------------------------------------------------------------------------------
    category = fields.ObjectField(
        attr="category",
        properties={
            "id": fields.IntegerField(),
            "name_uz": fields.TextField(),
            "name_ru": fields.TextField(),
        }
    )
    country = fields.ObjectField(
        attr="country",
        properties={
            "id": fields.IntegerField(),
            "name_uz": fields.TextField(),
            "name_ru": fields.TextField(),
        },
        multi=True
    )
    genres = fields.ObjectField(
        attr="genres",
        properties={
            "id": fields.IntegerField(),
            "name_uz": fields.TextField(),
            "name_ru": fields.TextField(),
            "slug": fields.TextField(),
            "ordering": fields.IntegerField()
        },
        multi=True
    )
    year = fields.IntegerField(attr="year")
    sponsors = fields.ObjectField(
        attr="sponsors",
        properties={
            "id": fields.IntegerField(),
            "name": fields.TextField(),
        },
        multi=True
    )
    # -------------------------------------------------------------------------------------------
    
    def get_queryset(self):
        return super().get_queryset().filter(draft=False).select_related(
            "category"
        ).prefetch_related("country", "genres", "sponsors")
    
    class Index:
        name = "contents"

    class Django:
        model = models.Content
        fields = ["id", "is_russian", "rating", "rating_count", "date_created"]


@registry.register_document
class PersonDocument(Document):
    name_ru = fields.TextField(
        attr="name_ru",
        fields={ 
            "person_multiple_words_analyzer": fields.TextField(analyzer=analyzers.person_multiple_words_analyzer),
            "person_strict_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.strict_edge_ngram_analyzer),
            "person_medium_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.medium_edge_ngram_analyzer),
            "person_soft_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.person_soft_edge_ngram_analyzer),
            "person_very_soft_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.very_soft_edge_ngram_analyzer),
            
            "person_strict_ngram_analyzer": fields.TextField(analyzer=analyzers.strict_ngram_analyzer),
            "person_medium_ngram_analyzer": fields.TextField(analyzer=analyzers.medium_ngram_analyzer),
            "person_soft_ngram_analyzer": fields.TextField(analyzer=analyzers.person_soft_ngram_analyzer),
            "person_very_soft_ngram_analyzer": fields.TextField(analyzer=analyzers.person_very_soft_ngram_analyzer),
        }
    )
    name_uz = fields.TextField(
        attr="name_uz",
        fields={
            "person_multiple_words_analyzer": fields.TextField(analyzer=analyzers.person_multiple_words_analyzer),
            "person_strict_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.strict_edge_ngram_analyzer),
            "person_medium_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.medium_edge_ngram_analyzer),
            "person_soft_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.person_soft_edge_ngram_analyzer),
            "person_very_soft_edge_ngram_analyzer": fields.TextField(analyzer=analyzers.very_soft_edge_ngram_analyzer),
            
            "person_strict_ngram_analyzer": fields.TextField(analyzer=analyzers.strict_ngram_analyzer),
            "person_medium_ngram_analyzer": fields.TextField(analyzer=analyzers.medium_ngram_analyzer),
            "person_soft_ngram_analyzer": fields.TextField(analyzer=analyzers.person_soft_ngram_analyzer),
            "person_very_soft_ngram_analyzer": fields.TextField(analyzer=analyzers.person_very_soft_ngram_analyzer),
        }
    )
    
    class Index:
        name = "persons"

    class Django:
        model = models.Person
        fields = "id",
