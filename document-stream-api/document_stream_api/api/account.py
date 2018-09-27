from sqlbuilder.smartsql import T

from ..database import Service
from .account_product import AccountProduct


class Account(Service):

    def selectone(self, account_id, include_products=False):
        with self.query() as Q:
            account = \
                (Q().tables(T.account)
                    .fields(
                        T.account.id,
                        T.account.currency_unit_id,
                        T.account.reason,
                        T.account.date,
                        T.account.provider_id,
                        T.account.purchaser_id,
                    )
                    .where(T.account.id == account_id)
                    .crud()
                    .selectone())

            if not account:
                return

            if include_products:
                account.update(products=AccountProduct(queryclass=Q).selectall(account_id=account_id))

            return account

    def selectall(self, include_products=False):
        with self.query() as Q:
            accounts = \
                (Q().tables(T.account)
                    .fields(
                        T.account.id,
                        T.account.reason,
                        T.account.date,
                    )
                    .crud()
                    .selectall())

            if include_products:
                for account in accounts:
                    account.update(products=AccountProduct(queryclass=Q).selectall(account_id=account['id']))

            return accounts

    def insertone(self, account):
        with self.query() as Q:
            account_id = \
                (Q().tables(T.account)
                    .crud()
                    .insert({
                        T.account.currency_unit_id: account['currency_unit_id'],
                        T.account.reason: account['reason'],
                        T.account.provider_id: account['provider_id'],
                        T.account.purchaser_id: account['purchaser_id'],
                    }))

            return account_id

    def updateone(self, account_id, account):

        with self.query() as Q:
            (Q().tables(T.account)
                .where(T.account.id == account_id)
                .crud()
                .update({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }))

            insert_products = []
            update_products = []
            delete_products = []

            for product in account['products']:

                product.update(account_id=account_id)

                if product.get('_crud', None) == 'insert':
                    insert_products.append(product)
                elif product.get('_crud', None) == 'update':
                    update_products.append(product)
                elif product.get('_crud', None) == 'delete':
                    delete_products.append(product)

            account_product_api = AccountProduct(queryclass=Q)

            if len(insert_products):
                account_product_api.insertmany(insert_products)

            if len(update_products):
                account_product_api.updatemany(update_products)

            if len(delete_products):
                account_product_api.deletemany(delete_products)

    def deleteone(self, account_id):
        with self.query() as Q:
            return \
                (Q().tables(T.account)
                    .where(T.account.id == account_id)
                    .crud()
                    .delete())
