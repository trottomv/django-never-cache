from http import HTTPStatus

from django.contrib.auth import get_user_model
from django.contrib.auth.models import AnonymousUser
from django.http import HttpResponse
from django.test import RequestFactory, TestCase
from django.views import View

from django_never_cache.mixins import NoCacheMixin, PrivateAreaMixin


class NoCacheMixinTest(TestCase):
    """Test NoCacheMixin."""

    def setUp(self):
        self.factory = RequestFactory()

    def test_no_cache_headers(self):
        """Test that the Cache-Control header is set to no-cache."""

        class AView(NoCacheMixin, View):
            def get(self, request, *args, **kwargs):
                return HttpResponse()

        view = AView.as_view()
        request = self.factory.get("/")
        response = view(request)
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(
            response.headers["Cache-Control"],
            "max-age=0, no-cache, no-store, must-revalidate, private",
        )


class PrivateAreaMixinTest(TestCase):
    """Test private area Cache-Control override."""

    factory = RequestFactory()

    @classmethod
    def setUpTestData(cls):
        """Initialize test data."""
        cls.user = get_user_model().objects.create_user(
            username="testuser",
            email="user@test.xyz",
            password="5tr0ngP4ssW0rd",
        )

    def test_login_required_and_no_cache_headers(self):
        """Test login required and Cache-Control dispatched."""

        class AView(PrivateAreaMixin, View):
            def get(self, request, *args, **kwargs):
                return HttpResponse()

            def dispatch(self, request, *args, **kwargs):
                return super().dispatch(request, *args, **kwargs)

        view = AView.as_view()

        with self.subTest("Anonymous user"):
            request = self.factory.get("/")
            request.user = AnonymousUser()
            response = view(request)
            self.assertEqual(response.status_code, HTTPStatus.FOUND)
            self.assertEqual("/accounts/login/?next=/", response.url)

        with self.subTest("Authenticated user"):
            request = self.factory.get("/")
            request.user = self.user
            response = view(request)
            self.assertEqual(response.status_code, HTTPStatus.OK)
            self.assertIn("Cache-Control", response.headers)
            self.assertEqual(
                response.headers["Cache-Control"],
                "max-age=0, no-cache, no-store, must-revalidate, private",
            )
