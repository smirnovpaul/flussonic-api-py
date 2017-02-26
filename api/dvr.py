# -*- coding: utf-8 -*-
import requests

from .log import LOGGER


class DvrApi(object):
    """
    Token is a simple method for check.

    http://flussonic.com/doc/dvr/api
    """
    def __init__(self, url, token, stream_name):
        self.payload = None
        self.url = url
        self.stream_name = stream_name
        self.token = token
        self.url = None

    @property
    def __connect(self):
        try:
            r = requests.get(self.url, params=self.payload)
        except requests.RequestException as e:
            LOGGER.error('Error request get: {}'.format(e))
            return None

        try:
            r.raise_for_status()
        except requests.HTTPError as e:
            LOGGER.error('Error request status_code: {}'.format(e))
            return None

        try:
            response = r.json()
        except ValueError as e:
            LOGGER.error('Error request json: {}'.format(e))
            return None
        else:
            return response

    def recording_status(self, from_time, to_time):
        """
        Recording status.

        ARGUMENTS:
            :param from_time
            :param to_time
            :return: json

        EXAMPLE:
        [{
            "stream":"hik2",
            "ranges":[
                {"from":1399917362,"duration":65},
                {"from":1399926545,"duration":102},
                {"from":1399965549,"duration":350}
            ],
            "brief_thumbnails":[
                1399917362,
                1399917373,
                1399917385,
                1399917397,
                1399917409,
                1399917421,
                1399926545
            ]
        }]
        """
        self.payload = {'from': from_time, 'to': to_time, 'token': self.token}
        self.url = 'http://{0}/{1}/recording_status.json'.format(self.url, self.stream_name)
        return self.__connect()

    @property
    def lock(self, from_time, duration):
        """
        Lock to delete from archive.

        ARGUMENTS:
            :param from_time
            :param duration
            :return: json

        EXAMPLE:
        [{
            "stream":"ort",
            "ranges":[
                {"duration":3687,"from":1483970675},
                {"duration":56758,"from":1483974376},
                {"duration":332,"from":1484031143}],
            "locks":[
            {"duration":1004,"from":1483971680}
            ]
        }]
        """
        self.payload = {
            'stream': self.stream_name, 'from': from_time,
            'duration': duration, 'token': self.token
        }
        self.url = 'http://{0}/flussonic/api/dvr/lock'.format(self.url)
        return self.__connect()
