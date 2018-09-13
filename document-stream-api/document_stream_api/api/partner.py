from sqlbuilder.smartsql import T

from ..database import Service


class Partner(Service):

    def selectall(self):

        with self.query() as Q:
            return (Q()
                .tables(T.partner)
                .fields(
                    T.partner.id,
                    T.partner.name,
                    T.partner.address,
                    T.partner.taxpayer_number,
                    T.partner.reason_code,
                    T.partner.bank_id,
                    T.partner.bank_checking_account,
                )
                .crud()
                .selectall())

    def selectone(self, partner_id):

        with self.query() as Q:
            return (Q()
                .tables((T.partner & T.bank).on(T.partner.bank_id == T.bank.id))
                .fields(
                    T.partner.id,
                    T.partner.name,
                    T.partner.address,
                    T.partner.taxpayer_number,
                    T.partner.reason_code,
                    T.partner.bank_id,
                    T.partner.bank_checking_account,

                    # bank attributes
                    T.bank.name.as_('bank_name'),
                    T.bank.taxpayer_number.as_('bank_taxpayer_number'),
                    T.bank.reason_code.as_('bank_reason_code'),
                    T.bank.identity_code.as_('bank_identity_code'),
                    T.bank.correspondent_account.as_('bank_correspondent_account'),
                )
                .where(T.partner.id == partner_id)
                .crud()
                .selectone())

    def updateone(self, partner_id, partner):

        with self.query() as Q:
            (Q().tables(T.partner)
                .where(T.partner.id == partner_id)
                .crud()
                .update({
                    T.partner.name: partner['name'],
                    T.partner.address: partner['address'],
                    T.partner.taxpayer_number: partner['taxpayer_number'],
                    T.partner.reason_code: partner['reason_code'],
                    T.partner.bank_id: partner['bank_id'],
                    T.partner.bank_checking_account: partner['bank_checking_account'],
                }))

    def deleteone(self, partner_id):

        with self.query() as Q:
            (Q().tables(T.partner)
                .where(T.partner.id == partner_id)
                .crud()
                .delete())

    def insertone(self, partner):
        with self.query() as Q:
            partner_id = (Q()
                .tables(T.partner)
                .crud()
                .insert({
                    T.partner.name: partner['name'],
                    T.partner.address: partner['address'],
                    T.partner.taxpayer_number: partner['taxpayer_number'],
                    T.partner.reason_code: partner['reason_code'],
                    T.partner.bank_id: partner['bank_id'],
                    T.partner.bank_checking_account: partner['bank_checking_account'],
                }))
            return partner_id
