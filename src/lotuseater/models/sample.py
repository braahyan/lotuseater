from sqlalchemy import Column, String, Numeric
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class Sample(Base):
    __tablename__ = 'samples'
    timestamp = Column(Numeric, primary_key=True)
    value = Column(String(50), primary_key=True)
    device_id = Column(String(50), primary_key=True)
    data = Column(Numeric)
