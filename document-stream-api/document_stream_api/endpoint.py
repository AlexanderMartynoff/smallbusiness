from .environment import SQLITE3_DB
from .database import SqliteDatabase
from .service import printer, number_to_word
from . import api


database = SqliteDatabase(SQLITE3_DB)

bank_service = api.Bank(database)
account_service = api.Account(database)


class Bank:
    @staticmethod
    def on_get(request, response):
        response.json = bank_service.selectall()

    @staticmethod
    def on_post(request, response):
        response.json = bank_service.insertone(request.json)

    class ID:
        @staticmethod
        def on_get(request, response, bank_id):
            response.json = bank_service.selectone(bank_id)

        @staticmethod
        def on_put(request, response, bank_id):
            response.json = bank_service.updateone(bank_id, request.json)

        @staticmethod
        def on_delete(request, response, bank_id):
            response.json = bank_service.deleteone(bank_id)


class CurrencyUnit:
    @staticmethod
    def on_get(request, response):
        response.json = api.CurrencyUnit(database).selectall()


class TimeUnit:
    @staticmethod
    def on_get(request, response):
        response.json = api.TimeUnit(database).selectall()


class Partner:
    @staticmethod
    def on_get(request, response):
        response.json = api.Partner(database).selectall()

    @staticmethod
    def on_post(request, response):
        response.json = api.Partner(database).insertone(request.json)

    class ID:
        @staticmethod
        def on_get(request, response, id):
            response.json = api.Partner(database).selectone(id)

        @staticmethod
        def on_put(request, response, id):
            response.json = api.Partner(database).updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id):
            response.json = api.Partner(database).deleteone(id)


class AccountProduct:
    @staticmethod
    def on_get(request, response, id=None):
        response.json = api.AccountProduct(database).selectall(request.params['account_id'])


class Account:

    @staticmethod
    def on_get(request, response):
        response.json = api.Account(database).table.selectall()

    @staticmethod
    def on_post(request, response):
        response.json = api.Account(database).insertone(request.json)

    class ID:
        @staticmethod
        def on_get(request, response, id):
            response.json = api.Account(database).selectone(id)

        @staticmethod
        def on_put(request, response, id):
            response.json = api.Account(database).updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id):
            response.json = api.Account(database).deleteone(id)


class NumberToWord:
    @staticmethod
    def on_get(request, response):
        response.json = number_to_word.number_to_word(
            request.params.get('number'),
            number_to_word.ruble,
            number_to_word.kopeck,
        )


class Report:

    class ID:
        @staticmethod
        def on_get(request, response, entity, entity_id):
            if entity == 'account':
                response.body = printer.account_as_pdf(account_service.selectone_filled(entity_id))
            elif entity == 'act':
                response.body = printer.act_as_pdf(account_service.selectone_filled(entity_id))
            elif entity == 'invoice':
                response.body = printer.invoice_as_pdf(account_service.selectone_filled(entity_id))
            else:
                raise NotImplementedError(f'Unknown report type - {entity}')

            if request.params.get('disposition', 'inline') == 'attachment':
                response.append_header('Content-Disposition', f'attachment; filename="{entity}.pdf"')
            else:
                response.append_header('Content-Disposition', 'inline')

            response.append_header('Content-Type', 'application/pdf')
