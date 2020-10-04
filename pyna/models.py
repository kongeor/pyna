from sqlalchemy import Column, Integer, String, Text, ForeignKey
from sqlalchemy.orm import relationship

from .database import Base

class Headline(Base):
    __tablename__ = 'headlines'
    id = Column(Integer, primary_key=True)

    source_id = Column(Integer, ForeignKey("sources.id"))
    source = relationship("Source", back_populates = "headlines")

    author = Column(Text())
    title = Column(Text())
    description = Column(Text())
    url = Column(Text())
    url_to_image = Column(Text())
    published_at_ts = Column(Integer(), index=True)
    published_at = Column(Text())
    content = Column(Text())

    def __init__(self, source=None, author=None, title=None, description=None, url=None, 
        url_to_image=None, published_at_ts=None, published_at=None, content=None):
        self.source = source
        self.author = author
        self.title = title
        self.description = description
        self.url = url
        self.url_to_image = url_to_image
        self.published_at_ts = published_at_ts
        self.published_at = published_at_ts
        self.content = content

    def __repr__(self):
        return '<Headline %r>' % (self.title)

class Source(Base):
    __tablename__ = 'sources'
    id = Column(Integer, primary_key=True)
    source_id = Column(Text())
    source_name = Column(Text())

    headlines = relationship("Headline", order_by=Headline.id, back_populates = "source")

    def __init__(self, source_id=None, source_name=None):
        self.source_id = source_id
        self.source_name = source_name

    def __repr__(self):
        return '<Source %r>' % (self.source_name)
