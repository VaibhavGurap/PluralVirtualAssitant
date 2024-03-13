import aiofiles
from sqlalchemy.orm import Session
import models, db
import schemas
import os
from utils import getEmbeddings
import pickle

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
            # response["res"]=db_item
        else:
            response["status"]=False
            response["error"]="Department doesn't exists"
        return response
    
    async def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        res=db.query(models.Employee).offset(skip).limit(limit).all()
        employees=[]
        for item in res:
            employees.append({"EmpId":item.empId, "FirstName":item.firstName, "LastName":item.lastName, "Email":item.email})
        return employees
    
    async def getEmployeesDictWithEmbeddings(db: Session):
        res=db.query(models.Employee).all()
        employees=dict()
        for item in res:
            employees[item.empId]=pickle.loads(item.embeddings)
        return employees
    
    async def getName(id : int, db: Session):
        res=db.query(models.Employee).get(id)
        return res.firstName+" "+res.lastName
