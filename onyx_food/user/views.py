from flask.views import MethodView
from flask import request, redirect, url_for
from flask_login import logout_user
from onyx_food.utils.helpers import render_template
from onyx_food.user.models import UserModel
from onyx_food.extensions import db
from onyx_food.utils.helpers import render_template, register_view

class UserIndex(MethodView):
    def get(self):
        users = UserModel.query.all()
        redirect(url_for("index.index"))
    
class RegisterView(MethodView):
    def get(self):
        return render_template("user/register.html")

    def post(self):
        if(UserModel.register(request)):
            return redirect(url_for("index.index"))
        return redirect(url_for("user.register"))

class LoginView(MethodView):

    def get(self):
        return render_template("user/login.html")

    def post(self):
        if(UserModel.login(request)):
            return redirect(url_for('index.index'))
        return render_template("user/login.html")

class LogoutView(MethodView):
    def logout(self):
        logout_user()
        return redirect(url_for('index.index'))
    
    def get(self):
        return self.logout()

    def post(self):
        return self.logout()
    