from typing import cast, Dict, Any
from datetime import datetime
import falcon
from falcon.errors import HTTPUnauthorized
from enum import Enum
import time
from datetime import datetime
from collections import namedtuple

from .service.api import endpoint
from .service.authorization import permission
from .instrument import number2currency
from .service import printer, mail, API
from .service.mail import parse_attachment
from .i18n import Translator
from .security import haspermission


@endpoint
class Security:
    @staticmethod
    def on_get(request, response, api):
        login = request.params.get('login', None)
        password = request.params.get('password', None)

        if not login or not password:
            raise HTTPUnauthorized()

        user = api.user.selectone_by_pair(login, password)

        if user is not None:
            api.security.put_context(user, request, response)
        else:
            raise HTTPUnauthorized()


@endpoint
class Session:
    @staticmethod
    @haspermission(permission.session.read)
    def on_get(request, response, api):
        response.json = api.security.get_context(request, response)


@endpoint
class Bank:

    @staticmethod
    @haspermission(permission.bank.read)
    def on_get(request, response, api):
        response.json = api.bank.selectall()

    @staticmethod
    @haspermission(permission.bank.write)
    def on_post(request, response, api):
        response.json = api.bank.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        @haspermission(permission.bank.read)
        def on_get(request, response, bank_id, api):
            response.json = api.bank.selectone(bank_id)

        @staticmethod
        @haspermission(permission.bank.update)
        def on_put(request, response, bank_id, api):
            response.json = api.bank.updateone(bank_id, request.json)

        @staticmethod
        @haspermission(permission.bank.delete)
        def on_delete(request, response, bank_id, api):
            response.json = api.bank.deleteone(bank_id)


@endpoint
class CurrencyUnit:

    @staticmethod
    @haspermission(permission.currencyunit.read)
    def on_get(request, response, api):
        response.json = api.currency_unit.selectall()


@endpoint
class TimeUnit:
    @staticmethod
    @haspermission(permission.timeunit.read)
    def on_get(request, response, api):
        response.json = api.time_unit.selectall()


@endpoint
class Partner:
    @staticmethod
    @haspermission(permission.partner.read)
    def on_get(request, response, api):
        response.json = api.partner.selectall()

    @staticmethod
    @haspermission(permission.partner.write)
    def on_post(request, response, api):
        response.json = api.partner.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        @haspermission(permission.partner.read)
        def on_get(request, response, id, api):
            response.json = api.partner.selectone(id)

        @staticmethod
        @haspermission(permission.partner.update)
        def on_put(request, response, id, api):
            response.json = api.partner.updateone(id, request.json)

        @staticmethod
        @haspermission(permission.partner.delete)
        def on_delete(request, response, id, api):
            response.json = api.partner.deleteone(id)


@endpoint
class AccountProduct:
    @staticmethod
    @haspermission(permission.accountproduct.read)
    def on_get(request, response, api):
        response.json = api.account_product.selectall(request.params['account_id'])


@endpoint
class Account:
    @staticmethod
    @haspermission(permission.account.read)
    def on_get(request, response, context, api):
        response.json = api.account.selectall()

    @staticmethod
    @haspermission(permission.account.write)
    def on_post(request, response, api):
        response.json = api.account.insertone(request.json)

    @endpoint
    class ID:
        @staticmethod
        @haspermission(permission.account.read)
        def on_get(request, response, id, api):
            response.json = api.account.selectone(id)

        @staticmethod
        @haspermission(permission.account.update)
        def on_put(request, response, id, api):
            response.json = api.account.updateone(id, request.json)

        @staticmethod
        @haspermission(permission.account.delete)
        def on_delete(request, response, id, api):
            response.json = api.account.deleteone(id)


@endpoint
class Number2Word:
    @staticmethod
    @haspermission(permission.number2word.read)
    def on_get(request, response):
        response.json = number2currency(request.params.get('number'), lang='ru', currency='RUB')


@endpoint
class Configuration:
    @staticmethod
    @haspermission(permission.configuration.read)
    def on_get(request, response, api):
        response.json = api.configuration.selectone()

    @staticmethod
    @haspermission(permission.configuration.update)
    def on_put(request, response, api):
        response.json = api.configuration.updateone(request.json)


@endpoint
class Mail:
    @staticmethod
    @haspermission(permission.mail.write)
    def on_post(request, response, api, settings, i18n):
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
                attachments=mail.parse_attachment(request.json.get('attachments', []), api, i18n),
            )


class Report:

    @endpoint
    class ID:
        @staticmethod
        @haspermission(permission.mail.read)
        def on_get(request, response, entity, entity_id, api, i18n: Translator):
            account = api.account.selectone_filled(entity_id)
            account_date = datetime.fromtimestamp(account['date'] / 1000).strftime('%Y_%m_d')

            if entity == 'account':
                response.body = printer.account_as_pdf(account, i18n)
            elif entity == 'act':
                response.body = printer.act_as_pdf(account, i18n)
            elif entity == 'invoice':
                response.body = printer.invoice_as_pdf(account, i18n)
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
