from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship


from .extensions import Base


class SensorData(Base):
    __tablename__ = 'sensordata'

    id = Column(Integer, primary_key=True, index=True)
    appId = Column(String, index=True)
    data = Column(Float)
    messageType = Column(String)
    ts = Column(Integer)
    

