[![License: MIT](https://img.shields.io/github/license/trottomv/django-never-cache.svg)](LICENSE)
[![CI](https://github.com/trottomv/django-never-cache/actions/workflows/ci.yml/badge.svg)](https://github.com/trottomv/django-never-cache/actions/workflows/ci.yml)
[![PyPI](https://img.shields.io/pypi/v/django-never-cache.svg)](https://pypi.org/project/django-never-cache/)
[![Python Versions](https://img.shields.io/pypi/pyversions/django-never-cache.svg)](https://pypi.org/project/django-never-cache/)
[![Django Versions](https://img.shields.io/pypi/djversions/django-never-cache.svg)](https://pypi.org/project/django-never-cache/)
[![Django Packages](https://img.shields.io/badge/Django_Packages-django--never--cache-8c3c26.svg)](https://djangopackages.org/packages/p/django-never-cache/)

# Django Never Cache

This Django app provides a suite of utilities to disable caching in your sensitive views.

## Requirements

- Python >= 3.8
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

### Mixins

#### NoCacheMixin

Use `NoCacheMixin` to disable caching for a view:

```python
from django.views.generic import TemplateView
from django_never_cache.mixins import NoCacheMixin

class MyView(NoCacheMixin, TemplateView):
    template_name = "my_template.html"
```

#### PrivateAreaMixin

Use `PrivateAreaMixin` to require login and disable caching for a private area:

```python
from django.views.generic import TemplateView
from django_never_cache.mixins import PrivateAreaMixin

class MyView(PrivateAreaMixin, TemplateView):
    template_name = "my_private_template.html"
```

### NeverCacheMiddleware

Use `NeverCacheMiddleware` if you want to disable caching for the whole site:

```python
MIDDLEWARE = [
    ...
    "django_never_cache.middlewares.NeverCacheMiddleware",
]
```

### allow_cache

If you have added `NeverCacheMiddleware` to `MIDDLEWARE`, you can re-enable caching for a specific view using the `allow_cache` decorator:

```python
from django.utils.decorators import method_decorator
from django.views.generic import TemplateView
from django_never_cache.decorators import allow_cache

@method_decorator(allow_cache, name="dispatch")
class MyCachedView(TemplateView):
    template_name = "my_cached_template.html"
```

`allow_cache` supports both synchronous and asynchronous views.

## Development

### Prerequisites

- tox
- Golang >= 1.21

### Run tests

To run the tests, run the following command:

```bash
tox
```

### Contribute

You can contribute to this project on [GitHub](https://github.com/trottomv/django-never-cache).

1. Fork the [repository](https://github.com/trottomv/django-never-cache).
2. Create a new branch: `git checkout -b my-branch-name`.
3. Install `pre-commit` with `pre-commit install` and make your changes.
4. Commit your changes: `git commit -am "Add some feature"`.
5. Push your branch: `git push origin my-branch-name`.
6. Create a pull request.

## License

This project is released under the [MIT License](LICENSE).
