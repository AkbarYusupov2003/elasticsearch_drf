# Generated by Django 4.2.6 on 2023-10-30 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Content',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title_ru', models.CharField(max_length=200, null=True, verbose_name='Название контента на [Russian]')),
                ('description_ru', models.TextField(blank=True, null=True, verbose_name='Описание на [Russian]')),
                ('title_en', models.CharField(max_length=200, null=True, verbose_name='Название контента на [English]')),
                ('description_en', models.TextField(blank=True, null=True, verbose_name='Описание на [English]')),
                ('title_uz', models.CharField(max_length=200, null=True, verbose_name='Название контента на [Uzbek]')),
                ('description_uz', models.TextField(blank=True, null=True, verbose_name='Описание на [Uzbek]')),
            ],
        ),
    ]
