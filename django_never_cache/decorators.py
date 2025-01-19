from functools import wraps

from asgiref.sync import iscoroutinefunction


def allow_cache(view_func):
    """Decorator that allow cache for specific views."""

    import django

    if django.get_version() < "5.0":

        @wraps(view_func)
        def _wrapped_view_func(request, *args, **kwargs):
            response = view_func(request, *args, **kwargs)
            if "Cache-Control" in response.headers:
                del response.headers["Cache-Control"]
            return response

        return _wrapped_view_func

    else:
        from django.views.decorators.cache import _check_request

        if iscoroutinefunction(view_func):

            async def _view_wrapper(request, *args, **kwargs):
                _check_request(request, "allow_cache")
                response = await view_func(request, *args, **kwargs)
                if "Cache-Control" in response.headers:
                    del response.headers["Cache-Control"]
                return response
        else:

            def _view_wrapper(request, *args, **kwargs):
                _check_request(request, "allow_cache")
                response = view_func(request, *args, **kwargs)
                if "Cache-Control" in response.headers:
                    del response.headers["Cache-Control"]
                return response

        return wraps(view_func)(_view_wrapper)
