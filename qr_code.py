import cv2
import qrcode
import os
from pyzbar.pyzbar import decode


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


    

