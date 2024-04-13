from onyx_food.extensions import db, cache
from sqlalchemy import ForeignKey, String, Integer, Float, Date, text, Text, ForeignKeyConstraint

from flask_login import AnonymousUserMixin, UserMixin, current_user, login_user
from onyx_food.utils.database import CRUDMixin, UTCDateTime
from onyx_food.utils.helpers import time_utcnow

from werkzeug.security import check_password_hash, generate_password_hash

class UserModel(db.Model, UserMixin, CRUDMixin):
    __bind_key__ = 'main'
    __tablename__ = 'users'
    id          = db.Column(Integer,     nullable=False, primary_key=True)
    email       = db.Column(String(130), nullable=False)
    phone       = db.Column(String(15),  nullable=False)
    name        = db.Column(String(45),  nullable=False)
    second_name = db.Column(String(45),  nullable=True)
    password    = db.Column('password', db.String(120), nullable=True)
    region      = db.Column(String(50))
    city        = db.Column(String(50))
    street      = db.Column(String(70))
    house       = db.Column(String(20))

    theme = db.Column(String(20))

    last_failed_login = db.Column(UTCDateTime(timezone=True), nullable=True)
    login_attempts = db.Column(db.Integer, default=0, nullable=False)

    @property
    def permissions(self):
        """Returns the permissions for the user."""
        return self.get_permissions()

    def check_password(self, password):
        """Check passwords. If passwords match it returns true, else false."""
        if self.password is None:
            return False
        return check_password_hash(self.password, password)
    
    def _get_password(self):
        """Returns the hashed password."""
        return self.password

    def _set_password(self, password):
        """Generates a password hash for the provided password."""
        if not password:
            return
        self.password = generate_password_hash(password)

    @classmethod
    def authenticate(self, login, password):
        """A classmethod for authenticating users.
        It returns the user object if the user/password combination is ok.
        If the user has entered too often a wrong password, he will be locked
        out of his account for a specified time.

        :param login: This can be either a username or a email address.
        :param password: The password that is connected to username and email.
        """
        user = UserModel.query.filter(db.or_(UserModel.phone == login,
                                       UserModel.email == login)).first()
        if user is not None:

            if user.check_password(password):
                # reset them after a successful login attempt
                user.login_attempts = 0
                user.save()
                return user
            
            # user exists, wrong password
            # never had a bad login before
            if user.login_attempts is None:
                user.login_attempts = 1
            else:
                user.login_attempts += 1
            user.last_failed_login = time_utcnow()
            user.save()

        # protection against account enumeration timing attacks
        check_password_hash("dummy password", password)
        
    @classmethod
    def register(self, request):
        NewUser = UserModel()
        NewUser.name = request.form.get("name")
        NewUser.second_name = request.form.get("second_name")

        if (UserModel.query.filter_by(email = request.form.get("email")).first()) is not None:
            return False
        NewUser.email = request.form.get("email")

        if (UserModel.query.filter_by(phone = request.form.get("phone")).first()) is not None:
            return False
        NewUser.phone = request.form.get("phone")

        if(request.form.get("password")==request.form.get("password-repeated")):
            NewUser._set_password(request.form.get("password"))
        else:
            return False
        
        db.session.add(NewUser)
        db.session.commit()
        db.session.refresh(NewUser)
        db.session.expunge_all()
        return True
    
    @classmethod
    def login(self, request):
        if current_user.is_authenticated:
            return True
        User = UserModel.authenticate(
            request.form.get("field-login"),
            request.form.get("field-password")
        )
        if User is not None:
            login_user(User, remember=request.form.get("remember_me"))
            return True
        else:
            return False
    
class GuestModel(AnonymousUserMixin):
    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""
        cache.delete_memoized(cls.get_permissions, cls)