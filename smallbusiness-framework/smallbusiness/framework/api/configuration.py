from sqlbuilder.smartsql import T, Q


from ..database import Service
from .database import TableSequence


class Configuration(Service):

    def selectone(self):
        with self.sqlbuilder.result() as result:
            account_table_sequence = TableSequence(result=result).selectone('account')

            if account_table_sequence is None:
                account_table_sequence = {}

            return {
                'sequence': {
                    'account': account_table_sequence.get('sequence', None)
                }
            }

    def updateone(self, configuration):
        with self.sqlbuilder.result() as result:
            return TableSequence(result=result) \
                .updateone('account', configuration['sequence']['account'])
