from typing import cast

from .database import SqliteDatabase, Database
from .service import printer, number_to_word, mail
from .environment import Environment
from . import api


environment = Environment.get()
database = environment.register.get('database')


bank_service = api.Bank(database)
currency_unit_service = api.CurrencyUnit(database)
time_unit_service = api.TimeUnit(database)
partner_service = api.Partner(database)
account_product_service = api.AccountProduct(database)
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
        response.json = currency_unit_service.selectall()


class TimeUnit:
    @staticmethod
    def on_get(request, response):
        response.json = time_unit_service.selectall()


class Partner:
    @staticmethod
    def on_get(request, response):
        response.json = partner_service.selectall()

    @staticmethod
    def on_post(request, response):
        response.json = partner_service.insertone(request.json)

    class ID:
        @staticmethod
        def on_get(request, response, id):
            response.json = partner_service.selectone(id)

        @staticmethod
        def on_put(request, response, id):
            response.json = partner_service.updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id):
            response.json = partner_service.deleteone(id)


class AccountProduct:
    @staticmethod
    def on_get(request, response, id=None):
        response.json = account_product_service.selectall(request.params['account_id'])


class Account:

    @staticmethod
    def on_get(request, response):
        response.json = account_service.selectall()

    @staticmethod
    def on_post(request, response):
        response.json = account_service.insertone(request.json)

    class ID:
        @staticmethod
        def on_get(request, response, id):
            response.json = account_service.selectone(id)

        @staticmethod
        def on_put(request, response, id):
            response.json = account_service.updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id):
            response.json = account_service.deleteone(id)


class NumberToWord:
    @staticmethod
    def on_get(request, response):
        response.json = number_to_word.number_to_word(
            float(request.params.get('number')),
            number_to_word.ruble,
            number_to_word.kopeck,
        )


class Mail:
    @staticmethod
    def on_post(request, response):

        with mail.Sender(
            environment['smtp']['host'],
            environment['smtp']['port'],
            environment['smtp']['user'],
            environment['smtp']['password'],
            environment['smtp']['ssl'],
        ) as sender:
            sender.send(
                from_address=environment['smtp']['from'],
                to_addresses=request.json['recipients'],
                body=request.json['body'],
                subject=request.json['subject'],
                attachments=mail.Attachment.parse(request.json.get('attachments', [])),
            )


class Report:

    class ID:
        @staticmethod
        def on_get(request, response, entity, entity_id):
            account = account_service.selectone_filled(entity_id)

            if entity == 'account':
                response.body = printer.account_as_pdf(account)
            elif entity == 'act':
                response.body = printer.act_as_pdf(account)
            elif entity == 'invoice':
                response.body = printer.invoice_as_pdf(account)
            else:
                raise NotImplementedError(f'Unknown report type `{entity}`')

            if request.params.get('disposition', None) == 'attachment':
                response.append_header('Content-Disposition', f'attachment; filename="{entity}.pdf"')
            else:
                response.append_header('Content-Disposition', 'inline')

            response.append_header('Content-Type', 'application/pdf')
