from typing import TypeVar, Any, Collection, Dict, Generator, Tuple, Optional
from contextlib import contextmanager
from sqlbuilder import smartsql
from sqlbuilder.smartsql import Q, T, compile, Compiler
from contextvars import ContextVar

from ..logger import getlogger
from ..service import api


logger = getlogger(__name__)
Cursor = Any


class Result(smartsql.Result):
    def __init__(self, compile: Compiler, cursor: Cursor):
        super().__init__(compile)
        self._cursor = cursor

    def execute_fetchnone(self) -> None:
        self._cursor.execute(*self.execute())

    def execute_fetchone(self) -> Dict[str, Any]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchall(self) -> Collection[Dict[str, Any]]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchall()

    def execute_fetchinsertid(self) -> Dict[str, Any]:
        raise NotImplementedError

    def operation(self) -> 'TerminalOperation':
        return TerminalOperation(self)

    delete = update = count = insert = select = operation


class TerminalOperation:
    """ Everyone query that was maked with sqlbuilder
        must terminated with one of thus methods.
    """

    def __init__(self, result: Result):
        self._result = result

    def execute(self) -> None:
        return self._result.execute_fetchnone()

    def fetchone(self) -> Dict[str, Any]:
        return self._result.execute_fetchone()

    def fetchall(self) -> Collection[Dict[str, Any]]:
        return self._result.execute_fetchall()

    def fetchinsertid(self) -> Dict[str, Any]:
        return self._result.execute_fetchinsertid()


class Database:
    """ Common facade for get DB services. """

    @contextmanager
    def cursor(self) -> Generator[Cursor, None, None]:
        raise NotImplementedError

    def result(self, cursor: Cursor) -> Result:
        raise NotImplementedError


class SqlBuilder:
    """ API facade for `sqlbuilder` package. """

    def __init__(self, database: Optional[Database] = None):
        self._database = database

    @contextmanager
    def result(self) -> Generator[Result, None, None]:
        database, cursor = _database.get(), _cursor.get()

        if database is None or cursor is None:
            assert self._database is not None, 'No database instance found'

            with self._database.cursor() as cursor:
                cursor_token = _cursor.set(cursor)
                database_token = _database.set(self._database)
                try:
                    yield self._database.result(cursor)
                except Exception as error:
                    raise error
                finally:
                    _cursor.reset(cursor_token)
                    _database.reset(database_token)
        else:
            yield database.result(cursor)


class Service:

    def __init__(self, database: Optional[Database] = None):
        self._database = database
        self._sqlbuilder = SqlBuilder(database=database)

    @property
    def database(self):
        return self._database

    @property
    def sqlbuilder(self) -> SqlBuilder:
        return self._sqlbuilder


_database: ContextVar[Optional[Database]] = ContextVar('database', default=None)
_cursor: ContextVar[Optional[Cursor]] = ContextVar('cursor', default=None)
