import uuid
from sqlalchemy import Column, Integer, String, Boolean, Enum
from sqlalchemy.types import Enum as SQLEnum
from app.db.models.Complaints import Base
from sqlalchemy.orm import validates

PROVIDER_CHOICES = ("google", "local")

class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True, autoincrement=True)
    firstname = Column(String(255), nullable=False)
    username = Column(String(255), unique=True, nullable=False)
    
    email = Column(String(255), unique = True, nullable= False)
    
    def __repr__(self):
        return f"<User(id={self.id}, username={self.username}, email={self.email})>"