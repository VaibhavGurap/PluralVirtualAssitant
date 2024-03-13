import aiofiles
from sqlalchemy.orm import Session
import models, db
import schemas
import os
from utils import getEmbeddings
import pickle

class EmployeeRepo:
    async def create(db: Session, firstName, lastName, email, img1, img2, img3, img4, img5):
        db_item = models.Employee(firstName=firstName, lastName=lastName, email=email)
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
        return db_item
    
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
