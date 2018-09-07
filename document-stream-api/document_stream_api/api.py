from sqlbuilder.smartsql import T

from .environment import SQLITE3_DB
from .database import MysqlDatabase, SqliteDatabase, Service


class Bank(Service):
    
    def selectall(self):
        with self.query() as Q:
            return (Q()
                .tables(T.bank)
                .fields(
                    T.bank.id,
                    T.bank.name,
                    T.bank.taxpayer_number,
                    T.bank.reason_code,
                    T.bank.identity_code,
                    T.bank.correspondent_account,
                )
                .crud()
                .selectall())


class CurrencyUnit(Service):

    def selectall(self):
        with self.query() as Q:
            return (Q()
                .tables(T.currency_unit)
                .fields(
                    T.currency_unit.id,
                    T.currency_unit.name,
                    T.currency_unit.code,
                )
                .crud()
                .selectall())


class TimeUnit(Service):

    def selectall(self):
        with self.query() as Q:
            return (Q()
                .tables(T.time_unit)
                .fields(
                    T.time_unit.id,
                    T.time_unit.name,
                )
                .crud()
                .selectall())


class Partner(Service):

    def selectall(self):

        with self.query() as Q:
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

    def selectone(self, partner_id):

        with self.query() as Q:
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
                .where(T.partner.id == partner_id)
                .crud()
                .selectone())

    def updateone(self, partner_id, partner):

        with self.query() as Q:
            (Q().tables(T.partner)
                .where(T.partner.id == partner_id)
                .crud()
                .update({
                    T.partner.name: partner['name'],
                    T.partner.address: partner['address'],
                    T.partner.taxpayer_number: partner['taxpayer_number'],
                    T.partner.reason_code: partner['reason_code'],
                    T.partner.bank_id: partner['bank_id'],
                    T.partner.bank_checking_account: partner['bank_checking_account'],
                }))

    def deleteone(self, partner_id):

        with self.query() as Q:
            (Q().tables(T.partner)
                .where(T.partner.id == partner_id)
                .crud()
                .delete())

    def insertone(self, partner):
        with self.query() as Q:
            partner_id = (Q()
                .tables(T.partner)
                .crud()
                .insert({
                    T.partner.name: partner['name'],
                    T.partner.address: partner['address'],
                    T.partner.taxpayer_number: partner['taxpayer_number'],
                    T.partner.reason_code: partner['reason_code'],
                    T.partner.bank_id: partner['bank_id'],
                    T.partner.bank_checking_account: partner['bank_checking_account'],
                }))
            return partner_id


class AccountProduct(Service):

    def selectall(self, account_id):
        
        with self.query() as Q:
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

    def updatemany(self, products):
        with self.query() as Q:
            for product in products:
                (Q().tables(T.account_product)
                    .where(T.account_product.id == product['id'])
                    .crud()
                    .update({
                        T.account_product.name: product['name'],
                        T.account_product.time_unit_id: product['time_unit_id'],
                        T.account_product.value: product['value'],
                        T.account_product.price: product['price'],
                    }))

    def deletemany(self, products):
        with self.query() as Q:
            for product in products:
                (Q().tables(T.account_product)
                    .where(T.account_product.id == product['id'])
                    .crud()
                    .delete())


    def insertmany(self, products):
        with self.query() as Q:
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


class Account(Service):

    def selectone(self, account_id, include_products=False):
        with self.query() as Q:
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

            return {**account, 'products': AccountProduct(queryclass=Q).selectall(account_id=account_id)}

    def selectall(self, include_products=False):
        with self.query() as Q:
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

    def insertone(self, account):
        with self.query() as Q:
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
            return (Q().tables(T.account)
                .where(T.account.id == account_id)
                .crud()
                .delete())
