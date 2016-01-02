from sqlalchemy import Column, Integer, String, DateTime, ForeignKey
from sqlalchemy.orm import relationship

from . import Base


class CitationAccident(Base):
    __tablename__ = 'citation_accident'

    accident_id = Column(String, ForeignKey('accident.id'), primary_key=True, index=True)
    citation_id = Column(Integer, ForeignKey('citation.id'), primary_key=True, index=True)
    certainty_id = Column(Integer, ForeignKey('citation_certainty.id'), default=0)

    accident = relationship('Accident', back_populates='citations')
    citation = relationship('Citation', back_populates='accidents')
    certainty = relationship('CitationCertainty')


class Citation(Base):
    __tablename__ = 'citation'

    id = Column(Integer, primary_key=True)

    url = Column(String, index=True, unique=True)
    domain = Column(String)

    title = Column(String, nullable=True)
    description = Column(String, nullable=True)
    image_url = Column(String, nullable=True)
    published = Column(DateTime(timezone=True), nullable=True)
    publisher = Column(String, nullable=True)

    added = Column(DateTime(timezone=True))
    last_crawled = Column(DateTime(timezone=True), nullable=True)

    accidents = relationship('CitationAccident', back_populates='citation')

    def to_json(self):
        return {'url': self.url,
                'title': self.title,
                'description': self.description,
                'imageURL': self.image_url,
                'published': self.published.isoformat() if self.published else None,
                'publisher': self.publisher}