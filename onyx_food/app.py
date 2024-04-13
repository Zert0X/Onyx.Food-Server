
import os
from flask import Flask

from onyx_food._compat import string_types
from onyx_food.extensions import (db, themes, cache, mail, login_manager, csrf)
from onyx_food.utils.helpers import get_config

from onyx_food.user.blueprint import user
from onyx_food.user.models import GuestModel, UserModel

from onyx_food.index.blueprint import index

from onyx_food.organization.blueprint import organization
from onyx_food.organization.models import OrganizationModel


def create_app(instance_path=None):
   app = Flask(
      "onyxfood", instance_path=instance_path, instance_relative_config=True
   )

   # instance folders are not automatically created by flask
   if not os.path.exists(app.instance_path):
      os.makedirs(app.instance_path)

   with app.app_context():
      configure_app(app)
      configure_extensions(app)
      configure_blueprints(app)
      #configure_template_filters(app)
      #configure_context_processors(app)
      #configure_before_handlers(app)
      #configure_errorhandlers(app)
      #configure_migrations(app)
      #configure_translations(app)

   return app

def configure_app(app):
   """Configures OnyxFood."""
   config = get_config(app)
   # Path
   if isinstance(config, string_types):
      app.config.from_pyfile(config)
   # Module
   else:
      # try to update the config from the object
      app.config.from_object(config)

def configure_extensions(app):
   # Flask-WTF CSRF
   #csrf.init_app(app)

   # Flask-Themes
   themes.init_themes(app, app_identifier="onyxfood", theme_url_prefix="/themes")
   
   # Flask-SQLAlchemy
   db.init_app(app)

   # Flask-Mail
   mail.init_app(app)

   # Flask-Cache
   cache.init_app(app)

   # Flask-Login
   login_manager.anonymous_user = GuestModel

   @login_manager.user_loader
   def load_user(user_id):
      """Loads the user. Required by the `login` extension."""
      user_instance = UserModel.query.filter_by(id=user_id).first()
      if user_instance:
         return user_instance
      else:
         return None

   login_manager.init_app(app)


def configure_blueprints(app):
    app.register_blueprint(user, url_prefix='/user')
    app.register_blueprint(organization, url_prefix='/organization')
    app.register_blueprint(index)