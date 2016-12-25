# -*- coding: utf-8 -*-
import logging
import requests

# Logger: from print to logging
# TODO test to connect


class DvrApi(object):
    """
    http://flussonic.com/doc/dvr/api
    """
    def __init__(self, url, token, stream_name, from_time, to_time):
        self.payload = {'from': from_time, 'to': to_time, 'token': token}
        self.url = 'http://{0}/{1}/recording_status.json'.format(url, stream_name)

    @property
    def get(self):
        try:
            r = requests.get(self.url, params=self.payload)
        except requests.RequestException as e:
            print('Error request get: {}'.format(e))
            return None

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            print('Error request status_code: {}'.format(e))
            return None

        try:
            r.json()
        except ValueError as e:
            print('Error request json: {}'.format(e))
            return None
        else:
            return r.json()
