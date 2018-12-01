from typing import Type, TypeVar, Generic, ContextManager
from contextlib import contextmanager
import sqlite3

from sqlbuilder.smartsql import Q, T, Result, compile
from sqlbuilder.smartsql.dialects import sqlite, mysql
from sqlbuilder.smartsql.factory import factory

# NOTE: make `_atom_camel_to_snake` more independent, move from `.addon.falcon`
from .addon.falcon import _atom_camel_to_snake


QueryT = TypeVar('QueryT', bound='Query')
BaseQueryT = TypeVar('BaseQueryT', bound='Q')


class CursorResult(Result):
    def __init__(self, compile, cursor):
        super().__init__(compile)
        self._cursor = cursor

    def terminal(self):
        return CursorResultTeminalOperation(self)

    delete = update = count = insert = select = terminal

    def execute_fetchnone(self):
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchone(self):
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchall(self):
        self._cursor.execute(*self.execute())
        return self._cursor.fetchall()

    def execute_fetchinsertid(self):
        raise NotImplementedError


class SqliteCursorResult(CursorResult):

    def execute_fetchinsertid(self):
        self._cursor.execute(*self.execute())

        return factory.get(self) \
            .Raw('SELECT LAST_INSERT_ROWID() as id', (), result=self) \
            .select() \
            .fetchone()


class CursorResultTeminalOperation:
    def __init__(self, result: CursorResult):
        self._result = result

    def execute(self):
        return self._result.execute_fetchnone()

    def fetchone(self):
        return self._result.execute_fetchone()

    def fetchall(self):
        return self._result.execute_fetchall()

    def fetchinsertid(self):
        return self._result.execute_fetchinsertid()


class Database:

    @contextmanager
    def result(self) -> ContextManager[CursorResult]:
        raise NotImplementedError


class SqliteDatabase(Database):

    def __init__(self, database):
        self._database = database

    @contextmanager
    def result(self) -> ContextManager[CursorResult]:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield SqliteCursorResult(compile=sqlite.compile, cursor=cursor)

            cursor.close()


class Service:

    def __init__(self, database: Database = None, result: Result = None):
        self._database = database
        self._result = result

    @contextmanager
    def result(self):
        if self._result is None:
            with self._database.result() as result:
                yield result
        else:
            yield self._result
