from mtcnn.mtcnn import MTCNN
from PIL import Image
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
from keras_vggface.utils import preprocess_input
from keras.applications.vgg16 import VGG16
from keras_vggface.vggface import VGGFace

def detect_extract_face(image_to_detect):
    mtcnn_detector = MTCNN()
    
    all_face_locations = mtcnn_detector.detect_faces(image_to_detect)
    if len(all_face_locations)<1:
        print("Face not detected.Please take photo again")
        return False,None
    elif len(all_face_locations)<1:
        msg="Please enter image with a single person only in it"
        return False,None
    print('There are {} no of faces in the image'.format(len(all_face_locations)))
    for index,current_face_location in enumerate(all_face_locations):
        x,y,width,height = current_face_location['box']

        left_x, left_y = x,y

        right_x, right_y = x+width, y+height

        current_face_image = image_to_detect[left_y:right_y,left_x:right_x]

        current_face_image = Image.fromarray(current_face_image)

        current_face_image = current_face_image.resize((224,224))

        current_face_image_np_array = np.asarray(current_face_image)

        return (True,current_face_image_np_array)
    
def model_embeddings(sample_face):
  print(sample_face.shape)
  sample_faces_1= np.asarray(sample_face,'float32')
  print(sample_faces_1.shape)
  sample_faces_1 = np.expand_dims(sample_face, axis=0).astype('float32')
  sample_faces_1 = preprocess_input(sample_faces_1)
  print(sample_faces_1.shape)
  vggface_model = VGGFace(include_top=False, model='resnet50', input_shape=(224,224,3), pooling='avg')  
  sample_faces_embeddings=vggface_model.predict(sample_faces_1)
  return sample_faces_embeddings
    
def getEmbeddings(path):
    images=os.listdir(path)
    images = [plt.imread(path+"/"+img) for img in images]
    embeddings = []
    for img in images:
        faceDetected,face = detect_extract_face(img)
        if not faceDetected:
            print("No face found")
        else:
            embeddings.append(model_embeddings(face))
    embeddings_blob=pickle.dumps(embeddings)
    return embeddings_blob