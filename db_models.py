from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column,Integer,String,Boolean,DateTime,Float
from sqlalchemy.sql import func

Base = declarative_base()

class dbPost(Base):

    __tablename__ = "posts"
    id = Column(Integer,primary_key=True)
    title = Column(String,nullable=False)
    content = Column(String,nullable=False)
    published = Column(Boolean,default=True)
    rating = Column(Float)
    created_at = Column(DateTime(timezone=True),server_default = func.now(),nullable=False)
    

class dbUser(Base):

    __tablename__ = "users"
    id = Column(Integer,primary_key=True,index=True)
    email = Column(String,nullable=False,unique=True)
    password = Column(String,nullable=False)
    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)