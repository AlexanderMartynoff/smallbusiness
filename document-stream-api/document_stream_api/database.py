import pymysql
import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects import mysql
from sqlbuilder.smartsql.dialects import sqlite
from contextlib import asynccontextmanager, contextmanager


class Database:
    def __init__(self, compile_):
        self._compile = compile_

    @contextmanager
    def connection(self):
        raise NotImplementedError
    
    @contextmanager
    def cursor(self):
        raise NotImplementedError

    @contextmanager
    def query(self):
        raise NotImplementedError


class SqliteDatabase(Database):
    def __init__(self, database, timeout=None):
        super().__init__(compile_=sqlite.compile)
        
        self._database = database
        self._timeout = timeout

    @contextmanager
    def query(self):
        with sqlite3.connect(self._database) as connection:
            cursor = connection.cursor()

            class Query(_Query):
                def __init__(_self, tables=None, result=None):
                    super().__init__(tables=tables, result=result or Result(compile=self._compile))

                @property
                def _cursor(self):
                    return cursor

            yield Query

            cursor.close()


class MysqlDatabase(Database):

    def __init__(self, parameters):
        super().__init__(parameters, compile_=mysql.compile)

    @contextmanager
    def query(self):
        with pymysql.connect(**self._parameters, cursorclass=self._cursor_type) as cursor:

            class Query(_Query):
                def __init__(_self, tables=None, result=None):
                    super().__init__(tables=tables, result=result or Result(compile=self._compile))

                @property
                def _cursor(self):
                    return cursor

            yield Query


class _Query(Q):

    @property
    def _cursor(self):
        raise NotImplementedError

    def crud(self):
        return Crud(self, self._cursor)


class Crud:
    def __init__(self, query, cursor):
        self._query = query
        self._cursor = cursor

    def selectone(self):
        self._cursor.execute(*self._query.select())
        return self._cursor.fetchone()

    def selectall(self):
        self._cursor.execute(*self._query.select())
        return self._cursor.fetchall()

    def count(self):
        self._cursor.execute(*self._query.count())
        return self._cursor.fetchone()

    def insert(self, *args, **kwargs):
        self._cursor.execute(*self._query.insert(*args, **kwargs))
        return self._cursor.fetchone()

    def update(self):
        self._cursor.execute(*self._query.update(*args, **kwargs))
        return self._cursor.fetchone()

    def delete(self):
        self._cursor.execute(*self._query.delete(*args, **kwargs))
        return self._cursor.fetchone()
