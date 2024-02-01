import os
from werkzeug.utils import ImportStringError, import_string
from onyx_food._compat import string_types
from flask_login import current_user
from flask import session, current_app, Blueprint
from flask_themes2 import render_theme_template

def render_template(template, **context):
    """A helper function that uses the `render_theme_template` function
    without needing to edit all the views
    """
    if current_user.is_authenticated and current_user.theme:
        theme = current_user.theme
    else:
        theme = session.get("theme", current_app.config["DEFAULT_THEME"])
    
    return render_theme_template(theme, template, **context)

def register_view(bp_or_app, routes, view_func, *args, **kwargs):
    for route in routes:
        bp_or_app.add_url_rule(route, view_func=view_func, *args, **kwargs)

def create_blueprint(*args):
    """A helper function that uses the `Blueprint` function
    without needing to edit all the blueprints
    """
    
    return Blueprint(*args, template_folder='/srv/Onyx.Food-Server/onyx_food/templates')

def get_config(app):
    # this would be so much nicer and cleaner if we wouldn't
    # support the root/project dir.
    # this walks back to flaskbb/ from flaskbb/flaskbb/cli/main.py
    project_dir = os.path.dirname(
        os.path.dirname(os.path.dirname(__file__))
    )
    project_config = os.path.join(project_dir, "main.cfg")

    # instance config doesn't exist
    instance_config = os.path.join(app.instance_path, "main.cfg")
    if os.path.exists(instance_config):
        return instance_config

    # config in root directory doesn't exist
    if os.path.exists(project_config):
        return project_config