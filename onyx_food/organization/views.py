from flask.views import MethodView
from flask import request, redirect, url_for
from flask_login import current_user, login_required, logout_user

from onyx_food.utils.helpers import render_template
from onyx_food.utils.decorators import organization_access_required
from onyx_food.user.models import UserModel

from onyx_food.organization.models import OrganizationModel
from onyx_food.organization.utils import *

from onyx_food.extensions import db
from onyx_food.utils.helpers import render_template, register_view

   
#SECTION - Auth
#ANCHOR - RegisterView
class RegisterView(MethodView):    
    def get(self):
        return render_template("organization/register.html", owner_email = current_user.email, owner_phone = current_user.phone)

    def post(self):
        if(OrganizationModel.register(request)):
            _organization =  OrganizationModel.query.filter_by(owner_id = current_user.id).first()
            return redirect(url_for("organization.dashboard", organizationID = _organization.id))
        return redirect(url_for("organization.register"))
    
#ANCHOR - LoginView
class LoginView(MethodView):
    def get(self):
        return render_template("user/login.html")

    def post(self):
        if(UserModel.login(request)):
            user_organizations = get_user_organizations()
            if (not len(user_organizations)):
                return redirect(url_for('organization.register'))
            if (len(user_organizations)>1):
                return redirect(url_for('organization.organization_choose'))
            _organization =  OrganizationModel.query.filter_by(owner_id = current_user.id).first()
            return redirect(url_for('organization.dashboard', organizationID = _organization.id))
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
    def get(self):
        organizations = get_user_organizations()
        return render_template("organization/organization_choose.html", organizations = organizations)
    
    def post(self):
        return redirect(url_for('organization.dashboard', organizationID = request.form.get("chosen_organization")))
    
#!SECTION
    
#SECTION Dashboard
        
#ANCHOR - Dashboard_RestaurantsView
class DashboardView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        user_restaurants = get_organization_restaurants(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/index.html", organization=_organization, restaurants=user_restaurants, new_order=_new_order)
    
    def post(self, organizationID):
        return redirect(url_for('organization.restaurant_dashboard', organizationID = organizationID, restaurantID = request.form.get("chosen_restaurant")))
    
class RestaurantAdd(MethodView):
    def get(self, organizationID):
        return render_template('organization/dashboard/restaurants/add.html')
    
    def post(self, organizationID):
        return RestaurantModel.add(request, organizationID)

class RestaurantDashboard(MethodView):
    def get(self, organizationID, restaurantID):
        _organization = get_organization_by_ID(organizationID)
        _restaurant = get_restaurant_by_ID(restaurantID)
        _new_order = check_new_orders(organizationID)
        return render_template('organization/dashboard/restaurants/index.html', organization=_organization, restaurant=_restaurant, new_order=_new_order)
    
class RestaurantReviews(MethodView):
    def get(self, organizationID, restaurantID):
        _organization = get_organization_by_ID(organizationID)
        _restaurant = get_restaurant_by_ID(restaurantID)
        _new_order = check_new_orders(organizationID)
        return render_template('organization/dashboard/restaurants/index.html', organization=_organization, restaurant=_restaurant, new_order=_new_order)
    
class RestaurantInfo(MethodView):
    def get(self, organizationID, restaurantID):
        _organization = get_organization_by_ID(organizationID)
        _restaurant = get_restaurant_by_ID(restaurantID)
        _new_order = check_new_orders(organizationID)
        return render_template('organization/dashboard/restaurants/index.html', organization=_organization, restaurant=_restaurant, new_order=_new_order)

class RestaurantDisable(MethodView):
    def get(self, organizationID, restaurantID):
        _organization = get_organization_by_ID(organizationID)
        _restaurant = get_restaurant_by_ID(restaurantID)
        return render_template('organization/dashboard/restaurants/index.html', organization=_organization, restaurant=_restaurant)
    
#ANCHOR - Dashboard_OrdersView
class Dashboard_OrdersView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _orders = get_orders(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/orders/index.html", organization=_organization, orders=_orders, new_order=_new_order)
    
class Dashboard_OrderInfo(MethodView):
    def get(self,organizationID, orderID):
        _organization = get_organization_by_ID(organizationID)
        _orders = get_orders(organizationID)
        return render_template("organization/dashboard/orders/info.html", organization=_organization, orders=_orders, orderID=orderID)
    
#ANCHOR - Dashboard_MenusView
class Dashboard_MenusView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _categories = get_categories(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/menu/index.html", organization=_organization, categories=_categories, new_order=_new_order)

class Dashboard_MenuInfo(MethodView):
    def get(self,organizationID, categoryID):
        _organization = get_organization_by_ID(organizationID)
        _category = get_category_by_ID(categoryID)
        return render_template("organization/dashboard/menu/info.html", organization=_organization, category=_category)

class Dashboard_MenuAddCategory(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _categories = get_categories()
        _org_categories = get_categories(organizationID)
        return render_template("organization/dashboard/menu/add_category.html", organization=_organization, categories = _categories, org_categories=_org_categories)
    
    def post(self, organizationID):
        return CategoriesToOrgsModel.add(request, organizationID)
   
#ANCHOR - Dashboard_StatisticsView
class Dashboard_StatisticsView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/statistics.html", organization=_organization, new_order=_new_order)

#ANCHOR - Dashboard_HistoryView
class Dashboard_HistoryView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/history.html", organization=_organization, new_order=_new_order)

#ANCHOR - Dashboard_WorkHoursView
class Dashboard_WorkHoursView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/work_hours.html", organization=_organization, new_order=_new_order)

#ANCHOR - Dashboard_CookingTimeView
class Dashboard_CookingTimeView(MethodView):
    def get(self, organizationID):
        _organization = get_organization_by_ID(organizationID)
        _new_order = check_new_orders(organizationID)
        return render_template("organization/dashboard/cooking_time.html", organization=_organization, new_order=_new_order)
    
#!SECTION