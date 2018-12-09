from sqlbuilder.smartsql import T, Q

from ..database import Service


class TableSequence(Service):

    def selectone(self, table):
        with self.result() as result:
            return Q(result=result) \
                .raw('SELECT name, seq as sequence FROM SQLITE_SEQUENCE WHERE name=?', [table]) \
                .select() \
                .fetchone()

    def updateone(self, table):
        with self.result() as result:
            return Q(result=result) \
                .raw('SELECT name, seq as sequence FROM SQLITE_SEQUENCE WHERE name=?', [table]) \
                .select() \
                .fetchone()
