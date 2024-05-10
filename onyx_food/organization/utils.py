from flask_login import current_user
from onyx_food.organization.models import *

def get_user_organizations():
    """
    A helper function that returns all organizations for current user
    """
    return OrganizationModel.query.filter_by(owner_id = current_user.id).all()

def get_organization_restaurants(organizationID):
    """
    A helper function that returns all restaurants for current user
    """
    return RestaurantModel.query.filter_by(org_id = organizationID).all()

def get_organization_by_ID(organizationID):
    """
    A helper function that returns organization by ID
    """
    return OrganizationModel.query.filter_by(id = organizationID).first()

def get_restaurant_by_ID(restaurantID):
    """
    A helper function that returns restaurant by ID
    """
    return RestaurantModel.query.filter_by(id = restaurantID).first()

def get_orders(organizationID, restaurantID=0):
    """
    A helper function that returns restaurant by ID
    """
    restaurant_IDs = list()
    restaurant_IDs.append(restaurantID)
    if(not restaurantID):
        organization_restaurants = get_organization_restaurants(organizationID)
        for restaurant in organization_restaurants:
            restaurant_IDs.append(restaurant.id)
    return OrderModel.query.filter(OrderModel.id.in_(restaurant_IDs)).all()