from typing import cast, Dict, Any
from datetime import datetime
import falcon

from .service.api import endpoint
from .instrument import number2currency
from .service import printer, mail, API
from .service.mail import parse_attachment


@endpoint
class Bank:

    @classmethod
    def on_get(cls, request, response, api, _):
        print(_('Ruble'))
        response.json = api.bank.selectall()

    @staticmethod
    def on_post(request, response, api):
        response.json = api.bank.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        def on_get(request, response, bank_id, api):
            response.json = api.bank.selectone(bank_id)

        @staticmethod
        def on_put(request, response, bank_id, api):
            response.json = api.bank.updateone(bank_id, request.json)

        @staticmethod
        def on_delete(request, response, bank_id, api):
            response.json = api.bank.deleteone(bank_id)


@endpoint
class CurrencyUnit:

    @staticmethod
    def on_get(request, response, api):
        response.json = api.currency_unit.selectall()


@endpoint
class TimeUnit:
    @staticmethod
    def on_get(request, response, api):
        response.json = api.time_unit.selectall()


@endpoint
class Partner:
    @staticmethod
    def on_get(request, response, api):
        response.json = api.partner.selectall()

    @staticmethod
    def on_post(request, response, api):
        response.json = api.partner.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        def on_get(request, response, id, api):
            response.json = api.partner.selectone(id)

        @staticmethod
        def on_put(request, response, id, api):
            response.json = api.partner.updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id, api):
            response.json = api.partner.deleteone(id)


@endpoint
class Security:
    @staticmethod
    def on_get(request, response, api):
        user = api.user.selectone_for_security(
            request.params['login'],
            request.params['password'],
        )

        if user is not None:
            api.security.put(user['login'], request, response)
            response.json = user
        else:
            response.status = falcon.HTTP_401
            response.json = None


@endpoint
class AccountProduct:
    @staticmethod
    def on_get(request, response, api):
        response.json = api.account_product.selectall(request.params['account_id'])


@endpoint
class Account:
    @staticmethod
    def on_get(request, response, context, api):
        response.json = api.account.selectall()

    @staticmethod
    def on_post(request, response, api):
        response.json = api.account.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        def on_get(request, response, id, api):
            response.json = api.account.selectone(id)

        @staticmethod
        def on_put(request, response, id, api):
            response.json = api.account.updateone(id, request.json)

        @staticmethod
        def on_delete(request, response, id, api):
            response.json = api.account.deleteone(id)


@endpoint
class Number2Word:
    @staticmethod
    def on_get(request, response):
        response.json = number2currency(request.params.get('number'), lang='ru', currency='RUB')


@endpoint
class Configuration:
    @staticmethod
    def on_get(request, response, api):
        response.json = api.configuration.selectone()

    @staticmethod
    def on_put(request, response, api):
        response.json = api.configuration.updateone(request.json)


@endpoint
class Mail:
    @staticmethod
    def on_post(request, response, api, settings):
        with mail.Sender(
            settings['smtp']['host'],
            settings['smtp']['port'],
            settings['smtp']['user'],
            settings['smtp']['password'],
            settings['smtp']['ssl'],
        ) as sender:
            sender.send(
                from_address=settings['smtp']['from'],
                to_addresses=request.json['recipients'],
                body=request.json['body'],
                subject=request.json['subject'],
                attachments=mail.parse_attachment(request.json.get('attachments', []), api),
            )


class Report:

    @endpoint
    class ID:
        @staticmethod
        def on_get(request, response, entity, entity_id, api):
            account = api.account.selectone_filled(entity_id)
            account_date = datetime.fromtimestamp(account['date'] / 1000).strftime('%Y_%m_d')

            if entity == 'account':
                response.body = printer.account_as_pdf(account)
            elif entity == 'act':
                response.body = printer.act_as_pdf(account)
            elif entity == 'invoice':
                response.body = printer.invoice_as_pdf(account)
            else:
                raise NotImplementedError(f'Unknown report type `{entity}`')

            if request.params.get('disposition', None) == 'attachment':
                response.append_header(
                    'Content-Disposition',
                    f'attachment; filename="{entity}_no_{entity_id}_from_{account_date}.pdf"'
                )
            else:
                response.append_header('Content-Disposition', 'inline')

            response.append_header('Content-Type', 'application/pdf')
