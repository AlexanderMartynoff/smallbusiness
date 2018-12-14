from typing import Type, TypeVar, ContextManager, Any, AnyStr, Sequence, Dict
from contextlib import contextmanager

from sqlbuilder.smartsql import Q, T, Result, compile, Compiler
from sqlbuilder.smartsql.factory import factory


DBAPICursorT = TypeVar('DBAPICursorT', bound=Any)


class CursorResult(Result):
    def __init__(self, compile, database, cursor):
        super().__init__(compile)

        self._database = database
        self._cursor = cursor

    def execute_fetchnone(self) -> None:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchone(self) -> Dict[AnyStr, Any]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchone()

    def execute_fetchall(self) -> Sequence[Dict[AnyStr, Any]]:
        self._cursor.execute(*self.execute())
        return self._cursor.fetchall()

    def execute_fetchinsertid(self) -> Dict[AnyStr, Any]:
        raise NotImplementedError

    def operation(self) -> 'CursorResultOperation':
        return CursorResultOperation(self)

    def context(self) -> 'ServiceContext':
        return ServiceContext(self._database, self._cursor)

    delete = update = count = insert = select = operation


class CursorResultOperation:
    def __init__(self, result: CursorResult):
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
    def cursor(self) -> ContextManager[DBAPICursorT]:
        raise NotImplementedError

    def result(self, cursor: DBAPICursorT) -> CursorResult:
        raise NotImplementedError


class SqlBuilder:
    """ API for `sqlbuilder` package. """

    def __init__(self, database: Database = None, context: 'ServiceContext' = None):
        self._database = database
        self._context = context

    @contextmanager
    def result(self) -> ContextManager[CursorResult]:
        if self._context is None:
            with self._database.cursor() as cursor:
                yield self._database.result(cursor)
        else:
            yield self._context.database.result(self._context.cursor)

    @property
    def cursor(self):
        return self._cursor


class ServiceContext:
    """ For reuse service state. """

    def __init__(self, database: Database, cursor: DBAPICursorT):
        self._database = database
        self._cursor = cursor

    @property
    def cursor(self) -> DBAPICursorT:
        return self._cursor

    @property
    def database(self) -> Database:
        return self._database


class Service:

    def __init__(self, database: Database = None,
                 context: ServiceContext = None):
        self._sqlbuilder = SqlBuilder(database=database, context=context)

    @property
    def sqlbuilder(self) -> SqlBuilder:
        return self._sqlbuilder
