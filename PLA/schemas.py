from typing import List, Optional
from pydantic import BaseModel

class EmployeeBase(BaseModel):
    firstName : str
    lastName : str
    email : str
    deptId : int

class EmployeeCreate(EmployeeBase):
    pass

class Employee(EmployeeBase):
    empId : int
    
    class Config:
        orm_mode = True

class Response(BaseModel):
    status : bool
    res : str
    error : str