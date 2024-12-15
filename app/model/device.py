from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from app.extensions import Base
from datetime import datetime


class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, unique=True, nullable=False)  # Name or identifier of the device
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True)     # Foreign key to associate with a user
    user = relationship('User', back_populates='device')  # Relationship to User
    sensordata = relationship('SensorData', back_populates='device')  # Relationship to SensorData
    status = Column(Integer, nullable=False)  # Status of the device
    last_updated = Column(DateTime, nullable=False, default=datetime.now)  # Last updated timestamp
