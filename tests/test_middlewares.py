from django.conf import settings
from django.test import Client, TestCase, override_settings


@override_settings(
    MIDDLEWARE=settings.MIDDLEWARE
    + ["django_never_cache.middelwares.NeverCacheMiddleware"]
)
class NeverCacheMiddlewareTest(TestCase):
    """Test NeverCacheMiddleware."""

    def setUp(self):
        self.client = Client()

    def test_cache_control_middleware(self):
        """Test that the Cache-Control header is set using `NeverCacheMiddleware`."""
        response = self.client.get("/")
        self.assertEqual(response.status_code, 200)
        self.assertIn("Cache-Control", response.headers)
        self.assertEqual(
            response.headers["Cache-Control"],
            "max-age=0, no-cache, no-store, must-revalidate, private",
        )
