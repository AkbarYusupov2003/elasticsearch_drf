import os
from django.core.exceptions import ValidationError


def validate_video_extension(value):
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = ['.mp4']
    if not ext.lower() in valid_extensions:
        raise ValidationError('Поддерживаются только видео  .mp4 формата')


def validate_image_extension(value):
    ext = os.path.splitext(value.name)[-1]
    valid_extensions = ['.jpg', '.jpeg', '.png', '.gif', '.webp', ]
    if not ext.lower() in valid_extensions:
        raise ValidationError(f'Поддерживаются картинки только {valid_extensions} форматов')


def validate_tag_name(value):
    import re
    reg = re.compile('^[\S+]+$')
    if not reg.match(value):
        raise ValidationError(u'%s Теги не должны иметь пробелы!' % value)


def validate_rating(value):
    if not 11 > value > 0:
        raise ValidationError("Рэйтинг от 1 до 10")


def validate_profile_year(value):
    if not 1912 < value < 2022:
        raise ValidationError("Можно указать значение только от 1912 до 2022")
