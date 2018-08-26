import json
import time
from pymysql.cursors import DictCursor
from sqlbuilder.smartsql import T

from .environment import APPLICATION_DIR, SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase
from . import api


database = SqliteDatabase(SQLITE3_DB)


class CurrencyUnit:
    def on_get(request, response):
        response.json = api.CurrencyUnit.selectall()

class TimeUnit:
    def on_get(request, response):
        response.json = api.TimeUnit.selectall()

class Partner:
    def on_get(request, response, id=None):
        response.json = api.Partner.selectall()

class AccountProduct:
    def on_get(request, response, id=None):
        response.json = api.AccountProduct.selectall(request.params['account_id'])


class Account:
    
    def on_get(request, response):
        response.json = api.Account.selectall()

    def on_post(request, response):
        response.json = api.Account.insertone(request.json)

    class Element:
        def on_get(request, response, id):
            response.json = api.Account.selectone(id, include_products=True)

        def on_put(request, response, id):
            response.json = api.Account.updateone(id, request.json)

        def on_delete(request, response, id):
            response.json = api.Account.deleteone(id)
