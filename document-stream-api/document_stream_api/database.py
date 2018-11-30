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


class Executor:

    def __init__(self, cursor, compile):
        self._cursor = cursor
        self._compile = compile

    def fetchone(self):
        return self._cursor.fetchone()

    def fetchall(self, query):
        return self._cursor.fetchall()

    def execute(self, query):
        return self._cursor.execute(*query)


    @property
    def result(self):
        return Result(compile=self._compile)


class Database:

    @contextmanager
    def result(self) -> Result:
        raise NotImplementedError


class SqliteDatabase(Database):

    def __init__(self, database):
        self._database = database

    @contextmanager
    def executor(self) -> Executor:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield Executor(cursor=cursor, compile=sqlite.compile)

            cursor.close()


class Service:

    def __init__(self, database: Database = None, result: Result = None):
        self._database = database
        self._result = result

    @contextmanager
    def executor(self):
        with self._database.executor() as executor:
            yield executor
