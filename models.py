from sqlalchemy import Column, Integer, String
from database.db import Base

class Gift(Base):
    __tablename__ = "gifts"
    
    id = Column(Integer, primary_key=True)
    gift_id = Column(Integer, unique=True)
    gift_type = Column(String)
    background = Column(String)
    model = Column(String)
    url = Column(String)