from http import HTTPStatus

from django.conf import settings
from django.http import HttpResponse
from django.test import RequestFactory, TestCase, override_settings
from django.utils.decorators import method_decorator
from django.views import View

from django_never_cache.decorators import allow_cache


@method_decorator(allow_cache, name="dispatch")
class CachedView(View):
    def get(self, request, *args, **kwargs):
        return HttpResponse()


@override_settings(
    MIDDLEWARE=settings.MIDDLEWARE
    + ["django_never_cache.middelwares.NeverCacheMiddleware"]
)
class CachedViewTest(TestCase):
    """Test a cached view with the `allow_cache` decorator."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_view_with_allow_cache_decorator(self):
        """Test a view with the `allow_cache` decorator."""

        @method_decorator(allow_cache, name="get")
        class CachedView(View):
            def get(self, request, *args, **kwargs):
                return HttpResponse()

        view = CachedView.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertNotIn("Cache-Control", response.headers)
