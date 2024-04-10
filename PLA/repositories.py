import aiofiles
from sqlalchemy.orm import Session
import models, db
from models import Employee
import schemas
import os
from sqlalchemy.orm import defer
from utils import getEmbeddings
import pickle
from pydantic import BaseModel

class DepartmentRepo:
    async def create(db: Session, name : str):
        db_item = models.Department(name=name)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)
        response=dict()
        response["status"]=True
        response["res"]=db_item
        return response
    
    async def getAll(db : Session):
        res= db.query(models.Department).all()
        return res
    
    async def exists(db : Session, deptId : int):
        res = db.query(models.Department).get(deptId)
        print(res)
        if res is None:
            return False
        return True
    
    async def getDept(db: Session, deptId : int):
        res = db.query(models.Department).get(deptId)
        return res

class EmployeeRepo:
    async def create(db: Session, firstName, lastName, email, deptId, img1, img2, img3, img4, img5):
        response=dict()
        flag=await DepartmentRepo.exists(db,deptId=deptId)
        print("Flag: "+str(flag))
        if(flag):
            db_item = models.Employee(firstName=firstName, lastName=lastName, email=email, deptId=deptId)
            db.add(db_item)
            db.commit()
            db.refresh(db_item)
            cwd = os.getcwd()
            cwd=cwd.replace('\\','/')
            parent_dir = cwd+"/PLA/images"
            directory = str(db_item.empId)
            path = os.path.join(parent_dir,directory)
            os.mkdir(path)
            
            async with aiofiles.open(path+"/"+img1.filename, 'wb') as outfile:
                content = await img1.read()  # async read
                await outfile.write(content)
            
            async with aiofiles.open(path+"/"+img2.filename, 'wb') as outfile:
                content = await img2.read()  # async read
                await outfile.write(content)

            async with aiofiles.open(path+"/"+img3.filename, 'wb') as outfile:
                content = await img3.read()  # async read
                await outfile.write(content)

            async with aiofiles.open(path+"/"+img4.filename, 'wb') as outfile:
                content = await img4.read()  # async read
                await outfile.write(content)

            async with aiofiles.open(path+"/"+img5.filename, 'wb') as outfile:
                content = await img5.read()  # async read
                await outfile.write(content)

            db_item.embeddings=getEmbeddings(path)
            # print(db_item.embeddings)
            db.commit()
            db.refresh(db_item)
            response["status"]=True
            response["res"]=db_item.empId
        else:
            response["status"]=False
            response["error"]="Department doesn't exists"
        return response
    
    async def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        res = db.query(Employee).options(defer(Employee.embeddings)).offset(skip).limit(limit).all()
        employees=[]
        for item in res:
            deptId=item.deptId
            dept=db.query(models.Department).get(deptId)
            employees.append({"EmpId":item.empId, "FirstName":item.firstName, "LastName":item.lastName, "Email":item.email, "Department":dept.name})
        return employees
        
    async def getEmployeesDictWithEmbeddings(db: Session):
        res=db.query(models.Employee).all()
        employees=dict()
        for item in res:
            employees[item.empId]=pickle.loads(item.embeddings)
        return employees
    
    async def getName(id : int, db: Session):
        res=db.query(models.Employee).get(id)
        if res:
            return res.firstName+" "+res.lastName
        else:
            return None
    
    async def getNameByEmail(email : str, db: Session):
        res=db.query(models.Employee).filter(models.Employee.email==email.lower()).first()
        print("Result")
        print(res)
        if res:
            return res.firstName+" "+res.lastName
        else:
            return None
    
    async def getEmailByEmpId(empid : int, db: Session):
        res=db.query(models.Employee).get(empid)
        if res:
            return res.email
        else:
            return None

    async def getEmail(employee_firstname:str ,employee_lastname:str,employee_dept_name:str,db:Session):
        dept = db.query(models.Department).filter(models.Department.name == employee_dept_name).first() #get deptID using the name to use in employee table query
        if dept is not None:
            dept_id = dept.deptId
        else:
            None    
        res=db.query(models.Employee).filter_by(firstName=employee_firstname,lastName=employee_lastname,deptId=dept_id).all()
        if res:
            return res[0].email
        else:
            return  None
        
        
class Person_Visited(BaseModel):
    person_name:str
    employee_firstName:str
    employee_lastName:str
    person_email_id:str
    phone_number:str
    employee_dept_name:str

