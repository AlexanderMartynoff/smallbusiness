from pymysql.cursors import DictCursor
from sqlbuilder.smartsql import T
import json

from .environment import APPLICATION_DIR, SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase


database = SqliteDatabase(SQLITE3_DB)


class Account:
    def on_get(request, response):
        with database.query() as Q:
            response.body = json.dumps(Q()
                .tables(T.account)
                .fields(T.account.id, T.account.name)
                .crud()
                .selectall())

    def on_post(request, response):
        response.body = json.dumps(Q()
            .tables(T.account)
            .fields(T.account.id, T.account.name)
            .crud()
            .selectall())

    def on_put(request, response):
        print('PUT')
        print(request)
