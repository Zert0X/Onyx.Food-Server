from flask_login import current_user
from onyx_food.organization.models import OrganizationModel

def get_user_organizations():
    """
    A helper function that returns all organizations for current user
    """
    return OrganizationModel.query.filter_by(owner_id = current_user.id).all()