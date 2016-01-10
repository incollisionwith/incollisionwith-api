from sqlalchemy import String, Column, SmallInteger
from . import Base

class PoliceForce(Base):
    __tablename__ = 'police_force'

    id = Column(SmallInteger, primary_key=True)
    uri = Column(String, index=True)
    label = Column(String)
    comment = Column(String)
    homepage = Column(String)
    logo_url = Column(String)

    def to_json(self, verbose=True):
        data = {
            'id': self.id,
            'label': self.label,
        }
        if verbose:
            data.update({
                '@id': self.uri,
                'comment': self.comment,
                'homepage': self.homepage,
                'logo': self.logo_url,
            })
        return data