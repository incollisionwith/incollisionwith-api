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

    def to_json(self):
        return {
            'id': self.id,
            '@id': self.uri,
            'label': self.label,
            'comment': self.comment,
            'homepage': self.homepage,
            'logo': self.logo_url,
        }