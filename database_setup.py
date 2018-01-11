import os
import sys

# _____________Configuration_______________________________
from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship
from sqlalchemy import create_engine

Base = declarative_base()


# ______________Class_______________________________________
class Restaurant(Base):
    # --------Table info-----------
    __tablename__ = 'restaurant'

    # --------Mapper---------------
    name = Column(String(250), nullable=False)
    id = Column(Integer, primary_key=True)

    @property
    def serialize(self):
        return {
            'name' : self.name,
            'id' : self.id,
        }

class MenuItem(Base):
    # --------Table info----------
    __tablename__ = 'menu_item'

    # --------Mapper--------------
    name = Column(String(80), nullable=False)
    id = Column(Integer, primary_key=True)
    course = Column(String(250))
    description = Column(String(250))
    price = Column(String(8))
    restaurant_id = Column(Integer, ForeignKey('restaurant.id'))
    restaurant = relationship(Restaurant)

    @property
    def serialize(self):
        # Returns object data in easily serializeable format
        return {
            'name' : self.name,
            'description' : self.description,
            'id' : self.price,
            'price' : self.price,
            'course' : self.course,
        }

# __________configuration End of File______________________

engine = create_engine('sqlite:///restaurantmenu.db')

Base.metadata.create_all(engine)
