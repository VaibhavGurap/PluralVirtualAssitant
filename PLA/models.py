
from sqlalchemy import Column, ForeignKey, Integer, String, Float, BLOB, LargeBinary, Date, DateTime
from sqlalchemy.orm import relationship

from db import Base

class Employee(Base):
    __tablename__="employees"

    empId = Column(Integer, primary_key=True, index=True)
    firstName = Column(String)
    lastName = Column(String)
    email = Column(String, unique=True)
    embeddings = Column(LargeBinary(length=(2**32)-1))
    deptId = Column(Integer)
class Department(Base):
    __tablename__="departments"

    deptId = Column(Integer, primary_key=True, index=True)
    name = Column(String, unique=True)

class Attendance(Base):
    __tablename__="attendance"
    attendanceId = Column(Integer, primary_key=True, index=True)
    empId = Column(Integer)
    date = Column(Date)
    checkIn = Column(DateTime)
    checkOut = Column(DateTime)