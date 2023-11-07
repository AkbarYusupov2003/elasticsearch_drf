def category_filename(instance, filename):
    return f"categories_ico/{instance.slug}.{filename.split('.')[-1]}"


def sponsor_filename(instance, filename):
    return f"sponsors/{instance.slug}.{filename.split('.')[-1]}"


def person_filename(instance, filename):
    return f"persons/{instance.slug}.{filename.split('.')[-1]}"


def content_logo_image_square_filename(instance, filename):
    return f"contents_meta/{instance.slug}/images/logo_image_square.{filename.split('.')[-1]}"


def content_logo_image_rectangle_filename(instance, filename):
    return f"contents_meta/{instance.slug}/images/logo_image_rectangle.{filename.split('.')[-1]}"


def content_poster_v_filename(instance, filename):
    return f"contents_meta/{instance.slug}/images/poster_v.{filename.split('.')[-1]}"


def content_poster_h_filename(instance, filename):
    return f"contents_meta/{instance.slug}/images/poster_h.{filename.split('.')[-1]}"


def content_bg_image_filename(instance, filename):
    return f"contents_meta/{instance.slug}/images/bg_image.{filename.split('.')[-1]}"


def episode_picture_filename(instance, filename):
    return f"contents_meta/{instance.seasons.serial.slug}/images/episode_{instance.seasons.season_numb}_{instance.episode_numb}_picture.{filename.split('.')[-1]}"


def trailer_picture_filename(instance, filename):
    return f"contents_meta/{instance.content.slug}/images/trailer_picture_{instance.trailer_numb}.{filename.split('.')[-1]}"


# def content_subs_filename(instance, filename):
#     try:
#         # Try to film
#         if instance.sub_ru.name == filename:
#             return f"contents_meta/{instance.film.slug}/subs/sub_ru.vtt"
#         elif instance.sub_en.name == filename:
#             return f"contents_meta/{instance.film.slug}/subs/sub_en.vtt"
#         elif instance.sub_uz.name == filename:
#             return f"contents_meta/{instance.film.slug}/subs/sub_uz.vtt"
#         raise ValueError("Subs folder error.")
#     except AttributeError:
#         # This subs is not in film
#         pass
#     try:
#         # Try to serial
#         if instance.sub_ru.name == filename:
#             return f"contents_meta/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/subs/sub_ru.vtt"
#         elif instance.sub_en.name == filename:
#             return f"contents_meta/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/subs/sub_en.vtt"
#         elif instance.sub_uz.name == filename:
#             return f"contents_meta/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/subs/sub_uz.vtt"
#         raise ValueError("Subs folder error.")
#     except AttributeError:
#         # This subs is not in serial
#         pass
#     try:
#         # Try to trailer
#         if instance.sub_ru.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/subs/sub_ru.vtt"
#         elif instance.sub_en.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/subs/sub_en.vtt"
#         elif instance.sub_uz.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/subs/sub_uz.vtt"
#         raise ValueError("Subs folder error.")
#     except AttributeError:
#         raise ValueError("Subs No Content.")


def content_subs_filename(instance, filename):
    try:
        # Try to film
        return f"contents_meta/{instance.film.slug}/subtitles/{filename}"
    except AttributeError:
        # This subs is not in film
        pass
    try:
        # Try to serial
        return f"contents_meta/{instance.seasons.serial.slug}/subtitles/{filename}"
    except AttributeError:
        # This subs is not in serial
        pass
    try:
        # Try to trailer
        return f"contents_meta/{instance.content.slug}/subtitles/{filename}"
    except AttributeError:
        raise ValueError("Subs No Content.")


# def content_audio_filename(instance, filename):
#     try:
#         # Try to film
#         if instance.audio_ru.name == filename:
#             return f"contents/{instance.film.slug}/audio/ru/ru.mp4"
#         elif instance.audio_en.name == filename:
#             return f"contents/{instance.film.slug}/audio/en/en.mp4"
#         elif instance.audio_uz.name == filename:
#             return f"contents/{instance.film.slug}/audio/uz/uz.mp4"
#         raise ValueError("Subs folder error.")
#     except AttributeError:
#         # This subs is not in trailer
#         pass
#     try:
#         # Try to serial
#         if instance.audio_ru.name == filename:
#             return f"contents/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/audio/ru/ru.mp4"
#         elif instance.audio_en.name == filename:
#             return f"contents/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/audio/en/en.mp4"
#         elif instance.audio_uz.name == filename:
#             return f"contents/{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}/audio/uz/uz.mp4"
#         raise ValueError("Audio folder error.")
#     except AttributeError:
#         # This subs is not in serial
#         pass
#     try:
#         # Try to trailer
#         if instance.audio_ru.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/audio/ru/ru.mp4"
#         elif instance.audio_en.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/audio/en/en.mp4"
#         elif instance.audio_uz.name == filename:
#             return f"contents_meta/{instance.content.slug}/trailer/{instance.trailer_numb}/audio/uz/uz.mp4"
#         raise ValueError("Audio folder error.")
#     except AttributeError:
#         raise ValueError("Audio No Content.")


# def content_video_filename(instance, filename):
#     instance.allow_split = True
#     instance.success_mpd = False
#     instance.audio_uz.name = ''
#     instance.audio_ru.name = ''
#     instance.audio_en.name = ''
#     instance.sub_uz.name = ''
#     instance.sub_ru.name = ''
#     instance.sub_en.name = ''
#     try:
#         # Try to film
#         slug = instance.film.slug
#         erase_content(f"contents/{slug}")
#         return f"contents/{slug}/video/original.mp4"
#     except AttributeError:
#         # This video is not in film
#         pass
#     try:
#         # Try to trailer
#         slug = instance.content.slug
#         erase_content(f"contents_meta/{slug}/trailer/{instance.trailer_numb}")
#         return f"contents_meta/{slug}/trailer/{instance.trailer_numb}/video/original.mp4"
#     except AttributeError:
#         # This video is not in trailer
#         pass
#     try:
#         # Try to serial
#         slug = f"{instance.seasons.serial.slug}/{instance.seasons.season_numb}/{instance.episode_numb}"
#         erase_content(f"contents/{slug}")
#         return f"contents/{slug}/video/original.mp4"
#     except AttributeError:
#         raise ValueError("No type content video folder")
