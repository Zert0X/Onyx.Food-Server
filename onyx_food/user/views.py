from flask.views import MethodView
from flask import request, redirect, url_for
from onyx_food.utils.helpers import render_template
from onyx_food.user.models import UserModel
from onyx_food.extensions import db_main
from onyx_food.utils.helpers import render_template, register_view

class UserIndex(MethodView):
    def get(self):
        return redirect(url_for("index"))
    
class RegisterView(MethodView):
    def _register(request):
        NewUser = UserModel()
        NewUser.name = request.form.get("name")
        NewUser.second_name = request.form.get("second_name")
        NewUser.email = request.form.get("email")
        NewUser.phone = request.form.get("phone")
        if(request.form.get("password")==request.form.get("password-repeated")):
            NewUser.password = request.form.get("password")
        else:
            return False
        db_main.session.add(NewUser)
        db_main.session.commit()
        db_main.session.refresh(NewUser)
        db_main.session.expunge_all()
        return True
    
    def get(self):
        return render_template("register.html")

    def post(self):
        if(self._register(request)):
            return redirect(url_for("index"))
        return redirect(url_for("user.register"))

class LoginView(MethodView):
    def _login(request):
        return

    def get(self):
        return render_template("login.html")

    def post(self):
        if(self._login(request)):
            return redirect(url_for("index"))
        return redirect(url_for("user.login"))
