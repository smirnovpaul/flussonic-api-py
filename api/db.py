# -*- coding: utf-8 -*-

import mysql

# todo http://erlyvideo.ru/doc/api/sql
# todo basic methods with mysql

class DataBaseApi(object):
    def __init__(self, user, password, host, db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self._cursor = None
        self._connect = None

    def _connect(self):
        pass

    def query(self):
        pass

    def basic(self):
        pass
