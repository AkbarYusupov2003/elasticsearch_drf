from django.contrib import admin
from django.conf import settings

from content import models

from django.utils.safestring import mark_safe


lang = {
    "ru": "Русский",
    "en": "Английский",
    "uz": "Узбекский",
}


@admin.register(models.Content)
class ContentAdmin(admin.ModelAdmin):
    list_display = ("id", "title_ru", "description_ru", "draft")
    list_filter = ("draft",)


admin.site.register(models.Person)


# ---------------------------------------------------------------------------------------
# Film
class FilmContentFilter(admin.SimpleListFilter):
    title = 'Существует ли контент'
    parameter_name = 'content_exists'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(film=None)
        elif self.value() == 'no':
            return queryset.filter(film=None)
        else:
            return queryset


@admin.register(models.Film)
class FilmAdmin(admin.ModelAdmin):
    list_display = ["id", "film", "duration"]
    list_filter = [FilmContentFilter]


# Trailer
class TrailerContentFilter(admin.SimpleListFilter):
    title = 'Существует ли контент'
    parameter_name = 'content_exists'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(content=None)
        elif self.value() == 'no':
            return queryset.filter(content=None)
        else:
            return queryset


@admin.register(models.Trailer)
class TrailerAdmin(admin.ModelAdmin):
    list_display = ["id", "content", "duration"]
    list_filter = [TrailerContentFilter]


# Episode
class EpisodeContentFilter(admin.SimpleListFilter):
    title = 'Существует ли сезон'
    parameter_name = 'season_exists'

    def lookups(self, request, model_admin):
        return (
            ('yes', 'Да'),
            ('no', 'Нет'),
        )

    def queryset(self, request, queryset):
        if self.value() == 'yes':
            return queryset.exclude(seasons=None)
        elif self.value() == 'no':
            return queryset.filter(seasons=None)
        else:
            return queryset


@admin.register(models.Episode)
class EpisodeAdmin(admin.ModelAdmin):
    list_display = ["id", "seasons", "video_hls"]
    list_filter = [EpisodeContentFilter]
    
# CrowdVideo
class CrowdVideoQualityFilter(admin.SimpleListFilter):
    title = 'Максимальное качество видео'
    parameter_name = 'quality'

    def lookups(self, request, model_admin):
        qualities = []
        for key in settings.VIDEO_QUALITY.keys():
            qualities.append([key, key])
        return qualities

    def queryset(self, request, queryset):
        if self.value() in settings.VIDEO_QUALITY.keys():
            for quality in settings.VIDEO_QUALITY.keys():
                if self.value() != quality:
                    queryset = queryset.exclude(**{f"codec_{quality}__isnull": False})
                else:
                    return queryset.exclude(**{f"codec_{self.value()}__isnull": True})
        else:
            return queryset


# ---------------------------------------------------------------------------------------
@admin.register(models.CrowdVideo)
class CrowdVideoAdmin(admin.ModelAdmin):
    list_display = [
        "id", "slug", "duration",
        "codec_4k", "codec_2k", "codec_1080p", 
        "codec_720p", "codec_480p", "codec_360p", "codec_240p",
    ]
    list_display_links = "id", "slug",
    list_filter = CrowdVideoQualityFilter,
    # list_filter = UnUsedVideo,
    search_fields = 'slug',
    readonly_fields = ['hls_player', 'get_related_contents', 'slug', 'duration']
    fieldsets = (
        ('Qualities',
         {'fields': ['is_mark_for_deletion'] + ['duration'] + ['get_related_contents']}),
        ('Player', {'fields': ('hls_player',)})
    )
    

    def get_actions(self, request):
        actions = super().get_actions(request)
        if 'delete_selected' in actions:
            del actions['delete_selected']
        return actions

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return request.user.is_superuser

    def hls_player(self, obj):
        vod_url = "https://api.splay.uz"
        # vod_url = "http://localhost:8002"
        output = '<video controls style="width:1280px; height: 720px" id="video"></video>' \
                 '<div id="qualities"></div>' \
                 '<script src="https://cdn.jsdelivr.net/npm/hls.js@1"></script>' \
                 '<script>const video = document.getElementById(\'video\');' \
                 'const qualitiesDom = document.getElementById(\'qualities\');' \
                 f'const url = "{vod_url}/en/api/v1/content/crowd-hls/{obj.id}/{settings.SECRET_KEY}";' \
                 "if (Hls.isSupported()) { var hls = new Hls(); hls.loadSource(url); hls.attachMedia(video);} " \
                 "else if (video.canPlayType('application/vnd.apple.mpegurl')) { video.src = url; }" \
                 "hls.on(Hls.Events.MANIFEST_PARSED, () => {" \
                 "var qualities = hls.levels; for (let i = 0; i < qualities.length; i++) {" \
                 "let quality = <button type='button' class=\"quality\"> ${qualities[i].height} </button>; " \
                 "qualitiesDom.innerHTML += quality; }" \
                 "let qualityDom = document.querySelectorAll('.quality'); for (let i = 0; i < qualityDom.length; i++) {" \
                 "qualityDom[i].addEventListener('click', () => setQuality(i)) }hls.currentLevel = 0; });" \
                 "function setQuality(index) { hls.currentLevel = index; console.log(hls.currentLevel) }</script>"

        return mark_safe(output)

    def get_related_contents(self, obj):
        trailer, episode, film = (False, False, False)
        try:
            trailer = obj.trailer.content
            trailer_detail = f"Трейлер {obj.trailer.trailer_numb}"
        except Exception as e:
            pass
        try:
            episode = obj.episode.seasons.serial
            episode_detail = f" Сезон {obj.episode.seasons.season_numb} - эпизод {obj.episode.episode_numb}"
        except Exception as e:
            pass
        try:
            film = obj.film.film
        except Exception as e:
            pass

        output = f"""
        Film  :  {f"<a href='/admin/content/content/{film.id}/change/'>{film}</a> <p>{''}</p>" if film else '-'}<br/>
        Episode : {f"{episode_detail} <a href='/admin/content/content/{episode.id}/change/'>{episode}</a>" if episode else '-'}<br/>
        Trailer: {f"{trailer_detail} <a href='/admin/content/content/{trailer.id}/change/'>{trailer}</a><p>{''}</p>" if trailer else '-'}<br/>
        """
        return mark_safe(output)

    get_related_contents.short_description = "Контент"
    # get_count_qualities.short_description = "Количество качеств"



@admin.register(models.CrowdAudio)
class CrowdAudioAdmin(admin.ModelAdmin):
    list_display = "slug",
    search_fields = 'slug',
    # readonly_fields = 'hls_player',
    fields = 'get_related_contents',
    # list_filter = UnUsedAudio,

    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        # return request.user.is_superuser
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def get_related_contents(self, obj):
        for iso in lang:
            try:
                locals()[f'trailer_audio_{iso}'] = getattr(obj, f'trailer_audio_{iso}').content
                locals()[f'trailer_audio_{iso}_detail'] = f"Трейлер {getattr(obj, f'trailer_audio_{iso}').trailer_numb}"
            except Exception as e:
                locals()[f'trailer_audio_{iso}'] = False
            try:
                locals()[f'episode_audio_{iso}'] = getattr(obj, f'episode_audio_{iso}').seasons.serial
                locals()[
                    f'episode_audio_{iso}_detail'] = f" Сезон {getattr(obj, f'episode_audio_{iso}').seasons.season_numb} - эпизод {getattr(obj, f'episode_audio_{iso}').episode_numb}"
            except Exception as e:
                locals()[f'episode_audio_{iso}'] = False
            try:
                locals()[f'film_audio_{iso}'] = getattr(obj, f'film_audio_{iso}')
            except Exception as e:
                locals()[f'film_audio_{iso}'] = False
        output = ''
        film, episode, trailer = ('', '', '')
        for iso in lang:
            film += f"""<span style='margin-left: 70px'>
            </span>audio {lang[iso]}: {f"<a href='/admin/content/content/{locals()[f'film_audio_{iso}'].film.id}/change/'>{locals()[f'film_audio_{iso}']}</a>" if locals()[f'film_audio_{iso}'] else '-'}<br/>"""
            episode += f"""<span style='margin-left: 70px'>
            </span>audio {lang[iso]}:
            {f"{locals()[f'episode_audio_{iso}_detail']} <a href='/admin/content/content/{locals()[f'episode_audio_{iso}'].seasons.instance.id}/change/'>{locals()[f'episode_audio_{iso}']}</a>" if locals()[f'episode_audio_{iso}'] else '-'}<br/>"""
            trailer += f"""<span style='margin-left: 70px'>
            </span>audio {lang[iso]}:
            {f"{locals()[f'trailer_audio_{iso}_detail']} <a href='/admin/content/content/{locals()[f'trailer_audio_{iso}'].film_video.instance.id}/change/'>{locals()[f'trailer_audio_{iso}']}</a>" if locals()[f'trailer_audio_{iso}'] else '-'}<br/>"""

        output = f"""
            Trailer: <br/>{trailer}<br/>
            Episode: <br/>{episode}<br/>
            Film: <br/>{film}<br/>
        """
        return mark_safe(output)

    get_related_contents.short_description = "Контент"