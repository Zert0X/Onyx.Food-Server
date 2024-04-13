from onyx_food.extensions import db
from flask_login import current_user
import requests, json

from sqlalchemy import ForeignKey, String, Integer, Boolean, Float, Date, text, Text, ForeignKeyConstraint
from onyx_food.utils.exceptions import ValidationError

class OrganizationModel(db.Model):
    __bind_key__  = 'main'
    __tablename__ = 'organizations'
    id       = db.Column(Integer,     nullable=False, primary_key=True)
    owner_id = db.Column(Integer, db.ForeignKey("users.id"), nullable=False)
    name     = db.Column(String(50), nullable=False)

    INN      = db.Column(String(12),  nullable=False)
    couriers = db.Column(Boolean,  nullable=False)

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
    region  = db.Column(String(50))
    city  = db.Column(String(50))
    street  = db.Column(String(50))
    house  = db.Column(String(20))

class MenuModel(db.Model):
    __bind_key__ = 'main'
    __tablename__ = 'menu'

    id    = db.Column(Integer, nullable=False, primary_key=True)
    name  = db.Column(String(255))

#!SECTION