from flask_login import current_user


class UserProvider:
    def id_provider(self, user_id):
        pass

    def email_provider(self, email):
        pass

    def results_provider(self, user_id):
        pass
