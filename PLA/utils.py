from mtcnn.mtcnn import MTCNN
from PIL import Image
import cv2
import os
import qrcode
from pyzbar.pyzbar import decode
import numpy as np
import os
import matplotlib.pyplot as plt
import pickle
from keras_vggface.utils import preprocess_input
from keras.applications.vgg16 import VGG16
from keras_vggface.vggface import VGGFace
import uuid 
import aiofiles

def detect_face_haar(image_to_detect):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image_to_detect, cv2.COLOR_BGR2GRAY)
    cwd = os.getcwd()

    # Load the Haar Cascade classifier for face detection
    face_cascade = cv2.CascadeClassifier(cwd+'/PLA/haarcascade_frontalface_default.xml')

    # Detect faces in the grayscale image
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.1, minNeighbors=5, minSize=(30, 30))

    # Check if any faces are detected
    if len(faces) < 1:
        print("Face not detected. Please take photo again")
        return False, None

    # Extract the bounding box of the first detected face
    x, y, w, h = faces[0]

    # Extract the face region from the image
    face_image = image_to_detect[y:y+h, x:x+w]

    # Resize the face image to (224, 224)
    face_image_resized = cv2.resize(face_image, (224, 224))

    return (True, face_image_resized)



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
#   print(sample_face.shape)
  sample_faces_1= np.asarray(sample_face,'float32')
#   print(sample_faces_1.shape)
  sample_faces_1 = np.expand_dims(sample_face, axis=0).astype('float32')
  sample_faces_1 = preprocess_input(sample_faces_1)
#   print(sample_faces_1.shape)
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
    embeddings_blob=pickle.dumps(embeddings)#changes made 
    return embeddings_blob

async def saveImg(img):
    cwd = os.getcwd()
    cwd=cwd.replace('\\','/')
    print(cwd)
    parent_dir = cwd+"/PLA/temp" 
    directory = str(uuid.uuid4().hex[:6].upper())
    path = os.path.join(parent_dir,directory)
    os.mkdir(path)
    
    async with aiofiles.open(path+"/"+img.filename, 'wb') as outfile:
        content = await img.read()  # async read
        await outfile.write(content)
    print(path+"/"+img.filename)    
    return path+"/"+img.filename

def generate_qr_code(data,filename):
    path=os.getcwd()
    full_path=os.path.join(path,"qr_images", filename)
    print(full_path)

    qr = qrcode.QRCode(
        version=1,
        error_correction=qrcode.constants.ERROR_CORRECT_L,
        box_size=10,
        border=4,
    )
    qr.add_data(data)
    qr.make(fit=True)

    img = qr.make_image(fill_color="black", back_color="white")
    img.save(full_path)


def verify_qr_code(filename1):
    path=os.getcwd()
    input_path=os.path.join(path,"test",filename1)
    image1=cv2.imread(input_path)
    decoded_objects1=decode(image1)
    full_path=os.path.join(path,"qr_images")
    for filename in os.listdir(full_path):
        if filename.endswith(".png"): 
            qr_code_path = os.path.join(full_path, filename)
            image2=cv2.imread(qr_code_path)
            decoded_objects2=decode(image2)
            if decoded_objects1==decoded_objects2:
                data=decoded_objects1[0].data.decode('utf-8')
                print(f"Employee data: {data}") 
            else:
                print(f"No QR Code detected")







