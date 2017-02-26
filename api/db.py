# -*- coding: utf-8 -*-
import logging
import MySQLdb

# Logger: from print to logging


def dictfetchall(cursor):
    """
    Return all rows from a cursor as a dict.
    """
    columns = [col[0] for col in cursor.description]
    return [
        dict(zip(columns, row))
        for row in cursor.fetchall()
    ]


class DataBaseApi(object):
    def __init__(self, user, password, host, db):
        self.user = user
        self.password = password
        self.host = host
        self.db = db
        self._db = None
        self._cursor = None

    def __connect(self):
        try:
            self._db = MySQLdb.connect(
                host=self.host, port=3306,
                user=self.user, passwd=self.password,
                db=self.db, charset='utf8'
            )
        except Exception as ex:
            print('Connection error with host {}, db {} : {2}'.format(self.host, self.db, ex))

    def _get_query(self, query, args):

        result = None
        try:
            self._cursor = self._db.cursor()
            self._cursor.execute(query, args)
            result = dictfetchall(self._cursor)
            self._cursor.close()
        except Exception as ex:
            print('Get query error: query {}; args{}'.format(query, args,  ex))
            return result
        else:
            return result

    def select(self, stream_name, time_for_utc):
        """
        Select all data from table dvr_status.
        http://erlyvideo.ru/doc/api/sql

        DON`T FORGET: name and utc are using only together.

        ARGUMENTS:
            :param stream_name:
            :param time_for_utc:
            :return: dict
        """
        query = """SELECT * FROM dvr_status WHERE name = %s AND utc > %s """
        return self._get_query(query, (stream_name, time_for_utc))
