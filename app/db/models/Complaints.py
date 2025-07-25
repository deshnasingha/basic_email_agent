from sqlalchemy import Column, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()

class Complaint(Base):
    __tablename__ = 'complaints'
    
    id = Column(Integer, primary_key=True, autoincrement=True)
    user_id = Column(Integer, nullable=False)
    content = Column(Text, nullable=False)
    status = Column(String(50), default='open')  # e.g., open, in_progress, resolved
    

    def __repr__(self):
        return f"<Complaint(id={self.id}, user_id={self.user_id}, status={self.status})>"