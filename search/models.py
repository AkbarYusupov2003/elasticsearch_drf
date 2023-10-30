from django.db import models


gettext = lambda s: s
lang = (
    ('ru', gettext('Russian')),
    ('en', gettext('English')),
    ('uz', gettext('Uzbek')),
)


class Content(models.Model):
    for iso in lang:
        locals()[f'title_{iso[0]}'] = models.CharField(
            f"Название контента на [{iso[1]}]", max_length=200, null=True
        )
        locals()[f'description_{iso[0]}'] = models.TextField(
            f"Описание на [{iso[1]}]", blank=True, null=True
        )
    
    @classmethod
    def create(cls, **kwargs):
        content = cls.objects.create(
            id=kwargs['id'],
            title_ru=kwargs['title_ru'],
            title_en=kwargs['title_en'],
            title_uz=kwargs['title_uz'],
            description_ru=kwargs['description_ru'],
            description_en=kwargs['description_en'],
            description_uz=kwargs['description_uz'],
        )
        return content
