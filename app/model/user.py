from sqlalchemy import Column, Integer, String, ForeignKey, Float, DateTime
from sqlalchemy.orm import relationship
from app.extensions import Base
import bcrypt as bycrpt


class User(Base):
    __tablename__ = 'user'

    id = Column(Integer, primary_key=True, autoincrement=True, index=True) # primary key of the table
    username = Column(String, unique=True, index=True, nullable=False) # unique username for each user
    email = Column(String, unique=True, index=True, nullable=False)    # unique email for each user
    password = Column(String, nullable=False) # password for each user
    sensordata = relationship('SensorData', back_populates='user') # relationship to SensorData
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
    