from typing import cast, Dict, Any
from datetime import datetime
import falcon

from .service.api import endpoint
from .instrument import number2currency
from .service import printer, mail
from .service.mail import parse_attachment


class Bank:
    @endpoint
    def on_get(request, response, api):
        response.json = api.bank.selectall()

    @endpoint
    def on_post(request, response, api):
        response.json = api.bank.insertone(request.json)

    class ID:
        @endpoint
        def on_get(request, response, bank_id, api):
            response.json = api.bank.selectone(bank_id)

        @endpoint
        def on_put(request, response, bank_id, api):
            response.json = api.bank.updateone(bank_id, request.json)

        @endpoint
        def on_delete(request, response, bank_id, api):
            response.json = api.bank.deleteone(bank_id)


class CurrencyUnit:
    @endpoint
    def on_get(request, response, api):
        response.json = api.currency_unit.selectall()


class TimeUnit:
    @endpoint
    def on_get(request, response, api):
        response.json = api.time_unit.selectall()


class Partner:
    @endpoint
    def on_get(request, response, api):
        response.json = api.partner.selectall()

    @endpoint
    def on_post(request, response, api):
        response.json = api.partner.insertone(request.json)

    class ID:
        @endpoint
        def on_get(request, response, id, api):
            response.json = api.partner.selectone(id)

        @endpoint
        def on_put(request, response, id, api):
            response.json = api.partner.updateone(id, request.json)

        @endpoint
        def on_delete(request, response, id, api):
            response.json = api.partner.deleteone(id)


class Security:
    @endpoint
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


class AccountProduct:
    @endpoint
    def on_get(request, response, api):
        response.json = api.account_product.selectall(request.params['account_id'])


class Account:

    @endpoint
    def on_get(request, response, context, api):
        response.json = api.account.selectall()

    @endpoint
    def on_post(request, response, api):
        response.json = api.account.insertone(request.json)

    class ID:
        @endpoint
        def on_get(request, response, id, api):
            response.json = api.account.selectone(id)

        @endpoint
        def on_put(request, response, id, api):
            response.json = api.account.updateone(id, request.json)

        @endpoint
        def on_delete(request, response, id, api):
            response.json = api.account.deleteone(id)


class Number2Word:
    @endpoint
    def on_get(request, response):
        response.json = number2currency(request.params.get('number'), lang='ru', currency='RUB')


class Configuration:
    @endpoint
    def on_get(request, response, api):
        response.json = api.configuration.selectone()

    @endpoint
    def on_put(request, response, api):
        response.json = api.configuration.updateone(request.json)


class Mail:
    @endpoint
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

    class ID:
        @endpoint
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
