from geoalchemy2 import Geometry
from sqlalchemy import String, Column, Integer, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class AccidentSeverity(Base):
    __tablename__ = 'accident_severity'

    id = Column(Integer, primary_key=True)
    label = Column(String)
    comment = Column(String)
    injury_definition = Column(String)
