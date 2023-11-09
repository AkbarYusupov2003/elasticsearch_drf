import operator
from functools import reduce
from django.db.models import Case, IntegerField, Value, When
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import filters
from rest_framework.views import APIView
from rest_framework.generics import GenericAPIView, ListAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework.pagination import LimitOffsetPagination
from elasticsearch_dsl import Q

from content import utils
from content import models
from content import serializers
from content import documents
from content import mixins


lang = {
    "ru": "Русский",
    "en": "Английский",
    "uz": "Узбекский",
}

class ContentRetrieveView(mixins.CacheViewMixin, RetrieveAPIView):
    serializer_class = serializers.WebContentSearchSerializer
    
    def get_queryset(self):
        age_restrictions = 18
        country_code = "UZ"
        return models.Content.objects.filter(
            age_restrictions__lte=age_restrictions, allowed_countries__in=(country_code,), draft=False
        )


class ContentFilterView(mixins.CacheViewMixin, GenericAPIView):
    document = documents.ContentDocument
    serializer_class = serializers.ContentFilterSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        lang = self.request.LANGUAGE_CODE

        age_restrictions = 18
        country_code = "UZ"

        document = self.document.search().filter("match", allowed_countries__country_code=country_code)
        document = document.filter({"range": {"age_restrictions": {"lte": age_restrictions}}}).extra(size=100)

        category = self.request.GET.get("category")
        search = self.request.GET.get("search")
        content_lang = self.request.GET.get("content_lang")
        country = self.request.GET.get("country")
        genres = self.request.GET.get("genres")
        year = self.request.GET.get("year")
        sponsors = self.request.GET.get("sponsors")
        ordering = self.request.GET.get("ordering")

        execute_query = []

        if category:
            execute_query.append(
                Q({"match": {"category.id": {"query": category}}})
            )

        if content_lang == "uzb": 
            execute_query.append(
                Q("match", is_russian=False)
            )
        elif content_lang == "rus":
            execute_query.append(
                Q("match", is_russian=True)
            )

        if country:
            for i in country.rstrip(",").split(","):
                execute_query.append(
                    Q({"match": {"country.id": i}})
                )
        
        if genres:
            for i in genres.rstrip(",").split(","):
                execute_query.append(
                    Q({"match": {"genres.id": i}})
                )
        
        if sponsors:
            for i in sponsors.rstrip(",").split(","):
                execute_query.append(
                    Q({"match": {"sponsors.id": i}})
                )
        
        if year:
            for i in year.rstrip(",").split(","):
                execute_query.append(
                    Q({"match": {"year": i}})
                )
        
        if execute_query:
            document = document.query(
                reduce(operator.iand, execute_query)
            )
            
        if search:
            document = document.query(Q({
                "match": {f"title_{lang}": {"query": search, }}
            }))
            
        if ordering:
            # asc desc
            if ordering == "rating":
                document = document.sort({"rating": "desc"})
            elif ordering == "date_created":
                document = document.sort({"date_created": "desc"})
        
        result = [x.id for x in document]
        
        return models.Content.objects.filter(pk__in=result).order_by(
            Case(
                *[When(pk=pk, then=Value(i)) for i, pk in enumerate(result)],
                output_field=IntegerField()
            ).asc()
        ).select_related("category").prefetch_related("genres", "country")
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            results = self.paginate_queryset(queryset)
            res = self.get_serializer(results, many=True)
            return self.get_paginated_response(res.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class ContentMainSearchView(mixins.CacheViewMixin, GenericAPIView):
    document =  documents.ContentDocument
    serializer_class = serializers.WebContentSearchSerializer
    pagination_class = LimitOffsetPagination

    def get_serializer_class(self):
        type_of_serializer = self.kwargs.get("type_of_serializer", None)
        
        if type_of_serializer == "mobile":
            return serializers.MobileContentSearchSerializer
        else:
            return self.serializer_class
    
    def get_serializer(self, *args, **kwargs):
        serializer_class = self.get_serializer_class()
        kwargs["context"] = self.get_serializer_context()
        return serializer_class(*args, **kwargs) 
    
    def get_queryset(self):
        search_query = self.request.query_params.get('search', None)

        if not search_query:
            return []
        
        lang = self.request.LANGUAGE_CODE
        
        age_restrictions = 18 # self.request.auth.payload.get("age", 18)
        country_code = "UZ" # self.request.auth.payload.get("c_code", "ALL")

        document = self.document.search().filter("match", allowed_countries__country_code=country_code)
        document = document.filter({"range": {"age_restrictions": {"lte": age_restrictions}}}).extra(size=100)
                    
        search_again = True
        while search_again:
            result = []
            
            if len(list(search_query.split())) > 1:
                response = document.query(Q({
                    "match": {f"title_{lang}.multiple_words_ngram": {"query": search_query, "fuzziness": "0"}}
                }))
                result = [x.id for x in response]
                response = document.query(Q({
                    "match": {f"title_{lang}.multiple_words_ngram": {"query": search_query.replace(" ", "-"), "fuzziness": "0"}}
                }))
                for x in response:
                    result.append(x.id)
                
            response = document.query(Q({
                "match": {f"title_{lang}.strict_edge": {"query": search_query, "fuzziness": "0"}}
            }))
            
            for x in response:
                result.append(x.id)
            
            counter = response.count()
            
            if counter < 100:
                helper_response = document.query(Q({
                    "match": {f"title_{lang}.medium_edge": {"query": search_query, "fuzziness": "0"}}
                }))
                for x in helper_response:
                    result.append(x.id)
                counter = len(result)
                
                if counter < 100:
                    helper_response = document.query(Q({
                        "match": {f"title_{lang}.strict_ngram": {"query": search_query, "fuzziness": "0"}}
                    }))
                    for x in helper_response:
                        result.append(x.id)
                    counter = len(result)
                    
                    if counter < 100 and counter != 0:
                        helper_response = document.query(Q({
                            "match": {f"title_{lang}.medium_ngram": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)
                    
                    if counter == 0:
                        helper_response = document.query(Q({
                            "match": {f"title_{lang}.soft_edge": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)
                    
                    if counter == 0:
                        helper_response = document.query(Q({
                            "match": {f"title_{lang}.soft_edge": {"query": search_query, "fuzziness": "1"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)
                        
                    if counter == 0:
                        helper_response = document.query(Q({
                            "match": {f"title_{lang}.very_soft_edge": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)

                    if counter == 0:
                        translated = utils.translate(search_query.lower())
                        if search_query.lower() == translated:
                            search_again = False
                        else:
                            search_query = translated
                            search_again = True
                    else:
                        search_again = False

            if not search_again:
                return models.Content.objects.filter(pk__in=result).order_by(
                    Case(
                        *[When(pk=pk, then=Value(i)) for i, pk in enumerate(result)],
                        output_field=IntegerField()
                    ).asc()
                ).select_related("category").prefetch_related("genres")

    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            results = self.paginate_queryset(queryset)
            res = self.get_serializer(results, many=True)
            return self.get_paginated_response(res.data)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class AvailableCountriesAPIView(mixins.CacheViewMixin, GenericAPIView):
    serializer_class = serializers.CountrySerializer
    
    def get_queryset(self):
        age_restrictions = 18
        country_code = "UZ"
        
        category = get_object_or_404(models.Category, pk=self.kwargs["pk"])
        content_ids = models.Content.objects.filter(
            age_restrictions__lte=age_restrictions, category=category, allowed_countries__in=(country_code,), draft=False,
        ).values_list("pk", flat=True)
        countries_ids = models.ContentCountry.objects.filter(content__id__in=content_ids).values_list("country__id", flat=True)
        
        countries = models.Country.objects.filter(pk__in=countries_ids)
        return countries

    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            res = self.get_serializer(queryset, many=True)
            return Response(res.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class AvailableGenresAPIView(mixins.CacheViewMixin, GenericAPIView):
    serializer_class = serializers.GenreSerializer
    
    def get_queryset(self):
        age_restrictions = 18
        country_code = "UZ"
        
        category = get_object_or_404(models.Category, pk=self.kwargs["pk"])
        content_ids = models.Content.objects.filter(
            age_restrictions__lte=age_restrictions, category=category, allowed_countries__in=(country_code,), draft=False,
        ).values_list("pk", flat=True)
        genres_ids = models.ContentGenre.objects.filter(content__id__in=content_ids).values_list("genre__id", flat=True)
        
        genres = models.Genre.objects.filter(pk__in=genres_ids)
        return genres
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            res = self.get_serializer(queryset, many=True)
            return Response(res.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class AvailableSponsorsAPIView(mixins.CacheViewMixin, GenericAPIView):
    serializer_class = serializers.SponsorsSerializer
    
    def get_queryset(self):        
        age_restrictions = 18
        country_code = "UZ"
        
        category = get_object_or_404(models.Category, pk=self.kwargs["pk"])
        
        content_ids = models.Content.objects.filter(
            age_restrictions__lte=age_restrictions, category=category, allowed_countries__in=(country_code,), draft=False,
        ).values_list("pk", flat=True)
        sponsors_ids = models.ContentSponsor.objects.filter(content__id__in=content_ids).values_list("sponsor_id", flat=True)
        
        genres = models.Sponsor.objects.filter(pk__in=sponsors_ids)
        return genres
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            res = self.get_serializer(queryset, many=True)
            return Response(res.data, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
    

class AvailableYearsAPIView(mixins.CacheViewMixin, ListAPIView):
    
    def get_queryset(self):
        age_restrictions = 18
        country_code = "UZ"
        
        category = get_object_or_404(models.Category, pk=self.kwargs["pk"])
        
        years = models.Content.objects.filter(
            age_restrictions__lte=age_restrictions, category=category, allowed_countries__in=(country_code,), draft=False,
        ).distinct("year").values_list("year", flat=True)
        
        return years
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            queryset = self.get_queryset()
            return Response({"years": queryset})
                        
        return Response(status=status.HTTP_400_BAD_REQUEST)


class MainAPIView(mixins.CacheViewMixin, APIView):
    serializer_class = serializers.CategorySerializer
    
    def get(self, request, *args, **kwargs):
        if request.LANGUAGE_CODE == "uz" or request.LANGUAGE_CODE == "ru":
            try:
                limit = int(request.GET.get("limit", 15))
                offset = int(request.GET.get("offset", 0))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            age_restrictions = 18
            country_code = "UZ"
            
            categories = models.Category.objects.all()
            res = []
            for category in categories:
                
                cat = self.serializer_class(category, context={"request": request}).data
                
                qs = models.Content.objects.filter(
                    age_restrictions__lte=age_restrictions, category=category, allowed_countries__in=(country_code,), draft=False,
                ).select_related("category").prefetch_related("genres", "country", "allowed_countries")
                
                cat["results"] = serializers.WebContentSearchSerializer(
                    qs[offset:limit+offset],
                    context={"request": request},
                    many=True
                ).data

                res.append(cat)
            
            return Response(res, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class CategoryListAPIView(mixins.CacheViewMixin, ListAPIView):
    serializer_class = serializers.CategorySerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        categories = models.Category.objects.all()
        return categories


class CollectionListAPIView(mixins.CacheViewMixin, ListAPIView):
    serializer_class = serializers.CollectionSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        is_kids = self.request.GET.get("is_kids", "False")
        return models.ContentCollection.objects.filter(is_kids=True if is_kids == "True" else False)


class CollectionRetrieveAPIView(mixins.CacheViewMixin, APIView):
    serializer_class = serializers.CollectionSerializer
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            try:
                limit = int(request.GET.get("limit", 30))
                offset = int(request.GET.get("offset", 0))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            age_restrictions = 18
            country_code = "UZ"
            
            collection = get_object_or_404(models.ContentCollection, pk=self.kwargs["pk"]) 
            
            res = {
                "collection": self.serializer_class(collection, context={"request": request}).data
            }
            
            ids = collection.content_collection.all().values_list("content__pk", flat=True)
            contents = models.Content.objects.filter(
                pk__in=ids, 
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False,
            ).select_related("category").prefetch_related("genres", "country", "allowed_countries")

            res["count"] = contents.count()
            res["results"] = serializers.WebContentSearchSerializer(contents[offset:limit+offset], context={"request": request}, many=True).data
            return Response(res, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class GenreListAPIView(mixins.CacheViewMixin, ListAPIView):
    serializer_class = serializers.GenreListSerializer
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        return models.Genre.objects.all()


class GenreRetrieveAPIView(mixins.CacheViewMixin, APIView):
    serializer_class = serializers.GenreSerializer
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            try:
                limit = int(request.GET.get("limit", 30))
                offset = int(request.GET.get("offset", 0))
            except:
                return Response(status=status.HTTP_400_BAD_REQUEST)
            
            age_restrictions = 18
            country_code = "UZ"
            
            genre = get_object_or_404(models.Genre, pk=self.kwargs["pk"]) 
            
            res = {
                "genre": self.serializer_class(genre, context={"request": request}).data
            }
            
            contents = genre.genres.all().filter( 
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False,
            ).select_related("category").prefetch_related("genres", "country", "allowed_countries")

            res["count"] = contents.count()
            res["results"] = serializers.WebContentSearchSerializer(contents[offset:limit+offset], context={"request": request}, many=True).data
            
            return Response(res, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PersonListAPIView(ListAPIView):
    serializer_class = serializers.PersonSerializer
    #filter_backends = filters.SearchFilter,
    queryset = models.Person.objects.all()
    search_fields = [f"name_{l}" for l in lang]
    pagination_class = LimitOffsetPagination
    
    def get_queryset(self):
        search_query = self.request.GET.get('search', None)
        
        if not search_query:
            return []
        
        search_again = True
        while search_again:
            result = []
            lang = self.request.LANGUAGE_CODE
            document = documents.PersonDocument.search().extra(size=100)
            
            response = document.query(Q({
                "match": {f"name_{lang}.person_multiple_words_analyzer": {"query": search_query, "fuzziness": "1"}}
            }))
            result = [x.id for x in response]
                    
            response = document.query(Q({
                "match": {f"name_{lang}.person_strict_edge_ngram_analyzer": {"query": search_query, "fuzziness": "0"}} # 1?
            }))
            for x in response:
                result.append(x.id)
            
            counter = response.count()
            
            if counter < 100:
                helper_response = document.query(Q({
                    "match": {f"name_{lang}.person_medium_edge_ngram_analyzer": {"query": search_query, "fuzziness": "0"}}
                }))
                for x in helper_response:
                    result.append(x.id)
                counter = len(result)
                
                if counter < 100:
                    helper_response = document.query(Q({
                        "match": {f"name_{lang}.person_strict_ngram_analyzer": {"query": search_query, "fuzziness": "0"}}
                    }))
                    for x in helper_response:
                        result.append(x.id)
                    counter = len(result)

                    if counter == 0:
                        helper_response = document.query(Q({
                            "match": {f"name_{lang}.person_soft_edge_ngram_analyzer": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)

                    if counter < 10:
                        helper_response = document.query(Q({
                            "match": {f"name_{lang}.person_soft_ngram_analyzer": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)

                    if counter == 0:
                        helper_response = document.query(Q({
                            "match": {f"name_{lang}.person_very_soft_edge_ngram_analyzer": {"query": search_query, "fuzziness": "0"}}
                        }))
                        for x in helper_response:
                            result.append(x.id)
                        counter = len(result)

            if counter == 0:
                translated = utils.translate(search_query.lower())
                if search_query.lower() == translated:
                    search_again = False
                else:
                    search_query = translated
                    search_again = True
            else:
                search_again = False
                        
        if not search_again:
            return models.Person.objects.filter(pk__in=result).order_by(
                Case(
                    *[When(pk=pk, then=Value(i)) for i, pk in enumerate(result)],
                    output_field=IntegerField()
                ).asc()
            )

    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            return super().get(request, args, kwargs)

        return Response(status=status.HTTP_400_BAD_REQUEST)


class PersonRetrieveAPIView(mixins.CacheViewMixin, APIView):
    serializer_class = serializers.PersonSerializer
    
    def get(self, request, *args, **kwargs):
        if self.request.LANGUAGE_CODE == "uz" or self.request.LANGUAGE_CODE == "ru":
            age_restrictions = 18
            country_code = "UZ"
            
            person = get_object_or_404(models.Person, pk=self.kwargs["pk"])
            res = {
                "person": self.serializer_class(person, context={"request": request}).data
            }
            
            actor = person.actors.all().filter(
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False
            )
            scenario = person.scenario.all().filter(
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False
            )
            producer = person.producer.all().filter(
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False
            )
            director = person.director.all().filter(
                age_restrictions__lte=age_restrictions,
                allowed_countries__in=(country_code,),
                draft=False
            )
            
            res["actor"] = serializers.PersonContentSerializer(actor, context={"request": request}, many=True).data
            res["scenario"] = serializers.PersonContentSerializer(scenario, context={"request": request}, many=True).data
            res["producer"] = serializers.PersonContentSerializer(producer, context={"request": request}, many=True).data
            res["director"] = serializers.PersonContentSerializer(director, context={"request": request}, many=True).data

            return Response(res, status=status.HTTP_200_OK)

        return Response(status=status.HTTP_400_BAD_REQUEST)
