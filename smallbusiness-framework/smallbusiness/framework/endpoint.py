from typing import cast, Dict, Any
from datetime import datetime
import falcon

from .instrument import number2currency
from .service import printer, mail
from .service.mail import parse_attachment
from . import security
from .api import api


class Endpoint:

    def __init__(self, api: api.API):
        self._api = api

    @property
    def api(self):
        return self._api

    @property
    def settings(self) -> Dict[str, Any]:
        return self._api.settings


class Bank(Endpoint):

    def on_get(self, request, response):
        response.json = self.api.bank.selectall()

    def on_post(self, request, response):
        response.json = self.api.insertone(request.json)

    class ID(Endpoint):
        def on_get(self, request, response, bank_id):
            response.json = self.api.selectone(bank_id)

        def on_put(self, request, response, bank_id):
            response.json = self.api.updateone(bank_id, request.json)

        def on_delete(self, request, response, bank_id):
            response.json = self.api.deleteone(bank_id)


class CurrencyUnit(Endpoint):
    def on_get(self, request, response):
        response.json = self.api.currency_unit.selectall()


class TimeUnit(Endpoint):
    def on_get(self, request, response):
        response.json = self.api.time_unit.selectall()


class Partner(Endpoint):
    def on_get(self, request, response):
        response.json = self.api.partner.selectall()

    def on_post(self, request, response):
        response.json = self.api.partner.insertone(request.json)

    class ID(Endpoint):
        def on_get(self, request, response, id):
            response.json = self.api.partner.selectone(id)

        def on_put(self, request, response, id):
            response.json = self.api.partner.updateone(id, request.json)

        def on_delete(self, request, response, id):
            response.json = self.api.partner.deleteone(id)


class Security(Endpoint):
    def on_get(self, request, response):

        try:
            pass
        except RuntimeError as error:
            pass
        else:
            self.api.security.remember(request.params['login'], request, response)

        response.status = falcon.HTTP_401


class AccountProduct(Endpoint):
    def on_get(self, request, response):
        response.json = self.api.account_product.selectall(request.params['account_id'])


class Account(Endpoint):

    def on_get(self, request, response):
        response.json = self.api.account.selectall()

    def on_post(self, request, response):
        response.json = self.api.account.insertone(request.json)

    class ID(Endpoint):

        def on_get(self, request, response, id):
            response.json = self.api.account.selectone(id)

        def on_put(self, request, response, id):
            response.json = self.api.account.updateone(id, request.json)

        def on_delete(self, request, response, id):
            response.json = self.api.account.deleteone(id)


class Number2Word(Endpoint):
    def on_get(self, request, response):
        response.json = number2currency(request.params.get('number'), lang='ru', currency='RUB')


class Configuration(Endpoint):
    def on_get(self, request, response):
        response.json = self.api.configuration.selectone()

    def on_put(self, request, response):
        response.json = self.api.configuration.updateone(request.json)


class Mail(Endpoint):
    def on_post(self, request, response):
        with mail.Sender(
            self.settings['smtp']['host'],
            self.settings['smtp']['port'],
            self.settings['smtp']['user'],
            self.settings['smtp']['password'],
            self.settings['smtp']['ssl'],
        ) as sender:
            sender.send(
                from_address=self.settings['smtp']['from'],
                to_addresses=request.json['recipients'],
                body=request.json['body'],
                subject=request.json['subject'],
                attachments=mail.parse_attachment(request.json.get('attachments', []), self.api),
            )


class Report:

    class ID(Endpoint):
        def on_get(self, request, response, entity, entity_id):
            account = self.api.account.selectone_filled(entity_id)
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
