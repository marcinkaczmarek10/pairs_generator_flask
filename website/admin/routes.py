from flask_admin import Admin
from website.database.models import (
    User, UsersPerson, DrawCount, RandomPair, WhichDraw
)
from website.database.DB import SessionFactory
from website.admin.views import AdminRequiredModelView, AdminRequiredIndexView

admin = Admin(index_view=AdminRequiredIndexView())


admin.add_view(AdminRequiredModelView(User, SessionFactory.session))
admin.add_view(AdminRequiredModelView(UsersPerson, SessionFactory.session))
admin.add_view(AdminRequiredModelView(DrawCount, SessionFactory.session))
admin.add_view(AdminRequiredModelView(RandomPair, SessionFactory.session))
admin.add_view(AdminRequiredModelView(WhichDraw, SessionFactory.session))
