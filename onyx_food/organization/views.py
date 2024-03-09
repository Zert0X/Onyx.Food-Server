from flask.views import MethodView
from flask import request, redirect, url_for
from flask_login import current_user, login_required

from onyx_food.utils.helpers import render_template
from onyx_food.utils.decorators import organization_access_required
from onyx_food.user.models import UserModel

from onyx_food.organization.models import OrganizationModel, MenuModel
from onyx_food.organization.utils import get_user_organizations

from onyx_food.extensions import db
from onyx_food.utils.helpers import render_template, register_view

   
#SECTION - Auth
#ANCHOR - RegisterView
class RegisterView(MethodView):    
    def get(self):
        return render_template("organization/register.html", owner_email = current_user.email, owner_phone = current_user.phone)

    def post(self):
        if(OrganizationModel.register(request)):
            user_organizations = get_user_organizations()
            return redirect(url_for("organization.dashboard", organizationId = user_organizations[0].id))
        return redirect(url_for("organization.register"))
    
#ANCHOR - LoginView
class LoginView(MethodView):
    def get(self):
        return render_template("user/login.html")

    def post(self):
        if(UserModel.login(request)):
            user_organizations = OrganizationModel.query.filter_by(owner_id = current_user.id).all()
            if (not len(user_organizations)):
                return redirect(url_for('organization.register'))
            user_organizations = get_user_organizations()
            if (len(user_organizations)>1):
                return render_template("organization/organization_choose.html", user_organizations = user_organizations)
            return redirect(url_for('organization.dashboard', organizationId = user_organizations[0].id))
        return render_template("user/login.html")

#ANCHOR - LogoutView
class LogoutView(MethodView):
    def logout(self):
        logout_user()
        return redirect(url_for('index.index'))
    
    def get(self):
        return self.logout()

    def post(self):
        return self.logout()

#ANCHOR - OrganizationChooseView
#Use this ONLY in cases when user have more than 1 organization
class OrganizationChooseView(MethodView):
    def get(self, user_organizations):
        return render_template("organization/organization_choose.html", user_organizations = user_organizations)
    
#!SECTION
    
#SECTION Dashboard
        
#ANCHOR - DashboardView
class DashboardView(MethodView):
    def get(self, organizationId):
        user_organizations = get_user_organizations()
        if (len(user_organizations)>1):
            return render_template("organization/organization_choose.html", user_organizations = user_organizations)
        return render_template("organization/dashboard/index.html", organization=user_organizations[0])

#ANCHOR - Dashboard_OrdersView
class Dashboard_OrdersView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/orders.html", organization=organization)

#ANCHOR - Dashboard_MenusView
class Dashboard_MenusView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/menus.html", organization=organization)

#ANCHOR - Dashboard_StatisticsView
class Dashboard_StatisticsView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/statistics.html", organization=organization)

#ANCHOR - Dashboard_HistoryView
class Dashboard_HistoryView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/history.html", organization=organization)

#ANCHOR - Dashboard_WorkHoursView
class Dashboard_WorkHoursView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/work_hours.html", organization=organization)

#ANCHOR - Dashboard_CookingTimeView
class Dashboard_CookingTimeView(MethodView):
    def get(self, organizationId):
        organization = OrganizationModel.query.filter_by(id = organizationId).first()
        return render_template("organization/dashboard/cooking_time.html", organization=organization)  
#!SECTION