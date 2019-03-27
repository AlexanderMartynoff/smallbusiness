from typing import Set, cast
from sqlbuilder.smartsql import T, Q

from ..database import Service


class Bank(Service):

    def deleteone(self, bank_id):
        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.bank) \
                .where(T.bank.id == bank_id) \
                .delete() \
                .execute()

    def updateone(self, bank_id, bank):

        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.bank) \
                .where(T.bank.id == bank_id) \
                .update({
                    T.bank.name: bank['name'],
                    T.bank.taxpayer_number: bank['taxpayer_number'],
                    T.bank.reason_code: bank['reason_code'],
                    T.bank.identity_code: bank['identity_code'],
                    T.bank.correspondent_account: bank['correspondent_account'],
                }) \
                .execute()

    def selectone(self, bank_id):

        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.bank) \
                .fields(
                    T.bank.id,
                    T.bank.name,
                    T.bank.taxpayer_number,
                    T.bank.reason_code,
                    T.bank.identity_code,
                    T.bank.correspondent_account,
                ) \
                .where(T.bank.id == bank_id) \
                .select() \
                .fetchone()

    def selectall(self):
        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.bank) \
                .fields(
                    T.bank.id,
                    T.bank.name,
                    T.bank.taxpayer_number,
                    T.bank.reason_code,
                    T.bank.identity_code,
                    T.bank.correspondent_account,
                ) \
                .select() \
                .fetchall()

    def insertone(self, bank):
        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.bank) \
                .insert({
                    T.bank.name: bank['name'],
                    T.bank.taxpayer_number: bank['taxpayer_number'],
                    T.bank.reason_code: bank['reason_code'],
                    T.bank.identity_code: bank['identity_code'],
                    T.bank.correspondent_account: bank['correspondent_account'],
                }) \
                .fetchinsertid()
