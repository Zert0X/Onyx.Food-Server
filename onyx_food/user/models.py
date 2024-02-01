from onyx_food.extensions import db_main, cache
from sqlalchemy import Column, ForeignKey, String, Integer, Float, Date, text, Text, ForeignKeyConstraint   
from flask_login import AnonymousUserMixin

class UserModel(db_main.Model):
    __bind_key__ = 'main'
    __tablename__ = 'users'
    id          = Column(Integer,     nullable=False, primary_key=True)
    email       = Column(String(130), nullable=False)
    phone       = Column(String(15),  nullable=False)
    name        = Column(String(45),  nullable=False)
    second_name = Column(String(45),  nullable=True)
    password    = Column(String(128), nullable=False)
    region      = Column(String(50))
    city        = Column(String(50))
    street      = Column(String(70))
    house       = Column(String(20))

class GuestModel(AnonymousUserMixin):
    @classmethod
    def invalidate_cache(cls):
        """Invalidates this objects cached metadata."""
        cache.delete_memoized(cls.get_permissions, cls)