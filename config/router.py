class SearchRouter:
    route_app_labels = {'content', }

    def db_for_read(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'search'
        return "default"

    def db_for_write(self, model, **hints):
        if model._meta.app_label in self.route_app_labels:
            return 'search'
        return "default"

    def allow_relation(self, obj1, obj2, **hints):
        if obj1._meta.app_label in self.route_app_labels or obj2._meta.app_label in self.route_app_labels:
            return True
        return "default"

    def allow_migrate(self, db, app_label, model_name=None, **hints):
        if app_label in self.route_app_labels:
            return db == 'search'
        return "default"