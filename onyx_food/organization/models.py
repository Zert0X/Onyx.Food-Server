from onyx_food.extensions import db
from flask_login import current_user
from flask import jsonify
import requests

from sqlalchemy import ForeignKey, DateTime, String, Integer, Boolean, Float
from sqlalchemy.orm import relationship
from onyx_food.utils.exceptions import ValidationError

#SECTION Organizations
class OrganizationModel(db.Model):
    __bind_key__  = 'main'
    __tablename__ = 'organizations'
    id       = db.Column(Integer,     nullable=False, primary_key=True)
    owner_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    name     = db.Column(String(50), nullable=False)

    INN      = db.Column(String(12),  nullable=False)

    region   = db.Column(String(50))
    city     = db.Column(String(50))
    street   = db.Column(String(70))
    house    = db.Column(String(20))
    
    @classmethod
    def register(self, request):
        NewOrganization = OrganizationModel()
        NewOrganization.INN = request.form.get("INN")
        NewOrganization_info = requests.get("https://htmlweb.ru/json/service/org/?inn="+NewOrganization.INN)
        NewOrganization_info = NewOrganization_info.json()
        if(NewOrganization_info['status']!='ACTIVE'):
            raise ValidationError("Неверно указанны данные либо организация недействительна!")
        
        if (OrganizationModel.query.filter_by(INN = request.form.get("INN")).first()) is not None:
            raise ValidationError("Данный ИНН уже зарегестрирован!")
                
        NewOrganization.owner_id = current_user.id
        
        NewOrganization.couriers = bool(request.form.get("couriers"))
       
        NewOrganization.name = NewOrganization_info['name']
        db.session.add(NewOrganization)
        db.session.commit()
        db.session.refresh(NewOrganization)
        db.session.expunge_all()
        return True


#!SECTION
#SECTION Restaurants
class RestaurantModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'restaurants'

    id    = db.Column(Integer, nullable=False, primary_key=True)
    name  = db.Column(String(50))

    org_id = db.Column(Integer, nullable=False)
    couriers = db.Column(Boolean,  nullable=False)

    region  = db.Column(String(50))
    city  = db.Column(String(50))
    street  = db.Column(String(50))
    house  = db.Column(String(20))
    
    @classmethod
    def add(self, request, organizationID):
        NewRestaurant = RestaurantModel()
        data = {}
        NewRestaurant.org_id    = organizationID
        if(request.form.get("add_name")==""):
            data["add_name"] = "Имя не может быть пустым"
        NewRestaurant.name      = request.form.get("add_name")
        NewRestaurant.couriers  = request.form.get("add_our_couriers")=="on" if True else False
        if(request.form.get("add_region")==""):
            data["map"] = "Ошибка с адресом попробуйте позже"
        NewRestaurant.region    = request.form.get("add_region")
        if(request.form.get("add_city")==""):
            data["map"] = "Ошибка с адресом попробуйте позже"
        NewRestaurant.city      = request.form.get("add_city")
        if(request.form.get("add_street")==""):
            data["map"] = "Ошибка с адресом попробуйте позже"
        NewRestaurant.street    = request.form.get("add_street")
        if(request.form.get("add_house")==""):
            data["map"] = "Ошибка с адресом попробуйте позже"
        NewRestaurant.house     = request.form.get("add_house")
        if(data):
            return jsonify(data), 200
        db.session.add(NewRestaurant)
        db.session.commit()
        db.session.refresh(NewRestaurant)
        db.session.expunge_all()
        return "ok"
#!SECTION
#SECTION Orders    
class OrderModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'orders'

    id    = db.Column(Integer, nullable=False, primary_key=True)
    datetime  = db.Column(DateTime)
    status = db.Column(Integer, nullable=False)
    user_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    courier_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(Integer, db.ForeignKey("restaurants.id"), nullable=False)
    restaurant = relationship("RestaurantModel")
    coordinates = db.Column(String, nullable=False)
    delivery_time = db.Column(Integer, nullable=False)
    comment = db.Column(String, nullable=False)
    people_quantity = db.Column(Integer, nullable=False)
    price = db.Column(Float, nullable=False)
#!SECTION
#SECTION Categories
class CategoryModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'categories'

    id       = db.Column(Integer, nullable=False, primary_key=True)
    name     = db.Column(String, nullable=False)
    default = db.Column(Boolean,  nullable=False, default=0)

class CategoriesToOrgsModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'categories_to_organizations'

    id       = db.Column(Integer, nullable=False, primary_key=True)
    org_id   = db.Column(Integer, db.ForeignKey("organizations.id"), nullable=False)
    category_id   = db.Column(Integer, db.ForeignKey("categories.id"), nullable=False)
    category = relationship("CategoryModel")
    
    @classmethod
    def add(self, request, organizationID):
        NewCategory = CategoryModel()
        
        data = {}
        NewCategory.org_id = organizationID
        if(request.form.get("default-category")!=""):
            NewCategoryLink = CategoriesToOrgsModel()
            NewCategoryLink.org_id = organizationID
            NewCategoryLink.category_id = request.form.get("default-category")
            db.session.add(NewCategoryLink)
            db.session.commit()
            db.session.refresh(NewCategoryLink)
            db.session.expunge_all()
            return "ok"
        else:
            if(request.form.get("add_name")==""):
                data["add_name"] = "Имя не может быть пустым"
            if(not data):
                NewCategory.name      = request.form.get("add_name")
                db.session.add(NewCategory)
                db.session.commit()
                db.session.refresh(NewCategory)

        if(data):
            return jsonify(data), 200
        
        NewCategoryLink = CategoriesToOrgsModel()
        NewCategoryLink.org_id = organizationID
        NewCategoryLink.category_id = NewCategory.id
        db.session.add(NewCategoryLink)
        db.session.commit()
        db.session.refresh(NewCategoryLink)
        db.session.expunge_all()
        return "ok"
#!SECTION
#SECTION FoodItems
class FoodItemModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'food_items'

    id              = db.Column(Integer, nullable=False, primary_key=True)
    org_id          = db.Column(Integer, db.ForeignKey("organizations.id"), nullable=False)
    name            = db.Column(String,  nullable=False)
    description     = db.Column(String)
    ingredients     = db.Column(String,  nullable=False)
    stop_list       = db.Column(Boolean, nullable=False, default=0)
    price           = db.Column(Float,   nullable=False, default=0)
    cooking_time    = db.Column(Integer, nullable=False)
    week            = db.Column(Integer)
    options         = db.Column(String)
    
#ANCHOR - FoodItemToRestaurants
class FoodItemToRestaurants(db.Model):
    __bind_key__  = 'main'
    __tablename__ = 'food_items_to_restaurants'

    id              = db.Column(Integer, nullable=False, primary_key=True)
    food_item_id    = db.Column(Integer, db.ForeignKey("food_items.id"), nullable=False)
    restaurant_id   = db.Column(Integer, db.ForeignKey("restaurants.id"))
    restaurant      = relationship("RestaurantModel")
    food_item       = relationship("FoodItemModel")

#ANCHOR - FoodItemToOrders
class FoodItemToOrders(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'food_items_to_orders'

    id              = db.Column(Integer, nullable=False, primary_key=True)
    food_item_id    = db.Column(Integer, db.ForeignKey("food_items.id"), nullable=False)
    order_id        = db.Column(Integer, db.ForeignKey("orders.id"), nullable=False)
    order           = relationship("OrderModel")
    food_item       = relationship("FoodItemModel")
    price           = db.Column(Float, nullable=False, default=0)
    options         = db.Column(String)

#ANCHOR - FoodItemToCategories
class FoodItemToCategories(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'food_items_to_categories'

    id              = db.Column(Integer, nullable=False, primary_key=True)
    food_item_id    = db.Column(Integer, db.ForeignKey("food_items.id"), nullable=False)
    category_id     = db.Column(Integer, db.ForeignKey("categories.id"), nullable=False)
    category        = relationship("CategoryModel")
    food_item       = relationship("FoodItemModel")

#!SECTIONs