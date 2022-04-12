from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Boolean
from constants import SHA_LEN


Base = declarative_base()

class Apikey(Base):
    __tablename__ = 'apikeys'
    id = Column(String(SHA_LEN), primary_key=True)
    name = Column(String)
    active = Column(Boolean)
    creationDate = Column(Date)
    description = Column(String)

    def __repr__(self):
        return "<Apikey(name='{}', active='{}', creationDate={}, description={})>" \
            .format(self.name, self.active, self.creationDate, self.description)