from django.contrib import admin

from content import models


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "title_ru", "description_ru", "draft")
    list_filter = ("draft",)


admin.site.register(models.Sponsor)
admin.site.register(models.ContentSponsor)
admin.site.register(models.ContentSubscription)
admin.site.register(models.ContentCollection)
admin.site.register(models.ContentCollectionContent)
admin.site.register(models.Category)
