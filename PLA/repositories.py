from sqlalchemy.orm import Session
import models, db
import schemas
import os

class EmployeeRepo:
    async def create(db: Session, firstName, lastName, email, img1, img2, img3, img4, img5):
        db_item = models.Employee(firstName=firstName, lastName=lastName, email=email)
        db.add(db_item)
        db.commit()
        db.refresh(db_item)

        parent_dir = "PLA/images"
        directory = str(db_item.empId)
        path = os.path.join(parent_dir,directory)
        os.mkdir(path)
        
        return db_item
    
    async def fetch_all(db: Session, skip: int = 0, limit: int = 100):
        return db.query(models.Employee).offset(skip).limit(limit).all()