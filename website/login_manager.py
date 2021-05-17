from flask_login import LoginManager
from website.DB import session
from website.models import User
#from abc import ABC, abstractmethod


#class FlaskLoginManager:
    #login_manager = LoginManager(app)
        #def __init__(self):
         #   self.login_manager = login_manager.login_view



#class AbstractLoginManager(ABC):
  #  @abstractmethod
   # def load_user:
   #     pass

login_manager = LoginManager()
login_manager.login_view = 'auth.login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return session.query(User).get(int(user_id))
