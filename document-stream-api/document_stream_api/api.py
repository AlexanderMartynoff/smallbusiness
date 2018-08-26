from sqlbuilder.smartsql import T, Q

from .environment import SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase


database = SqliteDatabase(SQLITE3_DB)  # IoC


class TimeUnit:

    @classmethod
    def selectall(cls):
        with database.query() as Q:
            return (Q()
                .tables(T.time_unit)
                .fields(
                    T.time_unit.id,
                    T.time_unit.name,
                )
                .crud()
                .selectall())


class Partner:
    @classmethod
    def selectall(cls):
        
        with database.query() as Q:
            return (Q()
                .tables(T.partner)
                .fields(
                    T.partner.id,
                    T.partner.name,
                    T.partner.address,
                    T.partner.taxpayer_number,
                    T.partner.reason_code,
                    T.partner.bank_id,
                    T.partner.bank_checking_account,
                )
                .crud()
                .selectall())


class AccountProduct:

    @classmethod
    def selectall(cls, account_id):
        
        with database.query() as Q:
            return (Q()
                .tables(T.account_product)
                .fields(
                    T.account_product.id,
                    T.account_product.name,
                    T.account_product.time_unit_id,
                    T.account_product.value,
                    T.account_product.price
                )
                .where(T.account_product.account_id == account_id)
                .crud()
                .selectall())


class Account:

    @classmethod
    def selectone(cls, account_id, include_products=False):
        with database.query() as Q:
            account = (Q()
                .tables(T.account)
                .fields(
                    T.Account.id,
                    T.Account.currency_unit_id,
                    T.Account.reason,
                    T.Account.date,
                    T.Account.provider_id,
                    T.Account.purchaser_id,
                )
                .where(T.account.id == account_id)
                .crud()
                .selectone())

            if not include_products:
                return account

            return {**account, 'products': AccountProduct.selectall(account_id=account_id)}

    @classmethod
    def selectall(cls, include_products=False):
        with database.query() as Q:
            accounts = (Q()
                .tables(T.account)
                .fields(
                    T.account.id,
                    T.account.reason,
                    T.account.date,
                )
                .crud()
                .selectall())

            if not include_products:
                return accounts

            return [{
                **account,
                'products': AccountProduct.selectall(account_id=account['id'])
            } for account in accounts]

    @classmethod
    def insertone(cls, account):
        print(account)
        with database.query() as Q:
            account_id = (Q()
                .tables(T.account)
                .crud()
                .insert({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }))
            return account_id

    @classmethod
    def updateone(cls, account_id, account):

        with database.query() as Q:
            (Q().tables(T.account)
                .where(T.account.id == account_id)
                .crud()
                .update({
                    T.account.currency_unit_id: account['currency_unit_id'],
                    T.account.reason: account['reason'],
                    T.account.provider_id: account['provider_id'],
                    T.account.purchaser_id: account['purchaser_id'],
                }))

            update_products = []
            insert_products = []

            for product in account['products']:

                if product.get('__phantom__', False):
                    insert_products.append(product)
                else:
                    update_products.append(product)

            if len(insert_products):

                (Q().tables(T.account_product)
                    .fields(
                        T.account_product.account_id,
                        T.account_product.name,
                        T.account_product.time_unit_id,
                        T.account_product.value,
                        T.account_product.price,
                    )
                    .crud()
                    .insert(
                        values=[(
                            account_id,
                            product['name'],
                            product['time_unit_id'],
                            product['value'],
                            product['price'],
                        ) for product in insert_products]
                    ))
    
    @classmethod
    def deleteone(cls, account_id):
        with database.query() as Q:
            return (Q().tables(T.account)
                .where(T.account.id == account_id)
                .crud()
                .delete())