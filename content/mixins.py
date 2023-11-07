from django.conf import settings
from django.core.cache import cache


class CacheViewMixin:
    def is_query_params_valid(self, query_params):
        allowed_keys = [
            "limit",
            "offset",
            "ordering",
            "country",
            "is_russian",
            "year",
            "genres",
            "sponsors",
            "category",
            "is_kids",
        ]
        
        for key, _ in query_params.items():
            if not (key in allowed_keys):
                return False

        return True
        
    def dispatch(self, request, *args, **kwargs):
        new_req = super().initialize_request(request, *args, **kwargs)
        age = 18 # new_req.auth.payload['age']
        c_code = "UZ" # new_req.auth.payload['c_code']
        
        try:
            super().initial(new_req, *args, **kwargs)
        except Exception as exc:
            response = super().handle_exception(exc)
            self.headers = super().default_response_headers
            end_response = super().finalize_response(new_req, response, *args, **kwargs)
            return end_response

        view = super().dispatch(request, *args, **kwargs).render()
        query_params = self.request.GET.dict()
        is_query_params_valid = self.is_query_params_valid(query_params)
        if is_query_params_valid:
            #
            limit = query_params.get('limit', 50)
            offset = query_params.get('offset', 0)
            ordering = query_params.get("ordering", "")
            country = query_params.get("country", "")
            is_russian = query_params.get("is_russian", "")
            year = query_params.get("year", "")
            genres = query_params.get("genres", "")
            sponsors = query_params.get("sponsors", "")
            category = query_params.get("category", "")
            #
            cache_key = f"{request.path}_c_code_{c_code}_age_{age}_li{limit}_of{offset}_or{ordering}_co{country}_ru{is_russian}_ye{year}_ge{genres}_sp{sponsors}_ca{category}" 
            
            cached_view = cache.get(cache_key, None)
            if not cached_view:
                cache.set(cache_key, view, settings.CACHE_TTL)
                print('CREATE CACHE')
                return view
            print('CACHED')
            return cached_view
        print('EMPTY CACHE')
        return super().dispatch(request, *args, **kwargs).render()
