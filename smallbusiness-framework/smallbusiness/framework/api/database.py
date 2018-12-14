from sqlbuilder.smartsql import T, Q

from ..database import Service


class TableSequence(Service):

    def selectone(self, table):
        with self.sqlbuilder.result() as result:
            return Q(result=result) \
                .raw('SELECT name, seq as sequence FROM SQLITE_SEQUENCE WHERE name = ?', [table]) \
                .select() \
                .fetchone()

    def updateone(self, table, sequence):
        with self.sqlbuilder.result() as result:
            return Q(result=result) \
                .raw('UPDATE SQLITE_SEQUENCE SET seq = ? WHERE name = ?', [sequence, table]) \
                .select() \
                .execute()
