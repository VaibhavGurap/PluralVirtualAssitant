from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import models
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import EmployeeRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from utils import saveImg
from verifyFace import verifyFace

app = FastAPI(title="Plural Virtual Assitant")
models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/employees',response_model=schemas.Employee,status_code=201)
async def createEmployee(firstName: str, lastName : str, email : str, img1 : UploadFile = File(...), img2 : UploadFile = File(...), img3 : UploadFile = File(...), img4 : UploadFile = File(...), img5 : UploadFile = File(...), db: Session = Depends(get_db)):
    return await EmployeeRepo.create(db=db, firstName=firstName, lastName=lastName, email=email, img1=img1, img2=img2, img3=img3, img4=img4, img5=img5)

@app.get('/employees',status_code=201)
async def getAllEmployees(db: Session = Depends(get_db)):
    employees = await EmployeeRepo.fetch_all(db)
    return employees

@app.post('/isEmployee',status_code=201)
async def isEmployee(img : UploadFile = File(...),db: Session= Depends(get_db)):
    path = await saveImg(img=img)
    status = await verifyFace(img_path=path,db=db)
    return status


if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)