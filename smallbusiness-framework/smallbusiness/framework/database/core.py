from typing import Type, TypeVar, ContextManager, Any, AnyStr, Sequence, Dict, NewType
from contextlib import contextmanager

from sqlbuilder import smartsql
from sqlbuilder.smartsql import Q, T, compile, Compiler

# Stub for DBAPI cursor type
# Just for code self-documentation
Cursor = Any


class Result(smartsql.Result):
    def __init__(self, compile: Compiler, database: 'Database', cursor: Cursor):
        super().__init__(compile)

        self._database = database
        self._cursor = cursor

    def state(self) -> 'State':
        return State(self._database, self._cursor)

    def execute_fetchnone(self) -> None:
        self._cursor.execute(*self.execute())

    def execute_fetchone(self) -> Dict[AnyStr, Any]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchall(self) -> Sequence[Dict[AnyStr, Any]]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchall()

    def execute_fetchinsertid(self) -> Dict[AnyStr, Any]:
        raise NotImplementedError

    def operation(self) -> 'TerminalOperation':
        return TerminalOperation(self)

    delete = update = count = insert = select = operation


class TerminalOperation:
    """ Everyone query that maked with sqlbuilder
        must terminated with one of thus methods.
    """

    def __init__(self, result: Result):
        self._result = result

    def execute(self) -> None:
        return self._result.execute_fetchnone()

    def fetchone(self) -> Dict[AnyStr, Any]:
        return self._result.execute_fetchone()

    def fetchall(self) -> Sequence[Dict[AnyStr, Any]]:
        return self._result.execute_fetchall()

    def fetchinsertid(self) -> Dict[AnyStr, Any]:
        return self._result.execute_fetchinsertid()


class Database:
    """ Common facade for get some DB services. """

    @contextmanager
    def cursor(self) -> ContextManager[Cursor]:
        raise NotImplementedError

    def result(self, cursor: Cursor) -> Result:
        raise NotImplementedError


class State:
    """ For re-use connection state. """

    def __init__(self, database: Database, cursor: Cursor):
        self._database = database
        self._cursor = cursor

    @property
    def cursor(self) -> Cursor:
        return self._cursor

    @property
    def database(self) -> Database:
        return self._database


class SqlBuilder:
    """ API facade for `sqlbuilder` package. """

    def __init__(self, database: Database = None, state: State = None):

        if database is None and state is None:
            raise ValueError('`database` or `state` must be provide')

        self._database = database
        self._state = state

    @contextmanager
    def result(self) -> ContextManager[Result]:
        if self._state is None:
            with self._database.cursor() as cursor:
                yield self._database.result(cursor)
        else:
            yield self._state.database.result(self._state.cursor)


class Service:

    def __init__(self, database: Database = None, state: State = None):
        self._database = database
        self._sqlbuilder = SqlBuilder(database=database, state=state)

    @property
    def database(self):
        return self._database

    @property
    def sqlbuilder(self) -> SqlBuilder:
        return self._sqlbuilder
