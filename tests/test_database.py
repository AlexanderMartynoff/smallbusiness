import pytest
from sqlbuilder.smartsql import Q, T, Result, compile

from document_stream_api.database import Query, Crud, SqliteCrud, Database


@pytest.fixture
def abstract_crud(cursor_cls):
    return Crud(Q(), cursor_cls(
        fetchone_factory=lambda: {},
        fetchall_factory=lambda: [],
    ))


@pytest.fixture
def sqlite_crud(cursor_cls):
    return SqliteCrud(Q(), cursor_cls(
        fetchone_factory=lambda: {},
        fetchall_factory=lambda: [],
    ))


def test_crud_selectone(abstract_crud):
    abstract_crud.selectone()

    assert abstract_crud._cursor.get_executed(0) == abstract_crud._query.select()
    assert abstract_crud._cursor.get_fetched(0) == {}


def test_crud_selectall(abstract_crud):
    abstract_crud.selectall()

    assert abstract_crud._cursor.get_executed(0) == abstract_crud._query.select()
    assert abstract_crud._cursor.get_fetched(0) == []


def test_crud_count(abstract_crud):
    abstract_crud.count()

    assert abstract_crud._cursor.get_executed(0) == abstract_crud._query.count()
    assert abstract_crud._cursor.get_fetched(0) == {}


def test_crud_sqlite_insert(sqlite_crud):
    sqlite_crud.insert({T.table.column: None})

    assert sqlite_crud._cursor.get_executed(1) == sqlite_crud._query.insert({T.table.column: None})
    assert sqlite_crud._cursor.get_executed(0) == ('SELECT LAST_INSERT_ROWID() as id', [])
    assert sqlite_crud._cursor.get_fetched(0) == {}
