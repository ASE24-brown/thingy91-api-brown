from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.extensions import Base



class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    username = Column(String, unique=True, index=True) # unique username for each user
    email = Column(String, unique=True, index=True)    # unique email for each user
    sensordata = relationship('SensorData', back_populates='user') # relationship to SensorData

    profile = relationship("UserProfile", uselist=False, back_populates="user")

class SensorData(Base):
    __tablename__ = 'sensordata'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    appId = Column(String, index=True) # appId of the sensor
    data = Column(String) # data from the sensor
    messageType = Column(String) # type of message
    ts = Column(Integer) # timestamp of the data
    user_id = Column(Integer, ForeignKey('user.id')) # foreign key to user table
    user = relationship('User', back_populates='sensordata') # relationship to User
    
class UserProfile(Base):
    __tablename__ = 'user_profile'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    full_name = Column(String, nullable=False) # full name of the user
    bio = Column(String) # bio of the user
    avatar_url = Column(String) # avatar url of the user
    user_id = Column(Integer, ForeignKey('user.id'), unique=True) # foreign key to user table

    user = relationship("User", back_populates="profile")