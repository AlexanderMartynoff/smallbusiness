from sqlbuilder.smartsql import T

from ..database import Service
from . import account


class AccountProduct(Service):

    def selectall(self, where):
        with self.query() as Q:
            return Q().tables(
                    T.account_product +
                    T.time_unit.on(T.time_unit.id == T.account_product.time_unit_id)
                ) \
                .fields(
                    T.account_product.id,
                    T.account_product.name,
                    T.account_product.time_unit_id,
                    T.time_unit.name.as_('time_unit_name'),
                    T.account_product.value,
                    T.account_product.price,
                ) \
                .where(where) \
                .crud() \
                .selectall()

    def updatemany(self, products):
        with self.query() as Q:
            for product in products:
                Q().tables(T.account_product) \
                    .where(T.account_product.id == product['id']) \
                    .crud() \
                    .update({
                        T.account_product.name: product['name'],
                        T.account_product.time_unit_id: product['time_unit_id'],
                        T.account_product.value: product['value'],
                        T.account_product.price: product['price'],
                    })

    def deletemany(self, products):
        with self.query() as Q:
            for product in products:
                Q().tables(T.account_product) \
                    .where(T.account_product.id == product['id']) \
                    .crud() \
                    .delete()

    def insertmany(self, products):
        with self.query() as Q:
            return Q().tables(T.account_product) \
                .fields(
                    T.account_product.account_id,
                    T.account_product.name,
                    T.account_product.time_unit_id,
                    T.account_product.value,
                    T.account_product.price,
                ) \
                .crud() \
                .insert(
                    values=[(
                        product['account_id'],
                        product['name'],
                        product['time_unit_id'],
                        product['value'],
                        product['price'],
                    ) for product in products]
                )
