import pymysql
import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects import mysql
from sqlbuilder.smartsql.dialects import sqlite
from contextlib import asynccontextmanager, contextmanager


class Database:
    def __init__(self, compile):
        self._compile = compile

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
        super().__init__(compile=sqlite.compile)
        
        self._database = database
        self._timeout = timeout

    @contextmanager
    def query(self):
        with sqlite3.connect(self._database) as connection:
            connection.row_factory = sqlite3.Row
            cursor = connection.cursor()

            yield _Query.with_context(
                compile=self._compile,
                cursor=cursor,
                crudclass=SqliteCrud
            )
            cursor.close()


class MysqlDatabase(Database):

    def __init__(self, parameters):
        super().__init__(parameters, compile=mysql.compile)

    @contextmanager
    def query(self):
        with pymysql.connect(**self._parameters, cursorclass=self._cursor_type) as cursor:
            yield _Query.with_context(
                compile=self._compile,
                cursor=cursor,
                crudclass=MysqlCrud
            )


class _Query(Q):
    def __init__(self, tables=None):
        super().__init__(tables=tables, result=Result(compile=self._compile))

    def crud(self):
        raise NotImplementedError

    @property
    def _compile(self):
        raise NotImplementedError('It is necessary to get the class using `with_conext` method')

    @staticmethod
    def with_context(compile, cursor, crudclass):
        
        class Query(_Query):

            @property
            def _compile(self):
                return compile

            def crud(self):
                return crudclass(self, cursor)

        return Query


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
        return self.last_insert_id()

    def update(self, *args, **kwargs):
        self._cursor.execute(*self._query.update(*args, **kwargs))
        return self._cursor.fetchone()

    def delete(self):
        self._cursor.execute(*self._query.delete())
        return self._cursor.fetchone()

    def execute(self, code):
        self._cursor.execute(code)
        return self._cursor.fetchone()

    def last_insert_id(self):
        # DOIT: replace with: (Q().call('LAST_INSERT_ROWID').crud().selectone())
        raise NotImplementedError


class SqliteCrud(Crud):
    def last_insert_id(self):
        return self.execute('SELECT LAST_INSERT_ROWID()')


class MysqlCrud(Crud):
    def last_insert_id(self, name):
        return self.execute('SELECT LAST_INSERT_ID()')
