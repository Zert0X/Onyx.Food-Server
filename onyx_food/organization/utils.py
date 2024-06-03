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

def get_categories(organizationID=0):
    """
    A helper function that returns categories by organizationID
    """
    if(not organizationID):
        return CategoryModel.query.filter_by(default = 1).all()
    
    categories = list()
    for category_link in CategoriesToOrgsModel.query.filter_by(org_id = organizationID).all():
        categories.append(category_link.category)
    return categories

def get_category_by_ID(categoryID):
    """
    A helper function that returns category by categoryID
    """
    return CategoryModel.query.filter_by(id=categoryID).first()

def get_orders(organizationID, restaurantID=0):
    """
    A helper function that returns orders by organizationID or restaurantID
    """
    restaurant_IDs = list()
    restaurant_IDs.append(restaurantID)
    if(not restaurantID):
        organization_restaurants = get_organization_restaurants(organizationID)
        for restaurant in organization_restaurants:
            restaurant_IDs.append(restaurant.id)
    return OrderModel.query.order_by(OrderModel.status, OrderModel.datetime).filter(OrderModel.id.in_(restaurant_IDs)).all()

def check_new_orders(organizationID):
    """
    A helper function that checks if there are a new orders for organization
    """
    restaurant_IDs = list()
    organization_restaurants = get_organization_restaurants(organizationID)
    for restaurant in organization_restaurants:
        restaurant_IDs.append(restaurant.id)
    
    if(OrderModel.query.filter(OrderModel.id.in_(restaurant_IDs), OrderModel.status==1).first()) is None:
        return False
    else:
        return True