# Generated by Django 4.2.6 on 2023-11-08 05:31

import content.etc.filename_path
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('content', '0001_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='content',
            options={'verbose_name': 'Контент', 'verbose_name_plural': '!Контент 0 Full'},
        ),
        migrations.RemoveField(
            model_name='content',
            name='ordering',
        ),
        migrations.RemoveField(
            model_name='contentsubscription',
            name='color',
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_1080p',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 1080p'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_240p',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 240p'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_2k',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 2k'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_360p',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 360p'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_480p',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 480p'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_4k',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 4k'),
        ),
        migrations.AddField(
            model_name='crowdvideo',
            name='codec_720p',
            field=models.CharField(blank=True, max_length=60, null=True, verbose_name='Кодек 720p'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_en',
            field=models.CharField(max_length=70, verbose_name='Название на [Английский]'),
        ),
        migrations.AlterField(
            model_name='category',
            name='name_uz',
            field=models.CharField(max_length=70, verbose_name='Название на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Описание на [Английский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='description_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Описание на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='is_en',
            field=models.BooleanField(default=False, verbose_name='доступен на языке [Английский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='is_uz',
            field=models.BooleanField(default=False, verbose_name='доступен на языке [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='slogan_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Слоган на [Английский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='slogan_uz',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Слоган на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='title_en',
            field=models.CharField(max_length=200, null=True, verbose_name='Название контента на [Английский]'),
        ),
        migrations.AlterField(
            model_name='content',
            name='title_uz',
            field=models.CharField(max_length=200, null=True, verbose_name='Название контента на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='contentcollection',
            name='title_en',
            field=models.CharField(max_length=200, verbose_name='Название коллекции на [Английский]'),
        ),
        migrations.AlterField(
            model_name='contentcollection',
            name='title_uz',
            field=models.CharField(max_length=200, verbose_name='Название коллекции на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='contentrelated',
            name='title_en',
            field=models.CharField(max_length=200, verbose_name='Название связанного контента на [Английский]'),
        ),
        migrations.AlterField(
            model_name='contentrelated',
            name='title_uz',
            field=models.CharField(max_length=200, verbose_name='Название связанного контента на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='description_en',
            field=models.CharField(max_length=500, verbose_name='Описание на [Английский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='description_list_en',
            field=models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание на [Английский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='description_list_uz',
            field=models.TextField(blank=True, max_length=1500, null=True, verbose_name='Описание на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='description_uz',
            field=models.CharField(max_length=500, verbose_name='Описание на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='title_en',
            field=models.CharField(max_length=60, verbose_name='Название на [Английский]'),
        ),
        migrations.AlterField(
            model_name='contentsubscription',
            name='title_uz',
            field=models.CharField(max_length=60, verbose_name='Название на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_en',
            field=models.CharField(max_length=100, verbose_name='Имя на [Английский]'),
        ),
        migrations.AlterField(
            model_name='country',
            name='name_uz',
            field=models.CharField(max_length=100, verbose_name='Имя на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='audio_en',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='episode_audio_en', to='content.crowdaudio', verbose_name='Аудиодорожка на [Английский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='audio_uz',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='episode_audio_uz', to='content.crowdaudio', verbose_name='Аудиодорожка на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='description_en',
            field=models.TextField(blank=True, null=True, verbose_name='Описание на [Английский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='description_uz',
            field=models.TextField(blank=True, null=True, verbose_name='Описание на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='sub_en',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Английский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='sub_uz',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название эпизода на [Английский]'),
        ),
        migrations.AlterField(
            model_name='episode',
            name='title_uz',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название эпизода на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='film',
            name='audio_en',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='film_audio_en', to='content.crowdaudio', verbose_name='Аудиодорожка на [Английский]'),
        ),
        migrations.AlterField(
            model_name='film',
            name='audio_uz',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='film_audio_uz', to='content.crowdaudio', verbose_name='Аудиодорожка на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='film',
            name='sub_en',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Английский]'),
        ),
        migrations.AlterField(
            model_name='film',
            name='sub_uz',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name_en',
            field=models.CharField(max_length=70, verbose_name='Название на [Английский]'),
        ),
        migrations.AlterField(
            model_name='genre',
            name='name_uz',
            field=models.CharField(max_length=70, verbose_name='Название на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name_en',
            field=models.CharField(max_length=100, verbose_name='Имя на [Английский]'),
        ),
        migrations.AlterField(
            model_name='person',
            name='name_uz',
            field=models.CharField(max_length=100, verbose_name='Имя на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='audio_en',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trailer_audio_en', to='content.crowdaudio', verbose_name='Аудиодорожка на [Английский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='audio_uz',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='trailer_audio_uz', to='content.crowdaudio', verbose_name='Аудиодорожка на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='sub_en',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Английский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='sub_uz',
            field=models.FileField(blank=True, null=True, upload_to=content.etc.filename_path.content_subs_filename, validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['vtt'])], verbose_name='Субтитры на [Узбекский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='title_en',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название трейлера на [Английский]'),
        ),
        migrations.AlterField(
            model_name='trailer',
            name='title_uz',
            field=models.CharField(blank=True, max_length=200, null=True, verbose_name='Название трейлера на [Узбекский]'),
        ),
    ]
