from sqlbuilder.smartsql import T

from ..database import Service


class Bank(Service):

    def deleteone(self, bank_id):
        with self.query() as Q:
            return \
                (Q().tables(T.bank)
                    .where(T.bank.id == bank_id)
                    .crud()
                    .delete())

    def updateone(self, bank_id, bank):

        with self.query() as Q:
            return \
                (Q().tables(T.bank)
                    .where(T.bank.id == bank_id)
                    .crud()
                    .update({
                        T.bank.name: bank['name'],
                        T.bank.taxpayer_number: bank['taxpayer_number'],
                        T.bank.reason_code: bank['reason_code'],
                        T.bank.identity_code: bank['identity_code'],
                        T.bank.correspondent_account: bank['correspondent_account'],
                    }))

    def selectone(self, bank_id):

        with self.query() as Q:
            return \
                (Q().tables(T.bank)
                    .fields(
                        T.bank.id,
                        T.bank.name,
                        T.bank.taxpayer_number,
                        T.bank.reason_code,
                        T.bank.identity_code,
                        T.bank.correspondent_account,
                    )
                    .where(T.bank.id == bank_id)
                    .crud()
                    .selectone())

    def selectall(self):
        with self.query() as Q:
            return \
                (Q().tables(T.bank)
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

    def insertone(self, bank):
        with self.query() as Q:
            return \
                (Q().tables(T.bank)
                    .crud()
                    .insert({
                        T.bank.name: bank['name'],
                        T.bank.taxpayer_number: bank['taxpayer_number'],
                        T.bank.reason_code: bank['reason_code'],
                        T.bank.identity_code: bank['identity_code'],
                        T.bank.correspondent_account: bank['correspondent_account'],
                    }))
