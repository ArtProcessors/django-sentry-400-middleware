from unittest import TestCase
from django.http import HttpResponse
from django.test import override_settings, RequestFactory
from django_sentry_400_middleware.middleware import Sentry400CatchMiddleware
from mock import Mock


class MiddlewareTests(TestCase):
    def get_middleware_with_mock_client(self, response):
        mock_client = Mock(**{
            'is_enabled.return_value': True,
            'get_data_from_request.side_effect': lambda req: dict(),
        })
        middleware = Sentry400CatchMiddleware(get_response=lambda x: response)
        middleware.client = mock_client
        return middleware

    def setUp(self):
        self.factory = RequestFactory()

    def test_only_4xx_status_codes_logged(self):
        cases = [
            (200, False),
            (304, False),
            (401, True),
            (404, True),
            (500, False),
        ]

        for status_code, expected_is_logged in cases:
            req = self.factory.get('/')
            resp = HttpResponse('OK', status=status_code)
            middleware = self.get_middleware_with_mock_client(resp)

            middleware.process_response(req, resp)

            assert middleware.client.captureMessage.called == expected_is_logged

    def test_404_not_logged_if_from_ignored_user_agent(self):
            for user_agent in (
                'Rackspace Monitoring/1.1 (https://monitoring.api.rackspacecloud.com)',
                'Rackspace Monitoring/1.2 (https://monitoring.api.rackspacecloud.com)',
            ):
                req = self.factory.get('/')
                req.META['HTTP_USER_AGENT'] = user_agent
                resp = HttpResponse('Not found', status=404)
                middleware = self.get_middleware_with_mock_client(resp)
                middleware.ignored_user_agents = (
                    r'^Rackspace Monitoring.*$',
                )

                middleware.process_response(req, resp)

                assert middleware.client.captureMessage.called == False
