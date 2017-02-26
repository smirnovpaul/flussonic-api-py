# -*- coding: utf-8 -*-
import requests

from .log import LOGGER
from requests.auth import HTTPBasicAuth as Auth


class HttpApi(object):
    """
    User and Password are data from Flussonic Server
    (see to edit_auth, view_auth).

    HTTP Basic auth.
    """
    def __init__(self, user, password, url):
        self.auth = Auth(user, password)
        self.message = None
        self.url = 'http://{}/flussonic/api/'.format(url)
        self.api = None

    @property
    def _connect(self):
        try:
            r = requests.get(''.join((self.url, self.api)), auth=self.auth)
        except (requests.RequestException, requests.Timeout) as e:
            LOGGER.error('Error request {}: {}'.format(self.message, e))
            return None

        try:
            # TODO for stream_health
            if r.status_code == 424:
                # stream is dead
                return False
            r.raise_for_status()
        except requests.HTTPError as e:
            LOGGER.error('Error request {}: {}'.format(self.message, e))
            return None

        try:
            response = r.json()
        except ValueError as e:
            LOGGER.error('Error request {}: {}'.format(self.message, e))
            return None
        else:
            return response

    def simple_method(self, api, message):
        """
        Simple basic method for API.

        If need to create something quickly.
        """
        self.api = api
        self.message = message
        return self._connect

    def dvr_status(self, year, month, day, stream_name):
        self.api = 'dvr_status/{}/{}/{}/{}'.format(year, month, day, stream_name)
        self.message = 'Recording map over the past day {}/{}/{}'.format(year, month, day)
        return self._connect

    def media_info(self, stream_name):
        self.api = 'media_info/{}'.format(stream_name)
        self.message = 'Stream information'
        return self._connect

    @property
    def server(self):
        self.api = 'server'
        self.message = 'Server info in JSON format.'
        return self._connect

    @property
    def sessions(self):
        self.api = 'sessions'
        self.message = 'Number of open sessions'
        return self._connect

    def sessions_stream(self, stream_name):
        self.api = 'sessions?name={}'.format(stream_name)
        self.message = 'List of open sessions for a specific stream'
        return self._connect

    def stream_health(self, stream_name):
        self.api = 'stream_health/{}'.format(stream_name)
        self.message = 'Stream quality'
        return self._connect

    @property
    def streams(self):
        self.api = 'streams'
        self.message = 'List of streams, clients and state of this streams'
        return self._connect
