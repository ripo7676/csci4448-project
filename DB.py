import pymysql
from interface import implements
from DBInterface import *

class DB(implements(DBInterface)):
    def __init__(self):
        try:
            self.connection = pymysql.connect(host='127.0.0.1', port=3306, user='root', password='root', db='gbar')
            self.cursor = self.connection.cursor()
        except pymysql.err.OperationalError:
            self.connection = None
            self.cursor = None


    def executeInsertionQuery(self, query):
        if (self.connection is not None) and (self.cursor is not None):
            try:
                self.cursor.execute(query)
                self.connection.commit()
            except pymysql.err.ProgrammingError:
                pass

    def executeSelectionQuery(self, query):
        if (self.connection is not None) and (self.cursor is not None):
            results = []
            try:
                self.cursor.execute(query)

                data = self.cursor.fetchone()
                while (data is not None):
                    results.append(data)
                    data = self.cursor.fetchone()

            except pymysql.err.ProgrammingError:
                pass

            return results
