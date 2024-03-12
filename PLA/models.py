
from sqlalchemy import Column, ForeignKey, Integer, String, Float, BLOB
from sqlalchemy.orm import relationship

from db import Base

class Employee(Base):
    __tablename__="employees"

    empId = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    embeddings = Column(BLOB)