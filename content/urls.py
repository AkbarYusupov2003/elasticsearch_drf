from django.urls import path
from django.views.decorators.cache import cache_page

from content import views


app_name = "search"

urlpatterns = [
    path("<str:type_of_serializer>/content-search/", views.ContentMainSearchView.as_view()),
    path("content-filter/", views.ContentFilterView.as_view()),
    path("content-detail/<int:pk>/", views.ContentRetrieveView.as_view()),
    #
    path("available-countries/<int:pk>/", views.AvailableCountriesAPIView.as_view()),
    path("available-genres/<int:pk>/", views.AvailableGenresAPIView.as_view()),
    path("available-sponsors/<int:pk>/", views.AvailableSponsorsAPIView.as_view()),
    path("available-years/<int:pk>/", views.AvailableYearsAPIView.as_view()),
    #
    path("test/", views.TestCacheView.as_view()),
    # path("test/", cache_page(CACHE_TTL)(views.TestCacheView.as_view())),
    path("main/", views.MainAPIView.as_view()),
    path("categories/", views.CategoryListAPIView.as_view()),
    path("collections/", views.CollectionListAPIView.as_view()),
    path("collections/<int:pk>/", views.CollectionRetrieveAPIView.as_view()),
    path("genres/", views.GenreListAPIView.as_view()),
    path("genres/<int:pk>/", views.GenreRetrieveAPIView.as_view()),
]
