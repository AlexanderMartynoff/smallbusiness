from sqlbuilder.smartsql import T, Q

from ..database import Service


class Permission(Service):
    def selectall(self, user_id):

        with self.sqlbuilder.result() as result:
            return Q(result=result) \
                .tables(T.user_permission) \
                .fields(
                    T.user_permission.id,
                    T.user_permission.entity,
                    T.user_permission.create,
                    T.user_permission.read,
                    T.user_permission.update,
                    T.user_permission.delete,
                ) \
                .where(T.user_permission.user_id == user_id) \
                .select() \
                .fetchall()

    def insertmany(self, permissions):

        with self.sqlbuilder.result() as result:
            Q(result=result) \
                .tables(T.user_permission) \
                .fields(
                    T.user_permission.entity,
                    T.user_permission.user_id,
                    T.user_permission.create,
                    T.user_permission.read,
                    T.user_permission.update,
                    T.user_permission.delete,
                ) \
                .insert(
                    values=[(
                        permission['entity'],
                        permission['user_id'],
                        permission['create'],
                        permission['read'],
                        permission['update'],
                        permission['delete'],
                    ) for permission in permissions]
                ) \
                .execute()

    def updatemany(self, permissions):
        with self.sqlbuilder.result() as result:
            for permission in permissions:
                Q(result=result) \
                    .tables(T.user_permission) \
                    .where(T.user_permission.id == permission['id']) \
                    .update({
                        T.user_permission.create: permission['create'],
                        T.user_permission.read: permission['read'],
                        T.user_permission.update: permission['update'],
                        T.user_permission.delete: permission['delete'],
                    }) \
                    .execute()
