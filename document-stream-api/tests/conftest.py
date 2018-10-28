import pytest
from collections import deque
from sqlbuilder import smartsql
from document_stream_api.database import Query, Crud, Database


@pytest.fixture
def cursor_cls():

    class Cursor:

        def __init__(self, fetchone_factory=lambda: ..., fetchall_factory=lambda: ...):
            self.arraysize = None

            self._response_history = deque(maxlen=100)
            self._query_history = deque(maxlen=100)

            self._fetchone_factory = fetchone_factory
            self._fetchall_factory = fetchall_factory

        @property
        def description(self):
            pass

        @property
        def rowcount(self):
            pass

        def callproc(self, name, parameters=None):
            pass

        def close(self):
            pass

        def execute(self, operation, parameters=None):
            self._query_history.appendleft((operation, parameters))

        def executemany(self, operation, parameters=None):
            pass

        def fetchone(self):
            self._response_history.appendleft(self._fetchone_factory())
            return self.get_fetched(0)

        def fetchmany(self, size=None):
            pass

        def fetchall(self):
            self._response_history.appendleft(self._fetchall_factory())
            return self.get_fetched(0)

        def nextset(self):
            pass

        def setinputsizes(self, sizes):
            pass

        def setoutputsize(self, sizes, column=None):
            pass

        def get_executed(self, index):
            if len(self._query_history) == 0:
                return None

            return self._query_history[index]

        def get_fetched(self, index):
            return self._response_history[index]

    return Cursor


@pytest.fixture
def query(cursor_cls):
    return Query.implement(smartsql.compile, Crud, cursor_cls(), Database)
