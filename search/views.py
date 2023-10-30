from rest_framework.views import APIView
from rest_framework.response import Response

from elasticsearch_dsl import Q
from django_elasticsearch_dsl_drf.viewsets import DocumentViewSet
from django_elasticsearch_dsl_drf.pagination import PageNumberPagination

from search import models
from search import serializers
from search import documents


# 1.Сначала предлагать по началу строки, 
# 2.потом по середине и в конце строки, 
# 3.потом по описанию (description)
class ContentDocumentView(DocumentViewSet):
    document = documents.ContentDocument
    serializer_class = serializers.ContentDocumentSerializer
    pagination_class = PageNumberPagination

    def get_queryset(self):
        qs = super().get_queryset()
        search_query = self.request.query_params.get('search', None)
        
        if search_query:
            q = Q("match", title_ru={"query": search_query, "fuzziness": "auto"})#| #Q("match", description_ru={"query": search_query, "fuzziness": "1"})
            #qs = qs.query(q)
            qs = qs.query(q)
            # .filter(
            #     "script", 
            #     script="""
            #         def docval = doc['text.keyword'].value;
            #         def length = docval.length();
            #         def index = (float) docval.indexOf('title_ru');
            #         // the sooner the word appears the better so 'invert' the 'index'
            #         return index > -1 ? (1 / index) : 0;
            #     """
            # )
        return qs


