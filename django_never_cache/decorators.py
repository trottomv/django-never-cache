from functools import wraps

import django
from asgiref.sync import iscoroutinefunction


def check_request(request):
    """Check if the request is allowed to cache."""
    if django.get_version() > "5.0":
        from django.views.decorators.cache import _check_request

        _check_request(request, "allow_cache")


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
