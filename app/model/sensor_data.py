from sqlalchemy import Column, Integer, Boolean, String, ForeignKey
from app.database import Base
from sqlalchemy.orm import relationship

class SensorData(Base):
    __tablename__ = 'sensordata'
    __table_args__ = {'extend_existing': True} 

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    appId = Column(String, index=True) # appId of the sensor
    data = Column(String) # data from the sensor
    messageType = Column(String) # type of message
    ts = Column(Integer) # timestamp of the data
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True) # foreign key to user table
    user = relationship('User', back_populates='sensordata') # relationship to User
    device_id = Column(Integer, ForeignKey('device.id'), nullable=True) # foreign key to device table
    device = relationship('Device', back_populates='sensordata') # relationship to Device
