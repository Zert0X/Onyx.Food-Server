from flask_login import current_user
from onyx_food.organization.models import OrganizationModel, RestaurantModel

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