from sqlbuilder.smartsql import T, Q


from ..database import Service
from .database import TableSequence


class Configuration(Service):

    def selectone(self):
        account_table_sequence = TableSequence(self.database).selectone('account')

        if account_table_sequence is None:
            account_table_sequence = {}

        return {
            'sequence': {
                'account': account_table_sequence.get('sequence', None)
            }
        }

    def updateone(self, configuration):
        return TableSequence(self.database) \
            .updateone('account', configuration['sequence']['account'])
