from sqlbuilder.smartsql import expressions, T, Q
from sqlbuilder.smartsql.expressions import func

from .account_product import AccountProduct
from ..database import Service
from ..instrument import groupbycrud


class Account(Service):
    def selectone_filled(self, account_id):

        with self.sqlbuilder.result() as result:
            account = Q(result=result).tables(
                    T.account +
                    T.partner.as_('provider').on(T.account.provider_id == T.provider.id) +
                    T.partner.as_('purchaser').on(T.account.purchaser_id == T.purchaser.id) +
                    T.bank.as_('provider_bank').on(T.provider.bank_id == T.provider_bank.id)
                ) \
                .fields(
                    T.account.id,
                    T.account.currency_unit_id,
                    T.account.reason,
                    T.account.date,
                    T.account.provider_id,
                    T.account.purchaser_id,

                    T.provider.name.as_('provider_name'),
                    T.provider.address.as_('provider_address'),
                    T.provider.taxpayer_number.as_('provider_taxpayer_number'),
                    T.provider.reason_code.as_('provider_reason_code'),
                    T.provider.bank_checking_account.as_('provider_bank_checking_account'),

                    T.purchaser.name.as_('purchaser_name'),
                    T.purchaser.address.as_('purchaser_address'),
                    T.purchaser.taxpayer_number.as_('purchaser_taxpayer_number'),
                    T.purchaser.reason_code.as_('purchaser_reason_code'),
                    T.purchaser.bank_checking_account.as_('purchaser_bank_checking_account'),

                    T.provider_bank.name.as_('provider_bank_name'),
                    T.provider_bank.taxpayer_number.as_('provider_bank_taxpayer_number'),
                    T.provider_bank.identity_code.as_('provider_bank_identity_code'),
                    T.provider_bank.correspondent_account.as_('provider_bank_correspondent_account'),
                    T.provider_bank.reason_code.as_('provider_bank_reason_code'),
                ) \
                .where(T.account.id == account_id) \
                .select() \
                .fetchone()

            if account:
                account.update(products=AccountProduct().selectall(
                    T.account_product.account_id == account_id
                ))

            return account

    def selectone(self, account_id):

        with self.sqlbuilder.result() as result:

            account = Q(result=result) \
                .tables(T.account) \
                .fields(
                    T.account.id,
                    T.account.currency_unit_id,
                    T.account.reason,
                    T.account.date,
                    T.account.provider_id,
                    T.account.purchaser_id,
                ) \
                .where(T.account.id == account_id) \
                .select() \
                .fetchone()

            if account:
                account.update(products=AccountProduct().selectall(
                    T.account_product.account_id == account_id
                ))

            return account

    def selectall(self):
        with self.sqlbuilder.result() as result:

            return Q(result=result) \
                .tables(
                    T.account +
                    T.partner.as_('purchaser').on(T.account.purchaser_id == T.purchaser.id)
                ) \
                .fields(
                    T.account.id,
                    T.account.date,
                    T.purchaser.name.as_('purchaser_name'),
                    (Q().tables(T.account_product)
                        .fields(func.sum(T.account_product.value * T.account_product.price))
                        .where(T.account_product.account_id == T.account.id)
                        .group_by(T.account_product.account_id)
                        .as_('price'))
                ) \
                .select() \
                .fetchall()

    def insertone(self, account):
        with self.sqlbuilder.result() as result:
            created_account = Q(result=result) \
                .tables(T.account) \
                .insert({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.date: account['date'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }) \
                .fetchinsertid()

            if account['products']:
                account_product_api = AccountProduct()

                for product in account['products']:
                    product['account_id'] = created_account['id']

                account_product_api.insertmany(account['products'])

            return created_account

    def updateone(self, account_id, account):

        with self.sqlbuilder.result() as result:
            Q(result=result) \
                .tables(T.account) \
                .where(T.account.id == account_id) \
                .update({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.date: account['date'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }) \
                .execute()

            account_product_api = AccountProduct()

            insert_products, update_products, delete_products = \
                groupbycrud(account.get('products', []), {'account_id': account_id})

            if len(insert_products):
                account_product_api.insertmany(insert_products)

            if len(update_products):
                account_product_api.updatemany(update_products)

            if len(delete_products):
                account_product_api.deletemany(delete_products)

    def deleteone(self, account_id):
        with self.sqlbuilder.result() as result:
            return Q(result=result) \
                .tables(T.account) \
                .where(T.account.id == account_id) \
                .delete() \
                .execute()
