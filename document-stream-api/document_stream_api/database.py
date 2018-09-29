import pymysql
import sqlite3

from sqlbuilder.smartsql import Q, T, Result
from sqlbuilder.smartsql.dialects import mysql
from sqlbuilder.smartsql.dialects import sqlite
from contextlib import contextmanager


class Service:

    def __init__(self, database=None, queryclass=None):
        self._database = database
        self._queryclass = queryclass
        self._table = _Table(self, self.__class__.__name__.lower(), 'id')

    @property
    def table(self):
        return self._table

    @contextmanager
    def query(self):
        if self._queryclass is not None:
            yield self._queryclass
        else:
            with self._database.query() as _Q:
                yield _Q


class _Table:

    def __init__(self, service, table_name, id_column_name):
        self._service = service
        self._table_name = table_name
        self._id_column_name = id_column_name

    def selectone(self, id_column_value):

        with self._service.query() as Q:
            return Q().tables(self._table) \
                .fields('*') \
                .where(self._id_column == id_column_value) \
                .crud() \
                .selectone()

    def selectall(self):

        with self._service.query() as Q:
            return Q().tables(self._table) \
                .fields('*') \
                .crud() \
                .selectall()

    @property
    def _table(self):
        return getattr(T, self._table_name)

    @property
    def _id_column(self):
        return getattr(self._table, self._id_column_name)


class _Database:
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


class SqliteDatabase(_Database):
    def __init__(self, database, timeout=None):
        super().__init__(compile=sqlite.compile)

        self._database = database
        self._timeout = timeout

    @contextmanager
    def query(self):

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield _Query.with_context(
                compile=self._compile,
                cursor=cursor,
                crudclass=SqliteCRUD,
                database=self,
            )
            cursor.close()


class _Query(Q):
    def __init__(self, tables=None):
        super().__init__(tables=tables, result=Result(compile=self._compile))

    def crud(self):
        raise NotImplementedError

    @property
    def _compile(self):
        raise NotImplementedError('It is necessary to get the class using `with_context` method')

    @staticmethod
    def with_context(compile, cursor, crudclass, database):

        class Query(_Query):

            @property
            def _compile(self):
                return compile

            @property
            def database(self):
                return database

            def crud(self):
                return crudclass(self, cursor)

        return Query


class CRUD:
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

    def last_insert_id(self):
        raise NotImplementedError


class SqliteCRUD(CRUD):
    def last_insert_id(self):
        self._cursor.execute(*self._query.raw('SELECT LAST_INSERT_ROWID() as id').select())
        return self._cursor.fetchone()
