from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Employee  # Import your SQLAlchemy model

SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# SQLAlchemy Employee model
class Employee(Base):
    __tablename__ = "employees"
    empId = Column(Integer, primary_key=True, index=True)
    firstName = Column(String, index=True)
    lastName = Column(String, index=True)
    email = Column(String, index=True)
    deptId = Column(Integer)

# Function to create and add an employee
def create_employee(db, employee_data: dict):
    db_employee = Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Example usage
def add_employee():
    db = SessionLocal()

    # Create employee data
    employee_data = {
        "firstName": "Rhea",
        "lastName": "Tarneja",
        "email": "rheal@gmail.com",
        "deptId": 2
    }

    # Add employee to the database
    created_employee = create_employee(db, employee_data)
    print("Employee added:", created_employee)

    db.close()

add_employee()
