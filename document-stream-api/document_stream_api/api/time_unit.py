from sqlbuilder.smartsql import T

from ..database import Service


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
