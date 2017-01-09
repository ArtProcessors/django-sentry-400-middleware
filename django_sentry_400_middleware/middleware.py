from __future__ import absolute_import, unicode_literals

import logging
import re

try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:
    MiddlewareMixin = object

from . import settings


class Sentry400CatchMiddleware(MiddlewareMixin):
    def __init__(self, get_response=None):
        from raven.contrib.django.models import client
        self.client = client
        self.ignored_user_agents = settings.IGNORED_USER_AGENTS
        self.get_response = get_response

    def process_response(self, request, response):

        status_code = response.status_code

        if (400 > status_code or status_code >= 500) or not self.client.is_enabled():
            return response

        for USER_AGENT in self.ignored_user_agents:
            if re.match(USER_AGENT, request.META['HTTP_USER_AGENT']):
                return response

        data = self.client.get_data_from_request(request)
        data.update({
            'level': logging.INFO,
            'logger': 'django',
        })
        result = self.client.captureMessage(
            message='Client Error (%s): %s' % (status_code, request.build_absolute_uri()),
            data=data,
            extra={
                'response_status_code': status_code,
                'response_content': response.content,
            },
        )
        if not result:
            return

        request.sentry = {
            'project_id': data.get('project', self.client.remote.project),
            'id': self.client.get_ident(result),
        }
        return response
