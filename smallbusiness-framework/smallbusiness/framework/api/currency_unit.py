from sqlbuilder.smartsql import T, Q

from ..database import Service


class CurrencyUnit(Service):

    def selectall(self):
        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.currency_unit) \
                .fields(
                    T.currency_unit.id,
                    T.currency_unit.name,
                    T.currency_unit.code,
                ) \
                .select() \
                .fetchall()
