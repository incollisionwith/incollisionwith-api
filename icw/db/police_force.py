from sqlalchemy import String, Column, Integer

from . import Base

class PoliceForce(Base):
    __tablename__ = 'police_force'

    id = Column(Integer, primary_key=True)
    uri = Column(String, index=True)
    label = Column(String)
    comment = Column(String)
    homepage = Column(String)
    logo_url = Column(String)