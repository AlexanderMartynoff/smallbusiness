import json
import time
from pymysql.cursors import DictCursor

from .environment import APPLICATION_DIR, SQLITE3_DB
from .database import SqliteDatabase
from .service import printer, number_to_word
from .addon.falcon import Request
from . import api


database = SqliteDatabase(SQLITE3_DB)


class Bank:
    def on_get(request, response):
        response.json = api.Bank(database).selectall()

    def on_post(request, response):
        response.json = api.Bank(database).insertone(request.json)

    class ID:
        def on_get(request, response, bank_id):
            response.json = api.Bank(database).selectone(bank_id)

        def on_put(request, response, bank_id):
            response.json = api.Bank(database).updateone(bank_id, request.json)

        def on_delete(request, response, bank_id):
            response.json = api.Bank(database).deleteone(bank_id)


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
        response.json = api.Account(database).table.selectall()

    def on_post(request, response):
        response.json = api.Account(database).insertone(request.json)

    class ID:
        def on_get(request, response, id):
            response.json = api.Account(database).table.selectone(id)

        def on_put(request, response, id):
            response.json = api.Account(database).updateone(id, request.json)

        def on_delete(request, response, id):
            response.json = api.Account(database).deleteone(id)


class NumberToWord:
    def on_get(request, response):
        response.json = number_to_word.number_to_word(
            request.params.get('number'),
            number_to_word.ruble,
            number_to_word.kopeck,
        )


class Report:

    class ID:
        def on_get(request, response, entity, entity_id, type, format):
            if entity == 'account':
                response.body = printer.account_as_pdf(
                    api.Account(database).selectone(entity_id))
            else:
                raise NotImplementedError

            response.append_header('Content-Type', 'application/pdf')
