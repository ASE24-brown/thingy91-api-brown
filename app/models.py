from sqlalchemy import Column, Integer, String, ForeignKey, Float
from sqlalchemy.orm import relationship
from app.extensions import Base
import bcrypt as bycrpt


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    username = Column(String, unique=True, index=True, nullable=False) # unique username for each user
    email = Column(String, unique=True, index=True, nullable=False)    # unique email for each user
    password = Column(String, nullable=False) # password for each user
    sensordata = relationship('SensorData', back_populates='user') # relationship to SensorData
    profile = relationship("Profile", back_populates="user")
    device = relationship('Device', back_populates='user', uselist=False) # relationship to Device

    def set_password(self, password):
        """
        Hash and set the password for the user.

        Args:
            password (str): The plain text password to be hashed.

        Returns:
            None
        """
        hashed = bycrpt.hashpw(password.encode('utf-8'), bycrpt.gensalt())
        self.password = hashed.decode('utf-8')

    def check_password(self, password):
        """
        Check the password against the stored hash.

        Args:
            password (str): The plain text password to check.

        Returns:
            bool: True if the password matches, False otherwise.
        """
        return bycrpt.checkpw(password.encode('utf-8'), self.password.encode('utf-8'))
    
class SensorData(Base):
    __tablename__ = 'sensordata'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    appId = Column(String, index=True) # appId of the sensor
    data = Column(String) # data from the sensor
    messageType = Column(String) # type of message
    ts = Column(Integer) # timestamp of the data
    user_id = Column(Integer, ForeignKey('user.id'), nullable=True) # foreign key to user table
    user = relationship('User', back_populates='sensordata') # relationship to User
    device_id = Column(Integer, ForeignKey('device.id'), nullable=True) # foreign key to device table
    device = relationship('Device', back_populates='sensordata') # relationship to Device

class Device(Base):
    __tablename__ = 'device'

    id = Column(Integer, primary_key=True, index=True)  # Primary key
    name = Column(String, unique=True, nullable=False)  # Name or identifier of the device
    user_id = Column(Integer, ForeignKey('user.id'))     # Foreign key to associate with a user
    user = relationship('User', back_populates='device')  # Relationship to User
    sensordata = relationship('SensorData', back_populates='device')  # Relationship to SensorData
    status = Column(String, nullable=False)  # Status of the device
    
class Profile(Base):
    __tablename__ = 'profile'

    id = Column(Integer, primary_key=True, index=True) # primary key of the table
    name = Column(String, nullable=False) # name of the profile
    description = Column(String) # description of the profile
    type = Column(String) # type of the profile
    level = Column(Integer) # level of the profile
    user_id = Column(Integer, ForeignKey('user.id', ondelete='SET NULL')) # foreign key to profile table
    user = relationship("User", back_populates="profile")

