
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

# Function to add an employee
def add_employee(db, employee_data: dict):
    db_employee = Employee(**employee_data)
    db.add(db_employee)
    db.commit()
    db.refresh(db_employee)
    return db_employee

# Function to delete an employee by ID
def delete_employee(db, employee_id: int):
    employee = db.query(Employee).filter(Employee.empId == employee_id).first()
    if employee:
        db.delete(employee)
        db.commit()
        return True
    return False

# Function to update an employee by ID
def update_employee(db, employee_id: int, new_data: dict):
    employee = db.query(Employee).filter(Employee.empId == employee_id).first()
    if employee:
        for key, value in new_data.items():
            setattr(employee, key, value)
        db.commit()
        db.refresh(employee)
        return employee
    return None

# Function to retrieve all employees
def get_employees(db):
    return db.query(Employee).all()

# Menu function
def menu():
    print("Menu:")
    print("1. Add Employee")
    print("2. Update Employee")
    print("3. Delete Employee")
    print("4. Show Employees")
    print("5. Exit")

    choice = input("Enter your choice: ")
    return int(choice) if choice.isdigit() else None

# Example usage
def manage_employees():
    db = SessionLocal()

    while True:
        choice = menu()

        if choice == 1:
            # Add employee
            employee_data = {
                "firstName": input("Enter first name: "),
                "lastName": input("Enter last name: "),
                "email": input("Enter email: "),
                "deptId": int(input("Enter department ID: "))
            }
            new_employee = add_employee(db, employee_data)
            print("Employee added:", new_employee)

        elif choice == 2:
            # Update employee
            employee_id = int(input("Enter employee ID to update: "))
            update_data = {
                "firstName": input("Enter new first name: "),
                "lastName": input("Enter new last name: "),
                "email": input("Enter new email: "),
                "deptId": int(input("Enter new department ID: "))
            }
            updated_employee = update_employee(db, employee_id, update_data)
            if updated_employee:
                print("Employee updated:", updated_employee)
            else:
                print("Employee not found")

        elif choice == 3:
            # Delete employee
            employee_id = int(input("Enter employee ID to delete: "))
            if delete_employee(db, employee_id):
                print(f"Employee with ID {employee_id} deleted successfully")
            else:
                print(f"Employee with ID {employee_id} not found")

        elif choice == 4:
            # Show all employees
            employees = get_employees(db)
            print("\nAll Employees:")
            for employee in employees:
                print(employee.empId, employee.firstName, employee.lastName, employee.email, employee.deptId)

        elif choice == 5:
            break

        else:
            print("Invalid choice. Please enter a number from 1 to 5.")

    db.close()

manage_employees()
