# Django Never Cache

This Django app provides mixins to disable caching for generic and login required views,
and a middleware to disable caching for the whole site.

## Prerequisites

- Python >= 3.9
- Django >= 3.2

## Installation

1. Install the package via pip:

    ```bash
    pip install django-never-cache
    ```

2. Add `django_never_cache` to your `INSTALLED_APPS` in `settings.py`:

    ```python
    INSTALLED_APPS = [
        ...
        "django_never_cache",
        ...
    ]
    ```

## Usage

### NoCacheMixin

Use `NoCacheMixin` to disable caching for a view:

```python
from django.views.generic import TemplateView
from django_never_cache.mixins import NoCacheMixin

class MyView(NoCacheMixin, TemplateView):
    template_name = "my_template.html"
```

### PrivateAreaMixin

Use `PrivateAreaMixin` to require login and disable caching for a private area:

```python
from django.views.generic import TemplateView
from django_never_cache.mixins import PrivateAreaMixin

class MyView(PrivateAreaMixin, TemplateView):
    template_name = "my_private_template.html"
```

### NoCacheMiddleware

Use `NoCacheMiddleware` if you want to disable caching for the whole site:

```python
MIDDLEWARE = [
    ...
    "django_never_cache.middleware.NeverCacheMiddleware",
]
```

If you have setted `NeverCacheMiddleware` in `MIDDLEWARE` you can exclude caching for a view using `allow_cache` decorator.

```python
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_never_cache.decorators import allow_cache

@method_decorator(allow_cache, name="dispatch")
class MyCachedView(TemplateView):
    template_name = "my_cached_template.html"
```

# Contribute

You can contribute to this project on [GitHub](https://github.com/trottomv/django-never-cache).

## How to Contribute

1. Fork the [repository](https://github.com/trottomv/django-never-cache).
2. Create a new branch: `git checkout -b my-branch-name`.
3. Install `pre-commit` with `pre-commit install` and make your changes.
4. Commit your changes: `git commit -am "Add some feature"`.
5. Push your branch: `git push origin my-branch-name`.
6. Create a pull request.

## Run tests

To run the tests, run the following command:

```bash
tox
```

# License

This project is released under the [MIT License](LICENSE).
