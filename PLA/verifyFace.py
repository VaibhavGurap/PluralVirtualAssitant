from repositories import EmployeeRepo, AttendanceRepo
from PIL import Image
import numpy as np
import os
import time
import matplotlib.pyplot as plt
import pickle
from keras_vggface.utils import preprocess_input
from keras.applications.vgg16 import VGG16
from keras_vggface.vggface import VGGFace
import uuid 
import aiofiles
from utils import detect_extract_face,detect_face_haar
import cv2
from scipy.spatial.distance import cosine
import datetime
import io
import tensorflow as tf

async def verifyFace(vggface_model,img_path,db,checkOut):
    start_time=time.time()
    employee_dict = await EmployeeRepo.getEmployeesDictWithEmbeddings(db)
    image_to_classify = plt.imread(img_path)
    image_to_classify_rgb=cv2.cvtColor(image_to_classify,cv2.COLOR_BGR2RGB)
    res1,res2=detect_face_haar(image_to_classify_rgb)#changed here haar cascade from mtcnn
    sample_faces = [res2]*5
    min=999
    reply=dict()
    # print(employee_dict)
    # print(res1)
    # print(employee_dict.keys())
    # print(sample_faces.shape)
    isEmployee=False
    if res1:
        if sample_faces is not None:
            # print("in")
            st1=time.time()
            sample_faces=np.asarray(sample_faces,'float32')
            st2=time.time()
            print("Time1: "+str(st2-st1))
            sample_faces = preprocess_input(sample_faces)
            st3=time.time()
            print("Time2: "+str(st3-st2))
            
            st4=time.time()
            print("Time3: "+str(st4-st3))
            start_time1=time.time()
            sample_faces_embeddings_test = vggface_model.predict(sample_faces)
            start_time2=time.time()
            print("TIme4: "+str(start_time2-start_time1))
            print("TIme5: "+str(start_time2-st1))
            id=""
            for key,value in employee_dict.items():
                # print("Comparing for "+str(key))
                value=np.asarray(value,'float32')
                value=value.flatten()
                
                sample_faces_embeddings_test=sample_faces_embeddings_test.flatten()
                
                # print(key)
                # print(value.shape)
                # print(sample_faces_embeddings_test.shape)
                face_distance = cosine(value,sample_faces_embeddings_test)
                # print(face_distance)
                if min>face_distance:
                    min=face_distance
                    id=str(key)
            if min<0.35:
                # print(str(id)+" Employee")
                isEmployee=True
    if isEmployee:
        name = await EmployeeRepo.getName(id,db)
        if checkOut:
            await AttendanceRepo.markCheckout(db,id,datetime.date.today(),datetime.datetime.today())
            reply = {"isEmployee":True, "name":name}
        else:
            firstTimeOfTheDay = await AttendanceRepo.createCheckIn(db,id,datetime.date.today(),datetime.datetime.today())
            reply = {"isEmployee":True, "name":name, "firstTimeOfTheDay":firstTimeOfTheDay}
    else:
        # reply="Not an Employee"
        reply = {"isEmployee":False}
    end_time=time.time()
    print("Total time:",end_time-start_time)    
    return reply
     
async def verifyFaceV2(img,db,checkOut):
    start_time=time.time()
    employee_dict = await EmployeeRepo.getEmployeesDictWithEmbeddings(db)
    # image_to_classify = plt.imread(img_path)
    cwd = os.getcwd()
    cwd=cwd.replace('\\','/')
    print(cwd)
    parent_dir = cwd+"/PLA/temp" 
    directory = str(uuid.uuid4().hex[:6].upper())
    path = os.path.join(parent_dir,directory)
    os.mkdir(path)
    content = await img.read()
    image_pil = Image.open(io.BytesIO(content))
    image_to_classify = np.array(image_pil)
    image_to_classify_rgb=cv2.cvtColor(image_to_classify,cv2.COLOR_BGR2RGB)
    res1,res2=detect_face_haar(image_to_classify_rgb)#changed here haar cascade from mtcnn
    sample_faces = [res2]*5
    min=999
    reply=dict()
    # print(employee_dict)
    # print(res1)
    # print(employee_dict.keys())
    # print(sample_faces.shape)
    isEmployee=False
    if res1:
        if sample_faces is not None:
            # print("in")
            sample_faces=np.asarray(sample_faces,'float32')
            sample_faces = preprocess_input(sample_faces)
            vggface_model = VGGFace(include_top=False, model='resnet50', input_shape=(224,224,3))  
            sample_faces_embeddings_test = vggface_model.predict(sample_faces)
            id=""
            for key,value in employee_dict.items():
                # print("Comparing for "+str(key))
                value=np.asarray(value,'float32')
                value=value.flatten()
                sample_faces_embeddings_test=sample_faces_embeddings_test.flatten()
                # print(key)
                # print(value.shape)
                # print(sample_faces_embeddings_test.shape)
                face_distance = cosine(value,sample_faces_embeddings_test)
                # print(face_distance)
                if min>face_distance:
                    min=face_distance
                    id=str(key)
            if min<0.35:
                # print(str(id)+" Employee")
                isEmployee=True
    if isEmployee:
        name = await EmployeeRepo.getName(id,db)
        if checkOut:
            await AttendanceRepo.markCheckout(db,id,datetime.date.today(),datetime.datetime.today())
            reply = {"isEmployee":True, "name":name}
        else:
            firstTimeOfTheDay = await AttendanceRepo.createCheckIn(db,id,datetime.date.today(),datetime.datetime.today())
            reply = {"isEmployee":True, "name":name, "firstTimeOfTheDay":firstTimeOfTheDay}
    else:
        # reply="Not an Employee"
        reply = {"isEmployee":False}
    end_time=time.time()
    print("Total time:",end_time-start_time)    
    return reply