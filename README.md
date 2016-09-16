# Django Sentry 400 Middleware

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
