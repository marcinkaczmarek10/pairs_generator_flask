from flask import redirect, url_for, request
from flask_admin import AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user


class AdminRequiredModelView(ModelView):

    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class AdminRequiredIndexView(AdminIndexView):
    def is_accessible(self):
        if current_user.is_authenticated and current_user.is_admin:
            return True
        return False

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))
