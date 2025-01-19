from django.contrib.auth.mixins import LoginRequiredMixin
from django.utils.decorators import method_decorator
from django.views.decorators.cache import never_cache


@method_decorator(never_cache, name="dispatch")
class NoCacheMixin:
    """Mixin to disable caching for views."""

    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


@method_decorator(never_cache, name="dispatch")
class PrivateAreaMixin(LoginRequiredMixin):
    """Mixin to require login and disable caching for views."""
