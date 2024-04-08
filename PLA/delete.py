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

# Function to delete an employee by ID
def delete_employee(db, employee_id: int):
    employee = db.query(Employee).filter(Employee.empId == employee_id).first()
    if employee:
        db.delete(employee)
        db.commit()
        return True
    return False

# Example usage
def remove_employee():
    db = SessionLocal()

    # Delete employee with ID 1
    employee_id = 7
    if delete_employee(db, employee_id):
        print(f"Employee with ID {employee_id} deleted successfully")
    else:
        print(f"Employee with ID {employee_id} not found")

    db.close()

remove_employee()
