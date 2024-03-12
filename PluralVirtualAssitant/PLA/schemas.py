from typing import List, Optional
from pydantic import BaseModel

class EmployeeBase(BaseModel):
    firstName : str
    lastName : str
    email : str

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    empId : int
    
    class Config:
        orm_mode = True