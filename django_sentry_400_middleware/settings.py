from django.conf import settings


IGNORED_USER_AGENTS = getattr(settings, 'SENTRY_404_IGNORED_USER_AGENTS', [])
