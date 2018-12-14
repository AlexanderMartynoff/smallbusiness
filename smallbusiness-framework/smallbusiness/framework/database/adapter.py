from typing import Type, TypeVar, Generic, ContextManager
import sqlite3
from contextlib import contextmanager
from sqlbuilder.smartsql.dialects import sqlite, mysql

from .core import (
    Database,
    SqlBuilder,
    CursorResult,
    DBAPICursorT
)


class SqliteDatabase(Database):

    def __init__(self, databasename):
        self._databasename = databasename

    @contextmanager
    def cursor(self) -> ContextManager[DBAPICursorT]:

        def row_factory(cursor, row):
            return {name: row[number] for number, (name, *_) in enumerate(cursor.description)}

        with sqlite3.connect(self._databasename) as connection:
            connection.row_factory = row_factory
            cursor = connection.cursor()

            yield cursor

            cursor.close()

    def result(self, cursor) -> CursorResult:
        return SqliteCursorResult(self, cursor)


class SqliteCursorResult(CursorResult):

    def __init__(self, database, cursor):
        super().__init__(sqlite.compile, database, cursor)

    def execute_fetchinsertid(self):
        self._cursor.execute(*self.execute())

        return factory.get(self) \
            .Raw('SELECT LAST_INSERT_ROWID() as id', (), result=self) \
            .select() \
            .fetchone()
