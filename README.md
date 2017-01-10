# Django Sentry 400 Middleware
[![Build Status](https://travis-ci.org/ArtProcessors/django-sentry-400-middleware.svg?branch=master)](https://travis-ci.org/ArtProcessors/django-sentry-400-middleware)

Django middleware to log 400 level errors to Sentry.

## Installation

```
$ pip install django-sentry-400-middleware
```

```python
MIDDLEWARE_CLASSES = (
    'django_sentry_400_middleware.Sentry400CatchMiddleware',
)
```
