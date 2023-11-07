from django.contrib import admin
from django.conf.urls.i18n import i18n_patterns
from django.urls import path, include


urlpatterns = [
    path("__debug__/", include("debug_toolbar.urls")),
]

urlpatterns += i18n_patterns(
    path('admin/', admin.site.urls),
    path("", include("content.urls", namespace="content")),
)
