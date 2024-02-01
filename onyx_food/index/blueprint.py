from onyx_food.utils.helpers import register_view, create_blueprint
from onyx_food.index.views import *

index = create_blueprint('index', __name__)

register_view(index, routes=["/"],view_func=IndexView.as_view("index"))
