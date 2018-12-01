from sqlbuilder.smartsql import T, Q
from sqlbuilder.smartsql.expressions import func

from ..database import Service
from ..shortcut import group_by_operations
from .account_product import AccountProduct


class Account(Service):

    def selectone_filled(self, account_id):
        with self.result() as result:
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
                account.update(products=AccountProduct(result=result).selectall(
                    T.account_product.account_id == account_id
                ))

            return account

    def selectone(self, account_id):

        with self.result() as result:

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
                account.update(products=AccountProduct(result=result).selectall(
                    T.account_product.account_id == account_id
                ))

            return account

    def selectall(self):
        with self.result() as result:
            return Q(result=result) \
                .tables(T.account) \
                .fields(
                    T.account.id,
                    T.account.date,
                ) \
                .select() \
                .fetchall()

    def insertone(self, account):
        with self.result() as result:
            return Q(result=result) \
                .tables(T.account) \
                .insert({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.date: account['date'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }) \
                .fetchinsertid()

    def updateone(self, account_id, account):

        with self.result() as result:
            Q(result=result).tables(T.account) \
                .where(T.account.id == account_id) \
                .update({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.date: account['date'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }) \
                .execute()

            account_product_api = AccountProduct(result=result)

            insert_products, update_products, delete_products = \
                group_by_operations(account['products'], {'account_id': account_id})

            if len(insert_products):
                account_product_api.insertmany(insert_products)

            if len(update_products):
                account_product_api.updatemany(update_products)

            if len(delete_products):
                account_product_api.deletemany(delete_products)

    def deleteone(self, account_id):
        with self.result() as result:
            return Q(result=result) \
                .tables(T.account) \
                .where(T.account.id == account_id) \
                .delete() \
                .execute()
