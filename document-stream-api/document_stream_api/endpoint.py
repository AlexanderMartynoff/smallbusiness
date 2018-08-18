import json
import time
from pymysql.cursors import DictCursor
from sqlbuilder.smartsql import T

from .environment import APPLICATION_DIR, SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase
from .extension.json import JSONEncoder


database = SqliteDatabase(SQLITE3_DB)


class Account:
    def on_get(request, response, id=None):
        with database.query() as Q:
            query = Q().tables(T.account).fields(T.account.id, T.account.name)

            if id:
                response.json = query.where(T.account.id == id).crud().selectone()
            else:
                response.json = query.crud().selectall()

    def on_post(request, response):
        with database.query() as Q:
            account_id = (Q()
                .tables(T.account)
                .crud()
                .insert({
                    'name': request.json.get('name', None),
                    'currency': request.json.get('currency', None),
                    'reason': request.json.get('reason', None)
                }))

        response.json = account_id

    def on_put(request, response, id):
        with database.query() as Q:
            (Q().tables(T.account)
                .where(T.account.id == id)
                .crud()
                .update({
                    'name': request.json.get('name', None),
                    'currency': request.json.get('currency', None),
                    'reason': request.json.get('reason', None)
                }))

    def on_delete(request, response, id):
        with database.query() as Q:
            (Q().tables(T.account)
                .where(T.account.id == id)
                .crud()
                .delete())
