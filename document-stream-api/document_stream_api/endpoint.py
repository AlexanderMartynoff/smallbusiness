import json
import time
from pymysql.cursors import DictCursor
from sqlbuilder.smartsql import T

from .environment import APPLICATION_DIR, SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase
from .service import xslx_report
from . import api


database = SqliteDatabase(SQLITE3_DB)


class Bank:
    def on_get(request, response):
        response.json = api.Bank(database).selectall()


class CurrencyUnit:
    def on_get(request, response):
        response.json = api.CurrencyUnit(database).selectall()


class TimeUnit:
    def on_get(request, response):
        response.json = api.TimeUnit(database).selectall()


class Partner:
    def on_get(request, response):
        response.json = api.Partner(database).selectall()
        
    def on_post(request, response):
        response.json = api.Partner(database).insertone(request.json)

    class ID:
        def on_get(request, response, id):
            response.json = api.Partner(database).selectone(id)

        def on_put(request, response, id):
            response.json = api.Partner(database).updateone(id, request.json)

        def on_delete(request, response, id):
            response.json = api.Partner(database).deleteone(id)


class AccountProduct:
    def on_get(request, response, id=None):
        response.json = api.AccountProduct(database).selectall(request.params['account_id'])


class Account:
    
    def on_get(request, response):
        response.json = api.Account(database).selectall()

    def on_post(request, response):
        response.json = api.Account(database).insertone(request.json)

    class ID:
        def on_get(request, response, id):
            response.json = api.Account(database).selectone(id, include_products=True)

        def on_put(request, response, id):
            response.json = api.Account(database).updateone(id, request.json)

        def on_delete(request, response, id):
            response.json = api.Account(database).deleteone(id)


class Report:

    class ID:
        def on_get(request, response, entity, entity_id, type, format):
            if entity == 'account':
                response.body = xslx_report.general_account(api.Account(database)
                    .selectone(entity_id, include_products=True))
            else:
                raise NotImplementedError

            response.append_header('Content-Type', 'application/vnd.ms-excel')
            response.append_header('Content-Disposition', f'attachment; filename="{entity}-report.xls"')
