from rest_framework import serializers

from content import utils
from content import models


class CategorySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField()
    
    class Meta:
        model = models.Category
        fields = ("id", "name",)
    
    def get_name(self, obj):
        return getattr(obj, f'name_{self.context["request"].LANGUAGE_CODE}', None)


class GenreSerializer(serializers.ModelSerializer):
    #name = serializers.SerializerMethodField(source="get_name")
    
    class Meta:
        model = models.Genre
        fields = ("id", "name_ru")

    def get_name(self, obj):
        return getattr(obj, f'name_{self.context["request"].LANGUAGE_CODE}', None)


class CountrySerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(source="get_name")
    
    class Meta:
        model = models.Country
        fields = ("id", "name")

    def get_name(self, obj):
        return getattr(obj, f'name_{self.context["request"].LANGUAGE_CODE}', None)
    
    
class SponsorsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.Sponsor
        fields = ("id", "name")
        

class AllowedCountrySerializer(serializers.ModelSerializer):
    
    class Meta:
        model = models.AllowedCountry
        fields = ("country_code", "country_name")
    
    
class ContentFilterSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    title = serializers.SerializerMethodField(source="get_title")
    genres = GenreSerializer(many=True)
    country = CountrySerializer(many=True)
    poster_h = utils.StdImageField()
    
    class Meta:
        model = models.Content
        fields = (
            "id",
            "title",
            "year",
            "age_restrictions",
            #"allowed_countries",
            "is_russian",
            "category",
            "genres",
            #"sponsors",
            "poster_h",
            "country",
            "rating",
            "rating_count",
            "date_created"
        )

    def get_title(self, obj):
        return getattr(obj, f'title_{self.context["request"].LANGUAGE_CODE}', None)   


class WebContentSearchSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    title = serializers.SerializerMethodField(source="get_title")
    genres = GenreSerializer(many=True)
    poster_h = utils.StdImageField()

    class Meta:
        model = models.Content
        fields = (
            "id",
            "title",
            "age_restrictions",
            "is_russian",
            "category",
            "genres",
            "poster_h",
        )

    def get_title(self, obj):
        return getattr(obj, f'title_{self.context["request"].LANGUAGE_CODE}', None)    
        # request = self.context.get("request")
        # if getattr(request, "LANGUAGE_CODE", "ru") == "uz":
        #     return obj.title_uz
        # else:
        #     return obj.title_ru


class MobileContentSearchSerializer(serializers.ModelSerializer):
    category = CategorySerializer()
    title = serializers.SerializerMethodField(source="get_title")

    class Meta:
        model = models.Content
        fields = (
            "id",
            "title",
            "is_russian",
            "category"
        )

    def get_title(self, obj):
        return getattr(obj, f'title_{self.context["request"].LANGUAGE_CODE}', None)   
    

# Collections
class CollectionSerializer(serializers.ModelSerializer):
    title = serializers.SerializerMethodField(source="get_title")
    picture = utils.StdImageField()

    class Meta:
        model = models.ContentCollection
        fields = ("id", "title", "picture", "is_kids")
    
    def get_title(self, obj):
        return getattr(obj, f'title_{self.context["request"].LANGUAGE_CODE}', None)


# Genres
class GenreListSerializer(serializers.ModelSerializer):
    name = serializers.SerializerMethodField(source="get_name")
    picture = utils.StdImageField()
    
    class Meta:
        model = models.Genre
        fields = ("id", "name", "picture")

    def get_name(self, obj):
        return getattr(obj, f'name_{self.context["request"].LANGUAGE_CODE}', None)
