from sqlbuilder.smartsql import T, Q

from ..database import Service


class User(Service):
    def selectone_for_authenticate(self, login, password):

        with self.sqlbuilder.result() as result:
            return Q(result=result).tables(T.user) \
                .fields(
                    T.user.id,
                    T.user.login,
                    T.user.password,
                ) \
                .where((T.user.login == login) & (T.user.password == password)) \
                .select() \
                .fetchone()
