from sqlbuilder.smartsql import T

from ..database import Service


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
