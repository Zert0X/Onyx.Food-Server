from onyx_food.extensions import db
from flask_login import current_user
from flask import jsonify
import requests

from sqlalchemy import ForeignKey, DateTime, String, Integer, Boolean, Float, Date, text, Text, ForeignKeyConstraint
from onyx_food.utils.exceptions import ValidationError

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
    
class OrderModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'orders'

    id    = db.Column(Integer, nullable=False, primary_key=True)
    datetime  = db.Column(DateTime)
    status = db.Column(Integer, nullable=False)
    user_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    courier_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    restaurant_id = db.Column(Integer, db.ForeignKey("restaurants.id"), nullable=False)
    coordinates = db.Column(String, nullable=False)
    delivery_time = db.Column(Integer, nullable=False)
    comment = db.Column(String, nullable=False)
    people_quantity = db.Column(Integer, nullable=False)
    price = db.Column(Float, nullable=False)

#!SECTIONs