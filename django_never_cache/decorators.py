from functools import wraps

from asgiref.sync import iscoroutinefunction
from django.views.decorators import cache


def check_request(request):
    """
    Check if the request is allowed to cache.

    `_check_request` is available in Django > 5.0
    """
    if hasattr(cache, "_check_request"):
        cache._check_request(request, "allow_cache")


def allow_cache(view_func):
    """Decorator that allow cache for specific views."""

    if iscoroutinefunction(view_func):

        async def _view_wrapper(request, *args, **kwargs):
            check_request(request)
            response = await view_func(request, *args, **kwargs)
            if "Cache-Control" in response.headers:
                del response.headers["Cache-Control"]
            return response
    else:

        def _view_wrapper(request, *args, **kwargs):
            check_request(request)
            response = view_func(request, *args, **kwargs)
            if "Cache-Control" in response.headers:
                del response.headers["Cache-Control"]
            return response

    return wraps(view_func)(_view_wrapper)
