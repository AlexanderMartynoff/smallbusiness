from typing import Type, TypeVar, Generic
from contextlib import contextmanager
import sqlite3

from sqlbuilder.smartsql import Q, T, Result, compile
from sqlbuilder.smartsql.dialects import sqlite

# NOTE: make `_atom_camel_to_snake` more independent, move from `.addon.falcon`
from .addon.falcon import _atom_camel_to_snake


QueryT = TypeVar('QueryT', bound='Query')
BaseQueryT = TypeVar('BaseQueryT', bound='Q')


class Query(Q):
    def __init__(self, tables=None):
        super().__init__(tables=tables, result=Result(compile=self._compile))

    @property
    def _compile(self):
        raise NotImplementedError('It is necessary to get the class using `implement` method')

    def crud(self):
        raise NotImplementedError

    @staticmethod
    def implement(compile, cursor, crudclass, database) -> Type[QueryT]:

        class ContextQuery(Query):

            @property
            def _compile(self):
                return compile

            @property
            def database(self):
                return database

            def crud(self):
                return crudclass(self, cursor)

        return ContextQuery


class Database:
    def __init__(self, compile):
        self._compile = compile

    @contextmanager
    def query(self) -> QueryT:
        raise NotImplementedError


class SqliteDatabase(Database):
    def __init__(self, database, timeout=None):
        super().__init__(compile=sqlite.compile)

        self._database = database
        self._timeout = timeout

    @contextmanager
    def query(self) -> QueryT:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield Query.implement(
                compile=self._compile,
                cursor=cursor,
                crudclass=SqliteCrud,
                database=self,
            )
            cursor.close()


class Crud:
    def __init__(self, query: BaseQueryT, cursor):
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


class SqliteCrud(Crud):
    def last_insert_id(self):
        self._cursor.execute(*self._query.raw('SELECT LAST_INSERT_ROWID() as id').select())
        return self._cursor.fetchone()


class Service:

    def __init__(self, database: Database = None,
                 queryclass: Type[QueryT] = None):
        self._database = database
        self._queryclass = queryclass

    @contextmanager
    def query(self):
        if self._queryclass is not None:
            yield self._queryclass
        else:
            with self._database.query() as ContextQuery:
                yield ContextQuery
