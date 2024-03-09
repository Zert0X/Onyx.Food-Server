from onyx_food.user.views import *
from onyx_food.utils.helpers import register_view, create_blueprint

user = create_blueprint('user', __name__)

register_view(user, routes=["/"],view_func=UserIndex.as_view("index"))
register_view(user, routes=["/login"],view_func=LoginView.as_view("login"))
register_view(user, routes=["/register"],view_func=RegisterView.as_view("register"))
register_view(user, routes=["/logout"],view_func=LogoutView.as_view("logout"))