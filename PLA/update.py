from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.orm import sessionmaker, declarative_base
from models import Employee  # Import your SQLAlchemy model

SQLALCHEMY_DATABASE_URL = "sqlite:///./data.db"

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

# Function to update an employee
def update_employee(db, employee_id: int, new_data: dict):
    employee = db.query(Employee).filter(Employee.empId == employee_id).first()
    if employee:
        for key, value in new_data.items():
            setattr(employee, key, value)
        db.commit()
        db.refresh(employee)
        return employee
    return None

# Example usage
def modify_employee():
    db = SessionLocal()

    # Update employee with ID 1
    updated_data = {
        "firstName": "rheal",
        "email": "rheal@hmail.com"
    }
    updated_employee = update_employee(db, employee_id=7, new_data=updated_data)

    if updated_employee:
        print("Employee updated:", updated_employee)
    else:
        print("Employee not found")

    db.close()

modify_employee()
