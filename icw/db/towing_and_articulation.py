from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class TowingAndArticulation(Base):
    __tablename__ = 'towing_and_articulation'

    id = Column(Integer, primary_key=True)
    label = Column(String)
