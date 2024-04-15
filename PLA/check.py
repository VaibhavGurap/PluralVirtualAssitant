
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Employee  

SQLALCHEMY_DATABASE_URL = "sqlite:///data.db"

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_employees():
    db = SessionLocal()
    employees = db.query(Employee).all()
    db.close()
    return employees

# Example usage
def display_employees():
    employees = get_employees()
    if employees:
        for employee in employees:
            print(f"ID: {employee.empId}, Name: {employee.firstName} {employee.lastName}, Email: {employee.email}, Department ID: {employee.deptId}")
    else:
        print("No Employees Found")


display_employees()
