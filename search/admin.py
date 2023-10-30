from django.contrib import admin

from search import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "title_ru", "description_ru")
