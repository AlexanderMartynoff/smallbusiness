from sqlbuilder.smartsql import T, Q

from ..database import Service


class TimeUnit(Service):

    def selectall(self):
        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.time_unit) \
                .fields(
                    T.time_unit.id,
                    T.time_unit.name,
                ) \
                .select() \
                .fetchall()
