from typing import Type, TypeVar, Generic, ContextManager
import sqlite3
import psycopg2.extras
from contextlib import contextmanager

from sqlbuilder import smartsql
from sqlbuilder.smartsql.dialects import sqlite, mysql
from sqlbuilder.smartsql.factory import factory

from .core import Database, SqlBuilder, Result, Cursor
from ..logger import getlogger


logger = getlogger(__name__)


class SqliteDatabase(Database):

    def __init__(self, database: str):
        self._database = database

    @contextmanager
    def cursor(self) -> ContextManager[Cursor]:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._database) as connection:
            connection.set_trace_callback(logger.debug)
            connection.row_factory = row_factory

            cursor = connection.cursor()

            yield cursor

            cursor.close()

    def result(self, cursor) -> Result:
        return SqliteResult(self, cursor)


class SqliteResult(Result):

    def __init__(self, database: Database, cursor: Cursor):
        super().__init__(sqlite.compile, database, cursor)

    def execute_fetchinsertid(self):
        self._cursor.execute(*self.execute())

        return factory.get(self) \
            .Raw('SELECT LAST_INSERT_ROWID() as id', (), result=self) \
            .select() \
            .fetchone()


class PostgresDatabase(Database):

    def __init__(self, database: str,
                 user: str,
                 password: str = None,
                 port: int = None,
                 host: str = None):

        self._database = database
        self._user = user
        self._password = password
        self._host = host
        self._port = port

    @contextmanager
    def cursor(self) -> ContextManager[Cursor]:
        connection = psycopg2.connect(
            dbname=self._database,
            user=self._user,
            port=self._port,
            password=self._password,
            host=self._host,
        )
        cursor = connection.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

        yield cursor

        connection.commit()
        cursor.close()
        connection.close()

    def result(self, cursor) -> Result:
        return PostgresResult(self, cursor)


class PostgresResult(Result):

    def __init__(self, database: Database, cursor: Cursor):
        super().__init__(smartsql.compile, database, cursor)

    def execute_fetchinsertid(self):
        self._cursor.execute(*self.execute())

        return factory.get(self) \
            .Raw('SELECT LASTVAL() as id', (), result=self) \
            .select() \
            .fetchone()
