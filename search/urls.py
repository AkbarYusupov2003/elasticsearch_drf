from django.http import HttpResponse
from rest_framework import routers
from django.urls import path

from search import views


app_name = "search"

router = routers.SimpleRouter(trailing_slash=False)

router.register(r'content-search', views.ContentDocumentView, basename='content-search')

urlpatterns = router.urls


import json
from .models import Content

def view(request):
    with open('contents_data.json', encoding='utf-8') as data_file:
        json_data = json.loads(data_file.read())

    for movie_data in json_data:
        movie = Content.create(**movie_data)
        movie.save()
        
    return HttpResponse("ok")


urlpatterns+= [path("load-content-data/", view)]