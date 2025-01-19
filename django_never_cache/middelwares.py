from django.utils.cache import add_never_cache_headers


class NeverCacheMiddleware:
    """Middleware to disable caching for the whole site."""

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        response = self.get_response(request)
        add_never_cache_headers(response)
        return response
