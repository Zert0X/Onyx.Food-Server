from flask import request, redirect, url_for
from functools import wraps
from flask_login import current_user

from onyx_food.organization.models import OrganizationModel
from onyx_food.organization.utils import get_user_organizations
from onyx_food.utils.exceptions import ValidationError

def organization_access_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if (not organizationID in get_user_organizations(current_user)):
            raise ValidationError("Нет доступа к организации")
        return f(*args, **kwargs)
    return decorated_function