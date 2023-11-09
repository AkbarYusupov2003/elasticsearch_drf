from rest_framework import serializers

from content.models import Content


class StdImageField(serializers.ImageField):

    def to_native(self, obj):
        return self.get_variations_urls(obj)

    def to_representation(self, obj):
        if not obj:
            return
        return self.get_variations_urls(obj)

    def get_variations_urls(self, obj):
        return_object = {}
        field = obj.field
        if hasattr(field, 'variations'):
            variations = field.variations
            for key in variations.keys():
                if hasattr(obj, key):
                    field_obj = getattr(obj, key, None)
                    if field_obj and hasattr(field_obj, 'url'):
                        return_object[key] = super(StdImageField, self).to_representation(field_obj)
        if hasattr(obj, 'url'):
            return_object['original'] = super(StdImageField, self).to_representation(obj)
        return return_object


def translate(s1):
    translation = {}

    translation[ord("`")] = "ё"

    translation[ord("q")] = "й"
    translation[ord("w")] = "ц"
    translation[ord("e")] = "у"
    translation[ord("r")] = "к"
    translation[ord("t")] = "е"
    translation[ord("y")] = "н"
    translation[ord("u")] = "г"
    translation[ord("i")] = "ш"
    translation[ord("o")] = "щ"
    translation[ord("p")] = "з"
    translation[ord("[")] = "х"
    translation[ord("]")] = "ъ"

    translation[ord("a")] = "ф"
    translation[ord("s")] = "ы"
    translation[ord("d")] = "в"
    translation[ord("f")] = "а"
    translation[ord("g")] = "п"
    translation[ord("h")] = "р"
    translation[ord("j")] = "о"
    translation[ord("k")] = "л"
    translation[ord("l")] = "д"
    translation[ord(";")] = "ж"
    translation[ord("'")] = "э"

    translation[ord("z")] = "я"
    translation[ord("x")] = "ч"
    translation[ord("c")] = "с"
    translation[ord("v")] = "м"
    translation[ord("b")] = "и"
    translation[ord("n")] = "т"
    translation[ord("m")] = "ь"
    translation[ord(",")] = "б"
    translation[ord(".")] = "ю"
    translation[ord("/")] = "."

    return s1.translate(translation)
