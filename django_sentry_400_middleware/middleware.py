from __future__ import absolute_import, unicode_literals

import logging


class Sentry400CatchMiddleware(object):
    def process_response(self, request, response):
        from raven.contrib.django.models import client

        status_code = response.status_code

        if (400 > status_code or status_code >= 500) or not client.is_enabled():
            return response

        data = client.get_data_from_request(request)
        data.update({
            'level': logging.INFO,
            'logger': 'django',
        })
        result = client.captureMessage(
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
            'project_id': data.get('project', client.remote.project),
            'id': client.get_ident(result),
        }
        return response
