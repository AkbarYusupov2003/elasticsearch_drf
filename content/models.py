import django.core.files.storage
import os
from datetime import time
from pathlib import Path
from django.core.validators import FileExtensionValidator
from django.db import models
from django.conf import settings
from django.core.exceptions import ValidationError
from content.etc.validators import validate_image_extension
from pytils.translit import slugify
# from apps.utils.storage import OverwriteStorage
from content.etc.utils import rmdir, erase_content

from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFit, ResizeToFill, Transpose
from django.core.files.images import get_image_dimensions
from content.etc.filename_path import *
from content.etc.country_choices import COUNTRY_CHOICES
from stdimage import StdImageField
from colorfield.fields import ColorField


lang = {
    "ru": "Русский",
    "en": "Английский",
    "uz": "Узбекский",
}

video_quality = settings.VIDEO_QUALITY

AGE_RESTRICTIONS = [
    (0, '0+'),
    (6, '6+'),
    (12, '12+'),
    (16, '16+'),
    (18, '18+'),
]


class AllowedCountry(models.Model):
    country_code = models.CharField(max_length=3, choices=COUNTRY_CHOICES, primary_key=True, )
    country_name = models.CharField(max_length=64, )

    def __str__(self):
        return self.country_name

    class Meta:
        verbose_name = 'Страна для разрешения'
        verbose_name_plural = 'Страны для разрешения'
    



class ContentSubscription(models.Model):
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f'Название на [{lang[iso]}]', max_length=60)
        locals()[f'description_{iso}'] = models.CharField(f'Описание на [{lang[iso]}]', max_length=500)
        locals()[f'description_list_{iso}'] = models.TextField(f'Описание на [{lang[iso]}]', max_length=1500,
                                                               null=True, blank=True)
    limit_sessions = models.PositiveSmallIntegerField('Лимит сессий', default=3)
    price = models.PositiveIntegerField('Цена подписки в месяц в тийинах', )
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)
    # color = ColorField('Цвет', blank=True, null=True)
    # color1 = ColorField('Градиент 1')
    # color2 = ColorField('Градиент 2')
    # color3 = ColorField('Градиент 3')
    icon = models.ImageField("Icon", blank=True, null=True)
    archive = models.BooleanField(default=False)

    def __str__(self):
        return self.title_ru

    class Meta:
        db_table = 'users_subscription'
        ordering = 'ordering',
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'


class CrowdVideo(models.Model):
    slug = models.CharField('Название', unique=True, editable=False, max_length=255)
    duration = models.PositiveIntegerField("Длительность", default=0)
    is_mark_for_deletion = models.BooleanField(default=False)

    for size in video_quality:
        locals()[f'codec_{size}'] = models.CharField(f'Кодек {size}', max_length=60, null=True, blank=True)

    def __str__(self):
        return self.slug

    def delete(self, using=None, keep_parents=False):
        try:
            audio = CrowdAudio.objects.get(slug=self.slug)
            audio.delete()
            super().delete()
        except CrowdAudio.DoesNotExist:
            super().delete()

    class Meta:
        ordering = "slug",
        verbose_name = "Все Видео"
        verbose_name_plural = "Все Видео"


class CrowdAudio(models.Model):
    slug = models.SlugField('Название', unique=True, editable=False, max_length=550)

    def __str__(self):
        return self.slug

    class Meta:
        ordering = "slug",
        verbose_name = 'Все Аудио'
        verbose_name_plural = 'Все Аудио'


class Genre(models.Model):
    for iso in lang:
        locals()[f'name_{iso}'] = models.CharField(f'Название на [{lang[iso]}]', max_length=70)
    slug = models.SlugField('SLUG', unique=True, max_length=100, blank=True, )
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)
    picture = StdImageField(
        'Картинка',
        max_length=250,
        upload_to='genre_pictures/',
        help_text="Рекомендуемый размер 1x1",
        variations={
            'large': (1080, 1080),
            'medium': (768, 768),
            'small': (200, 200),
            'thumb': (75, 75)
        },
        null=True,
    )

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_ru)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_ru

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Жанр'
        verbose_name_plural = 'Жанры'


class Sponsor(models.Model):
    name = models.CharField('Название', max_length=200)
    slug = models.SlugField('SLUG', unique=True, max_length=255, blank=True, )
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name)
        super().save(*args, **kwargs)

    # def clean(self):
    #     if self.logo:
    #         if ".png" not in self.logo.path:
    #             raise ValidationError("Доступное расширение logo  .png")
    #         else:
    #             w, h = get_image_dimensions(self.logo)
    #             if w != 50:
    #                 raise ValidationError("Ширина icon не равна 50px")
    #             if h != 30:
    #                 raise ValidationError("Высота icon не равна 30px")

    def __str__(self):
        return self.name

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Спонсор'
        verbose_name_plural = 'Спонсоры'


class Country(models.Model):
    for iso in lang:
        locals()[f'name_{iso}'] = models.CharField(f'Имя на [{lang[iso]}]', max_length=100)
    slug = models.SlugField('SLUG', unique=True, max_length=100, blank=True, )
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_ru)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_ru

    class Meta:
        ordering = ['ordering']
        verbose_name = "Страна"
        verbose_name_plural = "Страны"


class Category(models.Model):
    for iso in lang:
        locals()[f'name_{iso}'] = models.CharField(f'Название на [{lang[iso]}]', max_length=70)
    slug = models.SlugField('SLUG', unique=True, max_length=100, blank=True, )
    icon = models.ImageField('Картинка icon', storage=django.core.files.storage.FileSystemStorage(), null=True,
                             help_text="Поддерживается размер icon 90x90 px")
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", related_name='cat_genres', blank=True)
    sponsors = models.ManyToManyField(Sponsor, verbose_name="Спонсоры", related_name='cat_sponsors', blank=True)
    countries = models.ManyToManyField(Country, verbose_name="Страны", related_name='cat_countries', blank=True)
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)

    def clean(self):
        if not self.icon:
            raise ValidationError("Нет Картинки icon")
        # if ".png" not in self.icon.path:
        #     raise ValidationError("Доступное расширение картинки icon .png")
        elif not self.icon.closed:
            w, h = get_image_dimensions(self.icon)
            if w != 90:
                raise ValidationError("Ширина icon не равна 90px")
            if h != 90:
                raise ValidationError("Высота icon не равна 90px")

    def __str__(self):
        return self.name_ru

    class Meta:
        ordering = ['ordering']
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'


class Person(models.Model):
    for iso in lang:
        locals()[f'name_{iso}'] = models.CharField(f'Имя на [{lang[iso]}]', max_length=100)
    slug = models.SlugField('SLUG', unique=True, max_length=100, blank=True, )
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10)
    profile_pic = StdImageField('Фото', storage=django.core.files.storage.FileSystemStorage(),
                                help_text="Соотношение сторон фото 1х1", blank=True, null=True,
                                variations={
                                    'resized': (600, 600), 
                                    'large': (1080, 1080),
                                    'medium': (768, 768),
                                    'small': (200, 200),
                                    'thumb': (75, 75),
                                    })
    is_actor = models.BooleanField("Актер?", default=True)
    is_scenario = models.BooleanField("Сценарист?", default=True)
    is_producer = models.BooleanField("Продюсер?", default=True)
    is_director = models.BooleanField("Режиссер?", default=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.name_ru)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name_uz

    class Meta:
        ordering = ['ordering']
        verbose_name = "Участник"
        verbose_name_plural = "Участники"


class Content(models.Model):
    IS_SERIAL_CHOICES = [
        (True, 'Да, это Сериал'),
        (False, 'Нет, это Фильм'),
    ]
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f"Название контента на [{lang[iso]}]",
                                                    max_length=200, null=True)
        locals()[f'slogan_{iso}'] = models.CharField(f"Слоган на [{lang[iso]}]",
                                                     max_length=200, blank=True, null=True)
        locals()[f'description_{iso}'] = models.TextField(f"Описание на [{lang[iso]}]",
                                                          blank=True, null=True)
        locals()[f'is_{iso}'] = models.BooleanField(f"доступен на языке [{lang[iso]}]", default=False)
        
    slug = models.SlugField(max_length=200, unique=True, blank=True)
    year = models.PositiveSmallIntegerField("Дата выхода", default=2022)
    age_restrictions = models.PositiveSmallIntegerField("Возрастные ограничения",
                                                        default='0+', choices=AGE_RESTRICTIONS, )
    date_created = models.DateTimeField('Дата создания', auto_now_add=True)

    sponsors = models.ManyToManyField(Sponsor, verbose_name="Спонсоры", related_name='sponsors', through="ContentSponsor", blank=True)
    country = models.ManyToManyField(Country, verbose_name="Страна", related_name='country', through="ContentCountry", blank=True)
    actors = models.ManyToManyField(Person, verbose_name="В ролях", related_name='actors', through="ContentActor", blank=True)
    scenario = models.ManyToManyField(Person, verbose_name="Сценарист", related_name='scenario', through="ContentScenario", blank=True)
    producer = models.ManyToManyField(Person, verbose_name="Продюсер", related_name='producer', through="ContentProducer", blank=True)
    director = models.ManyToManyField(Person, verbose_name="Режиссер", related_name='director', through="ContentDirector", blank=True)
    genres = models.ManyToManyField(Genre, verbose_name="Жанры", related_name='genres', through="ContentGenre", blank=True)
    category = models.ForeignKey(Category, related_name='contents', on_delete=models.SET_NULL, null=True, )

    logo_image_square = StdImageField('Лого медиа квадрат',
                                      max_length=200,
                                      default="static/placeholders/logo_image_square.png",
                                      storage=django.core.files.storage.FileSystemStorage(),
                                      help_text="Рекомендуемое соотношение сторон 1x1"
                                                "<br>Минимальный размер 600px",
                                      variations={'resized': (600, 600), }
                                      )
    logo_image_rectangle = StdImageField('Лого медиа прямоуг',
                                         max_length=200,
                                         default="static/placeholders/logo_image_rectangle.png",
                                         storage=django.core.files.storage.FileSystemStorage(),
                                         help_text="Рекомендуемое соотношение сторон 16х9"
                                                   "<br>Минимальный размер 600px",
                                         variations={'resized': (600, -1), }
                                         )
    poster_v = StdImageField('Постер вертикальный',
                             max_length=200,
                             default="static/placeholders/poster_v.jpg",
                             storage=django.core.files.storage.FileSystemStorage(),
                             help_text="Рекомендуемое соотношение сторон 4x7"
                                       "<br>Минимальный размер 240,360px",
                             variations={'resized': (240, 360), }
                             )
    poster_h = StdImageField('Постер горизонтальный',
                             max_length=200,
                             default="static/placeholders/poster_h.jpg",
                             storage=django.core.files.storage.FileSystemStorage(),
                             help_text="Рекомендуемое соотношение сторон 16х9"
                                       "<br>Минимальный размер 336x189px",
                             variations={'resized': (336, 189), 'promo': (600, 300), }
                             )
    bg_image = StdImageField('Фоновая картинка',
                             max_length=200,
                             default="static/placeholders/bg_image.jpg",
                             storage=django.core.files.storage.FileSystemStorage(),
                             help_text="Рекомендуемое соотношение сторон 16х9"
                                       "<br>Минимальный размер 1920px",
                             variations={'resized': (600, 600), }
                             )

    rating = models.FloatField("Рэйтинг", default=10)
    rating_count = models.PositiveIntegerField("Количество оценок", null=True, blank=True, default=0)

    is_new = models.BooleanField("Премьера", default=False)
    is_soon = models.BooleanField("Скоро...", default=False)
    is_free = models.BooleanField("Бесплатно", default=False)
    is_russian = models.BooleanField("Русский контент", default=False)
    is_4k = models.BooleanField(default=False)
    is_full_hd = models.BooleanField(default=False)
    duration = models.PositiveSmallIntegerField("Длительность", null=True, blank=True)

    draft = models.BooleanField("Черновик", default=True)

    is_serial = models.BooleanField("Это сериал? ", choices=IS_SERIAL_CHOICES, )
    allowed_countries = models.ManyToManyField(AllowedCountry, verbose_name='Разрешенные страны', blank=True)
    allowed_subscriptions = models.ManyToManyField(ContentSubscription, verbose_name='Разрешенные подписки', blank=False)
    # ordering = models.PositiveIntegerField("Позиция в списке", default=100)

    def __str__(self):
        for iso in lang:
            if getattr(self, f"title_{iso}", None):
                return f'{self.id} - {getattr(self, f"title_{iso}", None)}'
        return self.id

    class Meta:
        #ordering = ['-id']
        verbose_name = "Контент"
        verbose_name_plural = "!Контент 0 Full"
    
    
    

class ContentInfoFilm(Content):
    class Meta:
        proxy = True
        verbose_name = '!Контент фильм'
        verbose_name_plural = '!Контент 1 Film Trailer'


class ContentSponsor(models.Model):
    content = models.ForeignKey(Content, related_name='content_sponsors', on_delete=models.CASCADE)
    sponsor = models.ForeignKey(Sponsor, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_sponsors"
        unique_together = ['content', 'sponsor']


class ContentGenre(models.Model):
    content = models.ForeignKey(Content, related_name='content_genres', on_delete=models.CASCADE)
    genre = models.ForeignKey(Genre, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_genres"
        unique_together = ['content', 'genre']


class ContentCountry(models.Model):
    content = models.ForeignKey(Content, related_name='content_countries', on_delete=models.CASCADE)
    country = models.ForeignKey(Country, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_country"
        unique_together = ['content', 'country']


class ContentActor(models.Model):
    content = models.ForeignKey(Content, related_name='content_actors', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_actors"
        unique_together = ['content', 'person']


class ContentDirector(models.Model):
    content = models.ForeignKey(Content, related_name='content_directors', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_director"
        unique_together = ['content', 'person']


class ContentProducer(models.Model):
    content = models.ForeignKey(Content, related_name='content_producers', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_producer"
        unique_together = ['content', 'person']


class ContentScenario(models.Model):
    content = models.ForeignKey(Content, related_name='content_scenarios', on_delete=models.CASCADE)
    person = models.ForeignKey(Person, on_delete=models.CASCADE)
    ordering = models.PositiveSmallIntegerField(default=10)

    class Meta:
        ordering = 'ordering',
        db_table = "content_content_scenario"
        unique_together = ['content', 'person']


class Season(models.Model):
    serial = models.ForeignKey(Content, related_name='seasons', on_delete=models.CASCADE)
    season_numb = models.PositiveSmallIntegerField("Номер сезона", )

    def validate_unique(self, exclude=None):
        qs = self.serial.seasons.all()
        if self.pk is None:
            if qs.filter(season_numb=self.season_numb).exists():
                raise ValidationError("Номер сезона должен быть уникальным")
        if self.pk:
            obj = Season.objects.get(id=self.pk)
            if obj.season_numb != self.season_numb:
                raise ValidationError(
                    f"Номер сезона не может быть изменен. Номер сезона был равен = <{obj.season_numb}>")

    def __str__(self):
        return f"{self.season_numb}"

    class Meta:
        ordering = 'season_numb',
        verbose_name = "Сезон"
        verbose_name_plural = "Сезоны --> Эпизоды"


class ContentRelated(models.Model):
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f"Название связанного контента на [{lang[iso]}]", max_length=200)

    def __str__(self):
        return self.title_ru

    class Meta:
        verbose_name = 'Связанный Контент'
        verbose_name_plural = 'Связанные Контенты'


class ContentRelatedContent(models.Model):
    content = models.OneToOneField(Content, on_delete=models.CASCADE,
                                   help_text="Контент должен быть уникальным", related_name='related')
    content_related_content = models.ForeignKey(ContentRelated, related_name='content_related',
                                                on_delete=models.SET_NULL, null=True)
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10, blank=True, null=True)

    def __str__(self):
        return self.content.title_ru

    class Meta:
        ordering = 'ordering',
        unique_together = ('content', 'content_related_content')
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"


class ContentCollection(models.Model):
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f"Название коллекции на [{lang[iso]}]", max_length=200)

    is_recommended = models.BooleanField("Рекомендация", default=False)
    is_kids = models.BooleanField("Детская коллекция", default=False)
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10, blank=True, null=True)
    picture = StdImageField(
        'Картинка',
        max_length=250,
        upload_to='collection_pictures/',
        help_text="Рекомендуемый размер 1x1",
        variations={
            'large': (1080, 1080),
            'medium': (768, 768),
            'small': (200, 200),
            'thumb': (75, 75)
        },
        null=True,
    )

    # def clean(self):
    #     if not self.is_recommended:
    #         return
    #     else:
    #         try:
    #             if ContentCollection.objects.get(is_recommended=True) == self:
    #                 return
    #             else:
    #                 raise ValidationError("Активная рекомендация может быть только одна")
    #         except ContentCollection.DoesNotExist:
    #             return

    def __str__(self):
        return self.title_ru

    class Meta:
        ordering = 'ordering',
        verbose_name = 'Коллекция'
        verbose_name_plural = 'Коллекции'


class ContentCollectionContent(models.Model):
    content = models.ForeignKey(Content, on_delete=models.CASCADE, related_name='collection')
    collection_content = models.ForeignKey(ContentCollection, related_name='content_collection',
                                           on_delete=models.SET_NULL, null=True)
    ordering = models.PositiveSmallIntegerField("Позиция в списке", default=10, blank=True, null=True)

    def __str__(self):
        return f"{self.ordering} - {self.content.title_ru}"

    class Meta:
        ordering = 'ordering',
        verbose_name = "Контент"
        verbose_name_plural = "Контенты"


def hls_subs(subs_file_name, output_file_path, runtime):
    m3u8_subs_content = f'#EXTM3U\n#EXT-X-TARGETDURATION:{runtime}\n#EXT-X-VERSION:3\n#EXT-X-MEDIA-SEQUENCE:1\n#EXT-X-PLAYLIST-TYPE:VOD\n#EXTINF:{runtime},\n{subs_file_name}\n#EXT-X-ENDLIST'
    name = os.path.basename(output_file_path)
    base = output_file_path[:-len(name)]
    os.path.join(base, name)
    with open(output_file_path, 'w+') as file:
        file.write(m3u8_subs_content)


class Episode(models.Model):
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f"Название эпизода на [{lang[iso]}]",
                                                    max_length=200, blank=True, null=True)
        locals()[f'description_{iso}'] = models.TextField(f"Описание на [{lang[iso]}]",
                                                          blank=True, null=True)
        locals()[f'audio_{iso}'] = models.OneToOneField(CrowdAudio, related_name=f'episode_audio_{iso}',
                                                        verbose_name=f"Аудиодорожка на [{lang[iso]}]",
                                                        on_delete=models.SET_NULL, null=True, blank=True)
        locals()[f'sub_{iso}'] = models.FileField(f"Субтитры на [{lang[iso]}]",
                                                  upload_to=content_subs_filename,
                                                  # storage=OverwriteStorage(),
                                                  blank=True, null=True,
                                                  validators=[FileExtensionValidator(allowed_extensions=['vtt'])])
        locals()[f'is_sub_{iso}'] = models.BooleanField('Добавлено', default=False, editable=False)

    picture = StdImageField("Картинка",
                            max_length=200,
                            upload_to=episode_picture_filename,
                            storage=django.core.files.storage.FileSystemStorage(),
                            help_text="Рекомендуемое соотношение сторон 16х9",
                            blank=True, null=True,
                            variations={'resized': (320, -1), }
                            )

    duration = models.PositiveSmallIntegerField("Длительность", default=0)
    #
    seasons = models.ForeignKey(Season, related_name='episodes', on_delete=models.SET_NULL, null=True, blank=True)
    episode_numb = models.PositiveSmallIntegerField("Номер эпизода",
                                                    help_text='Номер эпизода должен быть уникальным')
    video_hls = models.OneToOneField(CrowdVideo, on_delete=models.SET_NULL, null=True)

    opening_start_time = models.TimeField('Начальное время opening', default=time(0, 0, 0))
    opening_end_time = models.TimeField('Конечное время opening', default=time(0, 0, 0))
    final_start_time = models.TimeField('Начальное время final', default=time(0, 0, 0))
    draft = models.BooleanField("Черновик", default=False)


    class Meta:
        ordering = ['episode_numb', '-id']
        verbose_name = "Эпизод"
        verbose_name_plural = "Эпизоды"


class Film(models.Model):
    for iso in lang:
        locals()[f'sub_{iso}'] = models.FileField(f"Субтитры на [{lang[iso]}]",
                                                  upload_to=content_subs_filename,
                                                  # storage=OverwriteStorage(),
                                                  blank=True, null=True,
                                                  validators=[FileExtensionValidator(allowed_extensions=['vtt'])])

        locals()[f'audio_{iso}'] = models.OneToOneField(CrowdAudio, related_name=f'film_audio_{iso}',
                                                        verbose_name=f"Аудиодорожка на [{lang[iso]}]",
                                                        on_delete=models.SET_NULL, null=True, blank=True)
        locals()[f'is_sub_{iso}'] = models.BooleanField('Добавлено', default=False, editable=False)

    film = models.ForeignKey(Content, on_delete=models.SET_NULL, related_name='film_video',
                             null=True, blank=True, unique=True)
    duration = models.PositiveSmallIntegerField("Длительность", default=0)
    video_hls = models.OneToOneField(CrowdVideo, on_delete=models.SET_NULL, null=True)
    opening_start_time = models.TimeField('Начальное время opening', default=time(0, 0, 0))
    opening_end_time = models.TimeField('Конечное время opening', default=time(0, 0, 0))
    final_start_time = models.TimeField('Начальное время final', default=time(0, 0, 0))

    class Meta:
        verbose_name = 'Фильм'
        verbose_name_plural = 'Фильм'


class Trailer(models.Model):
    for iso in lang:
        locals()[f'title_{iso}'] = models.CharField(f"Название трейлера на [{lang[iso]}]",
                                                    max_length=200, blank=True, null=True)
        locals()[f'audio_{iso}'] = models.OneToOneField(CrowdAudio, related_name=f'trailer_audio_{iso}',
                                                        verbose_name=f"Аудиодорожка на [{lang[iso]}]",
                                                        on_delete=models.SET_NULL, null=True, blank=True)
        locals()[f'sub_{iso}'] = models.FileField(f"Субтитры на [{lang[iso]}]",
                                                  upload_to=content_subs_filename,
                                                  # storage=OverwriteStorage(),
                                                  blank=True, null=True,
                                                  validators=[FileExtensionValidator(allowed_extensions=['vtt'])])
        locals()[f'is_sub_{iso}'] = models.BooleanField('Добавлено', default=False, editable=False)

    picture = StdImageField("Картинка",
                            max_length=200,
                            upload_to=trailer_picture_filename,
                            storage=django.core.files.storage.FileSystemStorage(),
                            help_text="Рекомендуемое соотношение сторон 16х9",
                            blank=True, null=True,
                            variations={'resized': (320, -1), }
                            )
    duration = models.PositiveSmallIntegerField("Длительность", default=0)
    content = models.ForeignKey(Content, on_delete=models.SET_NULL, related_name='trailer', null=True)
    video_hls = models.OneToOneField(CrowdVideo, on_delete=models.SET_NULL, null=True)
    trailer_numb = models.PositiveSmallIntegerField("Номер трейлера",
                                                    help_text="Номер трейлера должен быть уникальным <br>"
                                                              "Номер трейлера 1 - Тизер", )

    class Meta:
        ordering = ('trailer_numb',)
        verbose_name = 'Трейлер'
        verbose_name_plural = 'Трейлеры'
