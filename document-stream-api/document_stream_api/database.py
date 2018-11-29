from typing import Type, TypeVar, Generic
from contextlib import contextmanager
import sqlite3

from sqlbuilder.smartsql import Q, T, Result, compile
from sqlbuilder.smartsql.dialects import sqlite, mysql
from sqlbuilder.smartsql.factory import factory

# NOTE: make `_atom_camel_to_snake` more independent, move from `.addon.falcon`
from .addon.falcon import _atom_camel_to_snake


QueryT = TypeVar('QueryT', bound='Query')
BaseQueryT = TypeVar('BaseQueryT', bound='Q')


class DbResultOperation:

    def __init__(self, cursor, result):
        self._cursor = cursor
        self._result = result

    def one(self):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError


class DbResult(Result):
    def __init__(self, cursor, compile):
        super().__init__(compile)
        self.cursor = cursor


class SqliteDbResultOperation:

    def one(self):
        raise NotImplementedError

    def all(self):
        raise NotImplementedError


class SqliteDbResult(DbResult):

    compile = sqlite.compile

    def select(self):
        return SqliteDbResultOperation(self._cursor, self)

    def count(self):
        return self.execute()

    def insert(self):
        return self.execute()

    def update(self):
        return self.execute()

    def delete(self):
        return self.execute()


class SqliteCrudOperation(AbstractCrudOperation):

    def one(self):
        self._cursor.execute(*self._result.execute())
        return self._cursor.fetchone()


class Database:

    @contextmanager
    def result(self) -> Result:
        raise NotImplementedError


class SqliteDatabase(Database):

    def __init__(self, database):
        self._database = database

    @contextmanager
    def result(self) -> Result:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield SqliteDbResult(cursor=cursor)

            cursor.close()


class Service:

    def __init__(self, database: Database = None, result: Result = None):
        self._database = database
        self._result = result

    @contextmanager
    def result(self):
        with self._database.result() as result:
            yield result
