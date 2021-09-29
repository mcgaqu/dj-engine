import random

class NeodRouter:
    """
    A router to control all database operations on models in the
    auth and contenttypes applications.
    """
    route_app_labels_neod = [
        'empresas', 'clasifarticulos', 'clasifclientes', 
        'personas', 'productos', 'tareas'
        ]
    route_app_labels_main = []

    def db_for_read(self, model, **hints):
        """
        Attempts to read auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels_neod:
                return 'firebird1'
        elif model._meta.app_label in self.route_app_labels_main:
                return 'main'
        return None

    def db_for_write(self, model, **hints):
        """
        Attempts to write auth and contenttypes models go to auth_db.
        """
        if model._meta.app_label in self.route_app_labels_neod:
                return 'firebird1'
        elif model._meta.app_label in self.route_app_labels_main:
                return 'main'
        return None

    def x_allow_relation(self, obj1, obj2, **hints):
        """
        Allow relations if a model in the auth or contenttypes apps is
        involved.
        """
        if (
            (obj1._meta.app_label not in self.route_app_labels and
            obj2._meta.app_label not in self.route_app_labels) or (
            obj1._meta.app_label in self.route_app_labels and
            obj2._meta.app_label in self.route_app_labels)
        ):
           return True
        return None

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        """
        Make sure the auth and contenttypes apps only appear in the
        'auth_db' database.
        """
        if db == 'firebird1':
            return False
        return None

       

# class PrimaryReplicaRouter:
#     def db_for_read(self, model, **hints):
#         """
#         Reads go to a randomly-chosen replica.
#         """
#         return random.choice(['replica1', 'replica2'])

#     def db_for_write(self, model, **hints):
#         """
#         Writes always go to primary.
#         """
#         return 'primary'

#     def allow_relation(self, obj1, obj2, **hints):
#         """
#         Relations between objects are allowed if both objects are
#         in the primary/replica pool.
#         """
#         db_set = {'primary', 'replica1', 'replica2'}
#         if obj1._state.db in db_set and obj2._state.db in db_set:
#             return True
#         return None

#     def allow_migrate(self, db, app_label, model_name=None, **hints):
#         """
#         All non-auth models end up in this pool.
#         """
#         return True