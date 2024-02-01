import os
from onyx_food import create_app

from werkzeug.debug import DebuggedApplication

_basepath = os.path.dirname(os.path.abspath(__file__))
app = create_app()

app.debug = True
app.wsgi_app = DebuggedApplication(app.wsgi_app, True)