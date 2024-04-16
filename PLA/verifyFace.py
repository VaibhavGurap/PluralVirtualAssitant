from repositories import EmployeeRepo
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

async def verifyFace(img_path,db):
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
            sample_faces=np.asarray(sample_faces,'float32')
            sample_faces = preprocess_input(sample_faces)
            vggface_model = VGGFace(include_top=False, model='resnet50', input_shape=(224,224,3))  
            sample_faces_embeddings_test = vggface_model.predict(sample_faces)
            id=""
            for key,value in employee_dict.items():
                print("Comparing for "+str(key))
                value=np.asarray(value,'float32')
                value=value.flatten()
                sample_faces_embeddings_test=sample_faces_embeddings_test.flatten()
                # print(key)
                # print(value.shape)
                # print(sample_faces_embeddings_test.shape)
                face_distance = cosine(value,sample_faces_embeddings_test)
                print(face_distance)
                if min>face_distance:
                    min=face_distance
                    id=str(key)
            if min<0.5:
                # print(str(id)+" Employee")
                isEmployee=True
    if isEmployee:
        name = await EmployeeRepo.getName(id,db)
        # reply = name + " is a Employee"
        reply = {"isEmployee":True, "name":name}
    else:
        # reply="Not an Employee"
        reply = {"isEmployee":False}
    end_time=time.time()
    print("Total time:",end_time-start_time)    
    return reply
     