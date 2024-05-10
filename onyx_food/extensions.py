import copy
from sqlalchemy import MetaData
from flask_sqlalchemy import SQLAlchemy
from flask_themes2 import Themes
from flask_login import LoginManager
from flask_mail import Mail
from flask_caching import Cache
from flask_wtf.csrf import CSRFProtect
from flask_bootstrap import Bootstrap

# Themes
themes = Themes()

# Login
login_manager = LoginManager()

# Mail
mail = Mail()

# Caching
cache = Cache()

# CSRF
csrf = CSRFProtect()

#Bootstrap
bootstrap = Bootstrap()

# Database
metadata = MetaData(
    naming_convention={
        "ix": "ix_%(column_0_label)s",
        "uq": "uq_%(table_name)s_%(column_0_name)s",
        "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
        "pk": "pk_%(table_name)s",
    }
)
metadata_main = copy.deepcopy(metadata)
db = SQLAlchemy(metadata=metadata_main, session_options={"expire_on_commit": False})