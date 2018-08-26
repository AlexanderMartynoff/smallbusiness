from sqlbuilder.smartsql import T

from .environment import SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase


database = SqliteDatabase(SQLITE3_DB)  # IoC


class CurrencyUnit(database.service):

    @classmethod
    def selectall(cls):
        with self.database.query() as Q:
            return (Q()
                .tables(T.currency_unit)
                .fields(
                    T.currency_unit.id,
                    T.currency_unit.name,
                    T.currency_unit.code,
                )
                .crud()
                .selectall())


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

    @classmethod
    def insertmany(cls, products):
        with database.query() as Q:
            return (Q().tables(T.account_product)
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
                        product['account_id'],
                        product['name'],
                        product['time_unit_id'],
                        product['value'],
                        product['price'],
                    ) for product in products]
                ))


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

            insert_products = []
            update_products = []
            delete_products = []

            for product in account['products']:

                product.update(account_id=account_id)

                if product.get('_insert', False):
                    insert_products.append(product)
                elif product.get('_update', False):
                    update_products.append(product)
                elif product.get('_delete', False):
                    delete_products.append(product)

            account_product_api = AccountProduct(queryclass=Q)
            
            if len(insert_products):
                account_product_api.insertmany(insert_products)
            
            if len(insert_products):
                account_product_api.updatemany(update_products)

            if len(insert_products):
                account_product_api.deletemany(update_products)
    
    @classmethod
    def deleteone(cls, account_id):
        with database.query() as Q:
            return (Q().tables(T.account)
                .where(T.account.id == account_id)
                .crud()
                .delete())
