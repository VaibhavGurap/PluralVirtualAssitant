from fastapi import Depends, FastAPI, HTTPException, File, UploadFile
from fastapi.responses import JSONResponse
import models
from db import get_db, engine
import models as models
import schemas as schemas
from repositories import EmployeeRepo, DepartmentRepo
from sqlalchemy.orm import Session
import uvicorn
from typing import List,Optional
from fastapi.encoders import jsonable_encoder
from utils import saveImg
from verifyFace import verifyFace
import requests
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(title="Plural Virtual Assitant")
origins = [
    "http://localhost:3000",
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)
models.Base.metadata.create_all(bind=engine)

@app.exception_handler(Exception)
def validation_exception_handler(request, err):
    base_error_message = f"Failed to execute: {request.method}: {request.url}"
    return JSONResponse(status_code=400, content={"message": f"{base_error_message}. Detail: {err}"})

@app.post('/departments',status_code=201)
async def createDept(name : str, db : Session = Depends(get_db)):
    return await DepartmentRepo.create(db,name=name)

@app.get('/departments',status_code=200)
async def getDepts(db : Session = Depends(get_db)):
    return await DepartmentRepo.getAll(db)


@app.post('/employees',status_code=201)
async def createEmployee(firstName: str, lastName : str, email : str, deptId : int, img1 : UploadFile = File(...), img2 : UploadFile = File(...), img3 : UploadFile = File(...), img4 : UploadFile = File(...), img5 : UploadFile = File(...), db: Session = Depends(get_db)):
    return await EmployeeRepo.create(db=db, firstName=firstName, lastName=lastName, email=email, deptId=deptId, img1=img1, img2=img2, img3=img3, img4=img4, img5=img5)

@app.get('/employees',status_code=201)
async def getAllEmployees(db: Session = Depends(get_db)):
    employees = await EmployeeRepo.fetch_all(db)
    return employees

@app.post('/isEmployee',status_code=201)
async def isEmployee(img : UploadFile = File(...),db: Session= Depends(get_db)):
    path = await saveImg(img=img)
    status = await verifyFace(img_path=path,db=db)
    return status

@app.post('/notify',status_code=200)
async def notify(email : str, msg : str):
    url = "https://prod-23.centralindia.logic.azure.com:443/workflows/6d812989a9394a38931510b7de6bcb50/triggers/manual/paths/invoke?api-version=2016-06-01&sp=%2Ftriggers%2Fmanual%2Frun&sv=1.0&sig=SUXDOT3mn2YL7E01-MTzxQZo4MtvcOkIp1ABvDei-FA"
    obj = {"email":email,"message":msg}
    requests.post(url,json=obj)
    return True

if __name__ == "__main__":
    uvicorn.run("main:app", port=9000, reload=True)